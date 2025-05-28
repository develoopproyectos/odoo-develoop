from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ai_service_api_key = fields.Char(string="AI Service API Key", config_parameter="tfg_power_bi_assistant.ai.service.api.key")

    ai_service_sub_code = fields.Char(string="AI Service Subscription Code", config_parameter="tfg_power_bi_assistant.ai.service.sub.code")
