from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _update_related_sale_orders_invoice_status(self):
        orders = self.invoice_line_ids.sale_line_ids.order_id

        if orders:
            orders._compute_invoice_status()

    def action_post(self):
        res = super().action_post()
        self._update_related_sale_orders_invoice_status()
        return res

    def button_draft(self):
        res = super().button_draft()
        self._update_related_sale_orders_invoice_status()
        return res

    def button_cancel(self):
        orders = self.invoice_line_ids.sale_line_ids.order_id

        res = super().button_cancel()

        orders._compute_invoice_status()

        return res