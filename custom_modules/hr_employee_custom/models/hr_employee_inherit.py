from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    x_plannable_hours = fields.Integer(string="Horas planificables")


    @api.depends('x_plannable_hours')
    def check_x_plannable_hours(self):
        for rec in self:
            if rec.x_plannable_hours < 0 and rec.x_plannable_hours > 12:
                raise ValidationError(_("Las horas planificables no pueden ser menos de 0 o mas de 12 "))
        return True