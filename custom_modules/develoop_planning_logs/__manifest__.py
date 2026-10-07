{
    'name': 'Develoop Planning Logs',
    'version': '19.0.0.0',
    'description': 'Módulo encargado de registrar los cambios realizados planificación',
    'summary': 'Módulo encargado de registrar los cambios realizados planificación',
    'author': 'Develoop Software',
    'website': 'https://www.develoop.net/',
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'depends': [
        'base', 'planning', 'project'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/planning_slot_log_views.xml"
    ],
    'assets': {
        'web.assets_backend_lazy': [
            'develoop_planning_logs/static/src/xml/planning_gantt.xml',
            'develoop_planning_logs/static/src/js/planning_gantt.js'
        ],
    },
    'demo': [],
    "images": ['static/description/icon.png'],
    'auto_install': False,
    'application': False
}