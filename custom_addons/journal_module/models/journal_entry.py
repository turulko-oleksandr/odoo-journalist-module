# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class JournalEntry(models.Model):
    _name = 'journal.entry'
    _description = 'Journal Entry'
    _order = 'entry_date desc, id desc'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )
    
    entry_date = fields.Date(
        string='Entry Date',
        required=True,
        default=fields.Date.context_today,
        index=True
    )

    specialist_id = fields.Many2one(
        'res.users',
        string='Specialist',
        default=lambda self: self.env.user,
        required=True,
        readonly=True,
        index=True
    )

    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        ondelete='cascade',
        index=True
    )

    content = fields.Html(
        string='Entry Text',
        required=True
    )
    
    template_ids = fields.Many2many(
        'journal.entry.template',
        'journal_entry_template_rel',
        'entry_id',
        'template_id',
        string='Insert Templates',
        help='Select templates to insert into entry text'
    )

    @api.depends('entry_date', 'client_id')
    def _compute_display_name(self):
        for entry in self:
            date_str = entry.entry_date.strftime('%Y-%m-%d') if entry.entry_date else ''
            client_name = entry.client_id.name if entry.client_id else ''
            entry.display_name = f"{date_str} - {client_name}"

    @api.constrains('content')
    def _check_content(self):
        for entry in self:
            if not entry.content or not entry.content.strip():
                raise ValidationError('Entry content cannot be empty.')
    
    @api.onchange('template_ids')
    def _onchange_template_ids(self):
        """Auto-insert selected templates into content"""
        if self.template_ids:
            template_content = '<br/><br/>'.join([
                f'<div><strong>{t.name}</strong><br/>{t.content}</div>' 
                for t in self.template_ids
            ])
            
            if self.content:
                self.content = self.content + '<br/><br/>' + template_content
            else:
                self.content = template_content