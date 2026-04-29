from odoo.upgrade import util

def migrate(cr, version):
    # Campo que bloquea la migración
    util.remove_field(
        cr,
        model='sale.subscription.report',
        field='payment_mode_id',
    )