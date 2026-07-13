# -*- coding: utf-8 -*-
{
    'name': "Develoop report custom",
    'version': '19.0.0.0',
    'author': "Develoop Software",
    'category': 'Uncategorized',
    'summary': 'Remover limitacion de montos.',
    'website': "https://www.develoop.net/",
    'description': """
        - Remover restricciones de rangos cuando se aplica un comparativo
        """,
    'depends': ['sale'],
    'data': [
        'reports/sale_order_report_inherit.xml'
    ],
    'demo': [],
    "images": ['static/description/icon.png'],
    "installable": True,
    "application": True,
    "auto_install": False,
    'license': 'LGPL-3',
}