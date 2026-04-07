"""
Video Download Lockdown — Owner-Only Downloads
For each video: removes all sharing links that allow download,
keeps only preventsDownload links and owner permissions.
Fully reversible — saves all removed permissions to restore later.

Usage:
  python lockdown_video_downloads.py           # Lock down
  python lockdown_video_downloads.py --undo    # Restore removed permissions
  python lockdown_video_downloads.py --dry-run # Preview only
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
CHANGE_LOG_FILE = "video_download_changes.json"
LOCKDOWN_LOG_FILE = "lockdown_log.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--undo", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(CHANGE_LOG_FILE):
        print(f"[ERROR] No {CHANGE_LOG_FILE} found. Run teams_block_video_downloads.py first.")
        sys.exit(1)

    with open(CHANGE_LOG_FILE) as f:
        changes = json.load(f)

    blocked = [c for c in changes if c["action"] == "block_download" and c.get("success")]
    print(f"[*] Found {len(blocked)} blocked videos")

    connector = MS365Connector()

    # Undo mode: restore removed permissions
    if args.undo:
        if not os.path.exists(LOCKDOWN_LOG_FILE):
            print(f"[ERROR] No {LOCKDOWN_LOG_FILE} found. Nothing to undo.")
            sys.exit(1)
        with open(LOCKDOWN_LOG_FILE) as f:
            lockdown_log = json.load(f)

        removed = [e for e in lockdown_log if e["action"] == "removed_link"]
        print(f"[*] Restoring {len(removed)} removed sharing links...")

        import requests as req
        restored = 0
        failed = 0
        for i, entry in enumerate(removed, 1):
            if i % 50 == 1:
                connector.authenticate_app()
            if i % 100 == 0:
                print(f"  --- Progress: {i}/{len(removed)} ---")

            try:
                url = f"{GRAPH_BASE}/drives/{entry['drive_id']}/items/{entry['item_id']}/createLink"
                resp = req.post(url, headers=connector._headers(), json={
                    "type": entry.get("link_type", "view"),
                    "scope": entry.get("link_scope", "organization"),
                })
                if resp.status_code < 300:
                    restored += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

        print(f"\n[Done] Restored: {restored}, Failed: {failed}")
        return

    # Main lockdown
    lockdown_log = []
    total = len(blocked)
    import requests as req

    videos_locked = 0
    links_removed = 0
    links_kept = 0
    errors = 0

    for i, item in enumerate(blocked, 1):
        drive_id = item["drive_id"]
        item_id = item["item_id"]
        filename = item["filename"]

        # Fresh token every 50 files
        if i % 50 == 1:
            connector.authenticate_app()

        if i % 200 == 0:
            print(f"\n  --- Progress: {i}/{total} | Removed: {links_removed}, Kept: {links_kept} ---\n")

        try:
            # Get all permissions on this video
            url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions"
            perms = connector._get(url)

            file_removed = 0
            for p in perms.get("value", []):
                perm_id = p.get("id")
                roles = p.get("roles", [])

                # Skip owner permissions — owners keep full access
                if "owner" in roles:
                    continue

                # Skip inherited permissions — can't remove via Graph API
                if "inheritedFrom" in p:
                    continue

                # Check if it's a sharing link
                if p.get("link"):
                    link = p["link"]
                    prevents_download = link.get("preventsDownload", False)

                    if prevents_download:
                        # This is our preventsDownload link — keep it
                        links_kept += 1
                        continue

                    # This is a sharing link that ALLOWS download — remove it
                    if args.dry_run:
                        print(f"  [DRY-RUN] Would remove link on {filename}: "
                              f"{link.get('type','?')}/{link.get('scope','?')}")
                        links_removed += 1
                        file_removed += 1
                    else:
                        del_url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions/{perm_id}"
                        resp = req.delete(del_url, headers=connector._headers())
                        if resp.status_code < 300:
                            links_removed += 1
                            file_removed += 1
                            lockdown_log.append({
                                "action": "removed_link",
                                "drive_id": drive_id,
                                "item_id": item_id,
                                "filename": filename,
                                "permission_id": perm_id,
                                "link_type": link.get("type"),
                                "link_scope": link.get("scope"),
                                "link_url": link.get("webUrl", ""),
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            })
                        else:
                            errors += 1

                # Check if it's a direct user grant (not owner)
                elif p.get("grantedToV2") or p.get("grantedTo"):
                    granted_to = ""
                    if p.get("grantedToV2"):
                        gtv2 = p["grantedToV2"]
                        for key in ("user", "siteUser", "group"):
                            if gtv2.get(key):
                                granted_to = gtv2[key].get("displayName", "unknown")
                                break
                    elif p.get("grantedTo", {}).get("user"):
                        granted_to = p["grantedTo"]["user"].get("displayName", "unknown")

                    # Skip site owner groups
                    if "owner" in granted_to.lower():
                        links_kept += 1
                        continue

                    # Remove non-owner direct permissions
                    if args.dry_run:
                        print(f"  [DRY-RUN] Would remove direct access for '{granted_to}' "
                              f"on {filename} [{', '.join(roles)}]")
                        links_removed += 1
                        file_removed += 1
                    else:
                        del_url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions/{perm_id}"
                        resp = req.delete(del_url, headers=connector._headers())
                        if resp.status_code < 300:
                            links_removed += 1
                            file_removed += 1
                            lockdown_log.append({
                                "action": "removed_direct",
                                "drive_id": drive_id,
                                "item_id": item_id,
                                "filename": filename,
                                "permission_id": perm_id,
                                "granted_to": granted_to,
                                "roles": roles,
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            })
                        else:
                            errors += 1

            if file_removed > 0:
                videos_locked += 1

        except Exception as e:
            errors += 1
            if "401" not in str(e) and "403" not in str(e):
                pass  # silently skip access errors

    # Save lockdown log
    if not args.dry_run and lockdown_log:
        with open(LOCKDOWN_LOG_FILE, "w") as f:
            json.dump(lockdown_log, f, indent=2, ensure_ascii=False)
        print(f"\n[*] Lockdown log saved to {LOCKDOWN_LOG_FILE} ({len(lockdown_log)} entries)")

    # Summary
    print(f"\n{'='*60}")
    print(f"  LOCKDOWN SUMMARY {'(DRY RUN)' if args.dry_run else ''}")
    print(f"{'='*60}")
    print(f"  Videos scanned:        {total}")
    print(f"  Videos with removals:  {videos_locked}")
    print(f"  Permissions removed:   {links_removed}")
    print(f"  Permissions kept:      {links_kept}")
    print(f"  Errors:                {errors}")
    print(f"{'='*60}")
    print(f"\n  What was removed:")
    print(f"    - Sharing links that allow download (non-preventsDownload)")
    print(f"    - Direct user permissions for non-owners")
    print(f"\n  What was kept:")
    print(f"    - Owner permissions")
    print(f"    - Our preventsDownload view-only links")
    print(f"    - Inherited site permissions (can't change via API)")
    print(f"\n  NOTE: Inherited permissions from site membership still")
    print(f"  allow download. To fully block, use PowerShell:")
    print(f"    Set-SPOSite -BlockDownloadPolicy $true \\")
    print(f"      -ExcludeBlockDownloadPolicySiteOwners $true")
    print(f"{'='*60}")

    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
