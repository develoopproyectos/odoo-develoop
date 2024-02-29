# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID

from odoo.addons.base.models.res_partner import _tz_get


class LeaveReportCalendar(models.Model):
    _inherit = "hr.leave.report.calendar"
    hr_leave_type_id = fields.Many2one('hr.leave.type', string='Tipo de ausencia', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_leave_report_calendar')
        self._cr.execute("""CREATE OR REPLACE VIEW hr_leave_report_calendar AS
        (SELECT 
            hl.id AS id,
            CONCAT(em.name, ': ', hl.duration_display) AS name,
            hl.date_from AS start_datetime,
            hl.date_to AS stop_datetime,
            hl.employee_id AS employee_id,
            hl.state AS state,
            hl.department_id AS department_id,
            em.company_id AS company_id,
            em.job_id AS job_id,
            hl.holiday_status_id AS hr_leave_type_id,
            COALESCE(
                CASE WHEN hl.holiday_type = 'employee' THEN COALESCE(rr.tz, rc.tz) END,
                cc.tz,
                'UTC'
            ) AS tz,
            hl.state = 'refuse' as is_striked,
            hl.state not in ('validate', 'refuse') as is_hatched
        FROM hr_leave hl            
            LEFT JOIN hr_employee em
                ON em.id = hl.employee_id
            LEFT JOIN resource_resource rr
                ON rr.id = em.resource_id
            LEFT JOIN resource_calendar rc
                ON rc.id = em.resource_calendar_id
            LEFT JOIN res_company co
                ON co.id = em.company_id
            LEFT JOIN resource_calendar cc
                ON cc.id = co.resource_calendar_id
        WHERE 
            hl.state IN ('confirm', 'validate', 'validate1')
        );
        """)