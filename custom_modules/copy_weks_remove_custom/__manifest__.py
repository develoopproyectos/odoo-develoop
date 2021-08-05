# -*- coding: utf-8 -*-
{
    'name': "Remueve el boton de copiar semana (Planificacion)",
    'summary': """
        Este modulo remueve el boton en la vista gantt""",
    'version': '0.1',
    'author': 'Develoop Software S.A.',
    'category': 'Develoop',
    'website': 'https://www.develoop.net/',

    # any module necessary for this one to work correctly
    'depends': ['base', 'planning'],

    # always loaded
    'data': [
    ],
    'qweb': [
        'views/templates.xml',
    ],
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
}
