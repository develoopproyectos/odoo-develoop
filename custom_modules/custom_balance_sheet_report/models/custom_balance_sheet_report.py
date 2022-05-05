# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from collections import OrderedDict, defaultdict

from odoo import _, models
from odoo.exceptions import UserError

# from odoo.custom_modules.mis_builder.models.accounting_none import AccountingNone
# from odoo.custom_modules.mis_builder.models.mis_kpi_data import ACC_SUM
# from odoo.custom_modules.mis_builder.models.mis_safe_eval import DataError, mis_safe_eval
# from odoo.custom_modules.mis_builder.models.simple_array import SimpleArray

try:
    import itertools.izip as zip
except ImportError:
    pass  # python 3

_logger = logging.getLogger(__name__)


class CustomBalanceSheetReport(models.Model):

    _inherit = 'mis.report.instance'

    # def as_dict(self):
    #     header = [{"cols": []}, {"cols": []}]
    #     for col in self.iter_cols():
    #         header[0]["cols"].append(
    #             {
    #                 "label": col.label,
    #                 "description": col.description,
    #                 "colspan": col.colspan,
    #             }
    #         )
    #         for subcol in col.iter_subcols():
    #             header[1]["cols"].append(
    #                 {
    #                     "label": subcol.label,
    #                     "description": subcol.description,
    #                     "colspan": 1,
    #                 }
    #             )

    #     body = []
    #     for row in self.iter_rows():
    #         if (
    #             row.style_props.hide_empty and row.is_empty()
    #         ) or row.style_props.hide_always:
    #             continue
    #         row_data = {
    #             "row_id": row.row_id,
    #             "parent_row_id": (row.parent_row and row.parent_row.row_id or None),
    #             "label": row.label,
    #             "description": row.description,
    #             "style": self._style_model.to_css_style(row.style_props),
    #             "main_class": 'child-' + row.parent_row.row_id if(row.parent_row and row.parent_row.row_id) else '',
    #             "cells": [],
    #         }
    #         for cell in row.iter_cells():
    #             if cell is None:
    #                 # TODO use subcol style here
    #                 row_data["cells"].append({})
    #             else:
    #                 if cell.val is AccountingNone or isinstance(cell.val, DataError):
    #                     val = None
    #                 else:
    #                     val = cell.val
    #                 col_data = {
    #                     "val": val,
    #                     "val_r": cell.val_rendered,
    #                     "val_c": cell.val_comment,
    #                     "style": self._style_model.to_css_style(
    #                         cell.style_props, no_indent=True
    #                     ),
    #                 }
    #                 if cell.drilldown_arg:
    #                     col_data["drilldown_arg"] = cell.drilldown_arg
                     
    #                 row_data["cells"].append(col_data)                    
            
    #         body.append(row_data)
       
    #     previous = None
    #     l = len(body)
    #     for index, obj in enumerate(body):
    #         if index > 0:
    #             previous = body[index - 1]
 
    #         if previous and previous['row_id'] == obj['parent_row_id']:
    #             previous['main_class'] ='parent' 

    #     return {"header": header, "body": body}
