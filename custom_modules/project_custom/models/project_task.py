# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import date

task_type_validation = ['planificacion','planificación','en desarrollo','desarrollo']

class Dev_ProjectTaskCustom(models.Model):
    
    _inherit = "project.task"

    @api.model
    def _search_x_is_planned(self, operator, operand):
        ext = "" # date_now = fields.Date.today()
        if self._context.get('active_id', False):
            ext = "WHERE project_id=" + str(self._context.get('active_id'))
        sql = """
            SELECT task_id FROM planning_slot WHERE end_datetime < cast(now() as date) and task_id in (SELECT id FROM project_task %s)
        """ % (ext)
        res = self._cr.execute(sql)
        ids = self._cr.fetchall()
        return [('id','not in', ids)]

    x_planning_slot = fields.One2many("planning.slot", compute="get_x_planning_slot", string="Planificaciones", help="Listado de planificaciones")
    x_planning_slot_str = fields.Char(string="Planificacion", compute="get_x_planning_slot")
    x_is_planning_delay = fields.Boolean("Tarea retrasada?", compute="get_x_is_planning_delay")
    x_is_planned = fields.Boolean(string="Esta planificada bool", compute='_compute_x_is_planned', search=_search_x_is_planned)

    def _compute_x_is_planned(self):
        for rec in self:
            rec.x_is_planned = False

    def get_x_planning_slot(self):
        for rec in self:
            plannings = self.env['planning.slot'].search([('task_id','=',rec.id)])
            rec.x_planning_slot = plannings
            rec.x_planning_slot_str = ""
            for data in plannings:
                rec.x_planning_slot_str += "<span>{} - {} ({}) - {} </span><br/>".format(data.start_datetime.strftime("%m/%d/%Y"), data.employee_id.name, str(data.allocated_hours), data.end_datetime.strftime("%m/%d/%Y"))

    def get_x_is_planning_delay(self):
        for rec in self:
            rec.x_is_planning_delay = False
            if rec.date_deadline and rec.date_deadline >= date.today():
                rec.x_is_planning_delay = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_project_id', False) == False:
                vals['display_project_id'] = vals.get('project_id')
        result = super(Dev_ProjectTaskCustom, self).create(vals_list)
        return result

    def write(self, vals):
        for rec in self:
            if rec.stage_id.name and not vals.get('sequence'):
                stage_name = rec.stage_id.name.lower()
                if vals.get('stage_id', False):
                    stage_name = self.env['project.task.type'].browse(vals.get('stage_id')).name
                if stage_name in task_type_validation:
                    if vals.get('planned_hours', rec.planned_hours) == 0 and (\
                            vals.get('name', False) or 
                            vals.get('project_id', False) or 
                            vals.get('sprint', False) or 
                            vals.get('user_id', False) or
                            vals.get('sequence', False) or
                            vals.get('date_deadline', False) or
                            vals.get('tag_ids', False) or
                            vals.get('planned_hours', False) or
                            vals.get('description', False)
                            ):
                        raise ValidationError("El campo horas planeadas es obligatorio")
        for rec2 in vals.get('child_ids', []):
            if len(rec2) == 3:
                if rec2[2]:
                    rec2[2]['display_project_id'] = rec2[2]['project_id']

        result = super(Dev_ProjectTaskCustom, self).write(vals)
        return result
