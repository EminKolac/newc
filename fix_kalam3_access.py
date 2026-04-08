"""
Fix Student Access — 2025 Kalam III ONLY

Problem: Students cannot VIEW videos in the "2025 Kalam III" team.
Root cause: lockdown_video_downloads.py removed all non-owner permissions,
and BlockDownloadPolicy blocks everything else.

This script:
  1. Finds the "2025 Kalam III" SharePoint site
  2. Scans all files in all drives
  3. For VIDEOS: creates organization-wide "view" links with preventsDownload=True
     (students can VIEW but NOT download)
  4. For NON-VIDEO files: creates organization-wide "view" links with download enabled
     (students can view AND download PDFs, docs, slides, etc.)

Usage:
  python fix_kalam3_access.py --audit              # Just scan and report
  python fix_kalam3_access.py --fix --dry-run      # Preview what would change
  python fix_kalam3_access.py --fix                # Apply the fix
  python fix_kalam3_access.py --undo               # Remove all links we created
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".wmv", ".flv", ".3gp"}
SITE_FILTER = "kalam"  # matches "2025 Kalam III" case-insensitive
LOG_FILE = "fix_kalam3_log.json"


def is_video(filename):
    return os.path.splitext(filename.lower())[1] in VIDEO_EXTENSIONS


class Kalam3Fixer:
    def __init__(self, connector):
        self.connector = connector
        self.log = []
        self.stats = {
            "sites_found": 0,
            "drives_scanned": 0,
            "total_files": 0,
            "video_files": 0,
            "non_video_files": 0,
            "videos_already_have_view_link": 0,
            "videos_need_view_link": 0,
            "videos_link_created": 0,
            "non_video_links_created": 0,
            "errors": 0,
        }

    def _get(self, url):
        import requests
        resp = requests.get(url, headers=self.connector._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _get_all(self, url):
        result = self._get(url)
        items = result.get("value", [])
        while "@odata.nextLink" in result:
            result = self._get(result["@odata.nextLink"])
            items.extend(result.get("value", []))
        return items

    def _post(self, url, payload):
        import requests
        resp = requests.post(url, headers=self.connector._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _delete(self, url):
        import requests
        resp = requests.delete(url, headers=self.connector._headers(), timeout=30)
        resp.raise_for_status()

    def find_kalam3_sites(self):
        """Find SharePoint sites matching '2025 Kalam III'."""
        print("[*] Searching for Kalam III sites...")
        all_sites = self._get_all(f"{GRAPH_BASE}/sites?search=*&$top=999")
        matches = []
        for site in all_sites:
            name = site.get("displayName", "")
            if SITE_FILTER.lower() in name.lower():
                matches.append(site)
                print(f"  MATCH: {name} ({site.get('webUrl', '')})")

        if not matches:
            print(f"\n  [!] No sites matching '{SITE_FILTER}' found.")
            print(f"  All sites:")
            for s in all_sites:
                print(f"    - {s.get('displayName', '?')} ({s.get('webUrl', '')})")

        self.stats["sites_found"] = len(matches)
        return matches

    def scan_drive_recursive(self, drive_id, folder_id="root"):
        """Recursively scan a drive for all files."""
        files = []
        try:
            items = self._get_all(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{folder_id}/children?$top=200"
            )
            for item in items:
                if "folder" in item:
                    files.extend(self.scan_drive_recursive(drive_id, item["id"]))
                elif "file" in item:
                    files.append({
                        "id": item["id"],
                        "name": item["name"],
                        "drive_id": drive_id,
                        "size": item.get("size", 0),
                        "web_url": item.get("webUrl", ""),
                        "created": item.get("createdDateTime", ""),
                    })
        except Exception as e:
            if "404" not in str(e) and "403" not in str(e):
                print(f"    [WARN] Scan error: {str(e)[:100]}")
                self.stats["errors"] += 1
        return files

    def check_file_permissions(self, drive_id, item_id):
        """Check current permissions on a file."""
        try:
            perms = self._get(f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions")
            result = {
                "has_prevents_download_link": False,
                "has_download_link": False,
                "has_org_view_link": False,
                "owner_count": 0,
                "link_count": 0,
                "direct_count": 0,
                "inherited_count": 0,
                "all_perms": [],
            }
            for p in perms.get("value", []):
                roles = p.get("roles", [])

                if "owner" in roles:
                    result["owner_count"] += 1
                elif p.get("link"):
                    link = p["link"]
                    result["link_count"] += 1
                    if link.get("preventsDownload", False):
                        result["has_prevents_download_link"] = True
                    else:
                        result["has_download_link"] = True
                    if link.get("scope") == "organization" and link.get("type") == "view":
                        result["has_org_view_link"] = True
                elif "inheritedFrom" in p:
                    result["inherited_count"] += 1
                else:
                    result["direct_count"] += 1

                result["all_perms"].append({
                    "id": p.get("id"),
                    "roles": roles,
                    "type": "link" if p.get("link") else ("inherited" if "inheritedFrom" in p else "direct"),
                    "link_type": p.get("link", {}).get("type") if p.get("link") else None,
                    "link_scope": p.get("link", {}).get("scope") if p.get("link") else None,
                    "prevents_download": p.get("link", {}).get("preventsDownload") if p.get("link") else None,
                    "granted_to": (
                        p.get("grantedToV2", p.get("grantedTo", {}))
                        .get("user", {}).get("displayName", "")
                    ) if not p.get("link") else None,
                })

            return result
        except Exception as e:
            self.stats["errors"] += 1
            return None

    def fix_video(self, drive_id, item_id, filename, dry_run=False):
        """Ensure video has a preventsDownload view link for students to VIEW."""
        perms = self.check_file_permissions(drive_id, item_id)
        if perms and perms["has_prevents_download_link"]:
            self.stats["videos_already_have_view_link"] += 1
            return "already_ok"

        self.stats["videos_need_view_link"] += 1

        if dry_run:
            print(f"    [DRY-RUN] Would create view-only link: {filename}")
            return "would_fix"

        try:
            result = self._post(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink",
                {
                    "type": "view",
                    "scope": "organization",
                    "preventsDownload": True,
                }
            )
            self.stats["videos_link_created"] += 1
            self.log.append({
                "action": "video_view_link_created",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "permission_id": result.get("id", ""),
                "link_url": result.get("link", {}).get("webUrl", ""),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            print(f"    [OK] View-only link created: {filename}")
            return "fixed"
        except Exception as e:
            self.stats["errors"] += 1
            print(f"    [ERROR] {filename}: {str(e)[:100]}")
            self.log.append({
                "action": "error",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "error": str(e)[:200],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return "error"

    def fix_non_video(self, drive_id, item_id, filename, dry_run=False):
        """Create download-enabled link for non-video file."""
        if dry_run:
            self.stats["non_video_links_created"] += 1
            return "would_fix"

        try:
            result = self._post(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink",
                {
                    "type": "view",
                    "scope": "organization",
                    # No preventsDownload = download is allowed
                }
            )
            self.stats["non_video_links_created"] += 1
            self.log.append({
                "action": "non_video_link_created",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "permission_id": result.get("id", ""),
                "link_url": result.get("link", {}).get("webUrl", ""),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return "fixed"
        except Exception as e:
            self.stats["errors"] += 1
            self.log.append({
                "action": "error",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "error": str(e)[:200],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return "error"

    def undo(self):
        """Remove all links we created (from log file)."""
        if not os.path.exists(LOG_FILE):
            print(f"[ERROR] No log file: {LOG_FILE}")
            return

        with open(LOG_FILE) as f:
            entries = json.load(f)

        created = [e for e in entries if e["action"].endswith("_created") and e.get("permission_id")]
        print(f"[*] Removing {len(created)} links we created...")

        removed = 0
        errors = 0
        for i, entry in enumerate(created):
            try:
                url = f"{GRAPH_BASE}/drives/{entry['drive_id']}/items/{entry['item_id']}/permissions/{entry['permission_id']}"
                self._delete(url)
                removed += 1
            except Exception as e:
                errors += 1
                print(f"  [ERROR] {entry['filename']}: {str(e)[:80]}")

            if (i + 1) % 50 == 0:
                self.connector.authenticate_app()
                print(f"  Progress: {i+1}/{len(created)} | Removed: {removed}")

        print(f"\n[Done] Removed: {removed}, Errors: {errors}")

    def run(self, mode="audit", dry_run=False):
        sites = self.find_kalam3_sites()
        if not sites:
            print("[ERROR] No matching sites found. Exiting.")
            return

        for si, site in enumerate(sites):
            site_id = site["id"]
            site_name = site.get("displayName", "Unknown")

            self.connector.authenticate_app()
            print(f"\n{'#'*60}")
            print(f"  SITE: {site_name}")
            print(f"{'#'*60}")

            try:
                drives_resp = self.connector.list_drives(site_id)
                drives = drives_resp.get("value", [])
            except Exception as e:
                print(f"  [ERROR] Can't list drives: {e}")
                continue

            for drive in drives:
                drive_id = drive["id"]
                drive_name = drive.get("name", "")
                self.stats["drives_scanned"] += 1

                print(f"\n  Drive: {drive_name}")
                files = self.scan_drive_recursive(drive_id)

                videos = [f for f in files if is_video(f["name"])]
                non_videos = [f for f in files if not is_video(f["name"])]

                self.stats["total_files"] += len(files)
                self.stats["video_files"] += len(videos)
                self.stats["non_video_files"] += len(non_videos)

                print(f"    Files: {len(files)} total ({len(videos)} video, {len(non_videos)} non-video)")

                if mode == "audit":
                    # Sample check permissions
                    print(f"\n    Checking permissions on sample videos...")
                    for f in videos[:5]:
                        perms = self.check_file_permissions(f["drive_id"], f["id"])
                        if perms:
                            has_view = "YES" if perms["has_prevents_download_link"] else "NO"
                            has_dl = "YES" if perms["has_download_link"] else "NO"
                            print(f"      {f['name'][:50]:50s} view-link={has_view} dl-link={has_dl} "
                                  f"owners={perms['owner_count']} inherited={perms['inherited_count']}")
                        else:
                            print(f"      {f['name'][:50]:50s} [ERROR reading perms]")

                    print(f"\n    Checking permissions on sample non-videos...")
                    for f in non_videos[:5]:
                        perms = self.check_file_permissions(f["drive_id"], f["id"])
                        if perms:
                            has_view = "YES" if perms["has_org_view_link"] else "NO"
                            has_dl = "YES" if perms["has_download_link"] else "NO"
                            print(f"      {f['name'][:50]:50s} org-link={has_view} dl-link={has_dl} "
                                  f"owners={perms['owner_count']} inherited={perms['inherited_count']}")

                elif mode == "fix":
                    # Fix videos: ensure they have preventsDownload view links
                    if videos:
                        print(f"\n    {'[DRY-RUN] ' if dry_run else ''}Fixing {len(videos)} videos (view-only links)...")
                        for i, f in enumerate(videos):
                            self.fix_video(f["drive_id"], f["id"], f["name"], dry_run=dry_run)
                            if (i + 1) % 50 == 0:
                                self.connector.authenticate_app()
                                print(f"      Progress: {i+1}/{len(videos)}")

                    # Fix non-videos: create download-enabled links
                    if non_videos:
                        print(f"\n    {'[DRY-RUN] ' if dry_run else ''}Fixing {len(non_videos)} non-video files (download links)...")
                        for i, f in enumerate(non_videos):
                            self.fix_non_video(f["drive_id"], f["id"], f["name"], dry_run=dry_run)
                            if (i + 1) % 50 == 0:
                                self.connector.authenticate_app()
                                print(f"      Progress: {i+1}/{len(non_videos)}")

        self.print_summary(mode, dry_run)
        self.save_log()

    def print_summary(self, mode, dry_run):
        s = self.stats
        label = "AUDIT" if mode == "audit" else ("FIX (DRY RUN)" if dry_run else "FIX APPLIED")
        print(f"""
{'='*65}
  2025 KALAM III — {label}
{'='*65}
  Sites found:             {s['sites_found']}
  Drives scanned:          {s['drives_scanned']}
  Total files:             {s['total_files']}
  Video files:             {s['video_files']}
  Non-video files:         {s['non_video_files']}
""")
        if mode == "fix":
            print(f"""  VIDEO ACCESS (view-only, no download):
    Already had view link:   {s['videos_already_have_view_link']}
    Needed view link:        {s['videos_need_view_link']}
    View links created:      {s['videos_link_created']}

  NON-VIDEO ACCESS (view + download):
    Download links created:  {s['non_video_links_created']}

  Errors:                  {s['errors']}
""")
        print(f"{'='*65}")

        if mode == "fix" and not dry_run:
            print("""
  Students should now be able to:
    - VIEW videos (via preventsDownload org links)
    - DOWNLOAD PDFs, docs, slides (via regular org links)
    - NOT download videos

  To undo: python fix_kalam3_access.py --undo
""")

    def save_log(self):
        if self.log:
            with open(LOG_FILE, "w") as f:
                json.dump(self.log, f, indent=2, ensure_ascii=False)
            print(f"[*] Log saved to {LOG_FILE} ({len(self.log)} entries)")


def main():
    parser = argparse.ArgumentParser(description="Fix student access for 2025 Kalam III")
    parser.add_argument("--audit", action="store_true", help="Scan and report only")
    parser.add_argument("--fix", action="store_true", help="Create sharing links to restore access")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--undo", action="store_true", help="Remove all links we created")
    args = parser.parse_args()

    if not any([args.audit, args.fix, args.undo]):
        print("Usage:")
        print("  python fix_kalam3_access.py --audit              # Scan & report")
        print("  python fix_kalam3_access.py --fix --dry-run      # Preview fix")
        print("  python fix_kalam3_access.py --fix                # Apply fix")
        print("  python fix_kalam3_access.py --undo               # Undo our changes")
        sys.exit(1)

    connector = MS365Connector()
    connector.authenticate_app()
    fixer = Kalam3Fixer(connector)

    if args.undo:
        fixer.undo()
    elif args.fix:
        fixer.run(mode="fix", dry_run=args.dry_run)
    else:
        fixer.run(mode="audit")


if __name__ == "__main__":
    main()
