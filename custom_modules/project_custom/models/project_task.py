# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError
from datetime import date

task_type_validation = ['planificacion','planificación','en desarrollo','desarrollo']

class Dev_ProjectTaskCustom(models.Model):
    
    _inherit = "project.task"

    x_planning_slot = fields.One2many("planning.slot", compute="get_x_planning_slot", string="Planificaciones", help="Listado de planificaciones")
    x_planning_slot_str = fields.Char(string="Planificacion", compute="get_x_planning_slot")
    x_is_planning_delay = fields.Boolean("Tarea retrasada?", compute="get_x_is_planning_delay")

    def get_x_planning_slot(self):
        for rec in self:
            plannings = self.env['planning.slot'].search([('task_id','=',rec.id)])
            rec.x_planning_slot = plannings
            rec.x_planning_slot_str = ""
            for data in plannings:
                rec.x_planning_slot_str += "<span>{} - {} ({}) - {} </span><br/>".format(data.start_datetime.strftime("%m/%d/%Y"), data.employee_id.name, str(data.allocated_hours), data.end_datetime.strftime("%m/%d/%Y"))

    def get_x_is_planning_delay(self):
        for rec in self:
            rec.x_is_planning_delay = False
            if rec.date_deadline and rec.date_deadline >= date.today():
                rec.x_is_planning_delay = True

    def write(self, vals):
        if self.stage_id.name:
            stage_name = self.stage_id.name.lower()
            if vals.get('stage_id', False):
                stage_name = self.env['project.task.type'].browse(vals.get('stage_id')).name
            if stage_name in task_type_validation:
                if vals.get('planned_hours', self.planned_hours) == 0 and (\
                        vals.get('name', False) or 
                        vals.get('project_id', False) or 
                        vals.get('sprint', False) or 
                        vals.get('user_id', False) or
                        vals.get('sequence', False) or
                        vals.get('date_deadline', False) or
                        vals.get('tag_ids', False) or
                        vals.get('planned_hours', False) or
                        vals.get('description', False)
                        ):
                    raise ValidationError("El campo horas planeadas es obligatorio")

        result = super(Dev_ProjectTaskCustom, self).write(vals)
        return result
