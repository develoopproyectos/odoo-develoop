# -*- coding: utf-8 -*-
{
    'name': "hr_planning_custom",
    'version': '15.0.0.0',
    'summary': """
        Modificacion del planning""",

    'description': """
    """,
    'author': "Develoop Software",
    'website': "http://www.yourcompany.com",
    'category': 'Custom',
    'depends': ['planning','project_forecast','web_gantt'],
    'data': [
        "views/planning_slot.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'planning_slot_custom/static/src/css/style.css',
            'planning_slot_custom/static/src/js/gantt_row.js',
        ],
    },
    'license': 'LGPL-3',
}
