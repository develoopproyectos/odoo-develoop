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
            ('open', 'Abierto'),
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
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    row_number() over (order by a_m.id desc) as id,
                    a_m.currency_id as x_currency_id,
                    a_m.number as x_invoice_number,
                    a_m.type as x_type,
                    a_m.state as x_state,
                    a_m.date_invoice as x_invoice_date,
                    a_m.partner_id as x_invoice_partner_id,
                    r_p.vat as x_invoice_dni_nif,
                    a_m.fiscal_position_id as x_invoice_fiscal_position_id,
                    CASE WHEN a_m.type = 'out_refund' OR a_m.type = 'in_refund' THEN a_i_t.base*-1 ELSE a_i_t.base END as x_invoice_amount_untaxes,
                    a_i_t.name as x_tax_name,
                    a_t.amount as x_tax_percent,
                    CASE WHEN a_m.type = 'out_refund' OR a_m.type = 'in_refund' THEN a_i_t.amount*-1  ELSE a_i_t.amount END as x_tax_value,
                    a_m.amount_total_signed as x_invoice_amount_total

                FROM account_invoice a_m INNER JOIN account_invoice_tax a_i_t ON a_m.id = a_i_t.invoice_id
                            INNER JOIN res_partner r_p ON a_m.partner_id = r_p.id
                            INNER JOIN account_tax a_t ON a_i_t.tax_id = a_t.id
            )
        ''' % (
            self._table,
        ))

    