from odoo import models, fields, api, _

class TfgReport(models.Model):
    _name = 'tfg.report'
    _description = 'TFG Report'

    name = fields.Char(string='Name', compute='generate_name', store=True)
    description = fields.Text(string='Description',required=True)
    business_report_attachment = fields.Binary(string='Business Report Attachment',filename="business_report_name")
    business_report_name = fields.Char(string='Business Report Name')
    active = fields.Boolean(string='Active', default=True)
    report_date = fields.Date(string='Report Date', required=True)

    @api.depends('report_date')
    def generate_name(self):
        for record in self:
            if record.report_date:
                record.name = _(f"Report - {record.report_date.strftime('%Y-%m-%d')}")
            else:
                record.name = _("Report")