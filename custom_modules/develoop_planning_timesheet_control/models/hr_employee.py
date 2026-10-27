
from datetime import datetime, timedelta, time
import pytz
from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def _cron_check_weekly_timesheets(self):
        today = fields.Date.context_today(self)

        # Ejecutar únicamente los martes y viernes.
        if today.weekday() not in (1, 4):
            return

        monday = today - timedelta(days=today.weekday() + 7)
        friday = monday + timedelta(days=4)
        saturday = friday + timedelta(days=1)

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

        Attendance = self.env["hr.attendance"]
        AnalyticLine = self.env["account.analytic.line"]

        urgent = today.weekday() == 4

        template_xmlid = ("develoop_planning_timesheet_control.mail_template_timesheet_urgent" if urgent else "develoop_planning_timesheet_control.mail_template_timesheet_reminder")

        template = self.env.ref(template_xmlid)

        tolerance = 0.25  # 15 minutos

        for employee in employees:
            tz_name = employee.resource_id.tz or "UTC"
            employee_tz = pytz.timezone(tz_name)

            def local_day_to_utc(day):
                local_dt = employee_tz.localize(datetime.combine(day, time.min))
                return (local_dt.astimezone(pytz.UTC).replace(tzinfo=None))

            week_start_utc = local_day_to_utc(monday)
            week_end_utc = local_day_to_utc(saturday)

            # Obtener las asistencias que se solapan con la semana.
            attendances = Attendance.search([
                ("employee_id", "=", employee.id),
                ("check_in", "<", week_end_utc),
                ("check_out", "!=", False),
                ("check_out", ">", week_start_utc),
            ])

            # Obtener las imputaciones de la semana con tarea.
            analytic_lines = AnalyticLine.search([
                ("employee_id", "=", employee.id),
                ("date", ">=", monday),
                ("date", "<=", friday),
                ("task_id", "!=", False),
            ])

            recorded_by_day = {}

            for line in analytic_lines:
                recorded_by_day[line.date] = (recorded_by_day.get(line.date, 0.0) + line.unit_amount)

            pending_days = []

            for day_offset in range(5):
                day = monday + timedelta(days=day_offset)

                day_start_utc = local_day_to_utc(day)
                day_end_utc = local_day_to_utc(day + timedelta(days=1))

                # Sumar solo las horas trabajadas dentro de este día.
                attendance_hours = 0.0

                day_attendances = attendances.filtered(
                    lambda attendance:
                        attendance.check_in < day_end_utc
                        and attendance.check_out > day_start_utc
                )

                for attendance in day_attendances:
                    attendance_hours += (attendance._get_worked_hours_in_range(day_start_utc, day_end_utc))

                recorded = recorded_by_day.get(day, 0.0)
                difference = abs(recorded - attendance_hours)

                # Ignorar diferencias de hasta 15 minutos.
                if difference <= tolerance:
                    continue

                pending = max(0.0, attendance_hours - recorded)
                excess = max(0.0, recorded - attendance_hours)

                pending_days.append({
                    "fecha": day.strftime("%d/%m/%Y"),
                    "horas_imputadas": round(recorded, 2),
                    "horas_asistencia": round(attendance_hours, 2),
                    "horas_pendientes": round(pending, 2),
                    "horas_exceso": round(excess, 2),
                })

            # No enviar correo si no existen diferencias relevantes.
            if not pending_days:
                continue

            total_pending = round(sum(day["horas_pendientes"] for day in pending_days), 2)

            semana_anterior = (f"{monday.strftime('%d/%m/%Y')} - {friday.strftime('%d/%m/%Y')}")

            template.with_context(
                Nombre_Empleado=employee.name,
                Semana_Anterior=semana_anterior,
                Dias_Faltantes=pending_days,
                total_pending=total_pending,
            ).send_mail(employee.id, force_send=False)