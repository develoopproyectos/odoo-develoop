# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import api, fields, models, SUPERUSER_ID, _

_logger = logging.getLogger(__name__)

class InvoiceReportListCustom(models.Model):

    _inherit = 'account.invoice.report'

    x_amount_untaxed_signed = fields.Monetary(string="Impuesto no incluido", currency_field='company_currency_id', compute="get_datas")
    x_amount_tax_signed = fields.Monetary(string='Impuesto', currency_field='company_currency_id', compute="get_datas")
    x_amount_total_signed = fields.Monetary(string='Total', currency_field='company_currency_id', compute="get_datas")
    x_residual_signed = fields.Monetary(string='Importe adeudado', currency_field='company_currency_id', compute="get_datas")

    def get_datas(self):
        for invoice in self:
            invoice.x_amount_untaxed_signed = invoice.move_id.amount_untaxed_signed
            invoice.x_amount_tax_signed = invoice.move_id.amount_tax
            invoice.x_amount_total_signed = invoice.move_id.amount_total_signed
            invoice.x_residual_signed = invoice.move_id.amount_residual_signed


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        #data2 = super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        if self._context.get('from_action', False) and self._context.get('from_action') == 'custom':
            # if self._context.get('params', False) == False or \
            #     (self._context.get('params',False) and self._context.get('params').get('view_type',False) and self._context.get('params').get('view_type') == 'list'):
            data = self.env['account.invoice.report2'].sudo().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
            toreturn = []
            for record in data:
                new_data = {
                    'id': record.get('id', False),
                    'move_id': record.get('move_id', False),
                    'product_id': record.get('product_id',False),
                    'account_id': record.get('account_id',False),
                    'analytic_account_id': record.get('analytic_account_id',False),
                    'journal_id': record.get('journal_id',False),
                    'company_id': record.get('company_id',False),
                    'company_currency_id': record.get('company_currency_id',False),
                    'commercial_partner_id': record.get('commercial_partner_id',False),
                    'state': record.get('state',False),
                    'move_type': record.get('move_type',False),
                    'partner_id': record.get('partner_id',False),
                    'invoice_user_id': record.get('invoice_user_id',False),
                    'fiscal_position_id': record.get('fiscal_position_id',False),
                    'payment_state': record.get('payment_state',False),
                    'invoice_date': record.get('invoice_date',False),
                    'invoice_date_due': record.get('invoice_date_due',False),
                    'product_uom_id': record.get('product_uom_id',False),
                    'product_categ_id': record.get('product_categ_id',False),
                    'quantity': record.get('quantity',False),
                    'price_subtotal': record.get('price_subtotal',False),
                    'price_average': record.get('price_average',False),
                    'country_id': record.get('country_id',False),

                    'x_amount_untaxed_signed': record.get('x_amount_untaxed_signed',False),
                    'x_amount_tax_signed': record.get('x_amount_tax_signed',False),
                    'x_amount_total_signed': record.get('x_amount_total_signed',False),
                    'x_residual_signed': record.get('x_residual_signed',False),
                }
                toreturn.append(new_data)
            return toreturn
        else:        
            return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)