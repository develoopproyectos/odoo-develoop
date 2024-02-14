from odoo.tools import pytz
from datetime import datetime, date, timedelta
import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class account_analitic_line_report(models.Model):
    _inherit = "account.analytic.line"

    x_compute_domain_for_task = fields.Many2many(comodel_name="project.task", compute="_compute_domain_for_task")

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

    @api.depends('date', 'project_id', 'user_id')
    def _compute_domain_for_task(self):
        for rec in self:
            if self.env.user.has_group('hr_timesheet_custom.x_force_task_in_planing_for_day'):
                task_ids = list()

                project_id = rec.project_id.id if rec.project_id.id else 0
                query = """
                    SELECT task_id as id
                    FROM planning_slot
                    WHERE task_id is not null and project_id = %s and user_id = %s and 
                        (CAST(start_datetime AS DATE) <= '%s' AND CAST(end_datetime AS DATE) >= '%s') or
                        (CAST(start_datetime AS DATE) = '%s' and CAST(end_datetime AS DATE) = '%s')
                    UNION 
                    SELECT id as id
                    FROM project_task
                    WHERE project_id='%s' and lower(name) like '%s'
                """ % (project_id, rec.user_id.id, rec.date, rec.date, rec.date, rec.date, project_id, '%no facturable%')

                self.env.cr.execute(query)
                data = self.env.cr.fetchall()

                for rec2 in data:
                    task_ids.append(rec2[0])

                rec.x_compute_domain_for_task = self.env['project.task'].search(
                    [('project_id', '=', rec.project_id.id), ('id', 'in', task_ids)])
            else:
                rec.x_compute_domain_for_task = self.env['project.task'].search(
                    [('project_id', '=', rec.project_id.id)])

    @api.model
    def create(self, vals):
        name = False
        if vals.get('name'):
            name = vals.get('name')
        elif len(self) == 1:
            name = self.name

        # if name and len(name) < 4:
        #     raise ValidationError("La descripción debe tener al menos 4 caracteres")
        return super(account_analitic_line_report, self).create(vals)

    def write(self, vals):
        name = False
        if vals.get('name'):
            name = vals.get('name')
        elif len(self) == 1:
            name = self.name

        # if name and len(name) < 4:
        #     raise ValidationError("La descripción debe tener al menos 4 caracteres")     
        # employee_time_zone = self.env.user.partner_id.tz
        # if self.env.user.has_group('hr_timesheet_custom.x_force_task_in_planing_for_day'):
        #     if employee_time_zone == 'America/La_Paz':
        #         if 'no facturable' not in self.project_id.name.lower():
        #             try:                    
        #                 # start_date, end_date = self.get_timezone(vals)               
        #                 project_id = vals.get('project_id', self.project_id.id)
        #                 task_id = self.task_id.id
        #                 employee_res = self.employee_id.resource_id.id            
        #                 query = """
        #                     SELECT task_id as id
        #                     FROM planning_slot
        #                     WHERE project_id = %s and task_id = %s and resource_id = %s and  '%s' >= DATE_TRUNC('day', start_datetime) and '%s' <= DATE_TRUNC('day', end_datetime)                
        #                     """ % (project_id, task_id, employee_res, self.date, self.date)
                    
        #                 self.env.cr.execute(query)
        #                 planning = self.env.cr.fetchall()
        #                 if not planning:
        #                     raise ValidationError("No puede ingresar horas si no se encuentra planificado para la fecha indicada")
        #                 res = super(account_analitic_line_report, self).write(vals)
        #                 self.get_hours_per_day(self.employee_id, self.date)
        #                 return res
        #             except Exception as e:
        #                 raise ValidationError(e)
        #         else:
        #             if self.unit_amount >0.5:
        #                 raise ValidationError("No puede ingresar mas de 30 min de Horas No Facturadas") 
        return super(account_analitic_line_report, self).write(vals)

    def get_timezone(self, vals):
        #tz_user = pytz.timezone(self.env.user.tz) or pytz.utc
        _date = vals.get('date', self.date)

        seconds = (fields.datetime.utcnow() - fields.datetime.now()).total_seconds()
        hour = int(seconds / (3600))
        start_date = fields.datetime(_date.year, _date.month, _date.day) + timedelta(hours=hour)
        end_date = start_date + timedelta(days=1)

        return start_date, end_date
    
    def get_hours_per_day(self, employee_id, date):
        is_correct_hours = False        
        tasks_day = self.env['account.analytic.line'].search([
            ('date', '=', date),
            ('employee_id', '=', employee_id.id)
            # Agrega más condiciones si es necesario
        ])
        message = "No puede ingresar más horas que las que tiene en asistencia"
        total_hours = 0        
        for task in tasks_day:
            total_hours += task.unit_amount
        
        attendances_day = self.env['hr.attendance'].search([
            ('check_in', 'like', f"{date}%"),
            ('employee_id', '=', employee_id.id)
            # Agrega más condiciones si es necesario
        ])
        total_attendance_hours = 0 
        
        for attendance in attendances_day:
            total_attendance_hours += round(attendance.worked_hours,2)
                
        
        if total_attendance_hours<8:
            
            aux_attendance_hours=0
           
            for attendance in attendances_day:
                if not attendance.check_out:
                    now = datetime.now(pytz.utc)
                    check_in = attendance.check_in.replace(tzinfo=pytz.utc)
                    
                    # now = datetime.strptime("25/10/2023 00:37:41","%d/%m/%Y %H:%M:%S")
                    # Calcular el tiempo restante
                    remaining_time = now - check_in
                    # Convertir el tiempo restante a formato de horas
                    remaining_hours = remaining_time.total_seconds()/3600
                    aux_attendance_hours = total_attendance_hours+remaining_hours
            if aux_attendance_hours >8:
                total_attendance_hours = aux_attendance_hours
                horas, minutos = divmod(total_attendance_hours * 60, 60)

                message = f"No puedes registrar mas horas que tu asistencia hasta ahora: {round(horas)} Horas y {round(minutos)} Minutos"
            else:
                total_attendance_hours = 8
                message = "Si no haz completado la asistencia en tu jornada, la cantidad maxima de horas para registrar son 8h"

                    
                    

        
        if total_hours<=total_attendance_hours:
            is_correct_hours = True

        if not is_correct_hours:
                        raise ValidationError(message)
        
        
