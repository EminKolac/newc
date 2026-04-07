"""
Teams Video Download Blocker
Finds all Teams meeting recordings from 2025 onwards and disables download.

Uses SharePoint SharingControls via Microsoft Graph API.
All changes are reversible — run with --undo to re-enable downloads.

Usage:
  python teams_block_video_downloads.py           # Block downloads on 2025+ videos
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

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"}
CHANGE_LOG_FILE = "video_download_changes.json"


class TeamsVideoManager:
    def __init__(self, connector: MS365Connector):
        self.connector = connector
        self.changes = []

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
            return found
        except Exception as e:
            print(f"  Error searching sites: {e}")
            # Fallback: try the root site directly
            print("[*] Trying root site directly...")
            try:
                root = self.connector._get(f"{GRAPH_BASE}/sites/{self.connector.sharepoint_site_url}")
                print(f"  Found root site: {root.get('displayName', 'N/A')}")
                return [root]
            except Exception as e2:
                print(f"  Error: {e2}")
                return []

    def find_teams_sites(self):
        """Find SharePoint sites that belong to Teams (groups)."""
        print("[*] Searching for Teams-linked sites...")
        groups = self.connector._get(f"{GRAPH_BASE}/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')&$select=id,displayName")
        teams = groups.get("value", [])
        sites = []
        for team in teams:
            try:
                site = self.connector._get(f"{GRAPH_BASE}/groups/{team['id']}/sites/root")
                site["_teamName"] = team["displayName"]
                sites.append(site)
                print(f"  Found team site: {team['displayName']}")
            except Exception as e:
                print(f"  Could not get site for team '{team['displayName']}': {e}")
        return sites

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
            else:
                print(f"  [FAIL] {resp.status_code} for {filename}: {resp.text[:200]}")

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
        for item in blocked_items:
            manager.unblock_download(
                item["drive_id"], item["item_id"], item["filename"],
                permission_id=item.get("permission_id"), dry_run=args.dry_run
            )
        if args.log:
            manager.save_change_log()
        print("\n[Done] Undo complete.")
        return

    # Step 1: Find all SharePoint sites (skip Groups API which needs extra permissions)
    print("[*] Searching all SharePoint sites directly...")
    sites = manager.find_all_sharepoint_sites()

    if not sites:
        print("[ERROR] No SharePoint sites found. Check API permissions.")
        sys.exit(1)

    # Step 2: For each site, find drives and scan for 2025+ videos
    all_videos = []
    for site in sites:
        site_name = site.get("_teamName", site.get("displayName", "Unknown"))
        if args.site_filter and args.site_filter.lower() not in site_name.lower():
            continue
        print(f"\n=== Site: {site_name} ===")
        try:
            drives = connector.list_drives(site["id"])
            for drive in drives.get("value", []):
                print(f"  Drive: {drive['name']}")
                videos = manager.find_videos_in_drive(drive["id"], drive["name"])
                all_videos.extend(videos)
        except Exception as e:
            print(f"  Error listing drives: {e}")

    print(f"\n{'='*60}")
    print(f"Found {len(all_videos)} videos from 2025+ across all Teams sites")
    print(f"{'='*60}")

    if not all_videos:
        print("[Done] No videos to process.")
        return

    # Step 3: Block downloads
    action = "Preview" if args.dry_run else "Blocking"
    print(f"\n[*] {action} downloads for {len(all_videos)} videos...\n")

    success_count = 0
    for video in all_videos:
        result = manager.block_download(
            video["drive_id"], video["item_id"], video["name"], args.dry_run
        )
        if result:
            success_count += 1

    print(f"\n[Done] {success_count}/{len(all_videos)} videos processed successfully.")

    if args.log or not args.dry_run:
        manager.save_change_log()

    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
