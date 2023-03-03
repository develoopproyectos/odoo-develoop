
import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class account_analitic_line_report(models.Model):
    
    _inherit = "account.analytic.line"

    x_compute_domain_for_task = fields.Many2many(comodel_name="project.task", compute="_compute_domain_for_task")

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

    @api.depends('date','project_id','user_id')
    def _compute_domain_for_task(self):
        for rec in self:
            if self.env.user.has_group('hr_timesheet_custom.x_force_task_in_planing_for_day'):
                task_ids = list()

                project_id = rec.project_id.id if rec.project_id.id else 0
                query = """
                    SELECT task_id
                    FROM planning_slot
                    WHERE task_id is not null and date_trunc('day',start_datetime) >= '%s' and date_trunc('day',end_datetime) <= '%s' and project_id = %s and user_id = %s
                """ % (rec.date, rec.date, project_id, rec.user_id.id)

                self.env.cr.execute(query)
                data = self.env.cr.fetchall()
                
                for rec2 in data: 
                    task_ids.append(rec2[0])
                
                rec.x_compute_domain_for_task = self.env['project.task'].search([('project_id','=',rec.project_id.id),('id','in',task_ids)])
            else:
                rec.x_compute_domain_for_task = self.env['project.task'].search([('project_id','=',rec.project_id.id)])

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
