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
            if self.planned_hours == 0 and not vals.get('project_id',False) and not vals.get('stage_id',False):
                raise ValidationError("El campo horas planeadas es obligatorio")

        result = super(Dev_ProjectTaskCustom, self).write(vals)
        return result
