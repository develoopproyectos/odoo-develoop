# -*- coding: utf-8 -*-
{
    'name': 'SEPA Report custom',
    'version': '13.0.1.0.0',
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
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
