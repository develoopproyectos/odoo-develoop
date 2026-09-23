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
    'demo': [],
    "images": ['static/description/icon.png'],
    'auto_install': False,
    'application': False,
    'assets': {}
}