{
    "name": "Journal Module",
    "version": "1.0",
    "category": "Productivity",
    "summary": "Manage specialist journal entries",
    "description": """
        Journal Management Module
        =========================
        This module allows specialists to:
        * Create journal entries for clients
        * Use templates for quick entry creation
        * View history of entries per client
    """,
    "author": "Oleksandr Turulko",
    "website": "https://github.com/turulko-oleksandr",
    "depends": ["base"],
    "data": [
        "security/journal_security.xml",
        "security/ir.model.access.csv",
        "views/journal_entry_views.xml",
        "views/menu.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
