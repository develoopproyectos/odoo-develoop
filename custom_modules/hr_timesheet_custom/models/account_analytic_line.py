
from odoo import api, fields, models

class account_analitic_line_report(models.Model):
    
    _inherit = "account.analytic.line"

    def get_report_timesheet_custom(self):
        project_ids = []
        for record in self:
            if record.project_id.id not in project_ids:
                project_ids.append(record.project_id.id)

        project_task_ids = self.env['project.task'].search([('project_id','in',project_ids),('parent_id','=',False)])
        planned_hours = sum(data.planned_hours for data in project_task_ids)

        toreturn = dict()
        toreturn['planned_hours'] = planned_hours
        return toreturn
