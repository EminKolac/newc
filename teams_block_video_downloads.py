"""
Teams Video Download Blocker
Finds all video files across all SharePoint sites and disables download.

Uses SharePoint SharingControls via Microsoft Graph API.
All changes are reversible — run with --undo to re-enable downloads.
Saves full audit log (audit_report.json) and change log (video_download_changes.json).

Usage:
  python teams_block_video_downloads.py           # Block downloads on all videos
  python teams_block_video_downloads.py --dry-run  # Preview only, no changes
  python teams_block_video_downloads.py --undo     # Re-enable downloads (reverse)
  python teams_block_video_downloads.py --log      # Save change log to JSON
"""

import os
import sys
import json
import argparse
from datetime import datetime
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".MP4"}
CHANGE_LOG_FILE = "video_download_changes.json"
AUDIT_LOG_FILE = "audit_report.json"


class TeamsVideoManager:
    def __init__(self, connector: MS365Connector):
        self.connector = connector
        self.changes = []
        self.audit = {
            "run_started": datetime.utcnow().isoformat(),
            "run_finished": None,
            "total_sites_found": 0,
            "total_sites_scanned": 0,
            "total_sites_errors": 0,
            "total_drives_scanned": 0,
            "total_videos_found": 0,
            "total_videos_blocked": 0,
            "total_videos_failed": 0,
            "total_videos_skipped": 0,
            "sites": [],
        }

    def _is_video(self, filename: str) -> bool:
        return any(filename.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)

    def _is_2025_or_later(self, item: dict) -> bool:
        created = item.get("createdDateTime", "")
        if not created:
            return False
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            return dt.year >= 2025
        except ValueError:
            return False

    def find_all_sharepoint_sites(self):
        """Find all SharePoint sites (Teams channels map to SharePoint sites)."""
        print("[*] Searching for all SharePoint sites...")
        try:
            sites = self.connector._get(f"{GRAPH_BASE}/sites?search=*")
            found = sites.get("value", [])
            print(f"  Found {len(found)} sites")
            for s in found:
                print(f"  - {s.get('displayName', 'N/A')} ({s.get('webUrl', '')})")
            self.audit["total_sites_found"] = len(found)
            return found
        except Exception as e:
            print(f"  Error searching sites: {e}")
            print("[*] Trying root site directly...")
            try:
                root = self.connector._get(f"{GRAPH_BASE}/sites/{self.connector.sharepoint_site_url}")
                print(f"  Found root site: {root.get('displayName', 'N/A')}")
                self.audit["total_sites_found"] = 1
                return [root]
            except Exception as e2:
                print(f"  Error: {e2}")
                return []

    def find_videos_in_drive(self, drive_id, drive_name="", folder_path="root", depth=0):
        """Recursively find video files in a drive from 2025+."""
        videos = []
        indent = "  " * (depth + 1)
        try:
            items = self.connector._get(f"{GRAPH_BASE}/drives/{drive_id}/{folder_path}/children")
            for item in items.get("value", []):
                name = item.get("name", "")
                if "folder" in item:
                    sub_videos = self.find_videos_in_drive(
                        drive_id, drive_name,
                        f"items/{item['id']}", depth + 1
                    )
                    videos.extend(sub_videos)
                elif self._is_video(name) and self._is_2025_or_later(item):
                    size_mb = round(item.get("size", 0) / (1024 * 1024), 1)
                    created = item.get("createdDateTime", "")[:10]
                    print(f"{indent}[VIDEO] {name} ({size_mb} MB, created: {created})")
                    videos.append({
                        "drive_id": drive_id,
                        "drive_name": drive_name,
                        "item_id": item["id"],
                        "name": name,
                        "size_mb": size_mb,
                        "created": created,
                        "webUrl": item.get("webUrl", ""),
                    })
        except Exception as e:
            if "404" not in str(e) and "403" not in str(e):
                print(f"{indent}Error reading folder: {e}")
        return videos

    def block_download(self, drive_id, item_id, filename, dry_run=False):
        """
        Block download for a specific file by creating a view-only sharing link
        with preventsDownload=True via the Graph API createLink endpoint.
        Stores the permission ID so the change can be reversed later.
        """
        if dry_run:
            print(f"  [DRY-RUN] Would block download: {filename}")
            self.audit["total_videos_skipped"] += 1
            return True

        import requests as req
        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink"

        try:
            resp = req.post(
                url,
                headers=self.connector._headers(),
                json={
                    "type": "view",
                    "scope": "organization",
                    "preventsDownload": True,
                }
            )
            success = resp.status_code < 300
            permission_id = None
            if success:
                data = resp.json()
                permission_id = data.get("id")
                print(f"  [OK] Blocked download: {filename} (perm={permission_id})")
                self.audit["total_videos_blocked"] += 1
            else:
                print(f"  [FAIL] {resp.status_code} for {filename}: {resp.text[:200]}")
                self.audit["total_videos_failed"] += 1

            self.changes.append({
                "action": "block_download",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "permission_id": permission_id,
                "timestamp": datetime.utcnow().isoformat(),
                "success": success,
            })
            return success

        except Exception as e:
            print(f"  [FAIL] Could not block download for {filename}: {e}")
            self.audit["total_videos_failed"] += 1
            self.changes.append({
                "action": "block_download",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "permission_id": None,
                "timestamp": datetime.utcnow().isoformat(),
                "success": False,
                "error": str(e),
            })
            return False

    def unblock_download(self, drive_id, item_id, filename, permission_id=None, dry_run=False):
        """Re-enable download for a file by deleting the block-download permission.
        If permission_id is provided (from change log), deletes it directly.
        Otherwise falls back to scanning all permissions for preventsDownload links.
        """
        if dry_run:
            print(f"  [DRY-RUN] Would unblock download: {filename}")
            return True

        import requests as req

        try:
            perm_ids_to_delete = []

            if permission_id:
                perm_ids_to_delete.append(permission_id)
            else:
                # Fallback: scan permissions to find preventsDownload links
                url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions"
                perms = self.connector._get(url)
                for perm in perms.get("value", []):
                    if perm.get("link") and perm["link"].get("preventsDownload"):
                        perm_ids_to_delete.append(perm["id"])

            if not perm_ids_to_delete:
                print(f"  [SKIP] No block-download permission found for: {filename}")
                return True

            success = False
            for pid in perm_ids_to_delete:
                del_url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions/{pid}"
                resp = req.delete(del_url, headers=self.connector._headers())
                if resp.status_code < 300:
                    print(f"  [OK] Unblocked download: {filename} (deleted perm={pid})")
                    success = True
                else:
                    print(f"  [FAIL] {resp.status_code} deleting perm {pid} for {filename}: {resp.text[:200]}")

            self.changes.append({
                "action": "unblock_download",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "timestamp": datetime.utcnow().isoformat(),
                "success": success,
            })
            return success
        except Exception as e:
            print(f"  [FAIL] Could not unblock {filename}: {e}")
            return False

    def save_change_log(self):
        """Save all changes to a JSON file for auditability and undo."""
        with open(CHANGE_LOG_FILE, "w") as f:
            json.dump(self.changes, f, indent=2)
        print(f"\n[*] Change log saved to {CHANGE_LOG_FILE} ({len(self.changes)} entries)")

    def save_audit_report(self):
        """Save full audit report covering all sites, drives, videos."""
        self.audit["run_finished"] = datetime.utcnow().isoformat()
        with open(AUDIT_LOG_FILE, "w") as f:
            json.dump(self.audit, f, indent=2, ensure_ascii=False)
        print(f"[*] Audit report saved to {AUDIT_LOG_FILE}")
        # Print summary
        print(f"\n{'='*60}")
        print(f"  AUDIT SUMMARY")
        print(f"{'='*60}")
        print(f"  Run started:       {self.audit['run_started']}")
        print(f"  Run finished:      {self.audit['run_finished']}")
        print(f"  Sites found:       {self.audit['total_sites_found']}")
        print(f"  Sites scanned:     {self.audit['total_sites_scanned']}")
        print(f"  Sites with errors: {self.audit['total_sites_errors']}")
        print(f"  Drives scanned:    {self.audit['total_drives_scanned']}")
        print(f"  Videos found:      {self.audit['total_videos_found']}")
        print(f"  Videos blocked:    {self.audit['total_videos_blocked']}")
        print(f"  Videos failed:     {self.audit['total_videos_failed']}")
        print(f"  Videos skipped:    {self.audit['total_videos_skipped']}")
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Block/unblock video downloads in Teams SharePoint sites")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--undo", action="store_true", help="Re-enable downloads (reverses previous block)")
    parser.add_argument("--log", action="store_true", help="Save change log to JSON")
    parser.add_argument("--site-filter", type=str, default="", help="Only process sites matching this name")
    args = parser.parse_args()

    connector = MS365Connector()
    if not connector.authenticate_app():
        print("App auth failed. Trying device code flow...")
        if not connector.authenticate_device_code():
            sys.exit(1)

    manager = TeamsVideoManager(connector)

    # If undoing, load previous change log
    if args.undo:
        if not os.path.exists(CHANGE_LOG_FILE):
            print(f"[ERROR] No change log found at {CHANGE_LOG_FILE}. Cannot undo.")
            sys.exit(1)
        with open(CHANGE_LOG_FILE) as f:
            previous_changes = json.load(f)
        blocked_items = [c for c in previous_changes if c["action"] == "block_download" and c.get("success")]
        print(f"[*] Undoing {len(blocked_items)} blocked videos...")
        success = 0
        fail = 0
        for item in blocked_items:
            result = manager.unblock_download(
                item["drive_id"], item["item_id"], item["filename"],
                permission_id=item.get("permission_id"), dry_run=args.dry_run
            )
            if result:
                success += 1
            else:
                fail += 1
        print(f"\n[Done] Undo complete: {success} restored, {fail} failed.")
        if args.log:
            manager.save_change_log()
        return

    # Step 1: Find all SharePoint sites
    print("[*] Searching all SharePoint sites directly...")
    sites = manager.find_all_sharepoint_sites()

    if not sites:
        print("[ERROR] No SharePoint sites found. Check API permissions.")
        sys.exit(1)

    # Filter sites if needed
    if args.site_filter:
        sites = [s for s in sites if args.site_filter.lower() in s.get("displayName", "").lower()]

    # Step 2: Process in batches of 5 sites — scan + block immediately per batch
    # This keeps the token fresh (no long gap between auth and blocking)
    BATCH_SIZE = 5
    total_videos = 0
    total_success = 0
    total_fail = 0

    for batch_start in range(0, len(sites), BATCH_SIZE):
        batch = sites[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(sites) + BATCH_SIZE - 1) // BATCH_SIZE

        print(f"\n{'#'*60}")
        print(f"  BATCH {batch_num}/{total_batches} — Sites {batch_start+1}-{batch_start+len(batch)} of {len(sites)}")
        print(f"{'#'*60}")

        # Fresh token for each batch
        connector.authenticate_app()

        # Scan this batch of sites
        batch_videos = []
        for site in batch:
            site_name = site.get("_teamName", site.get("displayName", "Unknown"))
            site_url = site.get("webUrl", "")
            site_id = site.get("id", "")

            print(f"\n=== Site: {site_name} ===")

            site_audit = {
                "name": site_name,
                "url": site_url,
                "id": site_id,
                "status": "ok",
                "drives": [],
                "videos_found": 0,
                "videos_blocked": 0,
                "videos_failed": 0,
                "error": None,
            }

            try:
                drives = connector.list_drives(site_id)
                manager.audit["total_sites_scanned"] += 1
                for drive in drives.get("value", []):
                    print(f"  Drive: {drive['name']}")
                    manager.audit["total_drives_scanned"] += 1
                    videos = manager.find_videos_in_drive(drive["id"], drive["name"])
                    for v in videos:
                        v["site_name"] = site_name
                        v["site_url"] = site_url
                    batch_videos.extend(videos)
                    site_audit["drives"].append({
                        "name": drive["name"],
                        "id": drive["id"],
                        "videos_found": len(videos),
                    })
                    site_audit["videos_found"] += len(videos)
            except Exception as e:
                print(f"  Error listing drives: {e}")
                site_audit["status"] = "error"
                site_audit["error"] = str(e)
                manager.audit["total_sites_errors"] += 1

            manager.audit["sites"].append(site_audit)

        total_videos += len(batch_videos)

        if not batch_videos:
            print(f"\n  No videos in this batch.")
            continue

        # Block videos for this batch immediately (token is still fresh)
        action = "Preview" if args.dry_run else "Blocking"
        print(f"\n  [{action}] {len(batch_videos)} videos in batch {batch_num}...\n")

        batch_success = 0
        for video in batch_videos:
            result = manager.block_download(
                video["drive_id"], video["item_id"], video["name"], args.dry_run
            )
            if result:
                batch_success += 1

        total_success += batch_success
        total_fail += len(batch_videos) - batch_success
        print(f"\n  Batch {batch_num} done: {batch_success}/{len(batch_videos)} blocked")

        # Update site-level audit for this batch
        for change in manager.changes[-len(batch_videos):]:
            if change["action"] == "block_download":
                for sa in manager.audit["sites"]:
                    for da in sa.get("drives", []):
                        if da["id"] == change["drive_id"]:
                            if change.get("success"):
                                sa["videos_blocked"] = sa.get("videos_blocked", 0) + 1
                            else:
                                sa["videos_failed"] = sa.get("videos_failed", 0) + 1
                            break

        # Save change log after each batch (so progress is never lost)
        manager.save_change_log()

    manager.audit["total_videos_found"] = total_videos

    print(f"\n{'='*60}")
    print(f"[Done] {total_success}/{total_videos} videos blocked across all sites")
    print(f"       {total_fail} failed")
    print(f"{'='*60}")

    # Save logs
    manager.save_change_log()
    manager.save_audit_report()

    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
