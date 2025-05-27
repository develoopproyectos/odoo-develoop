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
        gemini_key = "AIzaSyBxjxfph-Lb8gWdiMVIKSsmxyA_D9zDmkk"
        url = "https://odoo-ai-service-pre.develoop.net/api/chatbot/"
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwOTAvYXBpL2F1dGgvbG9naW4iLCJpYXQiOjE3NDgwMDUyODAsImV4cCI6MTc4NDAwNTI4MCwibmJmIjoxNzQ4MDA1MjgwLCJqdGkiOiI2cmttSldsVmI3bGJGN0N3Iiwic3ViIjoiMiIsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjcifQ.FYCf1Ecj7s-DaehnQECOi5t4hrzJxzlxHazDWU4jaaI"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "api_key": gemini_key,
            "chat_id": chat_id,
            "message": message
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()  # Lanza excepción si hay error HTTP            
            return response.json()
        except requests.exceptions.RequestException as e:            
            return None