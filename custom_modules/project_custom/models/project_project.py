# -*- coding: utf-8 -*-

from odoo import models, fields


class Dev_pc_ProjectProjectCustom(models.Model):
    _inherit = "project.project"

    x_theoretical_start_date = fields.Date("Theoretical start date")
    x_theoretical_end_date = fields.Date("Theoretical end date")
    x_estimated_end_date = fields.Date("Estimated end date")
    x_kanban_state = fields.Selection([
        ('normal', 'In progress'),
        ('done', 'Completed'),
        ('blocked', 'Blocked')], string='Estado',
        copy=False, default='normal', required=True)
    x_phase = fields.Selection([
        ('functional_analysis', 'Functional Analysis'),
        ('analysis', 'Analysis/Design'),
        ('development', 'Development'),
        ('maintenance', 'Maintenance'),
        ('maintenance_pack_hours', 'Maintenance Pack Hours'),
        ('maintenance_monthly_fee', 'Maintenance Monthly Fee'),
        ('canceled', 'Canceled'),
        ('finished', 'Finished'),
        ('stopped_by_customer', 'Stopped by customer'),
        ('rejected', 'Rejected'),
    ], index=True, string="Phase")
    x_technology = fields.One2many("project.technology", "project_id", string="Technology")

    def _get_sale_order_lines(self):
        super()._get_sale_order_lines()
        sale_orders = self._get_sale_orders()
        return self.env['sale.order.line'].search(
            [('order_id', 'in', sale_orders.ids), ('is_service', '=', True), ('is_downpayment', '=', False)],
            order='id asc')

    def _get_sold_items(self):
        sold_items = super()._get_sold_items()

        total_unit_amount = 0
        for line_id in self.analytic_account_id.line_ids:
            if line_id.user_id:
                total_unit_amount += line_id.unit_amount

        sold_items['effective_sold'] = self.total_timesheet_time

        return sold_items
