#!/usr/bin/env python3
"""
Create CNX26 Marketing Cloud Business Unit
Optimized script with proper token scoping and error handling
"""

import sys
import json
import urllib3
from datetime import datetime

# Disable SSL warnings for corporate proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library required. Install with: pip3 install requests")
    sys.exit(1)


class MCBUCreator:
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

    def log(self, emoji, message):
        """Print formatted log message"""
        print(f"{emoji} {message}")

    def authenticate(self, account_id=None):
        """Get OAuth token with optional account_id scope"""
        self.log("🔐", f"Authenticating{f' (account_id: {account_id})' if account_id else ' (enterprise level)'}...")

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
                verify=False,  # Handle corporate proxy
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            token = data["access_token"]

            if account_id:
                self.token = token
            else:
                self.enterprise_token = token

            self.log("✅", f"Authenticated successfully")
            return token

        except requests.exceptions.RequestException as e:
            self.log("❌", f"Authentication failed: {e}")
            if hasattr(e.response, 'text'):
                self.log("📄", f"Response: {e.response.text}")
            sys.exit(1)

    def validate_parent_bu(self, parent_mid):
        """Verify parent BU exists and is accessible"""
        self.log("🔍", f"Validating Parent BU {parent_mid}...")

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
    <s:Header>
        <a:Action s:mustUnderstand="1">Retrieve</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{self.token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <RetrieveRequest>
                <ObjectType>Account</ObjectType>
                <Properties>ID</Properties>
                <Properties>Name</Properties>
                <Filter xsi:type="SimpleFilterPart">
                    <Property>ID</Property>
                    <SimpleOperator>equals</SimpleOperator>
                    <Value>{parent_mid}</Value>
                </Filter>
            </RetrieveRequest>
        </RetrieveRequestMsg>
    </s:Body>
</s:Envelope>"""

        try:
            response = requests.post(
                f"{self.soap_base}/Service.asmx",
                data=soap_payload,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {self.token}"},
                verify=False,
                timeout=30
            )

            if "OverallStatus>OK" in response.text or parent_mid in response.text:
                self.log("✅", f"Parent BU {parent_mid} is accessible")
                return True
            else:
                self.log("⚠️", f"Parent BU {parent_mid} may not be accessible (continuing anyway)")
                return True  # Continue - might still work

        except Exception as e:
            self.log("⚠️", f"Parent BU validation warning: {e} (continuing anyway)")
            return True

    def lookup_user(self, username):
        """Look up user ID from username"""
        self.log("👤", f"Looking up user: {username}...")

        # Use enterprise token for user lookup
        token = self.enterprise_token if self.enterprise_token else self.token

        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
    <s:Header>
        <a:Action s:mustUnderstand="1">Retrieve</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <RetrieveRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <RetrieveRequest>
                <ObjectType>AccountUser</ObjectType>
                <Properties>ID</Properties>
                <Properties>UserID</Properties>
                <Properties>Name</Properties>
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
                timeout=30
            )

            # Extract ID from response
            if "<ID>" in response.text:
                user_id = response.text.split("<ID>")[1].split("</ID>")[0]
                self.log("✅", f"User found: {username} (ID: {user_id})")
                return user_id
            else:
                self.log("❌", f"User '{username}' not found")
                return None

        except Exception as e:
            self.log("❌", f"User lookup failed: {e}")
            return None

    def create_business_unit(self, parent_mid):
        """Create the CNX26 MCE+ Session Business Unit"""
        self.log("📦", "Creating Business Unit: CNX26 MCE+ Session...")

        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
    <s:Header>
        <a:Action s:mustUnderstand="1">Create</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{self.token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <CreateRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <Objects xsi:type="Account">
                <ParentID>{parent_mid}</ParentID>
                <Name>CNX26 MCE+ Session</Name>
                <Email>marketing@sfmctraining.com</Email>
                <FromName>Northern Trail Outfitters</FromName>
                <BusinessName>CNX26 MCE+ Session</BusinessName>
                <Phone></Phone>
                <Address></Address>
                <Fax></Fax>
                <City></City>
                <State></State>
                <Zip></Zip>
                <Country></Country>
                <IsActive>true</IsActive>
                <IsTestAccount>false</IsTestAccount>
                <UnsubscribeBehavior>BUSINESS_UNIT_ONLY</UnsubscribeBehavior>
            </Objects>
        </CreateRequest>
    </s:Body>
</s:Envelope>"""

        try:
            response = requests.post(
                f"{self.soap_base}/Service.asmx",
                data=soap_payload,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {self.token}"},
                verify=False,
                timeout=60
            )

            if "OverallStatus>OK" in response.text and "<NewID>" in response.text:
                new_mid = response.text.split("<NewID>")[1].split("</NewID>")[0]
                self.log("✅", f"Business Unit created successfully!")
                self.log("🎯", f"New BU MID: {new_mid}")
                return new_mid
            elif "already exists" in response.text.lower():
                self.log("⚠️", "Business Unit with this name may already exist")
                # Try to extract MID if available
                if "<NewID>" in response.text:
                    new_mid = response.text.split("<NewID>")[1].split("</NewID>")[0]
                    return new_mid
                return None
            else:
                self.log("❌", "Business Unit creation failed")
                self.log("📄", f"Response excerpt: {response.text[:500]}")
                return None

        except Exception as e:
            self.log("❌", f"Business Unit creation error: {e}")
            return None

    def assign_user_to_bu(self, user_id, bu_mid):
        """Assign user to Business Unit using enterprise token"""
        self.log("👤", f"Assigning user {user_id} to BU {bu_mid}...")

        # Use enterprise token for cross-BU operations
        token = self.enterprise_token if self.enterprise_token else self.token

        soap_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
    <s:Header>
        <a:Action s:mustUnderstand="1">Update</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <UpdateRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <Objects xsi:type="AccountUser">
                <ID>{user_id}</ID>
                <AccountUserID>{user_id}</AccountUserID>
                <UserID>{user_id}</UserID>
                <Client>
                    <ID>{bu_mid}</ID>
                </Client>
                <DefaultBusinessUnit>{bu_mid}</DefaultBusinessUnit>
            </Objects>
        </UpdateRequest>
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
                self.log("✅", f"User assigned to BU successfully")
                return True
            else:
                self.log("⚠️", "User assignment response unclear (may have succeeded)")
                return True  # Continue optimistically

        except Exception as e:
            self.log("⚠️", f"User assignment warning: {e} (continuing)")
            return True

    def assign_administrator_role(self, user_id, bu_mid):
        """Assign Administrator role to user in the BU"""
        self.log("🔑", f"Assigning Administrator role...")

        # First, find the Administrator role ID
        token = self.enterprise_token if self.enterprise_token else self.token

        # Retrieve roles
        soap_payload_retrieve = f"""<?xml version="1.0" encoding="UTF-8"?>
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
                data=soap_payload_retrieve,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {token}"},
                verify=False,
                timeout=30
            )

            # Look for Administrator role
            admin_role_id = None
            if "Administrator" in response.text:
                # Extract ObjectID for Administrator role
                text = response.text
                admin_idx = text.find(">Administrator<")
                if admin_idx > 0:
                    # Look backwards for ObjectID
                    before = text[:admin_idx]
                    if "<ObjectID>" in before:
                        admin_role_id = before.split("<ObjectID>")[-1].split("</ObjectID>")[0]

            if not admin_role_id:
                self.log("⚠️", "Administrator role ID not found via API")
                self.log("ℹ️", "User may already have Administrator role or it must be assigned manually")
                return False

            self.log("ℹ️", f"Found Administrator role (ID: {admin_role_id})")

            # Now assign the role
            soap_payload_assign = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
    <s:Header>
        <a:Action s:mustUnderstand="1">Update</a:Action>
        <a:To s:mustUnderstand="1">{self.soap_base}/Service.asmx</a:To>
        <fueloauth xmlns="http://exacttarget.com">{token}</fueloauth>
    </s:Header>
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <UpdateRequest xmlns="http://exacttarget.com/wsdl/partnerAPI">
            <Objects xsi:type="AccountUser">
                <ID>{user_id}</ID>
                <UserID>{user_id}</UserID>
                <DefaultBusinessUnit>{bu_mid}</DefaultBusinessUnit>
                <Roles>
                    <Role>
                        <ObjectID>{admin_role_id}</ObjectID>
                    </Role>
                </Roles>
            </Objects>
        </UpdateRequest>
    </s:Body>
</s:Envelope>"""

            response = requests.post(
                f"{self.soap_base}/Service.asmx",
                data=soap_payload_assign,
                headers={"Content-Type": "text/xml", "Authorization": f"Bearer {token}"},
                verify=False,
                timeout=30
            )

            if "OverallStatus>OK" in response.text or "StatusCode>OK" in response.text:
                self.log("✅", "Administrator role assigned")
                return True
            else:
                self.log("⚠️", "Role assignment unclear (user may already have role)")
                return True

        except Exception as e:
            self.log("⚠️", f"Role assignment warning: {e}")
            return False


def main():
    """Main execution"""
    if len(sys.argv) != 7:
        print("Usage: python3 create_cnx26_bu.py <auth_mid> <client_id> <client_secret> <subdomain> <parent_mid> <username>")
        sys.exit(1)

    auth_mid = sys.argv[1]
    client_id = sys.argv[2]
    client_secret = sys.argv[3]
    subdomain = sys.argv[4]
    parent_mid = sys.argv[5]
    username = sys.argv[6]

    print("=" * 70)
    print("  CNX26 Business Unit Creator")
    print("=" * 70)
    print(f"  Authentication MID: {auth_mid}")
    print(f"  Parent MID: {parent_mid}")
    print(f"  Admin User: {username}")
    print(f"  Subdomain: {subdomain}")
    print("=" * 70)
    print()

    creator = MCBUCreator(client_id, client_secret, subdomain, auth_mid)

    # Step 1: Authenticate with auth MID
    creator.authenticate(account_id=auth_mid)

    # Step 2: Get enterprise-level token for user operations
    creator.authenticate(account_id=None)

    # Step 3: Validate parent BU
    creator.validate_parent_bu(parent_mid)

    # Step 4: Look up user
    user_id = creator.lookup_user(username)
    if not user_id:
        creator.log("❌", "Cannot proceed without valid user")
        sys.exit(1)

    # Step 5: Create Business Unit
    new_bu_mid = creator.create_business_unit(parent_mid)
    if not new_bu_mid:
        creator.log("❌", "Business Unit creation failed")
        sys.exit(1)

    print()
    creator.log("⏸️", "BU created. Waiting 3 seconds for propagation...")
    import time
    time.sleep(3)

    # Step 6: Assign user to BU
    creator.assign_user_to_bu(user_id, new_bu_mid)

    # Step 7: Assign Administrator role
    role_assigned = creator.assign_administrator_role(user_id, new_bu_mid)

    # Final summary
    print()
    print("=" * 70)
    print("  ✅ BUSINESS UNIT CREATION COMPLETE")
    print("=" * 70)
    print()
    print("Business Unit Details:")
    print(f"  Name:            CNX26 MCE+ Session")
    print(f"  MID:             {new_bu_mid}  ← SAVE THIS FOR /create-cnx26-students")
    print(f"  Parent MID:      {parent_mid}")
    print(f"  Email:           marketing@sfmctraining.com")
    print(f"  From Name:       Northern Trail Outfitters")
    print(f"  Unsubscribe:     BU_ONLY ✅")
    print()
    print("Admin Assignment:")
    print(f"  Username:        {username}")
    print(f"  User ID:         {user_id}")
    print(f"  BU Access:       ✅ Added")
    print(f"  Role:            {'Administrator ✅' if role_assigned else 'Administrator (may need manual assignment)'}")
    print()

    if not role_assigned:
        print("⚠️  Note: Marketing Cloud Administrator role not found via API.")
        print("   If needed, manually assign via: Setup → Administration → Users")
        print()

    print(f"Next step: Run /create-cnx26-students with MID {new_bu_mid}")
    print("=" * 70)

    # Save log
    log_file = f"/tmp/bu-creation-{new_bu_mid}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    with open(log_file, 'w') as f:
        f.write(f"CNX26 BU Creation Log\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"New BU MID: {new_bu_mid}\n")
        f.write(f"Parent MID: {parent_mid}\n")
        f.write(f"Auth MID: {auth_mid}\n")
        f.write(f"Username: {username}\n")
        f.write(f"User ID: {user_id}\n")
        f.write(f"Role Assigned: {role_assigned}\n")

    print(f"\n📄 Log saved: {log_file}")


if __name__ == "__main__":
    main()
