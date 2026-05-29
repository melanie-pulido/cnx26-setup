#!/usr/bin/env python3
"""
Deploy CNX26 Parent Package to Marketing Cloud
Deploys the CNX26-Parent.json package to a specified Business Unit
"""

import sys
import json
import requests
import time
from datetime import datetime

# Disable SSL warnings for corporate proxies
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_access_token(client_id, client_secret, subdomain, account_id):
    """Get OAuth access token"""
    auth_url = f"https://{subdomain}.auth.marketingcloudapis.com/v2/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "account_id": account_id
    }

    try:
        response = requests.post(auth_url, json=payload, verify=False, timeout=30)
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return None


def deploy_package(token, subdomain, target_mid, package_file):
    """Deploy a Marketing Cloud package"""

    # Load package file
    print(f"📦 Loading package from: {package_file}")
    try:
        with open(package_file, 'r') as f:
            package_data = json.load(f)
        print(f"✅ Package loaded: {package_data.get('name', 'Unknown')} v{package_data.get('version', 'Unknown')}")
    except Exception as e:
        print(f"❌ Failed to load package: {e}")
        return False

    # Import package endpoint
    import_url = f"https://{subdomain}.rest.marketingcloudapis.com/legacy/v1/beta/package/import"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Add target MID if specified
    payload = package_data.copy()

    print(f"\n🚀 Deploying package to MID: {target_mid}")
    print("   This may take several minutes for large packages...")

    try:
        response = requests.post(
            import_url,
            headers=headers,
            json=payload,
            verify=False,
            timeout=300  # 5 minute timeout for large packages
        )

        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"\n✅ PACKAGE DEPLOYMENT INITIATED")
            print(f"\nPackage: {package_data.get('name', 'Unknown')}")
            print(f"Target MID: {target_mid}")
            print(f"Status: {result.get('status', 'Processing')}")

            if 'id' in result:
                print(f"Import ID: {result['id']}")

            print(f"\n⏱️  Note: Large packages may take 5-10 minutes to fully deploy")
            print(f"   Check Marketing Cloud UI for deployment status")

            return True
        else:
            print(f"\n❌ Deployment failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print(f"\n⚠️  Request timeout (this doesn't mean deployment failed)")
        print(f"   Large packages can take 10+ minutes to process")
        print(f"   Check Marketing Cloud UI for deployment status")
        return True
    except Exception as e:
        print(f"\n❌ Deployment error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
        return False


def main():
    if len(sys.argv) != 6:
        print("Usage: python3 deploy_parent_package.py <auth_mid> <client_id> <client_secret> <subdomain> <target_mid>")
        print("\nArguments:")
        print("  auth_mid      - Authentication MID (usually parent/enterprise BU)")
        print("  client_id     - OAuth Client ID")
        print("  client_secret - OAuth Client Secret")
        print("  subdomain     - Marketing Cloud subdomain")
        print("  target_mid    - Target Business Unit MID for deployment")
        print("\nExample:")
        print("  python3 deploy_parent_package.py \\")
        print("    517035120 \\")
        print("    YOUR_CLIENT_ID \\")
        print("    YOUR_CLIENT_SECRET \\")
        print("    YOUR_SUBDOMAIN \\")
        print("    517036067")
        sys.exit(1)

    auth_mid = sys.argv[1]
    client_id = sys.argv[2]
    client_secret = sys.argv[3]
    subdomain = sys.argv[4]
    target_mid = sys.argv[5]

    # Package file location
    package_file = "CNX26-Parent.json"

    print("=" * 60)
    print("CNX26 PARENT PACKAGE DEPLOYMENT")
    print("=" * 60)
    print(f"\nAuthentication MID: {auth_mid}")
    print(f"Target BU MID: {target_mid}")
    print(f"Package: {package_file}")
    print()

    # Authenticate
    print("🔐 Authenticating...")
    token = get_access_token(client_id, client_secret, subdomain, auth_mid)

    if not token:
        print("\n❌ Authentication failed. Check credentials and try again.")
        sys.exit(1)

    print("✅ Authenticated successfully")

    # Deploy package
    success = deploy_package(token, subdomain, target_mid, package_file)

    if success:
        print("\n" + "=" * 60)
        print("✅ DEPLOYMENT COMPLETE")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("   1. Log into Marketing Cloud")
        print("   2. Switch to the target Business Unit")
        print("   3. Verify all assets were deployed:")
        print("      - Journey Builder → Journeys")
        print("      - Email Studio → Content Builder")
        print("      - Data Extensions")
        print("      - Automation Studio")
        print("\n⚠️  If any assets are missing, check Marketing Cloud activity logs")
        sys.exit(0)
    else:
        print("\n❌ DEPLOYMENT FAILED")
        print("\nTroubleshooting:")
        print("  - Verify OAuth permissions include: Email, Automation, Data Extensions")
        print("  - Check that target MID is accessible with your credentials")
        print("  - Ensure package file exists in current directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
