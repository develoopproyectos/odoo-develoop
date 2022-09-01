
from odoo import api, fields, models

class dev_planning_slot_custom(models.Model):
    
    _inherit = "planning.slot"

    x_expiration_date = fields.Date(related='task_id.date_deadline')
    x_kanban_state = fields.Selection(related='task_id.kanban_state')
