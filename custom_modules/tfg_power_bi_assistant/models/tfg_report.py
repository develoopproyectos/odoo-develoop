from odoo import models, fields

class TfgReport(models.Model):
    _name = 'tfg.report'
    _description = 'TFG Report'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    business_report_attachment = fields.Binary(string='Business Report Attachment',filename="business_report_name")
    business_report_name = fields.Char(string='Business Report Name')
    active = fields.Boolean(string='Active', default=True)