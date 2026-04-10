# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID

from odoo.addons.base.models.res_partner import _tz_get


class LeaveReportCalendar(models.Model):
    _inherit = "hr.leave.report.calendar"
    hr_leave_type_id = fields.Many2one('hr.leave.type', string='Tipo de ausencia', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_leave_report_calendar')
        self.env.cr.execute("""CREATE OR REPLACE VIEW hr_leave_report_calendar AS
        (SELECT
            hl.id AS id,
            hl.id AS leave_id,
            hl.date_from AS start_datetime,
            hl.date_to AS stop_datetime,
            hl.employee_id AS employee_id,
            hl.state AS state,
            hl.department_id AS department_id,
            hl.number_of_days as duration,
            hl.private_name AS description,
            hl.holiday_status_id AS holiday_status_id,
            em.company_id AS company_id,
            v.job_id AS job_id,
            em.user_id AS user_id,
            COALESCE(
                rr.tz,
                rc.tz,
                cc.tz,
                'UTC'
            ) AS tz,
            hl.state = 'refuse' as is_striked,
            hl.state not in ('validate', 'refuse') as is_hatched,
            hl.holiday_status_id AS hr_leave_type_id
        FROM hr_leave hl
            LEFT JOIN hr_employee em
                ON em.id = hl.employee_id
            LEFT JOIN hr_version v ON v.id = em.current_version_id
            LEFT JOIN resource_resource rr
                ON rr.id = em.resource_id
            LEFT JOIN resource_calendar rc
                ON rc.id = v.resource_calendar_id
            LEFT JOIN res_company co
                ON co.id = em.company_id
            LEFT JOIN resource_calendar cc
                ON cc.id = co.resource_calendar_id
        WHERE
            hl.state IN ('confirm', 'validate', 'validate1', 'refuse')
        );
        """)