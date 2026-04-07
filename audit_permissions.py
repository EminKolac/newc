"""
Video Permissions Auditor
Scans all blocked videos and reports who can view each one.

Reads the change log from the blocking run, then checks Graph API
permissions for each video file.

Usage:
  python audit_permissions.py
"""

import os
import sys
import json
from datetime import datetime
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
CHANGE_LOG_FILE = "video_download_changes.json"
PERM_AUDIT_FILE = "permissions_audit.json"


def main():
    if not os.path.exists(CHANGE_LOG_FILE):
        print(f"[ERROR] No change log found at {CHANGE_LOG_FILE}. Run the blocker first.")
        sys.exit(1)

    with open(CHANGE_LOG_FILE) as f:
        changes = json.load(f)

    blocked = [c for c in changes if c["action"] == "block_download" and c.get("success")]
    print(f"[*] Found {len(blocked)} blocked videos to audit permissions for")

    connector = MS365Connector()

    audit_results = []
    total = len(blocked)

    for i, item in enumerate(blocked, 1):
        drive_id = item["drive_id"]
        item_id = item["item_id"]
        filename = item["filename"]

        # Fresh token every 50 files
        if i % 50 == 1:
            connector.authenticate_app()

        if i % 100 == 0:
            print(f"\n  --- Progress: {i}/{total} ---\n")

        try:
            url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions"
            perms = connector._get(url)

            perm_list = []
            for p in perms.get("value", []):
                entry = {
                    "id": p.get("id"),
                    "roles": p.get("roles", []),
                }

                # Who was granted access
                if p.get("grantedToV2"):
                    gtv2 = p["grantedToV2"]
                    if gtv2.get("user"):
                        entry["granted_to"] = gtv2["user"].get("displayName", gtv2["user"].get("email", "unknown user"))
                        entry["type"] = "user"
                    elif gtv2.get("siteUser"):
                        entry["granted_to"] = gtv2["siteUser"].get("displayName", "site user")
                        entry["type"] = "site_user"
                    elif gtv2.get("group"):
                        entry["granted_to"] = gtv2["group"].get("displayName", "group")
                        entry["type"] = "group"
                    elif gtv2.get("application"):
                        entry["granted_to"] = gtv2["application"].get("displayName", "app")
                        entry["type"] = "application"
                elif p.get("grantedTo"):
                    gt = p["grantedTo"]
                    if gt.get("user"):
                        entry["granted_to"] = gt["user"].get("displayName", gt["user"].get("email", "unknown"))
                        entry["type"] = "user"

                # Sharing link info
                if p.get("link"):
                    link = p["link"]
                    entry["type"] = "link"
                    entry["link_type"] = link.get("type", "unknown")
                    entry["link_scope"] = link.get("scope", "unknown")
                    entry["prevents_download"] = link.get("preventsDownload", False)
                    entry["link_url"] = link.get("webUrl", "")

                # Inherited or direct
                entry["inherited"] = "inheritedFrom" in p

                perm_list.append(entry)

            audit_results.append({
                "filename": filename,
                "drive_id": drive_id,
                "item_id": item_id,
                "permissions_count": len(perm_list),
                "permissions": perm_list,
            })

        except Exception as e:
            err_str = str(e)
            if "401" in err_str or "403" in err_str:
                audit_results.append({
                    "filename": filename,
                    "drive_id": drive_id,
                    "item_id": item_id,
                    "permissions_count": -1,
                    "error": err_str[:200],
                    "permissions": [],
                })
            else:
                print(f"  [ERROR] {filename}: {err_str[:100]}")
                audit_results.append({
                    "filename": filename,
                    "drive_id": drive_id,
                    "item_id": item_id,
                    "permissions_count": -1,
                    "error": err_str[:200],
                    "permissions": [],
                })

    # Save full audit
    with open(PERM_AUDIT_FILE, "w") as f:
        json.dump(audit_results, f, indent=2, ensure_ascii=False)
    print(f"\n[*] Full permissions audit saved to {PERM_AUDIT_FILE}")

    # Print summary
    print(f"\n{'='*70}")
    print(f"  PERMISSIONS AUDIT SUMMARY")
    print(f"{'='*70}")
    print(f"  Videos audited:  {len(audit_results)}")

    errors = [r for r in audit_results if r["permissions_count"] == -1]
    print(f"  Errors:          {len(errors)}")

    # Count download-blocked links
    blocked_count = 0
    not_blocked = 0
    for r in audit_results:
        has_block = False
        for p in r.get("permissions", []):
            if p.get("prevents_download"):
                has_block = True
                break
        if has_block:
            blocked_count += 1
        elif r["permissions_count"] >= 0:
            not_blocked += 1

    print(f"  Download blocked: {blocked_count}")
    print(f"  NOT blocked:      {not_blocked}")

    # Who can view - aggregate
    print(f"\n  ACCESS TYPES ACROSS ALL VIDEOS:")
    type_counts = {}
    scope_counts = {}
    viewer_set = set()

    for r in audit_results:
        for p in r.get("permissions", []):
            ptype = p.get("type", "unknown")
            type_counts[ptype] = type_counts.get(ptype, 0) + 1

            if ptype == "link":
                scope = p.get("link_scope", "unknown")
                scope_counts[scope] = scope_counts.get(scope, 0) + 1
            elif ptype in ("user", "site_user", "group"):
                viewer_set.add(p.get("granted_to", "unknown"))

    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"    {t}: {count} permissions")

    if scope_counts:
        print(f"\n  SHARING LINK SCOPES:")
        for s, count in sorted(scope_counts.items(), key=lambda x: -x[1]):
            print(f"    {s}: {count} links")

    if viewer_set:
        print(f"\n  NAMED USERS/GROUPS WITH ACCESS ({len(viewer_set)} unique):")
        for v in sorted(viewer_set):
            print(f"    - {v}")

    # Show first 5 videos as sample
    print(f"\n  SAMPLE (first 5 videos):")
    print(f"  {'-'*65}")
    for r in audit_results[:5]:
        print(f"  {r['filename']}")
        for p in r.get("permissions", []):
            if p.get("type") == "link":
                dl = "BLOCKED" if p.get("prevents_download") else "ALLOWED"
                print(f"    Link: {p.get('link_type','?')} / {p.get('link_scope','?')} / download={dl}")
            elif p.get("granted_to"):
                print(f"    {p['type']}: {p['granted_to']} [{', '.join(p.get('roles',[]))}]")
            else:
                print(f"    {p.get('type','?')}: roles={p.get('roles',[])}")
        print()

    print(f"{'='*70}")


if __name__ == "__main__":
    main()
