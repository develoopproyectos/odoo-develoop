
from odoo import api, fields, models
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class dev_planning_slot_custom(models.Model):
    
    _inherit = "planning.slot"

    x_expiration_date = fields.Date(related='task_id.date_deadline')
    x_kanban_state = fields.Selection(related='task_id.kanban_state')
    x_stage_id =  fields.Many2one(related='task_id.stage_id')
    color = fields.Char(compute='_compute_color_from_taks_tags', default="0")


    def _compute_color_from_taks_tags(self):
        for planning in self:
            task_ids = planning.task_id
            has_color = False
            if task_ids:                         
                for task in task_ids:
                    tags_ids = task.tag_ids
                    if tags_ids:
                        for tag in reversed(tags_ids):
                            if tag.name == 'prioritario' or tag.name == 'Subir a Producción' or tag.name == 'incidencia':
                                print(tag.color)
                                planning.color = tag.color
                                has_color = True
                                break                 
            if not has_color:
                planning.color = '0'        
    @api.constrains('task_id', 'project_id')
    def _check_task_in_project(self):
        for forecast in self:
            if forecast.task_id and (forecast.task_id not in forecast.project_id.with_context(active_test=False).tasks):
                _logger.info("ERROR: ID %s, Tarea (%s) %s, Proyecto (%s) %s" % (forecast.id, forecast.task_id.id, forecast.task_id.name, forecast.project_id.id, forecast.project_id.name))
                # raise ValidationError(_("Your task is not in the selected project."))
    