
from odoo import api, fields, models

task_type_validation = ['validacionpm','validacionpm','validacion pm','validacion pm']

class dev_planning_slot_custom(models.Model):
    
    _inherit = "planning.slot"

    x_expiration_date = fields.Date(related='task_id.date_deadline')
    x_kanban_state = fields.Selection(related='task_id.kanban_state')
    x_is_validation = fields.Boolean(string="Esta en etapa validacion o superior", compute="get_x_is_validation")

    def get_x_is_validation(self):
        for rec in self:
            rec.x_is_validation = False
            if rec.project_id:
                types = rec.project_id.type_ids
                task_type = list(_types for _types in types or [] if _types.name.lower() in task_type_validation)
                if task_type:
                    if rec.task_id.stage_id.sequence < task_type[0].sequence:
                        rec.x_is_validation = True
        