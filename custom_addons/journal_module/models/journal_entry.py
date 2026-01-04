# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class JournalEntry(models.Model):
    _name = "journal.entry"
    _description = "Journal Entry"
    _order = "create_date desc"
    _rec_name = "title"

    title = fields.Char(
        string="Title", required=True, index=True, help="Title of the entry"
    )

    content = fields.Html(
        string="Content", required=True, help="Content of the journal entry"
    )

    journal_id = fields.Many2one(
        "journal.journal",
        string="Journal",
        required=True,
        ondelete="cascade",
        index=True,
        help="Journal to which this entry belongs",
    )

    user_id = fields.Many2one(
        "res.users",
        string="Author",
        default=lambda self: self.env.user,
        readonly=True,
        required=True,
        help="User who created this entry",
    )

    create_date = fields.Datetime(
        string="Created on", readonly=True, help="Date when the entry was created"
    )

    write_date = fields.Datetime(
        string="Last Updated",
        readonly=True,
        help="Date when the entry was last updated",
    )

    tags = fields.Char(string="Tags", help="Comma-separated tags for this entry")

    attachment_ids = fields.Many2many(
        "ir.attachment",
        "journal_entry_attachment_rel",
        "entry_id",
        "attachment_id",
        string="Attachments",
        help="Files attached to this entry",
    )

    attachment_count = fields.Integer(
        string="Attachments",
        compute="_compute_attachment_count",
        help="Number of attachments",
    )

    state = fields.Selection(
        [("draft", "Draft"), ("published", "Published"), ("archived", "Archived")],
        string="Status",
        default="draft",
        required=True,
        help="Status of the entry",
    )

    color = fields.Integer(string="Color Index", default=0)

    @api.depends("attachment_ids")
    def _compute_attachment_count(self):
        """Compute the number of attachments"""
        for entry in self:
            entry.attachment_count = len(entry.attachment_ids)

    @api.constrains("title")
    def _check_title(self):
        """Validate that the title is not empty"""
        for entry in self:
            if entry.title and not entry.title.strip():
                raise ValidationError(
                    "Entry title cannot be empty or contain only spaces."
                )

    @api.constrains("content")
    def _check_content(self):
        """Validate that the content is not empty"""
        for entry in self:
            if entry.content and not entry.content.strip():
                raise ValidationError("Entry content cannot be empty.")

    def action_publish(self):
        """Publish the entry"""
        self.write({"state": "published"})

    def action_archive_entry(self):
        """Archive the entry"""
        self.write({"state": "archived"})

    def action_set_draft(self):
        """Set entry back to draft"""
        self.write({"state": "draft"})

    def action_view_attachments(self):
        """Action to view attachments"""
        self.ensure_one()
        return {
            "name": "Attachments",
            "type": "ir.actions.act_window",
            "res_model": "ir.attachment",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.attachment_ids.ids)],
            "context": {
                "default_res_model": "journal.entry",
                "default_res_id": self.id,
            },
        }
