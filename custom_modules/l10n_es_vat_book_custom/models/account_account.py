import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class Dev_account_account_Custom(models.Model):

    _inherit = "account.account"
    
    x_check_by_group = fields.Boolean("AEAT (Obtener por grupo)")
