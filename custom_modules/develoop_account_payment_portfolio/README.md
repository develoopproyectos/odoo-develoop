# Cartera de Cobros y Pagos

[![License: OPL-1](https://img.shields.io/badge/License-OPL--1-blue.svg)](https://www.odoo.com/documentation/17.0/legal/licenses.html)
[![Version](https://img.shields.io/badge/Odoo-19.0-informational.svg)](https://www.odoo.com)

Este módulo incorpora una pantalla centralizada desde la que es posible consultar y gestionar todos los vencimientos pendientes de clientes y proveedores en un único lugar.

La cartera muestra únicamente apuntes contables correspondientes a cuentas por cobrar y por pagar cuyo importe residual sea distinto de cero, facilitando de forma óptima la gestión diaria de los vencimientos.

---

## Características Principales

* **Vista Unificada:** Consulta centralizada de cuentas a cobrar (clientes) y a pagar (proveedores).
* **Gestión de Vencimientos:** Visualización clara de los importes residuales y fechas límite de vencimiento.
* **Operaciones Directas:** Registro de cobros y pagos directamente desde la plataforma de gestión.
* **Conciliación:** Conciliación rápida y eficiente de movimientos contables pendientes.

## Especificaciones Técnicas

* **Categoría:** Contabilidad (`Accounting`)
* **Aplicación:** Sí (Aparece en el menú de aplicaciones de Odoo)
* **Instalación Automática:** No

### Dependencias

Este módulo requiere que los siguientes módulos de Odoo estén instalados:
1. `account` (Contabilidad Básica de Odoo)
2. `account_sepa_direct_debit` (Adeudos Directos SEPA)

## Estructura de Datos y Vistas

El módulo modifica e integra nuevas funcionalidades en las siguientes rutas:
* `views/account_move_line_views.xml`: Añade e introduce los ajustes visuales para la correcta gestión de los apuntes contables en cartera.

---

## Autoría y Soporte

* **Autor:** Develoop Software
* **Sitio Web:** [https://www.develoop.net](https://www.develoop.net)
* **Licencia:** OPL-1 (Odoo Proprietary License v1.0)