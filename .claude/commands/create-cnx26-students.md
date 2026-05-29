---
name: create-cnx26-students
description: Create student user accounts in CNX26 Marketing Cloud Business Unit
---

# Create CNX26 Student Users

This skill creates student user accounts in an existing CNX26 MCE+ Session Business Unit.

**Optimized Script:** Uses `create_cnx26_students.py` for fast, reliable batch user creation.

## Usage

Type `/create-cnx26-students` and I'll guide you through:
1. OAuth credentials (Client ID, Client Secret, Subdomain)
2. Authentication MID
3. Target Business Unit MID (from `/create-cnx26-bu`)
4. Student list (CSV or text format)
5. Batch user creation

## Prerequisites

You need:
- **Business Unit already created** (use `/create-cnx26-bu` first)
- **Business Unit MID** from the BU creation
- **OAuth2 Installed Package** in Marketing Cloud
- **Role created:** Marketing_Cloud_Student
  - Setup → Users → Roles → Create
  - External Key: `Marketing_Cloud_Student`
  - View-only permissions, no admin access
- **Student list** (names and usernames)

## What I'll Do

1. **Run optimized Python script** (`create_cnx26_students.py`) with your credentials

2. **The script will:**
   - Authenticate with both scoped and enterprise-level tokens (parallel)
   - Validate target BU exists
   - Look up Marketing_Cloud_Student role
   - Parse student list (CSV or text format)
   - Check for existing users (auto-skip duplicates)
   - Create users in batch with progress indicators
   - For each student:
     - Create user account
     - Assign role: Marketing_Cloud_Student
     - Set default BU to target BU
     - Assign ONLY child BU (blocks parent access automatically)
     - Set email: marketing@sfmctraining.com
     - Set password: journey@1
     - Set MustChangePassword: false
   - Generate summary report and detailed log

3. **Key optimizations:**
   - Enterprise token for cross-BU operations
   - Duplicate detection before creation (no wasted API calls)
   - Handles SSL/proxy issues automatically
   - Clear progress indicators ([1/45], [2/45], etc.)
   - Detailed error messages per student
   - Batch processing with statistics

## Output

You'll get:
```
✅ STUDENT USER CREATION COMPLETE

Target Business Unit:
- Name: CNX26 MCE+ Session
- MID: 517099999

Role Configuration:
- Role: Marketing_Cloud_Student
- ObjectID: d2be5e3f-4a43-f011-a5d5-5cba2c6ff268 ✅

Student Creation Results:
✅ john.doe@example.com - Created
✅ jane.smith@example.com - Created
✅ bob.johnson@example.com - Created
⚠️ alice.williams@example.com - Skipped (already exists)

Summary:
- Total: 4 students
- Created: 3
- Skipped: 1
- Failed: 0

Access Configuration:
- Default BU: 517099999 (CNX26 MCE+ Session) ✅
- Parent BU Access: BLOCKED ✅
- Password: journey@1
- Must Change Password: false ✅

Log: ~/.aisuite/notebook/[date]/student-creation-517099999.log
```

## Student List Format

I'll accept either:

**CSV Format:**
```csv
Name,Username
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
```

**Or just paste:**
```
John Doe, john.doe@example.com
Jane Smith, jane.smith@example.com
```

## Example Usage

```
You: /create-cnx26-students

Me: I'll create student users in the CNX26 Business Unit.

Client ID:
[you paste]

Client Secret:
[you paste]

Subdomain:
[you paste]

Authentication MID:
[you paste]

Target Business Unit MID (from /create-cnx26-bu):
[you paste: 517099999]

🔐 Authenticating (account_id: 517035120)...
✅ Authenticated successfully
🔐 Authenticating (enterprise level)...
✅ Authenticated successfully
🔍 Validating Business Unit 517099999...
✅ Business Unit found: CNX26 MCE+ Session (MID: 517099999)
🔑 Looking up role: Marketing_Cloud_Student...
✅ Role found: Marketing_Cloud_Student (ID: d2be5e3f-4a43-f011-a5d5-5cba2c6ff268)

Please provide student list (CSV format or Name, Username per line):
[you paste student list]

👥 Creating 45 student users...
[1/45] ✅ john.doe@example.com - Created
[2/45] ✅ jane.smith@example.com - Created
[3/45] ⚠️ bob.jones@example.com - Already exists (skipped)
[... progress for each ...]
[45/45] ✅ alice.williams@example.com - Created

✅ Complete: 44 created, 1 skipped, 0 failed
Students can log in with password: journey@1
```

## Notes

- You can run this multiple times to add more students
- Existing students are automatically skipped (checked before creation)
- Students get ONLY child BU access (parent blocked automatically)
- Default password: journey@1
- Students don't need to change password on first login
- Role "Marketing_Cloud_Student" must exist before running
- **Execution time:** ~2-5 seconds per student (45 students ≈ 2-4 minutes)
- **SSL/Proxy:** Script handles corporate proxy SSL issues automatically

## Known Limitations

- **Role requirement:** The Marketing_Cloud_Student role must be created manually first
  - Setup → Users → Roles → Create
  - External Key: `Marketing_Cloud_Student`
  - Set appropriate view-only permissions
- **Duplicate detection:** Based on username - names can differ
- **Batch size:** No hard limit, but recommend batches of 50-100 for best performance

## Troubleshooting

### Role Not Found
If "Marketing_Cloud_Student" role not found:
1. Go to Setup → Users → Roles
2. Create new role: "Marketing_Cloud_Student"
3. Set External Key to: Marketing_Cloud_Student
4. Configure permissions (view-only, no admin access)
5. Re-run the script

### User Creation Fails
Common causes:
- Username already exists (automatically skipped)
- Invalid email format in username
- Target BU not accessible
- Insufficient OAuth permissions

### Authentication Issues
- Ensure Authentication MID is correct (typically parent/enterprise BU)
- Verify OAuth has permissions: Provisioning, Email, Automation, Users & Roles
- Check that target BU MID is valid and accessible

## Implementation Instructions (For Claude)

When the user invokes `/create-cnx26-students`, follow these steps:

1. **Collect all 5 required parameters:**
   - Authentication MID
   - Client ID
   - Client Secret
   - Subdomain
   - Target BU MID

2. **Locate the script:**
   ```bash
   SCRIPT_PATH="/Users/mricheson/Library/CloudStorage/GoogleDrive-mricheson@salesforce.com/My Drive/Events/CNX26/ORG SETUP/CNX26_Claude/create_cnx26_students.py"
   ```

3. **Verify dependencies:**
   ```bash
   python3 -c "import requests" 2>&1 || pip3 install requests
   ```

4. **Execute the script:**
   ```bash
   python3 "$SCRIPT_PATH" <auth_mid> <client_id> <client_secret> <subdomain> <target_bu_mid>
   ```

5. **Provide student list when prompted:**
   - Script will pause and ask for student list
   - User pastes CSV or text format
   - User presses Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) to complete input

6. **Show the output** - the script provides:
   - Progress indicators for each student
   - Success/skip/fail status per student
   - Final statistics summary
   - Log file location

**Example invocation:**
```bash
python3 create_cnx26_students.py \
  517035120 \
  YOUR_CLIENT_ID \
  "YOUR_CLIENT_SECRET" \
  YOUR_SUBDOMAIN \
  517036123
```

Then when prompted, paste student list:
```
Name,Username
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
```

**Expected execution time:** 2-5 seconds per student (45 students ≈ 2-4 minutes)

**If the script fails:**
- Check Marketing_Cloud_Student role exists
- Verify Target BU MID is correct
- Confirm OAuth permissions include Users & Roles
- Check student list format (Name,Username)
