# En un archivo Python dentro de tu módulo
from odoo import http
from odoo.http import request

class DiscussRedirectController(http.Controller):

    @http.route('/tfg/open_custom_chat', type='http', auth='user')
    def open_custom_chat(self, **kwargs):
        # Crear un canal nuevo si no existe
        channel = request.env['mail.channel'].sudo().create({
            'name': 'Canal Personalizado',
            'channel_type': 'chat',
            'channel_partner_ids': [(6, 0, [request.env.user.partner_id.id])]
        })

        # Redireccionar al canal en Discuss
        return request.redirect(f"/web#action=mail.action_discuss&active_id=mail.channel_{channel.id}")
