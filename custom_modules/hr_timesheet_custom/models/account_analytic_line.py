
from odoo import api, models
from odoo.exceptions import ValidationError

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

    @api.model
    def create(self, vals):
        name = vals.get('name') if vals.get('name') else ''
        if len(name) < 4:
            raise ValidationError("La descripción debe tener al menos 4 caracteres")
        return super(account_analitic_line_report, self).create(vals)

    def write(self, vals):
        name = vals.get('name') if vals.get('name') else self.name
        if len(name) < 4:
            raise ValidationError("La descripción debe tener al menos 4 caracteres")
        return super(account_analitic_line_report, self).write(vals)
