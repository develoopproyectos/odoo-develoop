
# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.osv import expression

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def _process_auto_invoice(self, invoice):
        """ Hook for extension, to support different invoice states """
        ###EVITAR QUE LAS NUEVAS FACTURAS CREADAS POR LA SUBSCRIPCION SE PUBLIQUEN O CONFIRMEN DE MANERA AUTOMATICA
        #invoice.action_post()
        print(invoice)
        return