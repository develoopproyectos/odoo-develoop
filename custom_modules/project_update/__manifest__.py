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
    'website': "http://www.develoop.com",
    'category': 'Develoop',
    'version': '15.0.0.0',

    'depends': ['base','project'],

    'data': [
        'security/ir.model.access.csv',
        'views/project_project_view.xml',
        'views/project_sprint_stage_view.xml',
        'views/project_sprint_view.xml',
        'views/project_task_view.xml',
        'data/project_task_type_data.xml',
        'data/project_sprint_type_data.xml',
      ],
      'license': 'LGPL-3',
}
