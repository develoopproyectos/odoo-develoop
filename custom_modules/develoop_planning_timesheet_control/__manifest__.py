{
    'name': 'Develoop Timesheets Control',
    'version': '19.0.0.0',
    'description': 'Módulo encargado de controlar la imputación de horas semanales, mediante advertencias por correo',
    'summary': 'Módulo encargado de controlar la imputación de horas semanales',
    'author': 'Develoop Software',
    'website': 'https://www.develoop.net/',
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'depends': [
        'base', 'hr'
    ],
    "data": [
        "data/mail_templates.xml",
        "data/ir_cron.xml",
    ],
    'assets': { },
    'demo': [],
    "images": ['static/description/icon.png'],
    'auto_install': False,
    'application': False
}