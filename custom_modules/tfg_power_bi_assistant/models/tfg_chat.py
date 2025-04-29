from odoo import models, fields, _
from odoo.http import request
class TfgChat(models.Model):
    _name = 'tfg.chat'    
    _description = 'TFG Chat'

    name = fields.Char(string='Name', required=True)


    def open_custom_chat(self):
        tfg_partner  = self.env.ref('tfg_power_bi_assistant.tfg_user_partner').id

        channel = self.env['discuss.channel'].sudo().create({
            'name': _('Custom Channel'),
            'channel_type': 'chat',
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

    