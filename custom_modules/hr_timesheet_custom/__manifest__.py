# -*- coding: utf-8 -*-
{
    'name': "hr_timesheet_custom",
    'summary': """
        Edición impreso parte horas""",

    'description': """
        
    """,

    'author': "Develoop Software",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_timesheet','analytic'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'views/hr_timesheet.xml',
        'report/report_timesheet_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}