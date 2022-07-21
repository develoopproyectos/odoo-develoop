# -*- coding: utf-8 -*-
{
    'name': "project_update",

    'summary': """
        Texto molon de verdad
        """,

    'description': """
        Esto es una extension para el modulo de proyectos
    """,

    'author': "Marc Cortadellas",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/project_project_view.xml',
        'views/project_sprint_view.xml',
        'views/project_task_view.xml',
        'data/project_task_type_data.xml',
      ],
    #     'report/project_report_views.xml','report/project_task_burndown_chart_report_views.xml'
  #'wizard/reason_delay.xml',


}
