# -*- coding: utf-8 -*-
{
    'name': 'SEPA Report custom',
    'version': '15.0.0.0',
    'summary': """SEPA Report.""",
    'description': """
        Modulo personalizado impreso mandato SEPA.
    """,
    'depends': ['base', 'account', 'account_sepa_direct_debit'],
    'data': [
        'views/sepa_report_view.xml',
    ],
    'author': 'Develoop Software',
    'images': ['static/description/icon.png'],
    'maintainer': 'Develoop Software',
    'website': 'https://www.develoop.net',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
