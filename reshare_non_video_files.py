"""
Re-share Non-Video Files with Download-Enabled Links

After enabling BlockDownloadPolicy (blocks ALL downloads for non-owners),
this script creates organization-wide sharing links WITH download for
all non-video files, so students can still download PDFs, docs, slides, etc.

Usage:
  python reshare_non_video_files.py --dry-run    # Preview: count files, no changes
  python reshare_non_video_files.py               # Create download links for non-video files
  python reshare_non_video_files.py --undo        # Remove the links we created

Requires: ms365_connector.py, .env with Azure credentials
"""

import os
import sys
import json
import argparse
from datetime import datetime
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".wmv", ".flv", ".3gp"}
LOG_FILE = "reshare_non_video_log.json"


class NonVideoReSharer:
    def __init__(self, connector: MS365Connector):
        self.connector = connector
        self.log = []
        self.stats = {
            "sites_scanned": 0,
            "drives_scanned": 0,
            "non_video_files_found": 0,
            "video_files_skipped": 0,
            "links_created": 0,
            "errors": 0,
        }

    def _is_video(self, filename: str) -> bool:
        ext = os.path.splitext(filename.lower())[1]
        return ext in VIDEO_EXTENSIONS

    def _get(self, url):
        headers = {"Authorization": f"Bearer {self.connector.access_token}"}
        resp = __import__("requests").get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _post(self, url, payload):
        headers = {
            "Authorization": f"Bearer {self.connector.access_token}",
            "Content-Type": "application/json",
        }
        resp = __import__("requests").post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def find_all_sites(self):
        """Get all SharePoint sites."""
        print("[*] Searching for all SharePoint sites...")
        result = self._get(f"{GRAPH_BASE}/sites?search=*&$top=999")
        sites = result.get("value", [])
        # Handle pagination
        while "@odata.nextLink" in result:
            result = self._get(result["@odata.nextLink"])
            sites.extend(result.get("value", []))
        print(f"  Found {len(sites)} sites")
        return sites

    def get_drives(self, site_id):
        """Get all document libraries for a site."""
        try:
            result = self._get(f"{GRAPH_BASE}/sites/{site_id}/drives")
            return result.get("value", [])
        except Exception as e:
            print(f"    [WARN] Could not get drives: {e}")
            return []

    def scan_drive_files(self, drive_id, folder_path="root"):
        """Recursively scan a drive for all files."""
        files = []
        try:
            url = f"{GRAPH_BASE}/drives/{drive_id}/items/{folder_path}/children?$top=200"
            result = self._get(url)
            items = result.get("value", [])

            while "@odata.nextLink" in result:
                result = self._get(result["@odata.nextLink"])
                items.extend(result.get("value", []))

            for item in items:
                if "folder" in item:
                    # Recurse into subfolders
                    sub_files = self.scan_drive_files(drive_id, item["id"])
                    files.extend(sub_files)
                elif "file" in item:
                    files.append({
                        "id": item["id"],
                        "name": item["name"],
                        "drive_id": drive_id,
                        "size": item.get("size", 0),
                        "mime": item.get("file", {}).get("mimeType", ""),
                        "web_url": item.get("webUrl", ""),
                    })
        except Exception as e:
            if "404" not in str(e):
                print(f"    [WARN] Error scanning folder: {e}")
        return files

    def create_download_link(self, drive_id, item_id, item_name, dry_run=False):
        """Create an organization-wide sharing link with download enabled."""
        if dry_run:
            return True

        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink"
        payload = {
            "type": "view",
            "scope": "organization",
        }
        # Note: NOT setting preventsDownload — so download IS allowed
        try:
            result = self._post(url, payload)
            link_url = result.get("link", {}).get("webUrl", "")
            self.log.append({
                "action": "link_created",
                "drive_id": drive_id,
                "item_id": item_id,
                "item_name": item_name,
                "permission_id": result.get("id", ""),
                "link_url": link_url,
                "timestamp": datetime.utcnow().isoformat(),
            })
            self.stats["links_created"] += 1
            return True
        except Exception as e:
            print(f"    [ERROR] Failed to create link for {item_name}: {e}")
            self.log.append({
                "action": "error",
                "drive_id": drive_id,
                "item_id": item_id,
                "item_name": item_name,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            })
            self.stats["errors"] += 1
            return False

    def undo(self):
        """Remove all sharing links we created (from log file)."""
        if not os.path.exists(LOG_FILE):
            print(f"[ERROR] No log file found: {LOG_FILE}")
            return

        with open(LOG_FILE) as f:
            entries = json.load(f)

        created = [e for e in entries if e["action"] == "link_created" and e.get("permission_id")]
        print(f"[*] Found {len(created)} links to remove")

        removed = 0
        errors = 0
        for i, entry in enumerate(created):
            drive_id = entry["drive_id"]
            item_id = entry["item_id"]
            perm_id = entry["permission_id"]
            try:
                url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions/{perm_id}"
                headers = {"Authorization": f"Bearer {self.connector.access_token}"}
                resp = __import__("requests").delete(url, headers=headers, timeout=30)
                resp.raise_for_status()
                removed += 1
            except Exception as e:
                print(f"  [ERROR] Could not remove link for {entry['item_name']}: {e}")
                errors += 1

            if (i + 1) % 200 == 0:
                print(f"  --- Undo progress: {i+1}/{len(created)} | Removed: {removed} ---")
                self.connector.refresh_token_if_needed(force=True)

        print(f"\n[*] Undo complete: {removed} removed, {errors} errors")

    def run(self, dry_run=False):
        """Main process: scan all sites, create download links for non-video files."""
        sites = self.find_all_sites()

        for si, site in enumerate(sites):
            site_id = site["id"]
            site_name = site.get("displayName", "Unknown")

            # Fresh token per site to avoid expiry
            self.connector.authenticate_app()

            print(f"\n[{si+1}/{len(sites)}] {site_name}")
            self.stats["sites_scanned"] += 1

            drives = self.get_drives(site_id)
            for drive in drives:
                drive_id = drive["id"]
                drive_name = drive.get("name", "")
                self.stats["drives_scanned"] += 1

                files = self.scan_drive_files(drive_id)
                non_video = [f for f in files if not self._is_video(f["name"])]
                video = [f for f in files if self._is_video(f["name"])]

                self.stats["non_video_files_found"] += len(non_video)
                self.stats["video_files_skipped"] += len(video)

                if non_video:
                    print(f"  Drive '{drive_name}': {len(non_video)} non-video files, {len(video)} videos skipped")

                for fi, file in enumerate(non_video):
                    self.create_download_link(file["drive_id"], file["id"], file["name"], dry_run=dry_run)

                    if (fi + 1) % 100 == 0:
                        self.connector.refresh_token_if_needed(force=True)

            # Progress every 10 sites
            if (si + 1) % 10 == 0:
                print(f"\n  --- Progress: {si+1}/{len(sites)} sites | "
                      f"Non-video: {self.stats['non_video_files_found']}, "
                      f"Links: {self.stats['links_created']}, "
                      f"Videos skipped: {self.stats['video_files_skipped']} ---\n")

        # Save log
        if not dry_run and self.log:
            with open(LOG_FILE, "w") as f:
                json.dump(self.log, f, indent=2)
            print(f"\n[*] Log saved to {LOG_FILE} ({len(self.log)} entries)")

        # Summary
        mode = " (DRY RUN)" if dry_run else ""
        print(f"""
============================================================
  RE-SHARE NON-VIDEO FILES{mode}
============================================================
  Sites scanned:         {self.stats['sites_scanned']}
  Drives scanned:        {self.stats['drives_scanned']}
  Non-video files found: {self.stats['non_video_files_found']}
  Video files skipped:   {self.stats['video_files_skipped']}
  Download links created:{self.stats['links_created']}
  Errors:                {self.stats['errors']}
============================================================

  Videos:     NO download link (blocked by policy + no link)
  Other files: Download link created (overrides policy)

  To undo:  python reshare_non_video_files.py --undo
============================================================""")


def main():
    parser = argparse.ArgumentParser(description="Re-share non-video files with download links")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    parser.add_argument("--undo", action="store_true", help="Remove links we created (from log)")
    args = parser.parse_args()

    connector = MS365Connector()
    connector.authenticate_app()
    sharer = NonVideoReSharer(connector)

    if args.undo:
        sharer.undo()
    else:
        sharer.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
