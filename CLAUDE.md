# CNX26 Org Setup

Tools for setting up Marketing Cloud orgs for the CNX26 event.

## Available Commands

- `/create-cnx26-bu` — Create a CNX26 MCE+ Session Business Unit and assign an admin user
- `/create-cnx26-students` — Batch-create student user accounts in an existing BU
- `/deploy-mc-package` — Deploy a Marketing Cloud package

## Typical Workflow

1. Run `/create-cnx26-bu` to create the session BU
2. Note the BU MID from the output
3. Run `/create-cnx26-students` with the BU MID and your student list

## Prerequisites

- Python 3.x
- `requests` library: `pip install requests`
- OAuth2 Installed Package in Marketing Cloud (Server-to-Server)
- `Marketing_Cloud_Student` role created in MC (Setup → Users → Roles)
