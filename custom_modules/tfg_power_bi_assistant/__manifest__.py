# -*- coding: utf-8 -*-
{
    'name': "Asistente IA Odoo",
    'summary': """Este módulo integra un asistente de negocio de Inteligencia Artificial en Odoo, dando contexto sobre los datos del sistema""",
    'description': """El módulo dispone de las siguientes funcionalidades:
                - Chatbot con IA integrando los datos de Contactos, Facturas, Ventas y Gastos
                - Generación de informes de negocio detallados impulsados por IA    
            Para que el módulo sea funcional es necesario contratar el servicio a Develoop Software S.L. y disponer de una API Key de Gemini propia, que será vinculada al sistema""",
    'license': "OPL-1",
    'author': "Develoop Software S.A.",
    'website': 'https://www.develoop.net/',    
    "depends": ['base', 'mail', 'product', 'sale', 'account', 'stock', 'purchase', 'contacts', 'stock'] ,
    "data": [
        "security/ir.model.access.csv",
        "data/bot_user_data.xml",     
        "data/ir_config_parameter.xml",
        "views/tfg_menu_views.xml",
        "views/tfg_report_views.xml",
        "views/tfg_res_settings_views.xml"
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
