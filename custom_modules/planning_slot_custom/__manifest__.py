# -*- coding: utf-8 -*-
{
    'name': "hr_planning_custom",
    'version': '19.0.0.1',
    'summary': """
        Modificacion del planning""",
    'description': """
    """,
    'author': "Develoop Software",
    'website': "http://www.yourcompany.com",
    'category': 'Custom',
    'depends': ['planning','project_forecast','web_gantt', 'sale_planning','hr_employee_custom', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        "views/planning_slot.xml",
        "views/project_task.xml",
    ],
    'assets': {
        'web.assets_backend_lazy': [
            'planning_slot_custom/static/src/css/style.css',
            'planning_slot_custom/static/src/js/gantt_renderer.js',
            'planning_slot_custom/static/src/js/gantt_controller.js',
            'planning_slot_custom/static/src/xml/planning_gantt.xml'
        ],
    },
    'license': 'LGPL-3',
}
