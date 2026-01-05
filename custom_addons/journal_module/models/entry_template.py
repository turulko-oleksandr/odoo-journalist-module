# -*- coding: utf-8 -*-

from odoo import models, fields


class EntryTemplate(models.Model):
    _name = "journal.entry.template"
    _description = "Journal Entry Template"
    _order = "sequence, name"

    name = fields.Char(string="Template Name", required=True, index=True)

    content = fields.Html(string="Template Content", required=True)

    sequence = fields.Integer(string="Sequence", default=10)

    active = fields.Boolean(string="Active", default=True)
