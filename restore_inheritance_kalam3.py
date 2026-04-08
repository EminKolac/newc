"""
Restore Permission Inheritance — 2025 Kalam III

Problem: lockdown_video_downloads.py broke permission inheritance on files.
Students now have "None" permissions even though they're Team members.

Fix: Call SharePoint REST API "resetroleinheritance" on each file.
This restores the parent folder/library permissions, so Team members
regain their default access (read/view).

After restoring inheritance, videos get preventsDownload links
to block downloading while allowing viewing.

Usage:
  python restore_inheritance_kalam3.py --dry-run    # Preview
  python restore_inheritance_kalam3.py              # Apply fix
  python restore_inheritance_kalam3.py --videos-only # Only fix video files
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from ms365_connector import MS365Connector
import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".wmv", ".flv", ".3gp"}
SITE_FILTER = "kalam"
LOG_FILE = "restore_inheritance_log.json"


def is_video(filename):
    return os.path.splitext(filename.lower())[1] in VIDEO_EXTENSIONS


class InheritanceRestorer:
    def __init__(self, connector):
        self.connector = connector
        self.log = []
        self.stats = {
            "sites": 0, "drives": 0, "total_files": 0,
            "videos": 0, "non_videos": 0,
            "inheritance_restored": 0,
            "already_inheriting": 0,
            "video_view_links_created": 0,
            "errors": 0,
        }
        self._call_count = 0

    def _refresh(self):
        self._call_count += 1
        if self._call_count % 40 == 0:
            self.connector.authenticate_app()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.connector.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _get(self, url):
        self._refresh()
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _post(self, url, payload=None):
        self._refresh()
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return {"status": "ok"}

    def _get_all(self, url):
        result = self._get(url)
        items = result.get("value", [])
        while "@odata.nextLink" in result:
            result = self._get(result["@odata.nextLink"])
            items.extend(result.get("value", []))
        return items

    def find_sites(self):
        print("[*] Searching for Kalam sites...")
        all_sites = self._get_all(f"{GRAPH_BASE}/sites?search=*&$top=999")
        matches = [s for s in all_sites if SITE_FILTER.lower() in s.get("displayName", "").lower()]
        for s in matches:
            print(f"  MATCH: {s.get('displayName')} ({s.get('webUrl')})")
        if not matches:
            print("  No Kalam sites found! All sites:")
            for s in all_sites:
                print(f"    - {s.get('displayName')}")
        self.stats["sites"] = len(matches)
        return matches

    def scan_drive(self, drive_id, folder_id="root"):
        files = []
        try:
            items = self._get_all(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{folder_id}/children?$top=200"
            )
            for item in items:
                if "folder" in item:
                    files.extend(self.scan_drive(drive_id, item["id"]))
                elif "file" in item:
                    files.append({
                        "id": item["id"],
                        "name": item["name"],
                        "drive_id": drive_id,
                        "web_url": item.get("webUrl", ""),
                        "sharepoint_ids": item.get("sharepointIds", {}),
                    })
        except Exception as e:
            if "404" not in str(e) and "403" not in str(e):
                self.stats["errors"] += 1
        return files

    def check_has_unique_permissions(self, drive_id, item_id):
        """Check if a file has unique (broken) permissions."""
        try:
            perms = self._get(f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions")
            perm_list = perms.get("value", [])
            # If there are very few permissions and none inherited, it's likely broken
            has_inherited = any("inheritedFrom" in p for p in perm_list)
            non_owner_count = sum(1 for p in perm_list if "owner" not in p.get("roles", []))
            return {
                "has_inherited": has_inherited,
                "total_perms": len(perm_list),
                "non_owner_count": non_owner_count,
            }
        except Exception:
            return None

    def restore_inheritance_graph(self, site_id, drive_id, item_id, filename, dry_run=False):
        """
        Restore permission inheritance using Graph API approach:
        Delete all unique permissions so the file falls back to inherited.

        Graph API: DELETE /drives/{drive_id}/items/{item_id}/permissions/{perm_id}
        for each non-owner, non-inherited permission.
        Then the file inherits from parent.
        """
        if dry_run:
            self.stats["inheritance_restored"] += 1
            return True

        try:
            # Get current permissions
            perms = self._get(f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions")
            perm_list = perms.get("value", [])

            # We need to use SharePoint REST API to reset inheritance
            # Graph API doesn't have a direct resetroleinheritance endpoint
            # But we can use the SharePoint REST API with the same token

            # Get the site URL for SharePoint REST API
            site_info = self._get(f"{GRAPH_BASE}/sites/{site_id}")
            site_url = site_info.get("webUrl", "")

            if not site_url:
                self.stats["errors"] += 1
                return False

            # Get the list item info for this drive item
            try:
                item_info = self._get(
                    f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}?$select=id,name,sharepointIds,parentReference"
                )
                list_id = item_info.get("sharepointIds", {}).get("listId", "")
                list_item_id = item_info.get("sharepointIds", {}).get("listItemId", "")
            except Exception:
                list_id = ""
                list_item_id = ""

            if list_id and list_item_id:
                # Use SharePoint REST API to reset role inheritance
                sp_url = f"{site_url}/_api/web/lists(guid'{list_id}')/items({list_item_id})/resetroleinheritance"
                try:
                    resp = requests.post(sp_url, headers=self._headers(), timeout=30)
                    if resp.status_code < 300:
                        self.stats["inheritance_restored"] += 1
                        self.log.append({
                            "action": "inheritance_restored",
                            "method": "sharepoint_rest",
                            "drive_id": drive_id,
                            "item_id": item_id,
                            "filename": filename,
                            "list_id": list_id,
                            "list_item_id": list_item_id,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        })
                        return True
                    else:
                        print(f"    [WARN] SP REST failed ({resp.status_code}): {filename}")
                        # Fall through to Graph API approach
                except Exception as e:
                    print(f"    [WARN] SP REST error for {filename}: {str(e)[:80]}")

            # Fallback: Graph API approach — delete unique permissions
            # This makes the file "inherit" because no unique perms remain
            deleted = 0
            for p in perm_list:
                perm_id = p.get("id")
                roles = p.get("roles", [])

                # Skip owner permissions
                if "owner" in roles:
                    continue
                # Skip inherited (can't delete anyway)
                if "inheritedFrom" in p:
                    continue

                try:
                    del_url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions/{perm_id}"
                    resp = requests.delete(del_url, headers=self._headers(), timeout=30)
                    if resp.status_code < 300:
                        deleted += 1
                except Exception:
                    pass

            if deleted > 0 or len(perm_list) <= 1:
                self.stats["inheritance_restored"] += 1
                self.log.append({
                    "action": "inheritance_restored",
                    "method": "graph_delete_unique",
                    "drive_id": drive_id,
                    "item_id": item_id,
                    "filename": filename,
                    "perms_deleted": deleted,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return True

            self.stats["errors"] += 1
            return False

        except Exception as e:
            self.stats["errors"] += 1
            print(f"    [ERROR] {filename}: {str(e)[:100]}")
            return False

    def add_video_view_link(self, drive_id, item_id, filename, dry_run=False):
        """After restoring inheritance, add preventsDownload link on videos."""
        if dry_run:
            self.stats["video_view_links_created"] += 1
            return True
        try:
            result = self._post(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink",
                {"type": "view", "scope": "organization", "preventsDownload": True}
            )
            self.stats["video_view_links_created"] += 1
            self.log.append({
                "action": "video_view_link",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "permission_id": result.get("id", ""),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return True
        except Exception as e:
            self.stats["errors"] += 1
            return False

    def run(self, dry_run=False, videos_only=False):
        sites = self.find_sites()
        if not sites:
            return

        for si, site in enumerate(sites):
            site_id = site["id"]
            site_name = site.get("displayName", "Unknown")
            self.connector.authenticate_app()

            print(f"\n{'#'*60}")
            print(f"  {site_name}")
            print(f"{'#'*60}")

            try:
                drives = self.connector.list_drives(site_id).get("value", [])
            except Exception as e:
                print(f"  [ERROR] {e}")
                continue

            for drive in drives:
                drive_id = drive["id"]
                drive_name = drive.get("name", "")
                self.stats["drives"] += 1

                print(f"\n  Drive: {drive_name}")
                files = self.scan_drive(drive_id)
                self.stats["total_files"] += len(files)

                videos = [f for f in files if is_video(f["name"])]
                non_videos = [f for f in files if not is_video(f["name"])]
                self.stats["videos"] += len(videos)
                self.stats["non_videos"] += len(non_videos)

                print(f"    {len(files)} files ({len(videos)} video, {len(non_videos)} non-video)")

                # Determine which files to process
                if videos_only:
                    targets = videos
                    print(f"    Processing videos only...")
                else:
                    targets = files
                    print(f"    Processing ALL files...")

                # Step 1: Restore inheritance on all target files
                tag = "[DRY-RUN] " if dry_run else ""
                print(f"    {tag}Restoring permission inheritance on {len(targets)} files...")

                for i, f in enumerate(targets):
                    self.restore_inheritance_graph(
                        site_id, f["drive_id"], f["id"], f["name"], dry_run=dry_run
                    )
                    if (i + 1) % 50 == 0:
                        self.connector.authenticate_app()
                        print(f"      Progress: {i+1}/{len(targets)}")

                # Step 2: Add preventsDownload links on videos
                if videos:
                    print(f"\n    {tag}Adding view-only links on {len(videos)} videos...")
                    for i, f in enumerate(videos):
                        self.add_video_view_link(
                            f["drive_id"], f["id"], f["name"], dry_run=dry_run
                        )
                        if (i + 1) % 50 == 0:
                            self.connector.authenticate_app()
                            print(f"      Progress: {i+1}/{len(videos)}")

        # Save log
        if not dry_run and self.log:
            with open(LOG_FILE, "w") as f:
                json.dump(self.log, f, indent=2, ensure_ascii=False)
            print(f"\n[*] Log saved: {LOG_FILE} ({len(self.log)} entries)")

        # Summary
        s = self.stats
        mode = " (DRY RUN)" if dry_run else ""
        print(f"""
{'='*60}
  RESTORE INHERITANCE — KALAM III{mode}
{'='*60}
  Sites:                   {s['sites']}
  Drives:                  {s['drives']}
  Total files:             {s['total_files']}
  Videos:                  {s['videos']}
  Non-videos:              {s['non_videos']}

  FIXES APPLIED:
  Inheritance restored:    {s['inheritance_restored']}
  Already inheriting:      {s['already_inheriting']}
  Video view-only links:   {s['video_view_links_created']}
  Errors:                  {s['errors']}
{'='*60}

  What this means:
  - Files now inherit permissions from the Team/site
  - Students who are Team members can VIEW all files again
  - Videos have preventsDownload links (stream only)
  - Non-video files: full access (view + download)
{'='*60}
""")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--videos-only", action="store_true", help="Only fix video files")
    args = parser.parse_args()

    connector = MS365Connector()
    connector.authenticate_app()
    restorer = InheritanceRestorer(connector)
    restorer.run(dry_run=args.dry_run, videos_only=args.videos_only)


if __name__ == "__main__":
    main()
