from odoo import api, models
from odoo.addons.sale_planning.models import planning_slot

class CustomPlanningSlot(models.Model):
    _inherit = 'planning.slot'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(CustomPlanningSlot, self).create(vals_list)

        # Agrega la condición if res: aquí
        if res:
            if res.sale_line_id:
                res.sale_line_id.sudo()._post_process_planning_sale_line(ids_to_exclude=res.ids)
                return res

        