"""
Microsoft 365 Connector - SharePoint & Outlook Integration
For admin: emin.kolac@usul.academy

Uses Microsoft Graph API to access:
- SharePoint: file browsing, download, upload, permissions
- Outlook: email read/send
"""

import os
import json
import sys
import msal
import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

SCOPES_DELEGATED = [
    "https://graph.microsoft.com/Files.ReadWrite.All",
    "https://graph.microsoft.com/Sites.ReadWrite.All",
    "https://graph.microsoft.com/Mail.ReadWrite",
    "https://graph.microsoft.com/Mail.Send",
    "https://graph.microsoft.com/User.Read",
]

SCOPES_APP = ["https://graph.microsoft.com/.default"]


class MS365Connector:
    def __init__(self):
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        self.user_email = os.getenv("MS365_USER_EMAIL", "emin.kolac@usul.academy")
        self.sharepoint_site_url = os.getenv("SHAREPOINT_SITE_URL", "usulacademy.sharepoint.com")
        self.sharepoint_site_name = os.getenv("SHAREPOINT_SITE_NAME", "")
        self.access_token = None

        if not all([self.tenant_id, self.client_id, self.client_secret]):
            print("ERROR: Missing Azure AD credentials. Set AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET in .env")
            sys.exit(1)

    def authenticate_app(self):
        """Authenticate using client credentials (app-only, no user interaction).
        Forces a fresh token (no cache) to pick up any newly granted permissions.
        """
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        # Use token_cache=None-equivalent: create a fresh app each time, no persistent cache
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret,
            token_cache=msal.SerializableTokenCache(),  # empty cache = force fresh token
        )
        result = app.acquire_token_for_client(scopes=SCOPES_APP)
        if "access_token" in result:
            self.access_token = result["access_token"]
            print(f"[OK] Authenticated as app for tenant {self.tenant_id}")
            return True
        else:
            print(f"[FAIL] Auth error: {result.get('error_description', result)}")
            return False

    def authenticate_device_code(self):
        """Authenticate using device code flow (interactive, delegated permissions)."""
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.PublicClientApplication(self.client_id, authority=authority)
        flow = app.initiate_device_flow(scopes=SCOPES_DELEGATED)
        if "user_code" not in flow:
            print(f"[FAIL] Could not create device flow: {flow}")
            return False
        print(f"\n>>> To sign in, visit: {flow['verification_uri']}")
        print(f">>> Enter code: {flow['user_code']}\n")
        result = app.acquire_token_by_device_flow(flow)
        if "access_token" in result:
            self.access_token = result["access_token"]
            print(f"[OK] Authenticated as {self.user_email}")
            return True
        else:
            print(f"[FAIL] Auth error: {result.get('error_description', result)}")
            return False

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _get(self, url):
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def _post(self, url, data):
        resp = requests.post(url, headers=self._headers(), json=data)
        resp.raise_for_status()
        return resp.json()

    # ─── User Info ────────────────────────────────────────────────

    def get_user_info(self):
        """Get profile info for the connected user."""
        url = f"{GRAPH_BASE}/users/{self.user_email}"
        return self._get(url)

    # ─── SharePoint ──────────────────────────────────────────────

    def get_sharepoint_site(self):
        """Get the SharePoint site info."""
        if self.sharepoint_site_name:
            url = f"{GRAPH_BASE}/sites/{self.sharepoint_site_url}:/sites/{self.sharepoint_site_name}"
        else:
            url = f"{GRAPH_BASE}/sites/{self.sharepoint_site_url}"
        return self._get(url)

    def list_sharepoint_sites(self):
        """List all SharePoint sites the user/app has access to."""
        url = f"{GRAPH_BASE}/sites?search=*"
        return self._get(url)

    def list_drives(self, site_id):
        """List document libraries (drives) for a SharePoint site."""
        url = f"{GRAPH_BASE}/sites/{site_id}/drives"
        return self._get(url)

    def list_files(self, drive_id, folder_path="root"):
        """List files in a SharePoint document library folder."""
        url = f"{GRAPH_BASE}/drives/{drive_id}/{folder_path}/children"
        return self._get(url)

    def list_root_files(self, drive_id):
        """List files at the root of a drive."""
        return self.list_files(drive_id, "root")

    def get_file_content(self, drive_id, item_id):
        """Download a file's content by item ID."""
        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/content"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.content

    def upload_file(self, drive_id, folder_path, filename, content):
        """Upload a file to SharePoint."""
        url = f"{GRAPH_BASE}/drives/{drive_id}/root:/{folder_path}/{filename}:/content"
        resp = requests.put(url, headers=self._headers(), data=content)
        resp.raise_for_status()
        return resp.json()

    def get_file_permissions(self, drive_id, item_id):
        """Get permissions for a specific file/folder."""
        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/permissions"
        return self._get(url)

    def create_sharing_link(self, drive_id, item_id, link_type="view", scope="organization"):
        """Create a sharing link for a file. link_type: view|edit, scope: anonymous|organization."""
        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/createLink"
        data = {"type": link_type, "scope": scope}
        return self._post(url, data)

    def grant_permission(self, drive_id, item_id, email, role="read"):
        """Grant permission on a file/folder to a user by email."""
        url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/invite"
        data = {
            "recipients": [{"email": email}],
            "roles": [role],
            "requireSignIn": True,
            "sendInvitation": True,
            "message": "Shared via MS365 Connector",
        }
        return self._post(url, data)

    def search_files(self, query):
        """Search across all SharePoint files."""
        url = f"{GRAPH_BASE}/search/query"
        data = {
            "requests": [{
                "entityTypes": ["driveItem"],
                "query": {"queryString": query},
            }]
        }
        return self._post(url, data)

    # ─── Outlook ─────────────────────────────────────────────────

    def list_emails(self, top=10, folder="inbox"):
        """List recent emails from the user's mailbox."""
        url = f"{GRAPH_BASE}/users/{self.user_email}/mailFolders/{folder}/messages?$top={top}&$orderby=receivedDateTime desc"
        return self._get(url)

    def get_email(self, message_id):
        """Get a specific email by ID."""
        url = f"{GRAPH_BASE}/users/{self.user_email}/messages/{message_id}"
        return self._get(url)

    def send_email(self, to_email, subject, body_html):
        """Send an email from the user's mailbox."""
        url = f"{GRAPH_BASE}/users/{self.user_email}/sendMail"
        data = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": body_html},
                "toRecipients": [{"emailAddress": {"address": to_email}}],
            },
            "saveToSentItems": True,
        }
        resp = requests.post(url, headers=self._headers(), json=data)
        resp.raise_for_status()
        return {"status": "sent"}

    def list_mail_folders(self):
        """List mail folders for the user."""
        url = f"{GRAPH_BASE}/users/{self.user_email}/mailFolders"
        return self._get(url)

    # ─── Calendar (bonus) ────────────────────────────────────────

    def list_events(self, top=10):
        """List upcoming calendar events."""
        url = f"{GRAPH_BASE}/users/{self.user_email}/events?$top={top}&$orderby=start/dateTime"
        return self._get(url)


def main():
    """Quick connectivity test."""
    connector = MS365Connector()

    if not connector.authenticate_app():
        print("Falling back to device code flow...")
        if not connector.authenticate_device_code():
            sys.exit(1)

    print("\n=== User Info ===")
    try:
        user = connector.get_user_info()
        print(f"  Display Name: {user.get('displayName')}")
        print(f"  Email: {user.get('mail')}")
        print(f"  Job Title: {user.get('jobTitle')}")
    except Exception as e:
        print(f"  Could not fetch user info: {e}")

    print("\n=== SharePoint Sites ===")
    try:
        sites = connector.list_sharepoint_sites()
        for site in sites.get("value", []):
            print(f"  - {site['displayName']} ({site['webUrl']})")
            print(f"    ID: {site['id']}")
    except Exception as e:
        print(f"  Could not list sites: {e}")

    print("\n=== Outlook (Recent Emails) ===")
    try:
        emails = connector.list_emails(top=5)
        for msg in emails.get("value", []):
            print(f"  - [{msg['receivedDateTime'][:10]}] {msg['subject']}")
            print(f"    From: {msg['from']['emailAddress']['address']}")
    except Exception as e:
        print(f"  Could not list emails: {e}")

    print("\n[Done] Connection test complete.")


if __name__ == "__main__":
    main()
