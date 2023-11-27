from odoo import models, fields

class ProjectTaskCustom(models.Model):    
    _inherit = 'project.task'

    qa_parent_id = fields.Many2one('project.task', string='Tarea QA padre', index=True)
    qa_child_ids = fields.One2many('project.task', 'qa_parent_id', string="QA-subtasks")    
    

    