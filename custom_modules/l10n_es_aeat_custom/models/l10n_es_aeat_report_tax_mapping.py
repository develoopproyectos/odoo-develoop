import logging
from odoo import models, _

_logger = logging.getLogger(__name__)

class Dev_l10n_es_aeat_report_tax_mapping_Custom(models.AbstractModel):

    _inherit = "l10n.es.aeat.report.tax.mapping"
    
    def _get_move_line_domain(self, date_start, date_end, map_line):
        self.ensure_one()
        taxes = self.get_taxes_from_map(map_line)
        move_line_domain = [
            ("company_id", "child_of", self.company_id.id),
            ("date", ">=", date_start),
            ("date", "<=", date_end),
            ("parent_state", "=", "posted"),
        ]
        if map_line.move_type == "regular":
            move_line_domain.append(
                ("move_id.financial_type", "in", ("receivable", "payable", "liquidity"))
            )
        elif map_line.move_type == "refund":
            move_line_domain.append(
                (
                    "move_id.financial_type",
                    "in",
                    ("receivable_refund", "payable_refund"),
                )
            )
        if map_line.field_type == "base":
            move_line_domain.append(("tax_ids", "in", taxes.ids))
        elif map_line.field_type == "amount":
            move_line_domain.append(("tax_line_id", "in", taxes.ids))
        else:  # map_line.field_type == 'both'
            move_line_domain += [
                "|",
                ("tax_line_id", "in", taxes.ids),
                ("tax_ids", "in", taxes.ids),
            ]
        if map_line.account_id:
            account = self.get_account_from_template(map_line.account_id)
            if len(account.ids) == 1:
                if account.x_check_by_group == True:
                    account = self.env['account.account'].search([('group_id','=',account.group_id.id)])
            move_line_domain.append(("account_id", "in", account.ids))
        if map_line.sum_type == "debit":
            move_line_domain.append(("debit", ">", 0))
        elif map_line.sum_type == "credit":
            move_line_domain.append(("credit", ">", 0))
        if map_line.exigible_type == "yes":
            move_line_domain.extend(
                (
                    "|",
                    ("move_id.tax_cash_basis_rec_id", "!=", False),
                    "|",
                    ("tax_line_id.tax_exigibility", "!=", "on_payment"),
                    ("tax_ids.tax_exigibility", "!=", "on_payment"),
                )
            )
        elif map_line.exigible_type == "no":
            move_line_domain.extend(
                (
                    ("move_id.tax_cash_basis_rec_id", "=", False),
                    ("tax_line_id.tax_exigibility", "=", "on_payment"),
                    ("tax_ids.tax_exigibility", "=", "on_payment"),
                )
            )
        move_line_domain += self._get_partner_domain()
        return move_line_domain
