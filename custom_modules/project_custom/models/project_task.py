# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError

class Dev_ProjectTaskCustom(models.Model):
    
    _inherit = "project.task"

    x_planning_slot = fields.One2many("planning.slot", compute="get_x_planning_slot", string="Planificaciones", help="Listado de planificaciones")
    x_planning_slot_str = fields.Char(string="Planificacion", compute="get_x_planning_slot")

    def get_x_planning_slot(self):
        for rec in self:
            plannings = self.env['planning.slot'].search([('task_id','=',rec.id)])
            rec.x_planning_slot = plannings
            rec.x_planning_slot_str = ""
            for data in plannings:
                rec.x_planning_slot_str += "<span>{} - {} ({}) - {} </span><br/>".format(data.start_datetime.strftime("%m/%d/%Y"), data.employee_id.name, str(data.allocated_hours), data.end_datetime.strftime("%m/%d/%Y"))

    def write(self, vals):
        #if vals.get('planned_hours',False):
        if "planned_hours" in vals:
            if vals.get('planned_hours') == 0:
                raise ValidationError("El campo horas planeadas es obligatorio")
        else:
            if self.planned_hours == 0 and (not "project_id" in vals and not "stage_id" in vals and not "sequence" in vals):
                raise ValidationError("El campo horas planeadas es obligatorio")

        result = super(Dev_ProjectTaskCustom, self).write(vals)
        return result
