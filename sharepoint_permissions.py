"""
SharePoint Permissions Manager
Handles file permission requests for emin.kolac@usul.academy

Usage:
  python sharepoint_permissions.py list-sites
  python sharepoint_permissions.py list-files <site-id> [drive-id]
  python sharepoint_permissions.py permissions <drive-id> <item-id>
  python sharepoint_permissions.py grant <drive-id> <item-id> <email> [read|write]
  python sharepoint_permissions.py share <drive-id> <item-id> [view|edit]
  python sharepoint_permissions.py search <query>
"""

import sys
import json
from ms365_connector import MS365Connector


def pretty(data):
    print(json.dumps(data, indent=2, default=str))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    connector = MS365Connector()

    if not connector.authenticate_app():
        if not connector.authenticate_device_code():
            sys.exit(1)

    if cmd == "list-sites":
        sites = connector.list_sharepoint_sites()
        for site in sites.get("value", []):
            print(f"\n  Site: {site['displayName']}")
            print(f"  URL:  {site['webUrl']}")
            print(f"  ID:   {site['id']}")
            # List drives for each site
            try:
                drives = connector.list_drives(site["id"])
                for drive in drives.get("value", []):
                    print(f"    Drive: {drive['name']} (ID: {drive['id']})")
            except Exception:
                pass

    elif cmd == "list-files":
        if len(sys.argv) < 3:
            print("Usage: list-files <site-id> [drive-id]")
            sys.exit(1)
        site_id = sys.argv[2]
        if len(sys.argv) >= 4:
            drive_id = sys.argv[3]
        else:
            drives = connector.list_drives(site_id)
            if not drives.get("value"):
                print("No drives found for this site.")
                sys.exit(1)
            drive_id = drives["value"][0]["id"]
            print(f"Using default drive: {drives['value'][0]['name']} ({drive_id})")

        files = connector.list_root_files(drive_id)
        for item in files.get("value", []):
            item_type = "folder" if "folder" in item else "file"
            size = item.get("size", 0)
            print(f"  [{item_type}] {item['name']}  (ID: {item['id']}, Size: {size})")

    elif cmd == "permissions":
        if len(sys.argv) < 4:
            print("Usage: permissions <drive-id> <item-id>")
            sys.exit(1)
        perms = connector.get_file_permissions(sys.argv[2], sys.argv[3])
        for p in perms.get("value", []):
            roles = ", ".join(p.get("roles", []))
            granted = p.get("grantedToV2", p.get("grantedTo", {}))
            user_info = granted.get("user", {}).get("displayName", "N/A")
            email = granted.get("user", {}).get("email", "")
            print(f"  {user_info} ({email}) - Roles: {roles}")
            if p.get("link"):
                print(f"    Link: {p['link'].get('webUrl', '')}")

    elif cmd == "grant":
        if len(sys.argv) < 5:
            print("Usage: grant <drive-id> <item-id> <email> [read|write]")
            sys.exit(1)
        drive_id, item_id, email = sys.argv[2], sys.argv[3], sys.argv[4]
        role = sys.argv[5] if len(sys.argv) >= 6 else "read"
        result = connector.grant_permission(drive_id, item_id, email, role)
        print(f"[OK] Granted '{role}' access to {email}")
        pretty(result)

    elif cmd == "share":
        if len(sys.argv) < 4:
            print("Usage: share <drive-id> <item-id> [view|edit]")
            sys.exit(1)
        drive_id, item_id = sys.argv[2], sys.argv[3]
        link_type = sys.argv[4] if len(sys.argv) >= 5 else "view"
        result = connector.create_sharing_link(drive_id, item_id, link_type)
        link = result.get("link", {}).get("webUrl", "N/A")
        print(f"[OK] Sharing link ({link_type}): {link}")

    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = connector.search_files(query)
        for hit_container in results.get("value", []):
            for hit in hit_container.get("hitsContainers", []):
                for item in hit.get("hits", []):
                    resource = item.get("resource", {})
                    print(f"  {resource.get('name', 'N/A')} - {resource.get('webUrl', '')}")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
