# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.osv import expression

class ProjectTemplate(models.Model):

    _inherit = 'mail.template'

    def send_mail(self, res_id, force_send=False, raise_exception=False, email_values=None, notif_layout=False):
        if self and self.model == 'sale.subscription':
            template = self.env.ref('sale_subscription.email_payment_reminder')
            if template.id == self.id:
                return
        return super(ProjectTemplate, self).send_mail(res_id, force_send=False, raise_exception=False, email_values=None, notif_layout=False)
        