
# -*- coding: utf-8 -*-

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    monthly_billing = fields.Monetary(string="Facturación Mes", currency_field='currency_id', tracking=True) 

    billing_advance = fields.Monetary(string="Facturación a Futuro", currency_field='currency_id', tracking=True)

    @api.constrains('monthly_billing', 'billing_advance')
    def _check_facturacion_split(self):
        for order in self:
            pending = order.amount_to_invoice or 0.0

            mes = order.monthly_billing or 0.0
            futuro = order.billing_advance or 0.0

            if mes > pending or futuro > pending:
                raise ValidationError(_("Ninguno de los campos puede ser mayor que el total pendiente de facturar."))

            if (mes + futuro) > pending:
                raise ValidationError(_("La suma de Facturación Mes y Facturación a Futuro no puede superar el total pendiente de facturar."))