"""
Grant View Access — Create organization-wide view links for all files on a site.
Gives all organization users the ability to view/stream files.

Usage:
  python grant_view_access.py --site "2025 Kalam III" --dry-run
  python grant_view_access.py --site "2025 Kalam III"
  python grant_view_access.py --all-sites --dry-run
  python grant_view_access.py --all-sites
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
LOG_FILE = "grant_view_log.json"


class ViewAccessGranter:
    def __init__(self, connector):
        self.connector = connector
        self.log = []
        self.stats = {
            "sites": 0,
            "drives": 0,
            "files_found": 0,
            "links_created": 0,
            "already_has_link": 0,
            "errors": 0,
        }

    def _get(self, url):
        import requests
        resp = requests.get(url, headers=self.connector._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _post(self, url, payload):
        import requests
        resp = requests.post(url, headers=self.connector._headers(),
                             json=payload, timeout=30)
        return resp

    def find_sites(self, site_filter=None):
        result = self._get(f"{GRAPH_BASE}/sites?search=*&$top=999")
        sites = result.get("value", [])
        while "@odata.nextLink" in result:
            result = self._get(result["@odata.nextLink"])
            sites.extend(result.get("value", []))

        if site_filter:
            sites = [s for s in sites if site_filter.lower() in s.get("displayName", "").lower()]

        return sites

    def get_drives(self, site_id):
        try:
            return self._get(f"{GRAPH_BASE}/sites/{site_id}/drives").get("value", [])
        except:
            return []

    def scan_files(self, drive_id, folder="root"):
        files = []
        try:
            url = f"{GRAPH_BASE}/drives/{drive_id}/items/{folder}/children?$top=200"
            result = self._get(url)
            items = result.get("value", [])
            while "@odata.nextLink" in result:
                result = self._get(result["@odata.nextLink"])
                items.extend(result.get("value", []))
            for item in items:
                if "folder" in item:
                    files.extend(self.scan_files(drive_id, item["id"]))
                elif "file" in item:
                    files.append({
                        "drive_id": drive_id,
                        "item_id": item["id"],
                        "name": item["name"],
                    })
        except Exception as e:
            if "404" not in str(e):
                print(f"    [WARN] {e}")
        return files

    def grant_view(self, drive_id, item_id, filename, dry_run=False):
        if dry_run:
            self.stats["links_created"] += 1
            return True

        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink"
        payload = {
            "type": "view",
            "scope": "organization",
        }
        try:
            resp = self._post(url, payload)
            if resp.status_code < 300:
                self.stats["links_created"] += 1
                self.log.append({
                    "action": "view_link_created",
                    "drive_id": drive_id,
                    "item_id": item_id,
                    "filename": filename,
                    "permission_id": resp.json().get("id", ""),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return True
            elif resp.status_code == 409:
                # Link already exists
                self.stats["already_has_link"] += 1
                return True
            else:
                print(f"    [ERROR] {resp.status_code} on {filename}: {resp.text[:150]}")
                self.stats["errors"] += 1
                return False
        except Exception as e:
            print(f"    [ERROR] {filename}: {e}")
            self.stats["errors"] += 1
            return False

    def run(self, sites, dry_run=False):
        for si, site in enumerate(sites, 1):
            site_name = site.get("displayName", "Unknown")
            site_id = site["id"]

            self.connector.authenticate_app()
            self.stats["sites"] += 1

            print(f"\n[{si}/{len(sites)}] {site_name}")

            drives = self.get_drives(site_id)
            for drive in drives:
                self.stats["drives"] += 1
                files = self.scan_files(drive["id"])
                self.stats["files_found"] += len(files)

                if files:
                    print(f"  Drive '{drive.get('name', '')}': {len(files)} files")

                for fi, f in enumerate(files):
                    self.grant_view(f["drive_id"], f["item_id"], f["name"], dry_run)

                    # Refresh token every 100 files
                    if (fi + 1) % 100 == 0:
                        self.connector.refresh_token_if_needed(force=True)
                        print(f"    --- {fi+1}/{len(files)} files processed ---")

        # Save log
        if not dry_run and self.log:
            with open(LOG_FILE, "w") as f:
                json.dump(self.log, f, indent=2)
            print(f"\n[*] Log saved to {LOG_FILE} ({len(self.log)} entries)")

        mode = " (DRY RUN)" if dry_run else ""
        print(f"""
{'='*60}
  GRANT VIEW ACCESS{mode}
{'='*60}
  Sites processed:       {self.stats['sites']}
  Drives scanned:        {self.stats['drives']}
  Files found:           {self.stats['files_found']}
  View links created:    {self.stats['links_created']}
  Already had link:      {self.stats['already_has_link']}
  Errors:                {self.stats['errors']}
{'='*60}
  All organization users can now VIEW these files.
  To undo: delete the sharing links using grant_view_log.json
{'='*60}""")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=str, help="Site name to grant access on")
    parser.add_argument("--all-sites", action="store_true", help="Grant on ALL sites")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.site and not args.all_sites:
        print("ERROR: Specify --site 'SiteName' or --all-sites")
        sys.exit(1)

    connector = MS365Connector()
    connector.authenticate_app()

    granter = ViewAccessGranter(connector)
    sites = granter.find_sites(site_filter=args.site if args.site else None)

    if not sites:
        print(f"[ERROR] No sites found matching '{args.site}'")
        sys.exit(1)

    print(f"[*] Will process {len(sites)} site(s):")
    for s in sites:
        print(f"  - {s.get('displayName', '')}")

    granter.run(sites, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
