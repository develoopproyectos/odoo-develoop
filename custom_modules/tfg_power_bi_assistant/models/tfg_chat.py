from odoo import models, fields

class TfgChat(models.Model):
    _name = 'tfg.chat'
    _description = 'TFG Chat'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)