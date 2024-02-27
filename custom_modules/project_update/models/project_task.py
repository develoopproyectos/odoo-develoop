# -*- coding: utf-8 -*-

from odoo import fields, models, api

class TaskTemplate(models.Model):
    _inherit = 'project.task'
    # default=lambda self: self.env.context.get('active_id')
    sprint = fields.Many2one('project.sprint', string='Sprint',
                             index=True, tracking=True, check_company=True, change_default=True)
    #dependencia = fields.Many2one('project.task', string='Dependencias', default=lambda self: self.env.context.get('active_id'), index=True, tracking=True, check_company=True, change_default=True)
    horas_planeadas = fields.Integer(string="Horas Planeadas")
    horas_dedicadas = fields.Integer(string="Horas dedidacas")
    horas_dedicadas_pctg = fields.Integer(string="Horas dedicadas (%)") # min=0, max= 10
    horas_desarrolladas_pctg = fields.Integer(string="Horas desarrollo (%)") # min=0, max= 10
    visible = fields.Boolean(default=False)
    first_attempt =fields.Boolean(default=False)
    motive_deadline = fields.Selection([('t1', 'Reestructuración proyecto'), ('t2', 'Falta de recursos'), ('t3', 'Replanificación otros proyectos'), ('t4','Falta material'), ('t5', 'falta de comunicación'), ('t6', 'Feedback')],
                                       string="Motivo", tracking = True, invisible=True)


    @api.onchange('date_deadline')
    def activar_motivo(self):
        self.motive_deadline = False
        if self.first_attempt: self.visible = True
        else: self.first_attempt = True

            
    def write(self, vals):
        if 'visible' in vals:
            vals['visible']=False
        if 'date_deadline' in vals:
            vals['first_attempt']=True

        if 'stage_id' in vals:
            if vals['stage_id'] == self.env.ref('project_update.type_epicas').id:
                vals['sprint'] = False

        if 'sprint_name' in self.activity_ids.env.context:
            vals['sprint'] = self.activity_ids.env.context['sprint_name']

        data=super(TaskTemplate, self).write(vals)
        return data

"""
    def sprint_action(self):
        view_kanban_id = self.env.ref('project_update.sprint_kanban').id
        """"""ctx opcional""""""
        ctx = dict(self.env.context or {})
        action = {
            'type': 'ir.actions.act_window',
            'domain': [('project_id', 'in', self.ids)],
            #'views': [(view_kanban_id, 'kanban')],
            'view_mode': 'kanban,form',
            'name': 'Sprints',
            'res_model': 'project.sprint',
            'context': ctx
        }
        return action
"""
