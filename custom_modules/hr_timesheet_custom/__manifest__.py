# -*- coding: utf-8 -*-
{
    'name': "hr_timesheet_custom",
    'summary': """
        Edición impreso parte horas""",
    'description': """
    """,
    'author': "Develoop Software",
    'website': "http://www.develoop.net",
    'category': 'Develoop',
    'version': '17.0',
    'depends': ['hr_timesheet','analytic','hr_attendance'],
    'data': [
        'data/data.xml',
        'views/hr_timesheet.xml',
        'report/report_timesheet_templates.xml',
    ],
    'license': 'LGPL-3',
}