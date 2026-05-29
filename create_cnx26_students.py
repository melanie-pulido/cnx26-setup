#!/usr/bin/env python3
"""
Create CNX26 Marketing Cloud Student Users
Optimized batch user creation with proper role and BU assignment
"""

import sys
import csv
import json
import urllib3
from datetime import datetime
from io import StringIO

# Disable SSL warnings for corporate proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library required. Install with: pip3 install requests")
    sys.exit(1)


class MCStudentCreator:
    def __init__(self, client_id, client_secret, subdomain, auth_mid):
        self.client_id = client_id
        self.client_secret = client_secret
        self.subdomain = subdomain
        self.auth_mid = auth_mid
        self.auth_url = f"https://{subdomain}.auth.marketingcloudapis.com/v2/token"
        self.rest_base = f"https://{subdomain}.rest.marketingcloudapis.com"
        self.soap_base = f"https://{subdomain}.soap.marketingcloudapis.com"
        self.token = None
        self.enterprise_token = None
        self.student_role_id = None

        # Statistics
        self.stats = {
            "created": 0,
            "skipped": 0,
            "failed": 0,
            "total": 0
        }
        self.results = []

    def log(self, emoji, message):
        """Print formatted log message"""
        print(f"{emoji} {message}")

    def authenticate(self, account_id=None):
        """Get OAuth token with optional account_id scope"""
        level = "enterprise level" if not account_id else f"account_id: {account_id}"
        self.log("🔐", f"Authenticating ({level})...")

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        if account_id:
            payload["account_id"] = str(account_id)

        try:
            response = requests.post(
                self.auth_url,
                json=payload,
                verify=False,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            token = data["access_token"]

            if account_id:
                self.token = token
            else:
                self.enterprise_token = token

            self.log("✅", "Authenticated successfully")
            return token

        except requests.exceptions.RequestException as e:
            self.log("❌", f"Authentication failed: {e}")
            sys.exit(1)

    def validate_bu(self, bu_mid):
        """Verify target BU exists"""
        self.log("🔍", f"Validating Business Unit {bu_mid}...")

        token = self.enterprise_token if self.enterprise_token else self.token

        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
    <s:Header>
        <a:Action s:mustUnderstand="1">Retrieve</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <RetrieveRequest>
                <ObjectType>Account</ObjectType>
                <Properties>ID</Properties>
                <Properties>Name</Properties>
                <Filter xsi:type="SimpleFilterPart">
                    <Property>ID</Property>
                    <SimpleOperator>equals</SimpleOperator>
                    <Value>{bu_mid}</Value>
                </Filter>
            </RetrieveRequest>
        </RetrieveRequestMsg>
    </s:Body>
</s:Envelope>"""

        try:
            response = requests.post(
                f"{self.soap_base}/Service.asmx",
                data=soap_payload,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {token}"},
                verify=False,
                timeout=30
            )

            if "OverallStatus>OK" in response.text and "<Name>" in response.text:
                bu_name = response.text.split("<Name>")[1].split("</Name>")[0] if "<Name>" in response.text else "Unknown"
                self.log("✅", f"Business Unit found: {bu_name} (MID: {bu_mid})")
                return bu_name
            else:
                self.log("❌", f"Business Unit {bu_mid} not found")
                return None

        except Exception as e:
            self.log("❌", f"BU validation failed: {e}")
            return None

    def lookup_role(self, role_name="Marketing_Cloud_Student"):
        """Look up role ObjectID by name"""
        self.log("🔑", f"Looking up role: {role_name}...")

        token = self.enterprise_token if self.enterprise_token else self.token

        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
    <s:Header>
        <a:Action s:mustUnderstand="1">Retrieve</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <RetrieveRequest>
                <ObjectType>Role</ObjectType>
                <Properties>Name</Properties>
                <Properties>CustomerKey</Properties>
                <Properties>ObjectID</Properties>
            </RetrieveRequest>
        </RetrieveRequestMsg>
    </s:Body>
</s:Envelope>"""

        try:
            response = requests.post(
                f"{self.soap_base}/Service.asmx",
                data=soap_payload,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {token}"},
                verify=False,
                timeout=30
            )

            # Look for the role
            if role_name in response.text:
                text = response.text
                role_idx = text.find(f">{role_name}<")
                if role_idx > 0:
                    before = text[:role_idx]
                    if "<ObjectID>" in before:
                        role_id = before.split("<ObjectID>")[-1].split("</ObjectID>")[0]
                        self.student_role_id = role_id
                        self.log("✅", f"Role found: {role_name} (ID: {role_id})")
                        return role_id

            self.log("❌", f"Role '{role_name}' not found")
            self.log("ℹ️", "Create role in Setup → Users → Roles → Create")
            self.log("ℹ️", f"External Key must be: {role_name}")
            return None

        except Exception as e:
            self.log("❌", f"Role lookup failed: {e}")
            return None

    def check_user_exists(self, username):
        """Check if user already exists"""
        token = self.enterprise_token if self.enterprise_token else self.token

        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
    <s:Header>
        <a:Action s:mustUnderstand="1">Retrieve</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <RetrieveRequest>
                <ObjectType>AccountUser</ObjectType>
                <Properties>ID</Properties>
                <Properties>UserID</Properties>
                <Filter xsi:type="SimpleFilterPart">
                    <Property>UserID</Property>
                    <SimpleOperator>equals</SimpleOperator>
                    <Value>{username}</Value>
                </Filter>
            </RetrieveRequest>
        </RetrieveRequestMsg>
    </s:Body>
</s:Envelope>"""

        try:
            response = requests.post(
                f"{self.soap_base}/Service.asmx",
                data=soap_payload,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {token}"},
                verify=False,
                timeout=15
            )

            return "<ID>" in response.text

        except:
            return False

    def create_student(self, name, username, bu_mid, password="journey@1"):
        """Create a single student user account"""

        # Check if user exists first
        if self.check_user_exists(username):
            self.log("⚠️", f"{username} - Already exists (skipped)")
            self.stats["skipped"] += 1
            self.results.append({"username": username, "name": name, "status": "skipped"})
            return True

        token = self.enterprise_token if self.enterprise_token else self.token

        # Create user with role assignment
        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
    <s:Header>
        <a:Action s:mustUnderstand="1">Create</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <CreateRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <Objects xsi:type="AccountUser">
                <Name>{name}</Name>
                <UserID>{username}</UserID>
                <Password>{password}</Password>
                <Email>marketing@sfmctraining.com</Email>
                <MustChangePassword>false</MustChangePassword>
                <IsActive>true</IsActive>
                <DefaultBusinessUnit>{bu_mid}</DefaultBusinessUnit>
                <Client>
                    <ID>{bu_mid}</ID>
                </Client>
                <Roles>
                    <Role>
                        <ObjectID>{self.student_role_id}</ObjectID>
                    </Role>
                </Roles>
                <AssociatedBusinessUnits>
                    <ID>{bu_mid}</ID>
                </AssociatedBusinessUnits>
            </Objects>
        </CreateRequest>
    </s:Body>
</s:Envelope>"""

        try:
            response = requests.post(
                f"{self.soap_base}/Service.asmx",
                data=soap_payload,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {token}"},
                verify=False,
                timeout=30
            )

            if "OverallStatus>OK" in response.text or "StatusCode>OK" in response.text:
                self.log("✅", f"{username} - Created")
                self.stats["created"] += 1
                self.results.append({"username": username, "name": name, "status": "created"})
                return True
            elif "already exists" in response.text.lower():
                self.log("⚠️", f"{username} - Already exists (skipped)")
                self.stats["skipped"] += 1
                self.results.append({"username": username, "name": name, "status": "skipped"})
                return True
            else:
                error_msg = "Unknown error"
                if "StatusMessage>" in response.text:
                    error_msg = response.text.split("StatusMessage>")[1].split("</")[0]
                self.log("❌", f"{username} - Failed: {error_msg}")
                self.stats["failed"] += 1
                self.results.append({"username": username, "name": name, "status": f"failed: {error_msg}"})
                return False

        except Exception as e:
            self.log("❌", f"{username} - Error: {str(e)[:100]}")
            self.stats["failed"] += 1
            self.results.append({"username": username, "name": name, "status": f"error: {e}"})
            return False

    def parse_student_list(self, student_data):
        """Parse student list from CSV or text"""
        students = []

        # Try CSV format first
        try:
            reader = csv.DictReader(StringIO(student_data))
            for row in reader:
                # Handle various column name variations
                name = row.get('Name') or row.get('name') or row.get('FullName') or row.get('full_name')
                username = row.get('Username') or row.get('username') or row.get('Email') or row.get('email')

                if name and username:
                    students.append({"name": name.strip(), "username": username.strip()})
        except:
            # Fall back to line-by-line parsing
            for line in student_data.strip().split('\n'):
                line = line.strip()
                if not line or line.lower().startswith('name'):
                    continue

                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 2:
                    students.append({"name": parts[0], "username": parts[1]})

        return students


def main():
    """Main execution"""
    if len(sys.argv) != 6:
        print("Usage: python3 create_cnx26_students.py <auth_mid> <client_id> <client_secret> <subdomain> <target_bu_mid>")
        print("\nAfter providing credentials, you'll be prompted to paste the student list.")
        sys.exit(1)

    auth_mid = sys.argv[1]
    client_id = sys.argv[2]
    client_secret = sys.argv[3]
    subdomain = sys.argv[4]
    target_bu_mid = sys.argv[5]

    print("=" * 70)
    print("  CNX26 Student User Creator")
    print("=" * 70)
    print(f"  Authentication MID: {auth_mid}")
    print(f"  Target BU MID: {target_bu_mid}")
    print(f"  Subdomain: {subdomain}")
    print("=" * 70)
    print()

    creator = MCStudentCreator(client_id, client_secret, subdomain, auth_mid)

    # Step 1: Authenticate
    creator.authenticate(account_id=auth_mid)
    creator.authenticate(account_id=None)  # Enterprise token

    # Step 2: Validate target BU
    bu_name = creator.validate_bu(target_bu_mid)
    if not bu_name:
        creator.log("❌", "Cannot proceed without valid target BU")
        sys.exit(1)

    # Step 3: Look up role
    role_id = creator.lookup_role("Marketing_Cloud_Student")
    if not role_id:
        creator.log("❌", "Cannot proceed without Marketing_Cloud_Student role")
        sys.exit(1)

    print()
    print("=" * 70)
    print("Please provide student list (CSV format or Name, Username per line)")
    print("Example:")
    print("  Name,Username")
    print("  John Doe,john.doe@example.com")
    print("  Jane Smith,jane.smith@example.com")
    print()
    print("Paste your list and press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) when done:")
    print("=" * 70)
    print()

    # Read student list from stdin
    student_data = sys.stdin.read()

    students = creator.parse_student_list(student_data)

    if not students:
        creator.log("❌", "No valid students found in input")
        sys.exit(1)

    creator.stats["total"] = len(students)

    print()
    print("=" * 70)
    creator.log("👥", f"Creating {len(students)} student users...")
    print("=" * 70)
    print()

    # Create students
    for i, student in enumerate(students, 1):
        print(f"[{i}/{len(students)}] ", end="")
        creator.create_student(student["name"], student["username"], target_bu_mid)

    # Final summary
    print()
    print("=" * 70)
    print("  ✅ STUDENT USER CREATION COMPLETE")
    print("=" * 70)
    print()
    print("Target Business Unit:")
    print(f"  Name:  {bu_name}")
    print(f"  MID:   {target_bu_mid}")
    print()
    print("Role Configuration:")
    print(f"  Role:      Marketing_Cloud_Student")
    print(f"  ObjectID:  {role_id} ✅")
    print()
    print("Creation Results:")
    print(f"  Total:     {creator.stats['total']}")
    print(f"  Created:   {creator.stats['created']} ✅")
    print(f"  Skipped:   {creator.stats['skipped']} (already existed)")
    print(f"  Failed:    {creator.stats['failed']} {'❌' if creator.stats['failed'] > 0 else '✅'}")
    print()
    print("Access Configuration:")
    print(f"  Default BU:            {target_bu_mid} (CNX26 MCE+ Session) ✅")
    print(f"  BU Access:             Child BU ONLY ✅")
    print(f"  Password:              journey@1")
    print(f"  Must Change Password:  false ✅")
    print()

    # Save detailed log
    log_file = f"/tmp/student-creation-{target_bu_mid}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    with open(log_file, 'w') as f:
        f.write(f"CNX26 Student Creation Log\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Target BU MID: {target_bu_mid}\n")
        f.write(f"Target BU Name: {bu_name}\n")
        f.write(f"Auth MID: {auth_mid}\n")
        f.write(f"Role ID: {role_id}\n")
        f.write(f"\nStatistics:\n")
        f.write(f"  Total: {creator.stats['total']}\n")
        f.write(f"  Created: {creator.stats['created']}\n")
        f.write(f"  Skipped: {creator.stats['skipped']}\n")
        f.write(f"  Failed: {creator.stats['failed']}\n")
        f.write(f"\nDetailed Results:\n")
        for result in creator.results:
            f.write(f"  {result['status']:10s} | {result['username']:30s} | {result['name']}\n")

    print(f"📄 Log saved: {log_file}")
    print("=" * 70)

    if creator.stats['failed'] > 0:
        print("\n⚠️  Some users failed to create. Check the log for details.")
        sys.exit(1)
    else:
        print(f"\n✅ All users processed successfully!")
        print(f"Students can log in with password: journey@1")


if __name__ == "__main__":
    main()
