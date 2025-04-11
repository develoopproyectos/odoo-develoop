# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models


class HRLeave(models.Model):
    _inherit = "hr.leave"

    def action_approve(self):
        res = super(HRLeave, self).action_approve()
        if not res:
            return res
        for leave in self:
            if leave.holiday_status_id.time_type != 'other' and leave.state in ['validate', 'validate1']:
                try:
                    role_id = self.env.ref('hr_holidays_custom.x_vacation').id
                    planning_leave = self.env['planning.slot'].sudo().create({
                        'template_id': None,
                        'project_id': leave.holiday_status_id.timesheet_project_id.id,
                        'employee_id': leave.employee_id.id,
                        'resource_id': leave.employee_id.resource_id.id,
                        'role_id': role_id,
                        'start_datetime': leave.date_from,
                        'end_datetime': leave.date_to,
                    })
                    planning_leave.action_publish()
                except Exception as ex:
                    raise ValueError("error al intentar crear una planificacion para el empleado {} {}".format(leave.employee_id.name, ex))
        
