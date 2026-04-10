# -*- coding: utf-8 -*-

import logging
from odoo import tools
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import AccessError, UserError, ValidationError

_logger = logging.getLogger(__name__)

class custom_report_list_iva(models.Model):
    
    _name = "report.list.iva.custom"
    _description = "List of Iva"
    _auto = False
    #_order = 'x_account_id desc'

    x_currency_id = fields.Many2one('res.currency', string='Currency')
    x_invoice_number = fields.Char(string="Número factura")
    x_type = fields.Selection([
            ('out_invoice','Factura de cliente'),
            ('in_invoice','Factura de proveedor'),
            ('out_refund','Factura rectificativa de cliente'),
            ('in_refund','Factura rectificativa de proveedor'),
        ], string="Tipo")
    x_state = fields.Selection([
            ('draft','Borrador'),
            ('posted', 'Abierto'),
            ('in_payment', 'En proceso de pago'),
            ('paid', 'Pagado'),
            ('cancel', 'Cancelado'),
        ], string='Estado')
    x_invoice_date = fields.Date(string="Fecha factura")
    x_invoice_partner_id = fields.Many2one('res.partner', string="Razón social")
    x_invoice_dni_nif = fields.Char(string="DNI/NIF")
    x_invoice_fiscal_position_id = fields.Many2one('account.fiscal.position', string="Posición fiscal")
    x_invoice_amount_untaxes = fields.Monetary(string="Impuesto no incluido")
    #x_invoice_tax_ids = fields.Many2many('account.tax', 'account_move_line_account_tax_rel', 'account_move_line_id')
    x_tax_name = fields.Char(string="% Impuesto")
    #x_invoice_taxes_percent = fields.Char(string="% Impuesto")
    x_tax_value = fields.Monetary(string="Total Impuesto")
    x_invoice_amount_total = fields.Monetary(string="Total Factura")


    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f'''
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT 
                    row_number() OVER (ORDER BY m.id DESC) AS id,
                    m.currency_id AS x_currency_id,
                    m.name AS x_invoice_number,
                    m.move_type AS x_type,
                    m.state AS x_state,
                    m.invoice_date AS x_invoice_date,
                    m.partner_id AS x_invoice_partner_id,
                    rp.vat AS x_invoice_dni_nif,
                    m.fiscal_position_id AS x_invoice_fiscal_position_id,

                    CASE 
                        WHEN m.move_type IN ('out_refund','in_refund') 
                            THEN -aml.tax_base_amount
                        ELSE aml.tax_base_amount
                    END AS x_invoice_amount_untaxes,

                    at.name AS x_tax_name,
                    at.amount AS x_tax_percent,

                    CASE 
                        WHEN m.move_type IN ('out_refund','in_refund') 
                            THEN -aml.balance
                        ELSE aml.balance
                    END AS x_tax_value,

                    m.amount_total_signed AS x_invoice_amount_total

                FROM account_move_line aml
                JOIN account_move m ON aml.move_id = m.id
                JOIN account_tax at ON aml.tax_line_id = at.id
                JOIN res_partner rp ON m.partner_id = rp.id

                WHERE aml.tax_line_id IS NOT NULL
                AND m.move_type IN ('out_invoice','in_invoice','out_refund','in_refund')
                AND m.state = 'posted'
            )
        ''')