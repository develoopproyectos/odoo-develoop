# -*- coding: utf-8 -*-
{
    'name': "Remueve el boton de copiar semana (Planificacion)",
    'summary': """
        Este modulo remueve el boton en la vista gantt""",
    'version': '15.0.0.0',
    'author': 'Develoop Software S.A.',
    'category': 'Develoop',
    'website': 'https://www.develoop.net/',

    'depends': ['planning'],
    'data': [],
    'assets': {
        'web.assets_qweb': [
            'copy_weks_remove_custom/static/src/xml/planning_gantt.xml',
        ],
    },
    'images': ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    "license": "AGPL-3",
}
