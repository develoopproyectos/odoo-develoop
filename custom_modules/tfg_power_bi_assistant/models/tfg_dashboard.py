from odoo import models, fields

class TfgDashboard(models.Model):
    _name = 'tfg.dashboard'
    _description = 'TFG Dashboard'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)