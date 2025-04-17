from odoo import http
from odoo.http import request
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context
from odoo.addons.mail.controllers.thread import ThreadController as BaseThreadController

class ThreadController(BaseThreadController):
    @http.route("/mail/message/post", methods=["POST"], type="json", auth="public")
    @add_guest_to_context
    def mail_message_post(self, thread_model, thread_id, post_data, context=None):        
        response = super().mail_message_post(thread_model, thread_id, post_data, context)
        ia_bot_id = request.env.ref('tfg_power_bi_assistant.tfg_user').id
        if response['author'] != ia_bot_id:
            channel = request.env['discuss.channel'].sudo().browse(thread_id)
            if ia_bot_id in channel.channel_member_ids.ids:
                #TODO MANDAR MENSAJE AL BOT
                print(channel)
        return response