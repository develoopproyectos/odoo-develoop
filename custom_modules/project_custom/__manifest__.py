# -*- coding: utf-8 -*-
{
    'name': 'Project Custom',
    'version': '19.0.0.0',
    'author': 'Develoop Software S.A.',
    'category': 'Develoop',
    'website': 'https://www.develoop.net/',
    'depends': ['base', 'project', 'sale_timesheet','planning','hr_timesheet'],
    'summary': 'Añade campos al proyecto',
    'data': [
        'security/ir.model.access.csv',
        'data/project_technology.xml',
        'views/project.xml',
        'views/project_task.xml',
    ],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
}
