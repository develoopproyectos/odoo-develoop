from odoo import http, _
from odoo.http import request
import requests

class ServicesValidation(http.Controller):
    @http.route("/validation/ai_service", methods=["POST"], type="json", auth="public")    
    def validate_ai_service_api_key(self, api_key):

        if not api_key:
            return {"status": "error", "message": _("API key is required.")}
        
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        ai_middleware_url = request.env['ir.config_parameter'].sudo().get_param('tfg_power_bi_assistant.ai.middleware.url')

        payload = {
            "api_key": api_key,
            "odoo_url": base_url
        }

        try:
            response = requests.post(ai_middleware_url + '/verify/ai-api-key', json=payload)            
            return response.json()
        except requests.exceptions.RequestException as e:            
            return None

    @http.route("/validation/subscription_code", methods=["POST"], type="json", auth="public")    
    def validate_ai_service_subscription_code(self, api_key):

        if not api_key:
            return {"status": "error", "message": _("Subscription code is required.")}
        ai_middleware_url = request.env['ir.config_parameter'].sudo().get_param('tfg_power_bi_assistant.ai.middleware.url')

        payload = {
            "api_key": api_key
        }

        try:
            response = requests.post(ai_middleware_url + '/verify/subscription-api-key', json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:            
            return None