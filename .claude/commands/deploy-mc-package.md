---
name: deploy-mc-package
description: Deploy or install packages in Marketing Cloud Business Units
---

# Deploy Marketing Cloud Package

This skill deploys/installs packages in Marketing Cloud Business Units using the SOAP API.

## Usage

**Quick Deploy (Recommended):**
```
/deploy-mc-package
Package Link: [paste AppExchange or package URL]
Target BU MID: 517099999
```
I'll extract the package details from the link and deploy with default settings.

**Full Control:**
Type `/deploy-mc-package` and I'll guide you through:
1. OAuth credentials
2. Target Business Unit(s)
3. Package details
4. Deployment execution

## Prerequisites

You need:
- **OAuth2 Installed Package** in Marketing Cloud with package deployment permissions
- **Target Business Unit MID(s)** where package should be deployed
- **Package details:**
  - Package ID (from AppExchange or custom package)
  - Package version (if applicable)
  - Configuration settings

## What I'll Do

1. **Collect credentials:**
   - Client ID
   - Client Secret
   - Subdomain
   - Parent MID
   - Target Business Unit MID(s)

2. **Collect package information:**
   - Package link (AppExchange URL or Marketing Cloud package URL)
   - OR Package ID/name (manual entry)
   - Version (defaults to latest if not specified)
   - Configuration (defaults to standard settings)

3. **Validate:**
   - Test OAuth authentication
   - Verify target BU(s) exist
   - Check package availability
   - Verify deployment permissions

4. **Deploy package:**
   - Install package to target BU(s)
   - Configure package settings
   - Verify installation status
   - Report results

5. **Report:**
   - Show success/failure for each BU
   - Package configuration details
   - Installation logs
   - Next steps

## Output

You'll get:
```
✅ PACKAGE DEPLOYMENT COMPLETE

Package Information:
- Package Name: [Package Name]
- Package ID: [Package ID]
- Version: [Version]

Target Business Units:
✅ CNX26 MCE+ Session (MID: 517099999) - Deployed
✅ CNX26 Student BU 1 (MID: 517099001) - Deployed
✅ CNX26 Student BU 2 (MID: 517099002) - Deployed

Summary:
- Total BUs: 3
- Successful: 3
- Failed: 0

Deployment Details:
- Installation Type: Full
- Configuration: Default settings applied
- Status: Active

Log: ~/.aisuite/notebook/[date]/package-deployment-[package-id].log
```

## Deployment Options

I support several deployment modes:

1. **Single BU deployment:**
   - Deploy to one specific Business Unit

2. **Bulk deployment:**
   - Deploy to multiple BUs at once
   - Provide list of MIDs

3. **Parent + Children:**
   - Deploy to parent BU and all child BUs
   - Automatic discovery of child BUs

4. **Configuration options:**
   - Default configuration (automatic)
   - Custom configuration (you provide settings)

## Example Usage

### Quick Deploy with Link

```
You: /deploy-mc-package

Me: I'll deploy a package to your Marketing Cloud Business Unit.

Provide your credentials and package details:

Client ID: [you paste]
Client Secret: [you paste]
Subdomain: [you paste]
Parent MID: [you paste]
Target BU MID: [you paste: 517099999]

Package Link or Package ID:
[you paste: https://appexchange.salesforce.com/appxListingDetail?listingId=xxxxx]

🔍 Validating credentials and extracting package details...
✅ Authenticated successfully
✅ Target BU verified: CNX26 MCE+ Session (517099999)
✅ Package identified: [Package Name] (latest version)

📦 Deploying with default settings...
✅ Package deployed successfully to MID 517099999

✅ Complete: Package is now active
```

### Bulk Deploy to Multiple BUs

```
You: /deploy-mc-package

Target Business Unit MID(s) - comma-separated:
[you paste: 517099999, 517099001, 517099002]

Package Link:
[you paste package URL]

📦 Deploying package to 3 Business Unit(s)...
✅ MID 517099999: Deployed successfully
✅ MID 517099001: Deployed successfully
✅ MID 517099002: Deployed successfully

✅ Complete: 3 deployed, 0 failed
```

## Common Use Cases

### 1. Quick Deploy from AppExchange Link (Recommended)
```
You: /deploy-mc-package
Package Link: https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000EcrGNUAZ
Target BU: 517099999
→ Installs latest version with default settings
```

### 2. Deploy to Multiple Student BUs
```
Package Link: [Your package URL]
Target BUs: 517099001, 517099002, 517099003, 517099004, 517099005
→ Bulk installs to all CNX26 student BUs at once
```

### 3. Manual Package ID Entry
```
Package ID: abc123def456
Target BU: 517099999
→ Use when you have the package ID but not the link
```

## API Operations

The skill uses these SOAP API operations:
- **Retrieve**: Check existing package installations
- **Create**: Install new package
- **Update**: Update existing package
- **Configure**: Set package parameters

## Package Permissions Required

Your OAuth package needs:
- **Installed Packages** → Read, Write, Execute
- **Packages** → Read, Write

Setup → Installed Packages → [Your Package] → Component Permissions

## Notes

- **Default settings:** All packages deploy with standard/default configuration automatically
- **Package links:** I support AppExchange URLs and direct Marketing Cloud package URLs
- **Bulk deploy:** Provide comma-separated BU MIDs to deploy to multiple BUs at once
- **Latest version:** Unless specified, I'll always deploy the latest available version
- **Deployment time:** Large packages can take several minutes to install
- **Prerequisites:** Some packages require specific features enabled in the target BU
- **Retries:** Failed deployments can be retried after addressing errors
- **Uninstallation:** Not supported via API (requires manual removal in UI)

## Troubleshooting

If deployment fails, I'll check:
- ✅ OAuth permissions include package deployment
- ✅ Target BU exists and is accessible
- ✅ Package is compatible with BU configuration
- ✅ No conflicting packages are installed
- ✅ Required features are enabled in the BU

## Related Skills

- `/create-cnx26-bu` - Create Business Units before package deployment
- `/create-cnx26-students` - Create users after package deployment
