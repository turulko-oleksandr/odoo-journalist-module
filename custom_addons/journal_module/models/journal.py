# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Journal(models.Model):
    _name = "journal.journal"
    _description = "Journal"
    _order = "create_date desc"
    _rec_name = "name"

    name = fields.Char(
        string="Journal Name", required=True, index=True, help="Name of the journal"
    )

    description = fields.Text(string="Description", help="Description of the journal")

    user_id = fields.Many2one(
        "res.users",
        string="Created by",
        default=lambda self: self.env.user,
        readonly=True,
        required=True,
        help="User who created this journal",
    )

    create_date = fields.Datetime(
        string="Created on", readonly=True, help="Date when the journal was created"
    )

    entry_ids = fields.One2many(
        "journal.entry", "journal_id", string="Entries", help="Entries in this journal"
    )

    entry_count = fields.Integer(
        string="Number of Entries",
        compute="_compute_entry_count",
        store=True,
        help="Total number of entries in this journal",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, it will allow you to hide the journal without removing it",
    )

    color = fields.Integer(
        string="Color Index", default=0, help="Color index for the kanban view"
    )

    @api.depends("entry_ids")
    def _compute_entry_count(self):
        """Compute the number of entries for each journal"""
        for journal in self:
            journal.entry_count = len(journal.entry_ids)

    @api.constrains("name")
    def _check_name(self):
        """Validate that the journal name is not empty"""
        for journal in self:
            if journal.name and not journal.name.strip():
                raise ValidationError(
                    "Journal name cannot be empty or contain only spaces."
                )

    def action_view_entries(self):
        """Action to view entries of this journal"""
        self.ensure_one()
        return {
            "name": f"Entries: {self.name}",
            "type": "ir.actions.act_window",
            "res_model": "journal.entry",
            "view_mode": "tree,form",
            "domain": [("journal_id", "=", self.id)],
            "context": {"default_journal_id": self.id},
        }

    def name_get(self):
        """Display journal name with entry count"""
        result = []
        for journal in self:
            name = f"{journal.name} ({journal.entry_count})"
            result.append((journal.id, name))
        return result
