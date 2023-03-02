# -*- coding: utf-8 -*-
{
    'name': "web_layout_custom",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description': """
            Long description of module's purpose
        """,
    'author': "Develoop",
    'website': "http://www.develoop.net",
    'category': 'Develoop',
    'version': '15.0.0.0',
    'depends': ['web','base','account','l10n_es_aeat_mod349','account_banking_mandate'],
    'data': [
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
    #'pre_init_hook':'pre_init_hook'
}
