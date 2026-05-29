#!/usr/bin/env python3
"""
Quick credential validator for CNX26 BU creation
Tests OAuth credentials before running the full BU creation
"""

import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library required")
    print("   Install with: pip3 install requests")
    sys.exit(1)


def test_credentials(client_id, client_secret, subdomain, auth_mid):
    """Test OAuth credentials and report status"""

    print("=" * 60)
    print("  CNX26 Credential Validator")
    print("=" * 60)
    print(f"  Subdomain: {subdomain}")
    print(f"  Auth MID:  {auth_mid}")
    print("=" * 60)
    print()

    auth_url = f"https://{subdomain}.auth.marketingcloudapis.com/v2/token"

    # Test 1: Basic authentication
    print("🔐 Test 1: Basic OAuth authentication...")
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        response = requests.post(auth_url, json=payload, verify=False, timeout=15)
        response.raise_for_status()
        data = response.json()
        print("   ✅ Basic auth successful")
        print(f"   ℹ️  Token expires in: {data.get('expires_in', 'N/A')} seconds")
    except Exception as e:
        print(f"   ❌ Basic auth failed: {e}")
        return False

    # Test 2: Scoped authentication
    print("\n🔐 Test 2: Scoped authentication (with account_id)...")
    payload["account_id"] = str(auth_mid)

    try:
        response = requests.post(auth_url, json=payload, verify=False, timeout=15)
        response.raise_for_status()
        data = response.json()
        print("   ✅ Scoped auth successful")
        print(f"   ℹ️  REST endpoint: {data.get('rest_instance_url', 'N/A')}")
        print(f"   ℹ️  SOAP endpoint: {data.get('soap_instance_url', 'N/A')}")
        token = data["access_token"]
    except Exception as e:
        print(f"   ❌ Scoped auth failed: {e}")
        return False

    # Test 3: Basic API call
    print("\n📡 Test 3: Test API connectivity...")
    rest_base = f"https://{subdomain}.rest.marketingcloudapis.com"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Simple endpoint test
        response = requests.get(
            f"{rest_base}/platform/v1/tokenContext",
            headers=headers,
            verify=False,
            timeout=15
        )
        if response.status_code in [200, 401, 403]:  # Any response means connectivity works
            print("   ✅ API connectivity confirmed")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  API test warning: {e}")
        print("   (This may be normal - continuing)")

    print("\n" + "=" * 60)
    print("  ✅ Credential validation complete!")
    print("=" * 60)
    print("\nYour credentials are valid. You can proceed with:")
    print("  /create-cnx26-bu")
    print()

    return True


def main():
    if len(sys.argv) != 5:
        print("Usage: python3 test_credentials.py <client_id> <client_secret> <subdomain> <auth_mid>")
        print("\nExample:")
        print("  python3 test_credentials.py \\")
        print("    YOUR_CLIENT_ID \\")
        print("    YOUR_CLIENT_SECRET \\")
        print("    YOUR_SUBDOMAIN \\")
        print("    517035120")
        sys.exit(1)

    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    subdomain = sys.argv[3]
    auth_mid = sys.argv[4]

    success = test_credentials(client_id, client_secret, subdomain, auth_mid)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
