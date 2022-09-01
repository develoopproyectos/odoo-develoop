# -*- coding: utf-8 -*-
{
    'name': 'Project Custom',
    'version': '1.0',
    'author': 'Develoop Software S.A.',
    'category': 'Develoop',
    'website': 'https://www.develoop.net/',
    'depends': ['base', 'project'],
    'summary': 'Añade campos al proyecto',
    'data': [
        'security/ir.model.access.csv',
        'data/project_technology.xml',
        'views/project.xml',
    ],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
}
