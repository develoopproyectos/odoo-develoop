from odoo import http
from odoo.http import request
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context
from odoo.addons.mail.controllers.thread import ThreadController as BaseThreadController
import re
import requests

class ThreadController(BaseThreadController):
    @http.route("/mail/message/post", methods=["POST"], type="json", auth="public")
    @add_guest_to_context
    def mail_message_post(self, thread_model, thread_id, post_data, context=None):        
        response = super().mail_message_post(thread_model, thread_id, post_data, context)
        ia_bot_id = request.env.ref('tfg_power_bi_assistant.tfg_user').partner_id.id
        msg = re.sub(r'<[^>]*>', '', str(response['body']))               
        if response['author'] != ia_bot_id:
            channel = request.env['discuss.channel'].sudo().browse(thread_id)
            if ia_bot_id in channel.channel_member_ids.partner_id.ids: 
                #MANDA MENSAJE A IA
                self.send_message(thread_id, msg)
        return response

    def send_message(self, chat_id, message):
        ai_middleware_url = request.env['ir.config_parameter'].sudo().get_param('tfg_power_bi_assistant.ai.middleware.url')
        subscription_code = request.env['ir.config_parameter'].sudo().get_param('tfg_power_bi_assistant.ai.service.sub.code')
        gemini_key = request.env['ir.config_parameter'].sudo().get_param('tfg_power_bi_assistant.ai.service.api.key')

        if not gemini_key:
            return None

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "api_key": subscription_code,
            "chat_id": chat_id,
            "message": message
        }

        try:
            response = requests.post(ai_middleware_url + '/chatbot', json=payload, headers=headers, timeout=10)
            #response.raise_for_status()  # Lanza excepción si hay error HTTP            
            return response.json()
        except requests.exceptions.RequestException as e:            
            return None