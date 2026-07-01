from odoo import models, fields, _
from odoo.exceptions import UserError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sdd_has_usable_mandate = fields.Boolean(related='move_id.sdd_has_usable_mandate')

    payment_term_id = fields.Many2one(
        "account.payment.term",
        related="move_id.invoice_payment_term_id",
        string="Payment Terms",
    )

    def action_register_portfolio_payment(self):
        account_types = {
            line.account_id.account_type
            for line in self
            if line.account_id.account_type in ('asset_receivable', 'liability_payable')
        }

        if len(account_types) > 1:
            raise UserError(_("You cannot register a payment for documents that mix customer and vendor documents."))
            
        return self.action_register_payment()
