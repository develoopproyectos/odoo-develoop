

from odoo import api, fields, models
from odoo.exceptions import UserError

class ReasonDelayWizard(models.TransientModel):

    _name = "reason_delay"

    #motivo = fields.Many2many('project_update.project_delay_date_reasons' ,required = True, )

    project_id = fields.Many2one('project.project', string='Project',
        index=True, tracking=True, readonly=True)
