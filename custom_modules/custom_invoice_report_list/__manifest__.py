# -*- coding: utf-8 -*-
{
    'name': "Custom invoice report in list",
    'version': '15.0.0.0',
    'author': "Develoop Software",
    'category': 'Develoop',
    'summary': 'Agregar una nueva vista de tipo lista en reporte de facturas.',
    'website': "https://www.develoop.net/",
    'description': """
        Agregar una nueva vista de tipo lista en reporte de facturas.
        """,
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_invoice_report_list.xml',
        'report/invoice_report_list_print.xml',
        'report/invoice_list_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_invoice_report_list/static/src/js/data_export_custom.js',
        ],
    },
    'qweb': [],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}