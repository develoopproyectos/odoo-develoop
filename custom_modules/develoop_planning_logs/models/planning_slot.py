
from odoo import api, fields, models
from odoo.tools import format_date, format_datetime
from markupsafe import Markup


class PlanningSlot(models.Model):
    _inherit = "planning.slot"

    def _format_dt(self, dt):
        if not dt:
            return ''

        dt_user = fields.Datetime.context_timestamp(self, dt)
        return dt_user.strftime('%d/%m/%Y')

    def _build_planning_body(self, action, resource, time, dt_old=None, dt_new=None):
        today = fields.Date.today().strftime('%d/%m/%Y')

        now_user = fields.Datetime.context_timestamp(
            self,
            fields.Datetime.now()
        )
        now = now_user.strftime('%H:%M')

        color_action = ''
        color_new = ''
        if action == "Creado":
            color_action = 'green'
            color_new = 'green'
        elif action == "Eliminado":
            color_action = 'red'
            color_new = 'red'

        fecha_anterior_html = ""
        if action == "Modificado" and dt_old:
            fecha_anterior_html = f"""
                <li style="text-decoration: line-through;">
                    <em><strong>Fecha inicio anterior:</strong> {self._format_dt(dt_old)}</em>
                </li>
            """
            
        fecha_nueva_html = ""
        if dt_new:
            fecha_nueva_html = f"""
                <li>
                    <em><strong style="color:{color_new}">Fecha inicio:</strong> 
                    <span style="color:{color_new}">{self._format_dt(dt_new)}</span></em>
                </li>
                <li>
                    <em><strong style="color:{color_new}">Horas Asignadas:</strong></em> 
                    <span style="color:{color_new}">{time} Hrs.</span>
                </li>
            """

        body = Markup(f"""
            <p><strong>Planificación:</strong></p>
            <ul>
                <li><strong>Día:</strong> {today} <strong>Hora:</strong> {now}</li>
                <li><strong>Recurso:</strong> {resource.name if resource else ''}</li>
                <li><strong style="color:{color_action}">Acción: {action}</strong></li>
                {fecha_anterior_html}
                {fecha_nueva_html}
            </ul>
        """)
        return body
    
    def _create_planning_message(self, task, body, subject):
        if not task:
            return

        self.env['mail.message'].create({
            'subject': subject,
            'body': body,
            'model': 'project.task',
            'res_id': task.id,
            'message_type': 'notification',
            'subtype_id': self.env.ref('mail.mt_note').id,
            'author_id': self.env.user.partner_id.id
        })
    
    def _create_planning_log(self, planning, action, old_dates=[]):
        self.env['planning.slot.log'].sudo().create({
            'partner_id': self.env.user.partner_id.id,
            'project_id': planning.project_id.id,
            'task_id': planning.task_id.id,
            'resource_id': planning.resource_id.id,
            'action': action,
            'old_start_date': old_dates[planning.id]['start_datetime'] if old_dates else False,
            'old_end_date': old_dates[planning.id]['end_datetime'] if old_dates else False,
            'new_start_date': planning.start_datetime,
            'new_end_date':planning.end_datetime,
        })

    
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)

        for record, vals in zip(res, vals_list):
            if not vals.get('start_datetime'):
                continue

            dt = fields.Datetime.from_string(vals['start_datetime'])

            resource = record.resource_id

            body = record._build_planning_body(
                action="Creado",
                resource=resource,
                time=vals['allocated_hours'],
                dt_new=dt
            )

            self._create_planning_log(record, 'created')

            record._create_planning_message(
                task=record.task_id,
                body=body,
                subject="Registro de Planificación"
            )
    
        return res

    def write(self, vals):
        old_dates = {
            rec.id: {
                'start_datetime': rec.start_datetime,
                'end_datetime': rec.end_datetime,
            }
            for rec in self
            if 'start_datetime' in vals
        }

        res = super().write(vals)

        if 'start_datetime' in vals:
            for rec in self:
                body = self._build_planning_body(
                    action="Modificado",
                    resource=rec.resource_id,
                    time= vals.get('allocated_hours') if vals.get('allocated_hours',False) else rec.allocated_hours,
                    dt_old=old_dates[rec.id]['start_datetime'],
                    dt_new=rec.start_datetime
                )

                self._create_planning_log(rec, 'modified', old_dates)

                self._create_planning_message(
                    task=rec.task_id,
                    body=body,
                    subject="Actualización de Planificación"
                )

        return res
    
    def unlink(self):
        records_data = []
        for record in self:
            records_data.append({
                'task': record.task_id,
                'resource': record.resource_id,
                'start_datetime': record.start_datetime,
                'end_datetime': record.end_datetime,
                'time': record.allocated_hours
            })
            self._create_planning_log(record, 'removed')

        for data in records_data:
            body = self._build_planning_body(
                action="Eliminado",
                resource=data['resource'],
                time=data['time'],
                dt_new=data['start_datetime'],
                dt_old=None
            )


            self._create_planning_message(
                task=data['task'],
                body=body,
                subject="Eliminación de Planificación"
            )
            
        return super().unlink()



