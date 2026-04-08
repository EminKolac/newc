"""
Grant View Access to ALL Files in 2025 Kalam III

Creates organization-wide sharing links on EVERY file:
  - Videos:     "view" link with preventsDownload=True (stream only, no download)
  - Non-videos: "view" link (view + download enabled)

This ensures ALL org users can access ALL files.

Usage:
  python grant_view_all_kalam3.py --dry-run    # Preview
  python grant_view_all_kalam3.py              # Apply
  python grant_view_all_kalam3.py --undo       # Remove links we created
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".wmv", ".flv", ".3gp"}
SITE_FILTER = "kalam"
LOG_FILE = "grant_view_all_log.json"


def is_video(filename):
    return os.path.splitext(filename.lower())[1] in VIDEO_EXTENSIONS


class ViewGranter:
    def __init__(self, connector):
        self.connector = connector
        self.log = []
        self.stats = {
            "sites": 0, "drives": 0, "total_files": 0,
            "videos": 0, "non_videos": 0,
            "video_links_created": 0, "non_video_links_created": 0,
            "already_has_link": 0, "errors": 0,
        }
        self._call_count = 0

    def _refresh(self):
        self._call_count += 1
        if self._call_count % 40 == 0:
            self.connector.authenticate_app()

    def _get(self, url):
        import requests
        self._refresh()
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
        self._refresh()
        resp = requests.post(url, headers=self.connector._headers(), json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _delete(self, url):
        import requests
        self._refresh()
        resp = requests.delete(url, headers=self.connector._headers(), timeout=30)
        resp.raise_for_status()

    def find_sites(self):
        print("[*] Searching for Kalam sites...")
        all_sites = self._get_all(f"{GRAPH_BASE}/sites?search=*&$top=999")
        matches = [s for s in all_sites if SITE_FILTER.lower() in s.get("displayName", "").lower()]
        for s in matches:
            print(f"  MATCH: {s.get('displayName')} ({s.get('webUrl')})")
        if not matches:
            print("  No Kalam sites found! All sites:")
            for s in all_sites:
                print(f"    - {s.get('displayName')} ({s.get('webUrl')})")
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
                    })
        except Exception as e:
            if "404" not in str(e) and "403" not in str(e):
                self.stats["errors"] += 1
        return files

    def has_org_view_link(self, drive_id, item_id):
        """Check if file already has an organization view link."""
        try:
            perms = self._get(f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions")
            for p in perms.get("value", []):
                if p.get("link"):
                    link = p["link"]
                    if link.get("scope") == "organization" and link.get("type") == "view":
                        return True
            return False
        except Exception:
            return False

    def grant_view(self, drive_id, item_id, filename, prevent_download=False, dry_run=False):
        """Create an organization-wide view link."""
        if dry_run:
            kind = "view-only (no dl)" if prevent_download else "view+download"
            self.stats["video_links_created" if prevent_download else "non_video_links_created"] += 1
            return True

        payload = {
            "type": "view",
            "scope": "organization",
        }
        if prevent_download:
            payload["preventsDownload"] = True

        try:
            result = self._post(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink",
                payload
            )
            perm_id = result.get("id", "")
            link_url = result.get("link", {}).get("webUrl", "")

            if prevent_download:
                self.stats["video_links_created"] += 1
            else:
                self.stats["non_video_links_created"] += 1

            self.log.append({
                "action": "link_created",
                "type": "video_view_only" if prevent_download else "non_video_download",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "permission_id": perm_id,
                "link_url": link_url,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return True
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
            return False

    def undo(self):
        if not os.path.exists(LOG_FILE):
            print(f"[ERROR] No log: {LOG_FILE}")
            return
        with open(LOG_FILE) as f:
            entries = json.load(f)
        created = [e for e in entries if e["action"] == "link_created" and e.get("permission_id")]
        print(f"[*] Removing {len(created)} links...")
        removed = errors = 0
        for i, entry in enumerate(created):
            try:
                self._delete(
                    f"{GRAPH_BASE}/drives/{entry['drive_id']}/items/{entry['item_id']}/permissions/{entry['permission_id']}"
                )
                removed += 1
            except Exception:
                errors += 1
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i+1}/{len(created)} removed={removed}")
        print(f"\n[Done] Removed: {removed}, Errors: {errors}")

    def run(self, dry_run=False):
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

                # Process videos — view-only (preventsDownload)
                if videos:
                    tag = "[DRY-RUN] " if dry_run else ""
                    print(f"    {tag}Creating view-only links for {len(videos)} videos...")
                    for i, f in enumerate(videos):
                        self.grant_view(f["drive_id"], f["id"], f["name"],
                                       prevent_download=True, dry_run=dry_run)
                        if (i + 1) % 100 == 0:
                            print(f"      {i+1}/{len(videos)} done")

                # Process non-videos — view + download
                if non_videos:
                    tag = "[DRY-RUN] " if dry_run else ""
                    print(f"    {tag}Creating view+download links for {len(non_videos)} non-video files...")
                    for i, f in enumerate(non_videos):
                        self.grant_view(f["drive_id"], f["id"], f["name"],
                                       prevent_download=False, dry_run=dry_run)
                        if (i + 1) % 100 == 0:
                            print(f"      {i+1}/{len(non_videos)} done")

        # Save
        if not dry_run and self.log:
            with open(LOG_FILE, "w") as f:
                json.dump(self.log, f, indent=2, ensure_ascii=False)
            print(f"\n[*] Log saved: {LOG_FILE} ({len(self.log)} entries)")

        # Summary
        s = self.stats
        mode = " (DRY RUN)" if dry_run else ""
        print(f"""
{'='*60}
  GRANT VIEW ACCESS — 2025 KALAM III{mode}
{'='*60}
  Sites:                   {s['sites']}
  Drives:                  {s['drives']}
  Total files:             {s['total_files']}

  VIDEOS (view only, NO download):
    Count:                 {s['videos']}
    Links created:         {s['video_links_created']}

  NON-VIDEOS (view + download):
    Count:                 {s['non_videos']}
    Links created:         {s['non_video_links_created']}

  Errors:                  {s['errors']}
{'='*60}

  Students can now:
    - VIEW/STREAM all videos (cannot download)
    - VIEW + DOWNLOAD all other files (PDFs, docs, etc.)

  To undo: python grant_view_all_kalam3.py --undo
{'='*60}
""")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--undo", action="store_true")
    args = parser.parse_args()

    connector = MS365Connector()
    connector.authenticate_app()
    granter = ViewGranter(connector)

    if args.undo:
        granter.undo()
    else:
        granter.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
