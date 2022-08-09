# -*- coding: utf-8 -*-
{
    'name': "hr_planning_custom",
    'summary': """
        Modificacion del planning""",

    'description': """
    """,
    'author': "Develoop Software",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['planning','project_forecast','web_gantt'],
    'data': [
        "views/assets.xml",
        "views/planning_slot.xml",
    ],
    'qweb': [
        #"static/src/xml/web_gantt.xml",
    ],
}