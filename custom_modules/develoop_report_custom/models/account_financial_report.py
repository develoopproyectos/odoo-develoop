# -*- coding: utf-8 -*-
import logging

from odoo import api, models, fields, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError
from datetime import datetime

_logger = logging.getLogger(__name__)

class account_custom_balance_in_group_0(models.Model):

    _inherit = 'account.financial.html.report.line'

    def _get_with_statement(self):
        self.ensure_one()
        financial_report = self._get_financial_report()
        if financial_report and financial_report.l10n_es_reports_modelo_number == '347' and self.l10n_es_mod347_threshold:
            if self.groupby != 'partner_id':
                raise UserError(_("Trying to use a groupby threshold for a line without grouping by partner_id isn't supported."))

            company = self.env['res.company'].browse(self.env.context['company_ids'][0])
            from_fiscalyear_dates = company.compute_fiscalyear_dates(datetime.strptime(self.env.context['date_from'], DEFAULT_SERVER_DATE_FORMAT))
            to_fiscalyear_dates = company.compute_fiscalyear_dates(datetime.strptime(self.env.context['date_to'], DEFAULT_SERVER_DATE_FORMAT))

            # ignore the threshold if from and to dates belong to different fiscal years
            if from_fiscalyear_dates == to_fiscalyear_dates:
                threshold_value = self._parse_threshold_parameter(company, from_fiscalyear_dates['date_to'])
                tables, where_clause, where_params = self.env['account.move.line']._query_get(domain=self._get_aml_domain())

                sql_with = f"""WITH account_move_line
                              AS (SELECT *
                                  FROM account_move_line
                                  WHERE partner_id IN (
                                      SELECT account_move_line.partner_id
                                      FROM {tables}
                                      WHERE {where_clause}
                                      GROUP BY account_move_line.partner_id
                                      HAVING ABS(SUM(debit - credit)) > %s
                                  )
                              )
                           """
                if self._context.get('l10n_es_reports_boe_conversion_date', False) and self._context.get('periods', False):
                    with_params = where_params + [0]
                else:
                    with_params = where_params + [threshold_value]

                return sql_with, with_params

        return '', []
