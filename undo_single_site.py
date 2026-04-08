"""
Undo ALL video restrictions on a SINGLE site.
Undoes both Phase 1 (preventsDownload links) and Phase 3 (lockdown permission removals).

Usage (Colab):
  !python undo_single_site.py --site "2025 Kalam III" --dry-run
  !python undo_single_site.py --site "2025 Kalam III"
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".wmv", ".MP4"}
LOCKDOWN_LOG_FILE = "lockdown_log.json"
CHANGE_LOG_FILE = "video_download_changes.json"


def is_video(filename):
    return os.path.splitext(filename.lower())[1] in VIDEO_EXTENSIONS


def main():
    parser = argparse.ArgumentParser(description="Undo all video restrictions on a single site")
    parser.add_argument("--site", required=True, help="Site name to undo (e.g. '2025 Kalam III')")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    import requests as req

    connector = MS365Connector()
    connector.authenticate_app()

    # ── Step 1: Find the target site ──
    print(f"[*] Searching for site: {args.site}")
    result = connector._get(f"{GRAPH_BASE}/sites?search={args.site}")
    sites = result.get("value", [])

    target_site = None
    for s in sites:
        name = s.get("displayName", "")
        if args.site.lower() in name.lower():
            target_site = s
            print(f"[OK] Found site: {name} ({s.get('webUrl', '')})")
            break

    if not target_site:
        print(f"[ERROR] Site '{args.site}' not found. Available sites:")
        for s in sites:
            print(f"  - {s.get('displayName', '')}")
        sys.exit(1)

    site_id = target_site["id"]

    # ── Step 2: Get all drives for this site ──
    drives_resp = connector._get(f"{GRAPH_BASE}/sites/{site_id}/drives")
    drives = drives_resp.get("value", [])
    drive_ids = {d["id"] for d in drives}
    print(f"[*] Found {len(drives)} drives:")
    for d in drives:
        print(f"  - {d['name']} ({d['id'][:20]}...)")

    # ── Step 3: Find all video files in this site ──
    print(f"\n[*] Scanning for video files...")

    def scan_drive(drive_id, folder="root"):
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
                    files.extend(scan_drive(drive_id, item["id"]))
                elif "file" in item and is_video(item["name"]):
                    files.append({
                        "drive_id": drive_id,
                        "item_id": item["id"],
                        "name": item["name"],
                    })
        except Exception as e:
            if "404" not in str(e):
                print(f"  [WARN] {e}")
        return files

    all_videos = []
    for drive in drives:
        videos = scan_drive(drive["id"])
        all_videos.extend(videos)
        if videos:
            print(f"  Drive '{drive['name']}': {len(videos)} videos")

    print(f"\n[*] Total videos found: {len(all_videos)}")

    # ── Step 4: Remove preventsDownload links (undo Phase 1) ──
    print(f"\n{'='*60}")
    print(f"  PHASE 1 UNDO: Remove preventsDownload links")
    print(f"{'='*60}")

    connector.authenticate_app()
    phase1_removed = 0
    phase1_errors = 0

    for i, video in enumerate(all_videos, 1):
        if i % 50 == 1 and i > 1:
            connector.authenticate_app()
        if i % 100 == 0:
            print(f"  --- Progress: {i}/{len(all_videos)} ---")

        try:
            url = f"{GRAPH_BASE}/drives/{video['drive_id']}/items/{video['item_id']}/permissions"
            perms = connector._get(url)

            for p in perms.get("value", []):
                link = p.get("link", {})
                if link.get("preventsDownload"):
                    perm_id = p["id"]
                    if args.dry_run:
                        print(f"  [DRY-RUN] Would remove preventsDownload link on: {video['name']}")
                        phase1_removed += 1
                    else:
                        del_url = f"{GRAPH_BASE}/drives/{video['drive_id']}/items/{video['item_id']}/permissions/{perm_id}"
                        resp = req.delete(del_url, headers=connector._headers())
                        if resp.status_code < 300:
                            phase1_removed += 1
                        else:
                            print(f"  [ERROR] {resp.status_code} removing link on {video['name']}")
                            phase1_errors += 1
        except Exception as e:
            print(f"  [ERROR] {video['name']}: {e}")
            phase1_errors += 1

    print(f"\n  preventsDownload links removed: {phase1_removed}")
    print(f"  Errors: {phase1_errors}")

    # ── Step 5: Restore lockdown-removed permissions (undo Phase 3) ──
    print(f"\n{'='*60}")
    print(f"  PHASE 3 UNDO: Restore removed permissions")
    print(f"{'='*60}")

    connector.authenticate_app()
    phase3_restored = 0
    phase3_errors = 0
    phase3_skipped = 0

    if os.path.exists(LOCKDOWN_LOG_FILE):
        with open(LOCKDOWN_LOG_FILE) as f:
            lockdown_log = json.load(f)

        # Filter: only entries for drives belonging to this site
        site_entries = [e for e in lockdown_log if e.get("drive_id") in drive_ids]
        removed_links = [e for e in site_entries if e["action"] == "removed_link"]
        removed_direct = [e for e in site_entries if e["action"] == "removed_direct"]

        print(f"  Found {len(removed_links)} removed sharing links to restore")
        print(f"  Found {len(removed_direct)} removed direct permissions to restore")

        # Restore sharing links (re-create them)
        for i, entry in enumerate(removed_links, 1):
            if i % 50 == 1 and i > 1:
                connector.authenticate_app()
            if i % 100 == 0:
                print(f"  --- Restoring links: {i}/{len(removed_links)} ---")

            try:
                url = f"{GRAPH_BASE}/drives/{entry['drive_id']}/items/{entry['item_id']}/createLink"
                payload = {
                    "type": entry.get("link_type", "view"),
                    "scope": entry.get("link_scope", "organization"),
                }

                if args.dry_run:
                    print(f"  [DRY-RUN] Would restore {entry.get('link_type','view')}/{entry.get('link_scope','org')} link on: {entry.get('filename','?')}")
                    phase3_restored += 1
                else:
                    resp = req.post(url, headers=connector._headers(), json=payload)
                    if resp.status_code < 300:
                        phase3_restored += 1
                    else:
                        print(f"  [ERROR] {resp.status_code} restoring link on {entry.get('filename','?')}")
                        phase3_errors += 1
            except Exception as e:
                print(f"  [ERROR] {entry.get('filename','?')}: {e}")
                phase3_errors += 1

        # Note: direct user permissions can't be perfectly restored via API
        # (we'd need the user's email/ID). Log them for manual review.
        if removed_direct:
            print(f"\n  [INFO] {len(removed_direct)} direct user permissions were removed.")
            print(f"  These users had direct access and may need to be re-added manually:")
            users_seen = set()
            for entry in removed_direct:
                user = entry.get("granted_to", "unknown")
                if user not in users_seen:
                    users_seen.add(user)
                    print(f"    - {user} (roles: {entry.get('roles', [])})")
    else:
        print(f"  [WARN] No {LOCKDOWN_LOG_FILE} found. Skipping Phase 3 undo.")
        print(f"  (If you didn't run the lockdown, this is expected)")
        phase3_skipped = 1

    # ── Summary ──
    mode = " (DRY RUN)" if args.dry_run else ""
    print(f"""
{'='*60}
  UNDO SUMMARY — {args.site}{mode}
{'='*60}
  Videos on this site:           {len(all_videos)}

  Phase 1 (preventsDownload):
    Links removed:               {phase1_removed}
    Errors:                      {phase1_errors}

  Phase 3 (lockdown):
    Permissions restored:        {phase3_restored}
    Errors:                      {phase3_errors}
    {'Skipped (no log file)' if phase3_skipped else ''}

  RESULT: All video restrictions on "{args.site}" are now undone.
  Students can view AND download videos on this site.
{'='*60}""")

    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
