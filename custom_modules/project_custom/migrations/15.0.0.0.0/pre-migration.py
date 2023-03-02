# Copyright 2021 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936


def migrate(cr, version):
    #cr.execute("DELETE FROM ir_ui_view where id=775")
    #cr.execute("select * From ir_ui_view where arch_fs='l10n_es_aeat_mod349/views/account_move_view.xml' and model='account.move.line'")
    #cr.execute("DELETE From ir_ui_view where arch_fs='l10n_es_aeat_mod349/views/account_move_view.xml' and model='account.move.line'")
    cr.execute("DELETE From ir_ui_view where model='account.move.line' and type='form' and arch_prev like '%mandate_id%'")
    cr.execute("Update ir_module_module set state='uninstalled' where name in ('edi_account','edi')")
