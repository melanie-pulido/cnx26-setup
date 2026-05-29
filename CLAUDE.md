# CNX26 Org Setup

Tools for setting up Marketing Cloud orgs for the CNX26 event.

## Getting Started

1. **Clone this repository:**
   ```bash
   git clone https://github.com/melanie-pulido/cnx26-setup.git
   cd cnx26-setup
   ```

2. **Open in AI Expert Suite:**
   - In Suite, click the workspace selector (top-left)
   - Choose "Open folder..."
   - Select the `cnx26-setup` folder you just cloned
   - The slash commands will be automatically available!

## Available Commands

- `/create-cnx26-bu` — Create a CNX26 MCE+ Session Business Unit and assign an admin user
- `/deploy-parent-package` — Deploy the CNX26 Parent package (Journey, Data Extensions, Content) to a BU
- `/create-cnx26-students` — Batch-create student user accounts in an existing BU
- `/deploy-mc-package` — Deploy a Marketing Cloud package (generic)

## Typical Workflow

1. Run `/create-cnx26-bu` to create the session BU
2. Note the BU MID from the output
3. Run `/deploy-parent-package` with the BU MID to deploy all CNX26 content
4. Run `/create-cnx26-students` with the BU MID and your student list

## Prerequisites

- Python 3.x
- `requests` library: `pip install requests`
- OAuth2 Installed Package in Marketing Cloud (Server-to-Server)
- `Marketing_Cloud_Student` role created in MC (Setup → Users → Roles)
