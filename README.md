# CNX26 Marketing Cloud Setup Tools

Automated tools for setting up Marketing Cloud Business Units and student accounts for CNX26 conference sessions.

## 🚀 Quick Start

### One-Line Setup (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/melanie-pulido/cnx26-setup/main/setup.sh | bash
```

This will:
- Clone the repository
- Install Python dependencies
- Show you exactly how to open it in AI Expert Suite

### Manual Setup

1. **Clone and setup:**
   ```bash
   git clone https://github.com/melanie-pulido/cnx26-setup.git
   cd cnx26-setup
   pip install requests
   ```

2. **Open in AI Expert Suite:**
   - Click the workspace selector (top-left in Suite)
   - Choose **"Open folder..."**
   - Select the `cnx26-setup` folder
   
3. **Use the slash commands:**
   - `/create-cnx26-bu` — Create a new Business Unit
   - `/deploy-parent-package` — Deploy CNX26 content (Journey, Data, Assets)
   - `/create-cnx26-students` — Batch-create student accounts
   - `/deploy-mc-package` — Deploy custom MC packages

The commands are powered by Claude and handle all the API complexity for you!

### Manual Python Usage

If you prefer to run the scripts directly:

```bash
# Install dependencies
pip install requests

# Test your credentials
python3 test_credentials.py YOUR_CLIENT_ID YOUR_CLIENT_SECRET YOUR_SUBDOMAIN YOUR_AUTH_MID

# Create Business Unit
python3 create_cnx26_bu.py AUTH_MID CLIENT_ID CLIENT_SECRET SUBDOMAIN PARENT_MID ADMIN_USERNAME

# Deploy parent package
python3 deploy_parent_package.py AUTH_MID CLIENT_ID CLIENT_SECRET SUBDOMAIN TARGET_BU_MID

# Create students
python3 create_cnx26_students.py AUTH_MID CLIENT_ID CLIENT_SECRET SUBDOMAIN TARGET_BU_MID
# Then paste CSV data (Name,Username) and press Ctrl+D
```

## 📋 Prerequisites

- **Marketing Cloud OAuth2 Package:**
  - Setup → Installed Packages → New
  - Server-to-Server integration
  - Permissions: Provisioning, Email, Automation, Users & Roles
  - Must be configured at Enterprise/Parent BU level

- **Marketing_Cloud_Student Role:**
  - Create in Marketing Cloud: Setup → Users → Roles
  - Required for `/create-cnx26-students`

- **Python 3.x** with `requests` library

## 📖 What's Included

- `create_cnx26_bu.py` — Creates "CNX26 MCE+ Session" BU
- `deploy_parent_package.py` — Deploys CNX26 Parent package to a BU
- `create_cnx26_students.py` — Batch-creates student users from CSV
- `test_credentials.py` — Validates OAuth credentials
- `CNX26-Parent.json` — Complete parent package (Journey, Data Extensions, Content)
- `.claude/commands/` — AI Expert Suite slash command definitions
- `example_students.csv` — Sample CSV format

## 🎯 Typical Workflow

1. Run `/create-cnx26-bu` to create the session BU
   - Saves the BU MID for next step
2. Run `/deploy-parent-package` with the BU MID
   - Deploys all CNX26 content (Journey, emails, data extensions)
   - Takes 5-10 minutes for large packages
3. Run `/create-cnx26-students` with the BU MID
   - Paste your student list (CSV format)
   - Creates all accounts in ~2-5 seconds per student

## 📝 CSV Format for Students

```csv
Name,Username
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
```

See `example_students.csv` for reference.

## 🔒 Security Note

Never commit real OAuth credentials. Use environment variables or secure vaults in production.

## 💡 Tips

- The scripts auto-handle SSL/proxy issues common in Salesforce environments
- BU propagation takes ~3 seconds (not minutes!)
- Detailed logs are saved to `~/.aisuite/notebook/[date]/`
- Marketing Cloud Administrator role requires manual assignment via UI

## 🐛 Troubleshooting

**"OAuth credentials invalid"**
- Verify the OAuth package is at Enterprise/Parent BU level
- Check permissions: Provisioning, Email, Automation, Users & Roles

**"User not found"**
- Ensure the admin username exists in Marketing Cloud
- Use exact username (email format)

**"Marketing_Cloud_Student role not found"**
- Create the role manually: Setup → Users → Roles

---

Built with ❤️ for CNX26 using AI Expert Suite
