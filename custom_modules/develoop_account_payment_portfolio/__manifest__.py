{
    "name": "Cartera de Cobros y Pagos",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "summary": "Gestión centralizada de vencimientos pendientes de cobro y pago.",
    "description": """
        Cartera de Cobros y Pagos
        =========================

        Este módulo incorpora una pantalla desde la que es posible consultar
        todos los vencimientos pendientes de clientes y proveedores en un único lugar.

        Características principales:
        - Consulta de partidas pendientes de cobro y pago.
        - Visualización de importes residuales y fechas de vencimiento.
        - Registro de cobros y pagos.
        - Conciliación de movimientos contables.
        - Vista unificada de cuentas a cobrar y a pagar.

        La cartera muestra únicamente apuntes contables correspondientes
        a cuentas por cobrar y por pagar cuyo importe residual sea distinto de cero,
        facilitando la gestión diaria de los vencimientos.
        """,
    "author": "Develoop Software",
    "website": "https://www.develoop.net",
    "license": "OPL-1",
    "depends": [
        "account",
        "account_sepa_direct_debit"
    ],
    "data": [
        "views/account_move_line_views.xml"
    ],
    "assets": {},
    "installable": True,
    "application": True,
    "auto_install": False,
}
