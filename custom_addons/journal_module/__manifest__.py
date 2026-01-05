# -*- coding: utf-8 -*-
{
    "name": "Journal Module",
    "version": "1.0",
    "category": "Productivity",
    "summary": "Specialist Journal for Client Records",
    "description": """
        Specialist Journal Module
        =========================
        This module allows specialists to:
        * Create journal entries for clients
        * Use templates for quick entry creation
        * View entry history directly in client cards
        * Manage and organize client interactions
    """,
    "author": "Oleksandr Turulko",
    "website": "https://github.com/turulko-oleksandr/odoo-journalist-module",
    "depends": ["base"],
    "data": [
        "security/journal_security.xml",
        "security/ir.model.access.csv",
        "views/journal_entry_views.xml",
        "views/entry_template_views.xml",
        "views/client_views.xml",
        "views/menu.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
