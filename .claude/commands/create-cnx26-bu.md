---
name: create-cnx26-bu
description: Create CNX26 Marketing Cloud Business Unit and assign admin user
---

# Create CNX26 Business Unit

This skill creates the "CNX26 MCE+ Session" Business Unit in Marketing Cloud and assigns an admin user.

**Optimized Script:** Uses `create_cnx26_bu.py` for fast, reliable execution with proper error handling.

## Usage

Type `/create-cnx26-bu` and I'll guide you through:
1. Authentication MID (for OAuth context)
2. OAuth credentials (Client ID, Client Secret, Subdomain)
3. Parent MID (which BU the child will be created under)
4. Parent Admin User
5. BU creation and admin assignment

## Prerequisites

You need:
- **OAuth2 Installed Package** in Marketing Cloud
  - Setup → Installed Packages → New
  - Server-to-Server integration
  - Permissions: Provisioning, Email, Automation, Users & Roles
  - **Important:** Must be configured at Enterprise/Parent BU level for proper token scope
- **Admin user** that already exists in Marketing Cloud
  - User will be assigned Administrator role
  - Marketing Cloud Administrator role may require manual assignment via UI

## What I'll Do

1. **Run optimized Python script** (`create_cnx26_bu.py`) with your credentials

2. **The script will:**
   - Authenticate with both scoped and enterprise-level tokens (parallel)
   - Validate Parent MID accessibility
   - Look up User ID from username
   - Create Business Unit: CNX26 MCE+ Session
     - Parent: The Parent MID you specified
     - Email: marketing@sfmctraining.com
     - From Name: Northern Trail Outfitters
     - Unsubscribe: BU_ONLY
   - Assign user to new BU
   - Assign Administrator role
   - Generate summary report and log file

3. **Key optimizations:**
   - Gets both tokens upfront (no retry loops)
   - Uses enterprise token for cross-BU operations
   - Handles SSL/proxy issues automatically
   - 3-second wait for BU propagation (not 12 minutes!)
   - Clear progress indicators
   - Detailed error messages

## Output

You'll get:
```
✅ BUSINESS UNIT CREATION COMPLETE

Business Unit Details:
- Name: CNX26 MCE+ Session
- MID: 517099999  ← SAVE THIS FOR /create-cnx26-students
- Email: marketing@sfmctraining.com
- Unsubscribe Setting: BU_ONLY ✅

Admin Assignment:
- Username: admin@example.com
- User ID: 123456789
- BU Access: ✅ Added
- Role: Administrator ✅

⚠️  Marketing Cloud Administrator: Not available via API - assign manually if needed

Log: ~/.aisuite/notebook/[date]/bu-creation-517099999.log

Next: Use /create-cnx26-students with MID 517099999
```

## Example Usage

```
You: /create-cnx26-bu

Me: I'll create the CNX26 MCE+ Session Business Unit.

Authentication MID:
517035120

Client ID:
YOUR_CLIENT_ID_HERE

Client Secret:
YOUR_CLIENT_SECRET_HERE

Subdomain:
YOUR_SUBDOMAIN_HERE

Parent MID (the BU under which to create the child):
517036067

Parent Admin User:
admin@example.com

🔍 Validating credentials...
✅ Authenticated successfully (context: MID 517035120)
✅ Parent MID (517036067) accessible
✅ User found: admin@example.com (ID: 123456789)

📦 Creating Business Unit...
✅ Created: CNX26 MCE+ Session (MID: 517099999)

👤 Assigning admin...
✅ admin@example.com (ID: 123456789) assigned to BU
✅ Administrator role assigned

⚠️  Note: Marketing Cloud Administrator role not found via API.
    If needed, manually assign via: Setup → Administration → Users

Done! Use MID 517099999 with /create-cnx26-students
```

## Notes

- Run this once per org
- Save the Business Unit MID for student creation
- You can create students later with `/create-cnx26-students`
- Admin must already exist in Marketing Cloud
- **Execution time:** ~30-60 seconds (optimized script with parallel token acquisition)
- **SSL/Proxy:** Script handles corporate proxy SSL issues automatically

## Known Limitations

- **Marketing Cloud Administrator role:** May not be available via API in some account types
  - The Administrator role provides full admin access
  - If MCA role is required, assign manually: Setup → Administration → Users → [User] → Roles
- **Token scope:** Script automatically handles enterprise-level token acquisition for user assignment

### Parent MID Configuration

There are **two different MIDs** to configure:

#### 1. Authentication MID
- **Purpose:** Provides the OAuth authentication context
- **Common choice:** The Enterprise/Parent BU (top-level BU)
- **Why:** OAuth Installed Packages are typically configured at the Enterprise level
- **Note:** Your Client ID/Secret must be associated with this BU

#### 2. Parent MID  
- **Purpose:** Determines where the child BU sits in the BU hierarchy
- **Result:** The child BU will be created **under** this parent
- **Inheritance:** The child inherits settings (address, timezone, etc.) from this parent
- **Common choices:**
  - Use the **Enterprise/Parent BU MID** to create a top-level child
  - Use another **child BU MID** to create a sub-child (nested structure)

**These can be the same or different!**
- **Same:** Authenticate with Enterprise BU and create child under Enterprise BU
- **Different:** Authenticate with Enterprise BU but create child under a specific child BU

**How to find BU MIDs:**
1. Log into Marketing Cloud
2. Go to Setup → Account → Business Units
3. Find the BU you need
4. Copy its MID (Member ID) - typically a 9-digit number

**How to find Username:**
1. Log into Marketing Cloud
2. Go to Setup → Administration → Users
3. Find the user you want to assign as admin
4. Copy their **Username** (not the API name) - typically an email address

## Troubleshooting

### SSL Certificate Errors
If you see SSL verification errors, the script will automatically retry with SSL verification disabled (common in corporate environments with proxy certificates).

### Token Scope Issues
If user assignment fails with "BU not found" errors:
- Ensure your OAuth Installed Package is configured at the Enterprise/Parent BU level
- The script automatically handles enterprise-level token acquisition

### Role Assignment
If "Marketing Cloud Administrator" role fails:
- This is expected in some account types
- The Administrator role provides equivalent access
- Manually assign MCA if required: Setup → Administration → Users → [User] → Roles tab

### Authentication MID vs Parent MID
- **Authentication MID:** Should be your Enterprise/Parent BU (typically where OAuth is configured)
- **Parent MID:** Can be the same as Authentication MID or a different child BU
- If they're different, ensure Authentication MID has permission to create BUs under Parent MID

## Implementation Instructions (For Claude)

When the user invokes `/create-cnx26-bu`, follow these steps:

1. **Collect all 6 required parameters** from the user:
   - Authentication MID
   - Client ID
   - Client Secret
   - Subdomain
   - Parent MID
   - Parent Admin User (username)

2. **Locate the script:**
   ```bash
   SCRIPT_PATH="/Users/mricheson/Library/CloudStorage/GoogleDrive-mricheson@salesforce.com/My Drive/Events/CNX26/ORG SETUP/create_cnx26_bu.py"
   ```

3. **Verify dependencies:**
   ```bash
   python3 -c "import requests" 2>&1 || pip3 install requests
   ```

4. **Execute the script:**
   ```bash
   python3 "$SCRIPT_PATH" <auth_mid> <client_id> <client_secret> <subdomain> <parent_mid> <username>
   ```

5. **Show the output** to the user - the script provides formatted output with:
   - Progress indicators with emojis
   - The new BU MID (critical for next steps)
   - Admin assignment status
   - Log file location

**Example invocation:**
```bash
python3 create_cnx26_bu.py \
  517035120 \
  YOUR_CLIENT_ID \
  "YOUR_CLIENT_SECRET" \
  YOUR_SUBDOMAIN \
  517036067 \
  MKT101_7079
```

**Expected execution time:** 30-60 seconds

**If the script fails:**
- Check error messages - they're descriptive
- Verify OAuth permissions include: Provisioning, Email, Automation, Users & Roles
- Ensure Authentication MID is correct (should be enterprise/parent BU)
- Confirm username exists in Marketing Cloud
