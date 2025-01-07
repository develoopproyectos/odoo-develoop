from odoo import api, models,fields
from odoo.addons.sale_planning.models import planning_slot

class CustomPlanningSlot(models.Model):
    _inherit = 'planning.slot'

    task_id = fields.Many2one(
    'project.task', string="Tarea", compute='_compute_task_id', store=True, readonly=False,
    copy=True, check_company=True, group_expand='_read_group_task_id',
    domain="[('company_id', '=', company_id), ('project_id', '=?', project_id), '|', '|', ('stage_id.name', 'ilike', 'qa'), ('stage_id.name', 'ilike', 'desarrollo'), ('stage_id.name', 'ilike', 'planifi')]")
    #, ('allow_forecast', '=', True)
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super(CustomPlanningSlot, self).create(vals_list)

        # Agrega la condición if res: aquí
        if res:
            if res.sale_line_id and res.sale_line_id.id:
                res.sale_line_id.sudo()._post_process_planning_sale_line(ids_to_exclude=res.ids)
            return res

    @api.depends('project_id', 'template_id.project_id')
    def _compute_task_id(self):
        for slot in self:
            if slot.project_id != slot.task_id.project_id:
                slot.task_id = False
            if slot.template_id:
                slot.previous_template_id = slot.template_id
                if slot.template_id.task_id:
                    slot.task_id = slot.template_id.task_id
            elif slot.previous_template_id and not slot.template_id and slot.previous_template_id.task_id == slot.task_id:
                slot.task_id = False       


    @api.depends(lambda self: self._display_name_fields())
    @api.depends_context('group_by')
    def _compute_display_name(self):
        group_by = self.env.context.get('group_by', [])
        #field_list = [fname for fname in self._display_name_fields() if fname not in group_by]
        field_list = ['task_id']

        # Sudo as a planning manager is not able to read private project if he is not project manager.
        self = self.sudo()
        for slot in self.with_context(hide_partner_ref=True):
            # label part, depending on context `groupby`
            name_values = [
                self._fields[fname].convert_to_display_name(slot[fname], slot) if fname != 'resource_id' else slot.resource_id.name
                for fname in field_list
                if slot[fname]
            ][:4]  # limit to 4 labels
            name = ' - '.join(name_values) or slot.resource_id.name

            # add unicode bubble to tell there is a note
            if slot.name:
                name = f'{name} \U0001F4AC'

            slot.display_name = name or ''             