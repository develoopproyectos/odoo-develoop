
from odoo import api, fields, models
from odoo.tools import format_date, format_datetime
from markupsafe import Markup


class PlanningSlotLog(models.Model):
    _name = "planning.slot.log"
    _description = "Historico de cambios en la planificación"
    
    _rec_name = "log_date"

    log_date = fields.Datetime(string="Dia y Hora", default=fields.Datetime.now)
    partner_id = fields.Many2one('res.partner', string="Responsable")
    project_id = fields.Many2one('project.project', string="Proyecto", readonly=True)    
    task_id = fields.Many2one('project.task', string="Tarea")
    resource_id = fields.Many2one('resource.resource', string="Recurso")
    action = fields.Selection([('created','Creado'),('modified','Modificado'),('removed','Eliminado')], string="Acción Realizada")
    old_start_date = fields.Datetime(string="Fecha inicio anterior")
    old_end_date = fields.Datetime(string="Fecha inicio anterior final")
    new_start_date = fields.Datetime(string="Fecha inicio")
    new_end_date = fields.Datetime(string="Fecha inicio final")