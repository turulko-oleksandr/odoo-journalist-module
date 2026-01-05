# Journal Module for Odoo

A custom Odoo module for maintaining structured journal entries by specialists about clients.

## Table of Contents

- [Description](#description)
- [Key Features](#key-features)
- [Technical Requirements](#technical-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Access Rights](#access-rights)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Test Task Implementation](#test-task-implementation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Author](#author)
- [License](#license)
- [Contribution](#contribution)
- [Support](#support)

## Description

**Journal Module** is a custom Odoo module designed for keeping structured records of specialists' work with clients. The module integrates directly into the client card (`res.partner`) and allows quick creation of entries using predefined templates.

### Core Concept

The module replaces the standard *Documents* block and provides specialists with a convenient tool for:

- Maintaining a history of client interactions
- Quickly creating entries using templates
- Viewing the full entry history directly in the client card

## Key Features

### Journal Entries
- Creation of dated entries per client
- HTML-formatted content
- Automatic assignment to the current user

### Template System
- Ready-to-use templates for typical entries
- Ability to combine multiple templates
- Editable content after template insertion

### Client Integration
- **"Journal Entries"** tab in the partner form
- Entry counter button in the `button_box`
- Sorting by date (newest first)

### Access Control
- Two access levels: Specialist and Administrator
- Row-level security for entries
- Restrictions on editing others' records

## Technical Requirements

- **Odoo version**: 14.0+ (tested on 14.0, 15.0, 16.0, 17.0)
- **Python**: 3.7+
- **PostgreSQL**: 10+
- **Dependencies**: `base` (standard Odoo module)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/turulko-oleksandr/odoo-journal-module.git
cd odoo-journal-module
```

### 2. Project Structure

Ensure the project structure looks like this:
```
odoo-journal-module/
├── custom_addons/
│   └── journal_module/
│       ├── models/
│       ├── security/
│       ├── views/
│       ├── __init__.py
│       └── __manifest__.py
├── odoo/                    # Core Odoo files
├── odoo_data/               # Database and filestore
├── odoo.conf                # Configuration file
└── README.md
```

### 3. Odoo Configuration

Edit `odoo.conf` according to your environment:
```ini
[options]
addons_path = /path/to/odoo-journal-module/custom_addons,/path/to/odoo/addons
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo_db
http_port = 8069
```

### 4. Run Odoo
```bash
# From the project root directory
python odoo/odoo-bin -c odoo.conf
```

### 5. Install the Module

1. Open Odoo in your browser: `http://localhost:8069`
2. Log in as administrator
3. Go to Apps → Update Apps List
4. Search for "Journal Module"
5. Click Install

## Configuration

### Database Settings

The module works with the following PostgreSQL configuration:
```ini
db_host = localhost
db_port = 5433
db_name = odoo_db
db_user = admin
db_password = admin
```

### Assign User Rights

1. Go to Settings → Users & Companies → Users
2. Select a user
3. In the Access Rights tab, assign one of the groups:
   - **Journal Specialist** — for specialists
   - **Journal Administrator** — for administrators

## Project Structure
```
custom_addons/journal_module/
│
├── models/
│   ├── __init__.py
│   ├── client.py
│   ├── journal_entry.py
│   └── entry_template.py
│
├── security/
│   ├── ir.model.access.csv
│   └── journal_security.xml
│
├── views/
│   ├── journal_entry_views.xml
│   ├── entry_template_views.xml
│   ├── client_views.xml
│   └── menu.xml
│
├── __init__.py
└── __manifest__.py
```

## Data Models

### `journal.entry`

Main model for storing specialists' entries.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `display_name` | Char | Auto-generated name (date + client) |
| `entry_date` | Date | Entry date (default: today) |
| `specialist_id` | Many2one(res.users) | Specialist (readonly, auto-filled) |
| `client_id` | Many2one(res.partner) | Client (required, cascade delete) |
| `content` | Html | Entry content |
| `template_ids` | Many2many | Applied templates |

**Notes:**
- Validation for empty content
- Automatic `display_name` generation
- Sorting: `entry_date desc, id desc`

### `journal.entry.template`

Templates for fast entry creation.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Template name |
| `content` | Html | HTML content |
| `sequence` | Integer | Sort order (drag-and-drop) |
| `active` | Boolean | Archive flag |

### `res.partner` (Extension)

**New Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `journal_entry_ids` | One2many | Client entries |
| `journal_entry_count` | Integer | Computed entry counter |

**UI Changes:**
- Counter button in `button_box`
- New "Journal Entries" tab

## Access Rights

### Journal Specialist

**Permissions:**
- Create entries
- Edit own entries
- View own entries
- Read all templates
- Cannot delete entries
- Cannot edit templates

**Row-level security:**
```python
[('specialist_id', '=', user.id)]
```

### Journal Administrator

**Permissions:**
- Full specialist rights
- View, edit, and delete all entries
- Create and manage templates

**Row-level security:**
```python
[(1, '=', 1)]
```

## Usage

### Create Entry from Client

**Method 1: Button**

1. Open Contacts
2. Select a client
3. Click "X Entries"
4. Create a new entry

**Method 2: Tab**

1. Open a client card
2. Go to "Journal Entries" tab
3. Click "Add a line"
4. Fill in the form and save

### Create Entry via Menu

1. Journal → Entries → All Entries
2. Click "Create"
3. Fill in required fields and save

### Working with Templates (Admin Only)

- Journal → Configuration → Entry Templates
- Create, reorder (drag-and-drop), archive templates

### Template Usage

Selected templates are automatically inserted into the content:
```html
<div><strong>Template Name</strong><br/>Template content</div>
```

## Technical Details

- Auto-filled date and specialist
- Computed fields (`display_name`, `journal_entry_count`)
- Onchange logic for template insertion
- Cascade delete for client entries

## Test Task Implementation

### Implemented Requirements

- Journal entries with date, specialist, text, and client
- Template model and multi-template insertion
- Access control (Specialist / Administrator)
- Clean module structure and documentation

**Bonus:**
- PDF report (not implemented)

**Development Time:** Approximately 6–7 hours

## Testing

Testing includes:
- Module installation
- Template creation
- Entry creation
- Access control validation
- Client integration checks

## Troubleshooting

### Module Not Visible

- Run Apps → Update Apps List

### Access Denied

- Ensure user belongs to "Journal Specialist" group

### Database Connection Issues

- Verify `odoo.conf` database settings

## Author

**Oleksandr Turulko**
- GitHub: https://github.com/turulko-oleksandr/odoo-journal-module

## License

LGPL-3

## Contribution

Issues and Pull Requests are welcome.

## Support

**Tested on:**
- Odoo 19.0