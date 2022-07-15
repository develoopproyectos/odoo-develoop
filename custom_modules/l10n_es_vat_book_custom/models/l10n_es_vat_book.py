# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)

class dev_l10n_es_vat_book2_custom(models.Model):

    _inherit = 'l10n.es.vat.book'

    def _calculate_vat_book(self):
        """
            This function calculate all the taxes, from issued invoices,
            received invoices and rectification invoices
        """
        for rec in self:
            if not rec.company_id.partner_id.vat:
                raise UserError(_("This company doesn't have VAT"))
            rec._clear_old_data()
            # Searches for all possible usable lines to report
            moves = rec._get_account_move_lines()
            for book_type in ["issued", "received"]:
                map_lines = self.env["aeat.vat.book.map.line"].search(
                    [("book_type", "=", book_type)]
                )
                taxes = self.env["account.tax"]
                accounts = {}
                for map_line in map_lines:
                    line_taxes = map_line.get_taxes(rec)
                    taxes |= line_taxes
                    if map_line.tax_account_id:
                        account = rec.get_account_from_template(map_line.tax_account_id)
                        ##############################
                        if account.x_check_by_group == True:
                            account = self.env['account.account'].search([('group_id','=',account.group_id.id)])
                        ##############################
                        accounts.update({tax: account for tax in line_taxes})
                # Filter in all possible data using sets for improving performance
                if accounts:
                    lines = moves.filtered(
                        lambda line: line.tax_ids & taxes
                        or (
                            line.tax_line_id in taxes
                            and line.account_id in accounts.get(line.tax_line_id, line.account_id)
                        )
                    )
                else:
                    lines = moves.filtered(
                        lambda line: (line.tax_ids | line.tax_line_id) & taxes
                    )
                rec.create_vat_book_lines(lines, map_line.book_type, taxes)
            # Issued
            book_type = "issued"
            issued_tax_lines = rec.issued_line_ids.mapped("tax_line_ids")
            rectification_issued_tax_lines = rec.rectification_issued_line_ids.mapped(
                "tax_line_ids"
            )
            tax_summary_data_recs = rec._prepare_vat_book_tax_summary(
                issued_tax_lines + rectification_issued_tax_lines, book_type
            )
            rec._create_vat_book_tax_summary(tax_summary_data_recs)
            rec._create_vat_book_summary(rec.issued_tax_summary_ids, book_type)

            # Received
            book_type = "received"
            received_tax_lines = rec.received_line_ids.mapped("tax_line_ids")
            # flake8: noqa
            rectification_received_tax_lines = rec.rectification_received_line_ids.mapped(
                "tax_line_ids"
            )
            tax_summary_data_recs = rec._prepare_vat_book_tax_summary(
                received_tax_lines + rectification_received_tax_lines, book_type
            )
            rec._create_vat_book_tax_summary(tax_summary_data_recs)
            rec._create_vat_book_summary(rec.received_tax_summary_ids, book_type)

            # If we require to auto-renumber invoices received
            if rec.auto_renumber:
                rec_invs = self.env["l10n.es.vat.book.line"].search(
                    [("vat_book_id", "=", rec.id), ("line_type", "=", "received")],
                    order="invoice_date asc, ref asc",
                )
                i = 1
                for rec_inv in rec_invs:
                    rec_inv.entry_number = i
                    i += 1
                rec_invs = self.env["l10n.es.vat.book.line"].search(
                    [
                        ("vat_book_id", "=", rec.id),
                        ("line_type", "=", "rectification_received"),
                    ],
                    order="invoice_date asc, ref asc",
                )
                i = 1
                for rec_inv in rec_invs:
                    rec_inv.entry_number = i
                    i += 1
                # Write state and date in the report
            rec.write(
                {"state": "calculated", "calculation_date": fields.Datetime.now()}
            )