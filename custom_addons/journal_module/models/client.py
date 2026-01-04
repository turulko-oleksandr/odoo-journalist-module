# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Client(models.Model):
    _inherit = "res.partner"

    journal_entry_ids = fields.One2many(
        "journal.entry",
        "client_id",
        string="Journal Entries",
        help="History of journal entries for this client",
    )

    journal_entry_count = fields.Integer(
        string="Journal Entries", compute="_compute_journal_entry_count"
    )

    @api.depends("journal_entry_ids")
    def _compute_journal_entry_count(self):
        for partner in self:
            partner.journal_entry_count = len(partner.journal_entry_ids)
