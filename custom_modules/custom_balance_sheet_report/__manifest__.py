# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Reporte Balance Situacional Custom",
    "version": "1.0.0.0",
    "category": "Reporting",
    "summary": """
        Build 'Reporte Balance Situacional con mejoras
    """,
    "author": "Develoop Software",
    "website": "https://www.develoop.net",
    "depends": [
        "mis_builder"
    ],
    "data": [
        "views/balance_situacional_instance.xml"
    ],
    "qweb": ["static/src/xml/balance_situacional_widget.xml"],
    "images": ['static/description/icon.png'],
    "installable": True,
    "application": True,
	'license': 'LGPL-3',
}
