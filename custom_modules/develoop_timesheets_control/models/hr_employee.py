
from datetime import timedelta

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def _cron_check_weekly_timesheets(self):
        today = fields.Date.context_today(self)

        # Ejecutar únicamente martes (1) y viernes (4).
        if today.weekday() not in (1, 4):
            return

        # Semana anterior: lunes a viernes.
        monday = today - timedelta(days=today.weekday() + 7)
        friday = monday + timedelta(days=4)

        # daily_hours = 8.0

        # Departamentos admitidos.
        # Solo se incluyen empleados activos de estos departamentos.
        department_names = [
            "Barcelona",
            "Project Manager",
            "Desarrollo",
            "Desarrollo Bolivia",
            "Desarrollo Venezuela",
        ]

        employees = self.search([
            ("active", "=", True),
            ("department_id.name", "in", department_names),
            ("work_email", "!=", False),
        ])

        AnalyticLine = self.env["account.analytic.line"]

        urgent = today.weekday() == 4

        template_xmlid = (
            "develoop_timesheets_control.mail_template_timesheet_urgent"
            if urgent
            else "develoop_timesheets_control.mail_template_timesheet_reminder"
        )

        template = self.env.ref(template_xmlid)

        daily_hours = 8
        for employee in employees:
            #daily_hours = employee.x_plannable_hours or 8

            if daily_hours <= 0:
                continue

            lines = AnalyticLine.search([
                ("employee_id", "=", employee.id),
                ("date", ">=", monday),
                ("date", "<=", friday),
                ("task_id", "!=", False),
            ])

            # Agrupar las horas imputadas por fecha.
            recorded_by_day = {}

            for line in lines:
                recorded_by_day[line.date] = (recorded_by_day.get(line.date, 0.0)+ line.unit_amount)

            pending_days = []
            total_pending = 0.0

            # Revisar los cinco días laborables.
            for offset in range(5):
                day = monday + timedelta(days=offset)
                recorded = recorded_by_day.get(day, 0.0)

                pending = max(0.0, daily_hours - recorded)

                if pending > 0.01:
                    pending_days.append({
                        "date": day.strftime("%d/%m/%Y"),
                        "recorded": recorded,
                        "pending": pending,
                    })
                    total_pending += pending
            
            if not pending_days:
                continue

            dias_faltantes = [
                {
                    "fecha": day["date"],
                    "horas_imputadas": day["recorded"],
                    "horas_pendientes": day["pending"],
                }
                for day in pending_days
            ]

            semana_anterior = (
                f"{monday.strftime('%d/%m/%Y')} - "f"{friday.strftime('%d/%m/%Y')}")

            template.with_context(
                Nombre_Empleado=employee.name,
                Semana_Anterior=semana_anterior,
                Dias_Faltantes=dias_faltantes,
                total_pending=total_pending,
            ).send_mail(employee.id, force_send=True)