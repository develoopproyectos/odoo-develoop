from odoo import models, fields, _
from odoo.http import request
class TfgChat(models.Model):
    _name = 'tfg.chat'    
    _description = 'TFG Chat'

    name = fields.Char(string='Name', required=True)


    def open_custom_chat(self):
        ia_chats = self.clean_custom_chat()
        tfg_partner  = self.env.ref('tfg_power_bi_assistant.tfg_user_partner').id

        channel = self.env['discuss.channel'].sudo().create({
            'name': _('Custom Channel'),
            'channel_type': 'aichat',
            'channel_partner_ids': [(6, 0, tfg_partner)]
        })

        # Devolver acción que abre Discuss con ese canal activo
        return {
            'type': 'ir.actions.client',
            'tag': 'mail.action_discuss',
            'params': {
                'active_id': f"mail.channel_{channel.id}",
            },
        }
    
    def clean_custom_chat(self):
        ia_chats = self.env['discuss.channel'].with_context(lang='en_US').search([
            ('name', '=', 'Canal Personalizado'),
            ('channel_type', '=', 'chat')
        ])

        messages = self.env['mail.message'].search([
            ('model', '=', 'discuss.channel'),
            ('res_id', 'in', ia_chats.ids)
        ])

        message_channel_ids = set(message.res_id for message in messages)

        empty_channel_ids = [channel_id for channel_id in ia_chats.ids if channel_id not in message_channel_ids]

        empty_channels = ia_chats.browse(empty_channel_ids)
        
        if empty_channels:
            empty_channels.unlink()

        return True

class DiscussChannel(models.Model):
    """ Chat Session
        Reprensenting a conversation between users.
        It extends the base method for anonymous usage.
    """

    _inherit = 'discuss.channel'

    channel_type = fields.Selection(selection_add=[('aichat', 'AI Conversation')], ondelete={'aichat': 'cascade'})