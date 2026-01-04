# -*- coding: utf-8 -*-
{
    "name": "Journal Module",
    "version": "1.0",
    "category": "Productivity",
    "summary": "Manage journals and entries",
    "description": """
        Journal Management Module
        =========================
        This module allows you to:
        * Create and manage journals
        * Add entries to journals
        * Track creation dates and authors
    """,
    "author": "Oleksandr Turulko",
    "website": "https://github.com/turulko-oleksandr",
    "depends": ["base"],
    "data": [
        "security/journal_security.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
