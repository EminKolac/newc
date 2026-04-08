"""
Restore Permission Inheritance on video files.

The lockdown broke inheritance on files — they have "unique permissions"
with only sharing links, but no user/group grants. This script calls
SharePoint REST API to reset inheritance, so files inherit from the
parent library/site — giving Members (students) their access back.

Usage:
  python restore_inheritance.py --site "2025 Kalam III" --dry-run
  python restore_inheritance.py --site "2025 Kalam III"
  python restore_inheritance.py --all-sites --dry-run
  python restore_inheritance.py --all-sites
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".wmv", ".MP4"}
LOG_FILE = "restore_inheritance_log.json"


def is_video(filename):
    return os.path.splitext(filename.lower())[1] in VIDEO_EXTENSIONS


def get_sharepoint_token(connector):
    """Get a SharePoint-scoped access token (separate from Graph token)."""
    import msal
    authority = f"https://login.microsoftonline.com/{connector.tenant_id}"
    app = msal.ConfidentialClientApplication(
        connector.client_id,
        authority=authority,
        client_credential=connector.client_secret,
        token_cache=msal.SerializableTokenCache(),
    )
    result = app.acquire_token_for_client(
        scopes=[f"https://{connector.sharepoint_site_url}/.default"]
    )
    if "access_token" in result:
        print("[OK] Got SharePoint token")
        return result["access_token"]
    else:
        print(f"[FAIL] SharePoint token error: {result.get('error_description', result)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Restore permission inheritance on video files")
    parser.add_argument("--site", type=str, help="Site name to restore")
    parser.add_argument("--all-sites", action="store_true")
    parser.add_argument("--all-files", action="store_true", help="Restore ALL files, not just videos")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.site and not args.all_sites:
        print("ERROR: Specify --site 'SiteName' or --all-sites")
        sys.exit(1)

    import requests as req

    connector = MS365Connector()
    connector.authenticate_app()

    # Get SharePoint-scoped token for REST API calls
    sp_token = get_sharepoint_token(connector)
    if not sp_token:
        print("[ERROR] Cannot get SharePoint token. Check app permissions.")
        print("  Your app needs Sites.FullControl.All in Azure AD.")
        sys.exit(1)

    sp_headers = {
        "Authorization": f"Bearer {sp_token}",
        "Accept": "application/json;odata=verbose",
    }

    # ── Find target sites ──
    print(f"[*] Searching for sites...")
    result = connector._get(f"{GRAPH_BASE}/sites?search=*&$top=999")
    all_sites = result.get("value", [])
    while "@odata.nextLink" in result:
        result = connector._get(result["@odata.nextLink"])
        all_sites.extend(result.get("value", []))

    if args.site:
        sites = [s for s in all_sites if args.site.lower() in s.get("displayName", "").lower()]
    else:
        sites = all_sites

    if not sites:
        print(f"[ERROR] No sites found matching '{args.site}'")
        sys.exit(1)

    print(f"[*] Will process {len(sites)} site(s)")

    log = []
    stats = {
        "sites": 0, "files_found": 0, "inheritance_restored": 0,
        "already_inheriting": 0, "errors": 0,
    }

    for si, site in enumerate(sites, 1):
        site_name = site.get("displayName", "Unknown")
        site_id = site["id"]
        site_url = site.get("webUrl", "")

        # Refresh tokens
        connector.authenticate_app()
        sp_token = get_sharepoint_token(connector)
        sp_headers["Authorization"] = f"Bearer {sp_token}"

        print(f"\n[{si}/{len(sites)}] {site_name}")
        print(f"  URL: {site_url}")
        stats["sites"] += 1

        # Get drives
        try:
            drives = connector._get(f"{GRAPH_BASE}/sites/{site_id}/drives").get("value", [])
        except Exception as e:
            print(f"  [ERROR] Could not get drives: {e}")
            stats["errors"] += 1
            continue

        for drive in drives:
            drive_id = drive["id"]
            drive_name = drive.get("name", "")

            # Scan for files (with SharePoint IDs)
            files = scan_drive(connector, drive_id, args.all_files)
            stats["files_found"] += len(files)

            if files:
                print(f"  Drive '{drive_name}': {len(files)} files to restore")

            for fi, f in enumerate(files):
                # Get the SharePoint list item info
                try:
                    item_details = connector._get(
                        f"{GRAPH_BASE}/drives/{drive_id}/items/{f['item_id']}?$select=id,name,sharepointIds,parentReference"
                    )
                    sp_ids = item_details.get("sharepointIds", {})
                    list_id = sp_ids.get("listId", "")
                    list_item_id = sp_ids.get("listItemId", "")
                    site_url_from_item = sp_ids.get("siteUrl", site_url)

                    if not list_id or not list_item_id:
                        print(f"    [SKIP] No SharePoint IDs for: {f['name']}")
                        continue

                    # Call SharePoint REST API to reset role inheritance
                    reset_url = f"{site_url_from_item}/_api/web/lists(guid'{list_id}')/items({list_item_id})/resetroleinheritance"

                    if args.dry_run:
                        print(f"    [DRY-RUN] Would restore inheritance: {f['name']}")
                        stats["inheritance_restored"] += 1
                    else:
                        resp = req.post(reset_url, headers=sp_headers)
                        if resp.status_code < 300:
                            stats["inheritance_restored"] += 1
                            log.append({
                                "action": "inheritance_restored",
                                "site": site_name,
                                "filename": f["name"],
                                "drive_id": drive_id,
                                "item_id": f["item_id"],
                                "list_id": list_id,
                                "list_item_id": list_item_id,
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            })
                        elif resp.status_code == 200 or "already inherits" in resp.text.lower():
                            stats["already_inheriting"] += 1
                        else:
                            print(f"    [ERROR] {resp.status_code} on {f['name']}: {resp.text[:150]}")
                            stats["errors"] += 1

                except Exception as e:
                    print(f"    [ERROR] {f['name']}: {e}")
                    stats["errors"] += 1

                # Token refresh every 50 files
                if (fi + 1) % 50 == 0:
                    connector.authenticate_app()
                    sp_token = get_sharepoint_token(connector)
                    sp_headers["Authorization"] = f"Bearer {sp_token}"
                    print(f"    --- {fi+1}/{len(files)} processed ---")

    # Save log
    if not args.dry_run and log:
        with open(LOG_FILE, "w") as f_out:
            json.dump(log, f_out, indent=2)
        print(f"\n[*] Log saved to {LOG_FILE} ({len(log)} entries)")

    mode = " (DRY RUN)" if args.dry_run else ""
    print(f"""
{'='*60}
  RESTORE INHERITANCE{mode}
{'='*60}
  Sites processed:          {stats['sites']}
  Files found:              {stats['files_found']}
  Inheritance restored:     {stats['inheritance_restored']}
  Already inheriting:       {stats['already_inheriting']}
  Errors:                   {stats['errors']}
{'='*60}
  Files now inherit permissions from their parent library/site.
  Students who are site Members can now view these files.
{'='*60}""")


def scan_drive(connector, drive_id, all_files=False, folder="root"):
    """Recursively scan a drive for video files (or all files)."""
    files = []
    try:
        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{folder}/children?$top=200"
        result = connector._get(url)
        items = result.get("value", [])
        while "@odata.nextLink" in result:
            result = connector._get(result["@odata.nextLink"])
            items.extend(result.get("value", []))
        for item in items:
            if "folder" in item:
                files.extend(scan_drive(connector, drive_id, all_files, item["id"]))
            elif "file" in item:
                if all_files or is_video(item["name"]):
                    files.append({"item_id": item["id"], "name": item["name"]})
    except Exception as e:
        if "404" not in str(e):
            print(f"    [WARN] {e}")
    return files


if __name__ == "__main__":
    main()
