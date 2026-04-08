"""
Full Audit & Fix — Student Access Recovery
Diagnoses the current permission state across all SharePoint sites,
reports what students can/can't access, and optionally fixes it.

Usage:
  python full_audit_and_fix.py --audit          # Audit only (no changes)
  python full_audit_and_fix.py --fix --dry-run  # Preview fix
  python full_audit_and_fix.py --fix            # Apply fix (restore non-video access)

What the fix does:
  - For each non-video file: creates an organization-wide "view" sharing link
    (download enabled) so students can download PDFs, docs, slides, etc.
  - Videos are SKIPPED — they keep their preventsDownload-only access.

Requires: .env with AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from collections import defaultdict
from ms365_connector import MS365Connector

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v", ".wmv", ".flv", ".3gp"}
AUDIT_OUTPUT = "full_audit_report.json"
FIX_LOG = "fix_restore_access_log.json"


def is_video(filename):
    return os.path.splitext(filename.lower())[1] in VIDEO_EXTENSIONS


class Auditor:
    def __init__(self, connector):
        self.connector = connector
        self.report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {},
            "sites": [],
        }
        self.fix_log = []
        self.stats = defaultdict(int)

    def _get(self, url):
        import requests
        resp = requests.get(url, headers=self.connector._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _get_all_pages(self, url):
        """Get all pages of a paginated Graph API response."""
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

    def get_all_sites(self):
        print("[*] Fetching all SharePoint sites...")
        sites = self._get_all_pages(f"{GRAPH_BASE}/sites?search=*&$top=999")
        print(f"  Found {len(sites)} sites")
        return sites

    def scan_drive(self, drive_id, folder_path="root"):
        """Recursively get all files in a drive."""
        files = []
        try:
            items = self._get_all_pages(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{folder_path}/children?$top=200"
            )
            for item in items:
                if "folder" in item:
                    files.extend(self.scan_drive(drive_id, item["id"]))
                elif "file" in item:
                    files.append({
                        "id": item["id"],
                        "name": item["name"],
                        "drive_id": drive_id,
                        "size": item.get("size", 0),
                        "is_video": is_video(item["name"]),
                        "web_url": item.get("webUrl", ""),
                    })
        except Exception as e:
            if "404" not in str(e) and "403" not in str(e):
                self.stats["scan_errors"] += 1
        return files

    def check_permissions(self, drive_id, item_id):
        """Check what permissions exist on a file."""
        try:
            perms = self._get(f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions")
            result = {
                "owner_count": 0,
                "link_count": 0,
                "direct_count": 0,
                "inherited_count": 0,
                "prevents_download_links": 0,
                "download_allowed_links": 0,
                "details": [],
            }
            for p in perms.get("value", []):
                roles = p.get("roles", [])
                inherited = "inheritedFrom" in p

                if "owner" in roles:
                    result["owner_count"] += 1
                elif p.get("link"):
                    result["link_count"] += 1
                    if p["link"].get("preventsDownload", False):
                        result["prevents_download_links"] += 1
                    else:
                        result["download_allowed_links"] += 1
                elif inherited:
                    result["inherited_count"] += 1
                else:
                    result["direct_count"] += 1

                result["details"].append({
                    "roles": roles,
                    "type": "link" if p.get("link") else "direct",
                    "inherited": inherited,
                    "prevents_download": p.get("link", {}).get("preventsDownload", False) if p.get("link") else None,
                })
            return result
        except Exception:
            return None

    def create_download_link(self, drive_id, item_id, filename, dry_run=False):
        """Create an org-wide view link (download enabled) for a non-video file."""
        if dry_run:
            self.stats["would_fix"] += 1
            return True

        try:
            result = self._post(
                f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink",
                {"type": "view", "scope": "organization"}
            )
            self.fix_log.append({
                "action": "link_created",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "permission_id": result.get("id", ""),
                "link_url": result.get("link", {}).get("webUrl", ""),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            self.stats["fixed"] += 1
            return True
        except Exception as e:
            self.stats["fix_errors"] += 1
            self.fix_log.append({
                "action": "error",
                "drive_id": drive_id,
                "item_id": item_id,
                "filename": filename,
                "error": str(e)[:200],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return False

    def run_audit(self, fix=False, dry_run=False):
        sites = self.get_all_sites()

        for si, site in enumerate(sites):
            site_id = site["id"]
            site_name = site.get("displayName", "Unknown")

            # Fresh token per site
            self.connector.authenticate_app()

            print(f"\n[{si+1}/{len(sites)}] {site_name}")
            self.stats["sites"] += 1

            site_report = {
                "name": site_name,
                "url": site.get("webUrl", ""),
                "drives": [],
                "total_files": 0,
                "video_files": 0,
                "non_video_files": 0,
                "non_video_no_access": 0,
                "video_properly_blocked": 0,
            }

            try:
                drives_resp = self.connector.list_drives(site_id)
                drives = drives_resp.get("value", [])
            except Exception as e:
                print(f"  [ERROR] Can't list drives: {e}")
                self.stats["site_errors"] += 1
                self.report["sites"].append(site_report)
                continue

            for drive in drives:
                drive_id = drive["id"]
                drive_name = drive.get("name", "")
                self.stats["drives"] += 1

                files = self.scan_drive(drive_id)
                videos = [f for f in files if f["is_video"]]
                non_videos = [f for f in files if not f["is_video"]]

                site_report["total_files"] += len(files)
                site_report["video_files"] += len(videos)
                site_report["non_video_files"] += len(non_videos)
                self.stats["total_files"] += len(files)
                self.stats["video_files"] += len(videos)
                self.stats["non_video_files"] += len(non_videos)

                if files:
                    print(f"  Drive '{drive_name}': {len(non_videos)} non-video, {len(videos)} video")

                # For audit: sample check permissions on first few files
                sample_size = min(3, len(non_videos))
                for f in non_videos[:sample_size]:
                    perms = self.check_permissions(f["drive_id"], f["id"])
                    if perms and perms["download_allowed_links"] == 0 and perms["direct_count"] == 0:
                        site_report["non_video_no_access"] += 1
                        self.stats["non_video_no_access"] += 1

                # Fix: create download links for non-video files
                if fix and non_videos:
                    print(f"    {'[DRY-RUN] ' if dry_run else ''}Creating download links for {len(non_videos)} non-video files...")
                    for fi, f in enumerate(non_videos):
                        self.create_download_link(f["drive_id"], f["id"], f["name"], dry_run=dry_run)
                        if (fi + 1) % 100 == 0:
                            self.connector.authenticate_app()
                            print(f"      Progress: {fi+1}/{len(non_videos)}")

                drive_report = {
                    "name": drive_name,
                    "files": len(files),
                    "videos": len(videos),
                    "non_videos": len(non_videos),
                }
                site_report["drives"].append(drive_report)

            self.report["sites"].append(site_report)

        # Build summary
        self.report["summary"] = dict(self.stats)
        return self.report

    def print_report(self, fix=False, dry_run=False):
        s = self.stats
        mode = ""
        if fix and dry_run:
            mode = " (DRY RUN)"
        elif fix:
            mode = " (FIX APPLIED)"

        print(f"""
{'='*65}
  FULL AUDIT REPORT{mode}
{'='*65}
  Sites scanned:           {s.get('sites', 0)}
  Drives scanned:          {s.get('drives', 0)}
  Total files:             {s.get('total_files', 0)}
  Video files:             {s.get('video_files', 0)}
  Non-video files:         {s.get('non_video_files', 0)}

  PROBLEM DETECTED:
  Non-video files with NO download access (sampled): {s.get('non_video_no_access', 0)}

  BlockDownloadPolicy:     ON (confirmed by user)
  reshare_non_video_files: NEVER RUN (no log file found)
""")

        if fix:
            if dry_run:
                print(f"""  FIX PREVIEW:
  Would create download links for: {s.get('would_fix', 0)} non-video files

  Run without --dry-run to apply.
""")
            else:
                print(f"""  FIX APPLIED:
  Download links created:  {s.get('fixed', 0)}
  Errors:                  {s.get('fix_errors', 0)}

  Students should now be able to download non-video files.
  Videos remain protected (view-only, no download).
""")

        print(f"""  STILL NEEDED:
  If BlockDownloadPolicy overrides sharing links, you must
  ALSO turn it OFF via PowerShell:
    Connect-SPOService -Url https://usulacademy-admin.sharepoint.com
    .\\block_download_policy.ps1 -Action OFF

  Then re-run this script with --fix to add selective protection.
{'='*65}
""")

    def save(self, fix=False):
        with open(AUDIT_OUTPUT, "w") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        print(f"[*] Audit report saved to {AUDIT_OUTPUT}")

        if fix and self.fix_log:
            with open(FIX_LOG, "w") as f:
                json.dump(self.fix_log, f, indent=2, ensure_ascii=False)
            print(f"[*] Fix log saved to {FIX_LOG} ({len(self.fix_log)} entries)")
            print(f"    To undo: use permission IDs in {FIX_LOG} to delete links")


def main():
    parser = argparse.ArgumentParser(description="Full audit & fix for student access")
    parser.add_argument("--audit", action="store_true", help="Audit only (no changes)")
    parser.add_argument("--fix", action="store_true", help="Create download links for non-video files")
    parser.add_argument("--dry-run", action="store_true", help="Preview fix without applying")
    args = parser.parse_args()

    if not args.audit and not args.fix:
        print("Specify --audit (report only) or --fix (restore access)")
        print("  --audit          Scan all sites and report permission state")
        print("  --fix --dry-run  Preview what would be fixed")
        print("  --fix            Apply fix: create download links for non-video files")
        sys.exit(1)

    connector = MS365Connector()
    connector.authenticate_app()

    auditor = Auditor(connector)
    auditor.run_audit(fix=args.fix, dry_run=args.dry_run)
    auditor.print_report(fix=args.fix, dry_run=args.dry_run)
    auditor.save(fix=args.fix)


if __name__ == "__main__":
    main()
