# -*- coding: utf-8 -*-
{
    'name': "<TITULO DEL MODULO>",
    'summary': """<RESUMEN DEL MODULO>""",
    'description': """<DESCRIPCION DEL MODULO DETALLADA>
            - <DESCRIPCION DEL MODULO DETALLADA>
            - <DESCRIPCION DEL MODULO DETALLADA>    
            """,
    'license': "OPL-1",
    'author': "Develoop Software S.A. (AQUI SOLEMOS PONER ESTO PERO EN ESTE CASO YA ME DICES)",
    'website': 'https://www.develoop.net/ (OPCIONAL)',    
    "depends": ['base', 'mail', 'product', 'sale', 'account', 'stock', 'purchase', 'contacts', 'stock'] ,
    "data": [
        "security/ir.model.access.csv",
        "data/bot_user_data.xml",     
        "data/ir_config_parameter.xml",
        "views/tfg_res_settings_views.xml",
        "views/tfg_menu_views.xml",
        "views/tfg_report_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'tfg_power_bi_assistant/static/src/components/**/*.js',
            'tfg_power_bi_assistant/static/src/components/**/*.xml',
            'tfg_power_bi_assistant/static/src/widgets/**/*.js',
            'tfg_power_bi_assistant/static/src/widgets/**/*.xml',
            'tfg_power_bi_assistant/static/src/components/**/*.scss',
            'tfg_power_bi_assistant/static/src/components/discuss_category/*.js'
        ],
    },
    'images': ['static/description/icon.png'],
    'application': True,
}
