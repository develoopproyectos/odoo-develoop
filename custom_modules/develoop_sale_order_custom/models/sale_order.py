
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


    def _get_total_invoiced_amount(self):
        """
        Obtiene el importe acumulado de las facturas
        contabilizadas relacionadas con el pedido.

        Las notas de crédito descuentan el importe facturado.
        Los importes se convierten a la moneda del pedido.
        """
        self.ensure_one()

        total_invoiced = 0.0

        invoices = self.invoice_ids.filtered(
            lambda move: move.state == 'posted'
            and move.move_type in (
                'out_invoice',
                'out_refund',
                'out_receipt',
            )
        )

        for invoice in invoices:
            amount = invoice.amount_total

            if invoice.currency_id != self.currency_id:
                amount = invoice.currency_id._convert(
                    amount,
                    self.currency_id,
                    self.company_id,
                    invoice.invoice_date or invoice.date,
                )

            if invoice.move_type == 'out_refund':
                total_invoiced -= amount
            else:
                total_invoiced += amount

        return total_invoiced


    @api.depends(
        'state',
        'order_line.invoice_status',
        'amount_total',
        'currency_id',
        'invoice_ids.state',
        'invoice_ids.move_type',
        'invoice_ids.amount_total',
        'invoice_ids.currency_id',
        'invoice_ids.invoice_date',
        'invoice_ids.date',
    )
    def _compute_invoice_status(self):
        """
        Conserva el cálculo estándar de Odoo y añade
        la validación por importe total facturado.
        """
        super()._compute_invoice_status()

        for order in self.filtered(
            lambda record: record.state == 'sale'
        ):
            invoices = order.invoice_ids.filtered(
                lambda move: move.state == 'posted'
                and move.move_type in (
                    'out_invoice',
                    'out_refund',
                    'out_receipt',
                )
            )

            if not invoices:
                continue

            invoiced_amount = order._get_total_invoiced_amount()

            if order.currency_id.compare_amounts(invoiced_amount, order.amount_total) >= 0:
                order.invoice_status = 'invoiced'
    
    @api.model
    def _cron_update_invoice_status(self):
        orders = self.search([
            ('state', '=', 'sale'),
            ('invoice_status', '!=', 'invoiced'),
        ])

        if orders:
            orders._compute_invoice_status()
            orders.flush_recordset(['invoice_status'])