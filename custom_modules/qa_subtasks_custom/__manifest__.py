# -*- coding: utf-8 -*-
{
    'name': 'QA Sub Task Custom',
    'version': '1.0',
    'author': 'Develoop Software S.A.',
    'category': 'Develoop',
    'website': 'https://www.develoop.net/',
    'depends': ['base', 'project'],
    'summary': 'Se creara una vista para las sub tareas que corresponde a QA y que tendran como tarea padre a otra',
    'data': [
        'security/ir.model.access.csv',
        # 'data/data.xml',
        'views/project_task_inherit.xml',
        'wizard/test_cases_wizard.xml',
        # 'data/project_technology.xml',
        # 'views/project.xml',
        # 'views/project_task.xml',
    ],
    'qweb': [],
    'assets': {
        'web.assets_backend': [
            'qa_subtasks_custom/static/src/js/project_kanban_inherit.js'
        ],
    },
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
}
