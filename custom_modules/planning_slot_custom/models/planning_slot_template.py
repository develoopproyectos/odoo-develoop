
from odoo import api, fields, models


class CustomPlanningTemplate(models.Model):
    _inherit = 'planning.slot.template'

    task_id = fields.Many2one('project.task', string="Task",
                              company_dependent=True, domain="[('project_id', '=?', project_id)]")


    @api.onchange('task_id')
    def _onchange_task_id(self):
        if self.task_id:
            self.project_id = self.task_id.project_id

    @api.depends('task_id.project_id')
    def _compute_project_id(self):
        # Disclaimer : Dead code.
        # TODO : Remove me in master
        for slot in self:
            if slot.task_id:
                slot.project_id = slot.task_id.project_id                    