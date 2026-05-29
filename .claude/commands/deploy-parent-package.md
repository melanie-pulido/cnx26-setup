---
name: deploy-parent-package
description: Deploy CNX26 Parent package to Marketing Cloud Business Unit
---

# Deploy CNX26 Parent Package

This skill deploys the complete CNX26 parent package (Journey, Data Extensions, Content, Automations) to a Marketing Cloud Business Unit.

**Package Contents:**
- Journey Builder journeys
- Content Builder assets (emails, images)
- Data Extensions
- Event Definitions
- Categories and folder structure

## Usage

Type `/deploy-parent-package` and I'll guide you through:
1. Authentication MID (for OAuth context)
2. OAuth credentials (Client ID, Client Secret, Subdomain)
3. Target MID (which BU to deploy to)
4. Package deployment

## Prerequisites

You need:
- **OAuth2 Installed Package** in Marketing Cloud
  - Setup → Installed Packages → New
  - Server-to-Server integration
  - Permissions: Email, Automation, Data Extensions, Journey Builder
  - **Important:** Must be configured at Enterprise/Parent BU level
- **Target Business Unit** already created (use `/create-cnx26-bu` if needed)

## What I'll Do

1. **Collect deployment credentials:**
   - Authentication MID (usually parent/enterprise BU)
   - OAuth Client ID and Secret
   - Marketing Cloud subdomain
   - Target Business Unit MID

2. **Run deployment script** (`deploy_parent_package.py`)

3. **The script will:**
   - Authenticate with Marketing Cloud REST API
   - Load CNX26-Parent.json package
   - Deploy all assets to target BU
   - Report deployment status
   - Provide verification checklist

4. **Deployment includes:**
   - ✉️  Email templates and content blocks
   - 🗂️  Data Extensions with proper folder structure
   - 🚀 Journey Builder journeys
   - 📊 Event Definitions for journey triggers
   - 📁 Categories and organization

## Output

You'll get:
```
✅ DEPLOYMENT COMPLETE

Package: CNX26 v3
Target MID: 517099999
Status: Processing

⏱️  Note: Large packages may take 5-10 minutes to fully deploy
   Check Marketing Cloud UI for deployment status

📋 Next Steps:
   1. Log into Marketing Cloud
   2. Switch to the target Business Unit
   3. Verify all assets were deployed:
      - Journey Builder → Journeys
      - Email Studio → Content Builder
      - Data Extensions
      - Automation Studio
```

## Example Usage

```
You: /deploy-parent-package

Me: I'll deploy the CNX26 Parent package to your Marketing Cloud Business Unit.

Authentication MID (usually parent BU):
517035120

Client ID:
YOUR_CLIENT_ID

Client Secret:
YOUR_CLIENT_SECRET

Subdomain:
YOUR_SUBDOMAIN

Target BU MID (where to deploy the package):
517099999

🔐 Authenticating...
✅ Authenticated successfully

📦 Loading package: CNX26-Parent.json
✅ Package loaded: CNX26 v3

🚀 Deploying package to MID: 517099999
   This may take several minutes for large packages...

✅ PACKAGE DEPLOYMENT INITIATED

Package: CNX26
Target MID: 517099999
Status: Processing
Import ID: abc-123-def

⏱️  Note: Large packages may take 5-10 minutes to fully deploy
   Check Marketing Cloud UI for deployment status
```

## Important Notes

- **Deployment time:** Large packages can take 5-10 minutes to fully process
- **Timeout handling:** If the script times out, deployment may still succeed - check MC UI
- **Overwrites:** Package deployment may overwrite existing assets with the same name
- **Dependencies:** All package dependencies (Data Extensions, Categories) are included

## Verification Steps

After deployment completes:

1. **Log into Marketing Cloud** and switch to the target BU
2. **Check Journey Builder:**
   - Journey Builder → Browse Journeys
   - Look for CNX26 journeys
3. **Check Content Builder:**
   - Email Studio → Content Builder
   - Verify emails and content blocks
4. **Check Data Extensions:**
   - Email Studio → Data Extensions
   - Verify CNX26 data extensions exist
5. **Check Automation Studio:**
   - Automation Studio → Automations
   - Verify any automations were deployed

## Troubleshooting

**"Authentication failed"**
- Verify OAuth package is at Enterprise/Parent BU level
- Check permissions: Email, Automation, Data Extensions, Journey Builder

**"Deployment timeout"**
- This is normal for large packages
- Check Marketing Cloud UI - deployment likely succeeded
- Wait 5-10 minutes and verify assets

**"Missing assets after deployment"**
- Check Marketing Cloud activity logs
- Verify OAuth permissions are complete
- Some assets may require manual configuration (e.g., Journey activation)

## Technical Details

**How it works:**
1. Authenticates with Marketing Cloud REST API v2
2. Uses Legacy Package Import API (`/legacy/v1/beta/package/import`)
3. Uploads complete package JSON with all dependencies
4. Marketing Cloud processes deployment asynchronously
5. Returns import ID for tracking

**API Endpoint:**
```
POST https://{subdomain}.rest.marketingcloudapis.com/legacy/v1/beta/package/import
```

**Script:** `deploy_parent_package.py`
**Package:** `CNX26-Parent.json` (included in repo)
