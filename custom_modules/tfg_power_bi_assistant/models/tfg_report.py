from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests
import logging
_logger = logging.getLogger(__name__)

class TfgReport(models.Model):
    _name = 'tfg.report'
    _description = 'TFG Report'

    name = fields.Char(string='Name', compute='generate_name', store=True)
    description = fields.Text(string='Description')
    business_report_attachment = fields.Binary(string='Business Report Attachment',filename="business_report_name")
    business_report_name = fields.Char(string='Business Report Name')
    report_state = fields.Char(string="Report State")
    report_date = fields.Date(string='Report Date', required=True, default=fields.Date.context_today)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('report_date')
    def generate_name(self):
        for record in self:
            if record.report_date:
                record.name = _(f"Report - {record.report_date.strftime('%Y-%m-%d')}")
            else:
                record.name = _("Report")

    def send_report(self):
        ai_middleware_url = self.env['ir.config_parameter'].sudo().get_param('tfg_power_bi_assistant.ai.middleware.url')
        subscription_code = self.env['ir.config_parameter'].sudo().get_param('tfg_power_bi_assistant.ai.service.sub.code')
        
        if not ai_middleware_url or not subscription_code:
            raise ValidationError(_("AI Middleware URL or Subscription Code is not configured."))

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "api_key": subscription_code,
            "odoo_report_id": self.id,
            "title": self.name
        }

        try:
            response = requests.post(ai_middleware_url + '/reports/', json=payload, headers=headers, timeout=10)                
            if response.status_code != 200:
                _logger.error("Error sending report: %s", response.text)
                return False
            _logger.info("Successfull sending report: %s", response.text)
            return response.json()
        except requests.exceptions.RequestException as e:      
            _logger.error("Error sending report: %s", response.text)      
            return False

    @api.model
    def create(self, vals):
        res = super(TfgReport, self).create(vals)
        res.send_report()
        return res