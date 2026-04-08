"""
Restore Permission Inheritance — Graph API version.
Uses Microsoft Graph invite endpoint to grant the site's Members group
Read access to video files, fixing "None" permissions for students.

No SharePoint REST API needed — works with existing Graph permissions.

Usage:
  python restore_inheritance.py --site "2025 Kalam III" --dry-run
  python restore_inheritance.py --site "2025 Kalam III"
  python restore_inheritance.py --all-sites --dry-run
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


def main():
    parser = argparse.ArgumentParser(description="Restore student view access on video files")
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

    # ── Find target sites ──
    print("[*] Searching for sites...")
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
        "sites": 0, "files_found": 0, "access_granted": 0,
        "already_has_access": 0, "errors": 0, "group_not_found": 0,
    }

    for si, site in enumerate(sites, 1):
        site_name = site.get("displayName", "Unknown")
        site_id = site["id"]

        connector.authenticate_app()
        stats["sites"] += 1

        print(f"\n{'='*60}")
        print(f"[{si}/{len(sites)}] {site_name}")
        print(f"{'='*60}")

        # ── Step 1: Find the M365 group (Members) for this site ──
        members_group = find_members_group(connector, site_name, req)

        if not members_group:
            print(f"  [WARN] No Members group found for {site_name}")
            print(f"  Trying to find site group via site permissions...")
            members_group = find_group_from_site_permissions(connector, site_id, req)

        if not members_group:
            print(f"  [SKIP] Cannot find Members group — skipping site")
            stats["group_not_found"] += 1
            continue

        group_id = members_group["id"]
        group_name = members_group.get("displayName", "Unknown")
        group_email = members_group.get("mail", "")
        print(f"  [OK] Members group: {group_name} (id={group_id[:20]}...)")
        if group_email:
            print(f"       Email: {group_email}")

        # ── Step 2: Get drives and scan files ──
        try:
            drives = connector._get(f"{GRAPH_BASE}/sites/{site_id}/drives").get("value", [])
        except Exception as e:
            print(f"  [ERROR] Could not get drives: {e}")
            stats["errors"] += 1
            continue

        for drive in drives:
            drive_id = drive["id"]
            drive_name = drive.get("name", "")

            files = scan_drive(connector, drive_id, args.all_files)
            stats["files_found"] += len(files)

            if files:
                print(f"  Drive '{drive_name}': {len(files)} files")

            # ── Step 3: Grant Members group Read access to each file ──
            for fi, f in enumerate(files):
                try:
                    if args.dry_run:
                        print(f"    [DRY-RUN] Would grant '{group_name}' Read on: {f['name']}")
                        stats["access_granted"] += 1
                    else:
                        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{f['item_id']}/invite"
                        payload = {
                            "recipients": [{"objectId": group_id}],
                            "roles": ["read"],
                            "requireSignIn": True,
                            "sendInvitation": False,
                        }
                        resp = req.post(url, headers=connector._headers(), json=payload, timeout=30)

                        if resp.status_code < 300:
                            stats["access_granted"] += 1
                            log.append({
                                "action": "granted_read",
                                "site": site_name,
                                "filename": f["name"],
                                "drive_id": drive_id,
                                "item_id": f["item_id"],
                                "group_id": group_id,
                                "group_name": group_name,
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            })
                        elif resp.status_code == 409 or "already" in resp.text.lower():
                            stats["already_has_access"] += 1
                        else:
                            print(f"    [ERROR] {resp.status_code} on {f['name']}: {resp.text[:200]}")
                            stats["errors"] += 1

                except Exception as e:
                    print(f"    [ERROR] {f['name']}: {e}")
                    stats["errors"] += 1

                # Token refresh every 50 files
                if (fi + 1) % 50 == 0:
                    connector.authenticate_app()
                    print(f"    --- {fi+1}/{len(files)} processed ---")

    # Save log
    if not args.dry_run and log:
        with open(LOG_FILE, "w") as f_out:
            json.dump(log, f_out, indent=2)
        print(f"\n[*] Log saved to {LOG_FILE} ({len(log)} entries)")

    mode = " (DRY RUN)" if args.dry_run else ""
    print(f"""
{'='*60}
  RESTORE ACCESS{mode}
{'='*60}
  Sites processed:          {stats['sites']}
  Files found:              {stats['files_found']}
  Access granted:           {stats['access_granted']}
  Already had access:       {stats['already_has_access']}
  Groups not found:         {stats['group_not_found']}
  Errors:                   {stats['errors']}
{'='*60}
  The Members group now has Read access on these files.
  Students should see files when they check permissions.
{'='*60}""")


def find_members_group(connector, site_name, req):
    """Find the M365 group for a Teams site by searching groups."""
    # Try exact name search
    headers = connector._headers()
    headers["ConsistencyLevel"] = "eventual"

    # Search for the group by site name
    search_terms = [
        site_name,                    # exact name
        site_name.replace(" ", ""),    # no spaces
    ]

    for term in search_terms:
        try:
            url = f'{GRAPH_BASE}/groups?$search="displayName:{term}"&$select=id,displayName,mail,groupTypes&$top=10'
            resp = req.get(url, headers=headers, timeout=30)
            if resp.status_code < 300:
                groups = resp.json().get("value", [])
                for g in groups:
                    # Match: group name equals site name or is very close
                    if g.get("displayName", "").lower() == site_name.lower():
                        return g
                    if site_name.lower() in g.get("displayName", "").lower():
                        return g
        except:
            pass

    # Fallback: try filter
    try:
        url = f"{GRAPH_BASE}/groups?$filter=displayName eq '{site_name}'&$select=id,displayName,mail"
        resp = req.get(url, headers=connector._headers(), timeout=30)
        if resp.status_code < 300:
            groups = resp.json().get("value", [])
            if groups:
                return groups[0]
    except:
        pass

    return None


def find_group_from_site_permissions(connector, site_id, req):
    """Try to find the Members group by looking at existing site permissions."""
    try:
        # Check site-level permissions
        url = f"{GRAPH_BASE}/sites/{site_id}/permissions"
        resp = req.get(url, headers=connector._headers(), timeout=30)
        if resp.status_code < 300:
            perms = resp.json().get("value", [])
            for p in perms:
                identity = p.get("grantedToIdentitiesV2", []) or p.get("grantedToIdentities", [])
                for ident in identity:
                    app = ident.get("application", {})
                    user = ident.get("user", {})
                    group = ident.get("group", {})
                    if group and group.get("id"):
                        return {"id": group["id"], "displayName": group.get("displayName", "Unknown")}
    except:
        pass

    # Try getting the group from the associated Teams team
    try:
        url = f"{GRAPH_BASE}/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')&$select=id,displayName,mail&$top=999"
        resp = req.get(url, headers=connector._headers(), timeout=30)
        if resp.status_code < 300:
            groups = resp.json().get("value", [])
            for g in groups:
                # Find matching group by name similarity
                gname = g.get("displayName", "").lower()
                if gname in connector._get(f"{GRAPH_BASE}/sites/{site_id}").get("displayName", "").lower():
                    return g
    except:
        pass

    return None


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
