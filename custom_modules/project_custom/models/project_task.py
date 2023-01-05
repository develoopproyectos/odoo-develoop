# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError

class Dev_ProjectTaskCustom(models.Model):
    
    _inherit = "project.task"

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
