import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class account_analitic_line_report(models.Model):
    
    _inherit = "account.analytic.line"

    def get_report_timesheet_custom(self):
        project_ids = []
        for record in self:
            if record.project_id.id not in project_ids:
                project_ids.append(record.project_id.id)

        project_task_ids = self.env['project.task'].search(
            [('project_id', 'in', project_ids), ('parent_id', '=', False)])
        planned_hours = sum(data.planned_hours for data in project_task_ids)

        toreturn = dict()
        toreturn['planned_hours'] = planned_hours
        return toreturn

    @api.model
    def create(self, vals):
        name = False
        if vals.get('name'):
            name = vals.get('name')
        elif len(self) == 1:
            name = self.name

        if name and len(name) < 4:
            raise ValidationError("La descripción debe tener al menos 4 caracteres")
        return super(account_analitic_line_report, self).create(vals)

    def write(self, vals):
        name = False
        if vals.get('name'):
            name = vals.get('name')
        elif len(self) == 1:
            name = self.name

        if name and len(name) < 4:
            raise ValidationError("La descripción debe tener al menos 4 caracteres")
        return super(account_analitic_line_report, self).write(vals)
