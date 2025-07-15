# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import date, datetime
from markupsafe import Markup
task_type_validation = ['planificacion','planificación','en desarrollo','desarrollo']

class Dev_ProjectTaskCustom(models.Model):
    
    _inherit = "project.task"

    @api.model
    def _search_x_is_planned(self, operator, operand):
        ext = "" # date_now = fields.Date.today()
        if self._context.get('active_id', False):
            ext = "WHERE project_id=" + str(self._context.get('active_id'))
        sql = """
            SELECT task_id FROM planning_slot WHERE cast(end_datetime as date) >= cast(now() as date) and task_id in (SELECT id FROM project_task %s)
        """ % (ext)
        res = self._cr.execute(sql)
        ids = self._cr.fetchall()
        return [('id','not in', ids)]

    x_planning_slot = fields.One2many("planning.slot", compute="get_x_planning_slot", string="Planificaciones", help="Listado de planificaciones")
    x_planning_slot_str = fields.Char(string="Planificacion", compute="get_x_planning_slot")
    x_is_planning_delay = fields.Boolean("Tarea retrasada?", compute="get_x_is_planning_delay")
    x_is_planned = fields.Boolean(string="Esta planificada bool", compute='_compute_x_is_planned', search=_search_x_is_planned)
    has_trello = fields.Boolean(related='project_id.has_trello')
    url_trello = fields.Char(string='Enlace Trello')

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
            if rec.date_deadline and rec.date_deadline >= datetime.today():
                rec.x_is_planning_delay = True


    @api.model_create_multi
    def create(self, vals_list):
        if not isinstance(vals_list, list):
            raise ValueError("Los valures tienen que ser una lista de diccionarios")

        for vals in vals_list:
            if not isinstance(vals, dict):
                raise ValueError("Cada item en los valores tiene que ser un diccionario")

            if not vals.get('company_id'):
                project_id = vals.get('project_id')
                if project_id:
                    if isinstance(project_id, int):
                        project = self.env['project.project'].browse(project_id)
                        vals['company_id'] = project.company_id.id or self.env.user.company_id.id
                    else:
                        vals['company_id'] = project_id.company_id.id
                else:
                    vals['company_id'] = self.env.company.id or self.env.user.company_id.id

        return super().create(vals_list)
    #@api.model_create_multi
    #def create(self, vals_list):
        #COMENTADO por que ya no existe display_project_id
        # for vals in vals_list:
        #     if vals.get('display_project_id', False) == False:
        #         vals['display_project_id'] = vals.get('project_id')
        #if not vals_list[0].get('company_id', False):
        #    vals_list['company_id'] = self.env.company.id if not self.project_id.company_id else self.project_id.company_id

        #result = super(Dev_ProjectTaskCustom, self).create(vals_list)
        #Crear notas a partir del cambio de tags
        #self.message_post_tags(vals_list[0],result)
        # if 'stage_id' in vals:
            # stage_name = self.env['project.task.type'].browse(vals.get('stage_id')).name.lower()
            # if stage_name in task_type_validation:
            #     users_to_subscribe = self.env['res.users'].sudo().search([('id','=', 48)])  # Puedes obtener el usuario actual o cualquier otro
            #     result.message_subscribe(partner_ids=users_to_subscribe.partner_id.ids)
            #     self.enviar_notificacion_a_usuario(users_to_subscribe, f"Fuiste suscrito a la tarea <strong style='font-size:16px'>{result.name}</strong> que paso a la etapa de <strong style='font-size:16px'>{stage_name}</strong>", result, f"Tarea {result.name} Cambio de Estapa")                
                
        #return result

    def write(self, vals):
        for rec in self:
            if rec.stage_id.name and not vals.get('sequence'):
                stage_name = rec.stage_id.name.lower()
                if vals.get('stage_id', False):
                    stage_name = self.env['project.task.type'].browse(vals.get('stage_id')).name
                
                # if stage_name in task_type_validation:
                #     if vals.get('allocated_hours', rec.allocated_hours) == 0 and (\
                #             vals.get('name', False) or 
                #             vals.get('project_id', False) or 
                #             vals.get('sprint', False) or 
                #             vals.get('user_id', False) or
                #             vals.get('sequence', False) or
                #             vals.get('date_deadline', False) or
                #             vals.get('tag_ids', False) or
                #             vals.get('allocated_hours', False) or
                #             vals.get('description', False)
                #             ):  
                #         raise ValidationError("El campo horas planeadas es obligatorio")
                    
            if 'stage_id' in vals:
                stage = self.env['project.task.type'].browse(vals.get('stage_id')).name
                stage_name = stage.lower() if stage else False
                # if stage_name and stage_name in task_type_validation:
                #     users_to_subscribe = self.env['res.users'].sudo().search([('id','=', 48)])  # Puedes obtener el usuario actual o cualquier otro
                #     rec.message_subscribe(partner_ids=users_to_subscribe.partner_id.ids)
                #     self.enviar_notificacion_a_usuario(users_to_subscribe, f"Fuiste suscrito a la tarea <strong style='font-size:16px'>{rec.name}</strong> que paso a la etapa de <strong style='font-size:16px'>{stage_name}</strong>", rec, f"Tarea {rec.name} Cambio de Estapa")                    
                    
                    
                # else:
                #     users_to_subscribe = self.env['res.users'].sudo().search([('id','=', 48)])
                #     rec.message_unsubscribe(partner_ids=users_to_subscribe.partner_id.ids)           

        #Crear notas a partir del cambio de tags
        self.message_post_tags(vals,False)
        old_users = self.user_ids
        result = super(Dev_ProjectTaskCustom, self).write(vals)
        # if 'user_ids' in vals and self.stage_id.name.lower() in task_type_validation:
        #         users_to_notifi = self.env['res.users'].sudo().search([('id','=', 48)])
        #         self.enviar_notificacion_a_usuario(users_to_notifi, "La tarea <strong style='font-size:16px'>{}</strong> fue asignada a:  <strong style='font-size:16px'>{}</strong><div title='Cambiado' role='img' class='o_Message_trackingValueSeparator o_Message_trackingValueItem fa fa-long-arrow-right'></div><strong style='font-size:16px'>{}</strong>".format(rec.name, "".join(f" {user.name}," for user in old_users.user_ids),"".join(f" {user.name}," for user in self.user_ids)) , self, f"Tarea {self.name} Re Asignacion")
        return result


    def message_post_tags(self,vals,result): 
        if vals.get('tag_ids', []):
            new_tags_old = vals.get('tag_ids', [])
            added_tags = [tag[1] for tag in new_tags_old if tag[0] == 4]
            removed_tags = [tag[1] for tag in new_tags_old if tag[0] == 3]
            if added_tags:
                tags = []
                for tag in added_tags:
                    tags.append(self.env['project.tags'].search([('id', '=', tag)]))
                added_notes = "Se agregaron las siguientes etiquetas:<ul style='list-style-position: inside;'>{}</ul>".format("".join(f"<li><div class='border-radius: 10px;  badge rounded-pill mt-2' style='border-color: {self.get_bootstrap_color_class(tag.color)[0]}; background-color: {self.get_bootstrap_color_class(tag.color)[0]}; color: {self.get_bootstrap_color_class(tag.color)[1]} ;font-size: 11px; padding: 6px;'>{tag.name}</div></li>" for tag in tags))
                if result:
                    result.message_post(body=Markup(added_notes))
                else:    
                    self.message_post(body=Markup(added_notes))

            # Creamos notas para las etiquetas eliminadas
            if removed_tags:
                tags = []
                for tag in removed_tags:
                    tags.append(self.env['project.tags'].search([('id', '=', tag)]))
                removed_notes = "Se quitaron las siguientes etiquetas:<ul style='list-style-position: inside;'>{}</ul>".format("".join(f"<li><div class='border-radius: 10px;  badge rounded-pill mt-2' style='border-color: {self.get_bootstrap_color_class(tag.color)[0]}; background-color: {self.get_bootstrap_color_class(tag.color)[0]}; color: {self.get_bootstrap_color_class(tag.color)[1]} ;font-size: 11px; padding: 6px;'>{tag.name}</div></li>" for tag in tags))
                if result:
                    result.message_post(body=Markup(removed_notes))
                else:    
                    self.message_post(body=Markup(removed_notes))

    def get_bootstrap_color_class(self, color_number):
        font_color = "black"
        attrs = []
        bootstrap_colors = {
        0: 'white',
        1: '#F06050',
        2: '#F4A460',
        3: '#F7CD1F',
        4: '#6CC1ED',
        5: '#814968',
        6: '#EB7E7F',
        7: '#2C8397',
        8: '#475577',
        9: '#D6145F',
        10: '#30C381',
        11: '#9365B8',  
        }
        if color_number:
            if color_number == 11 or color_number == 8 or color_number == 7 or color_number == 6 or color_number == 5 or color_number == 1   :
                font_color = "white"
            attrs.append(bootstrap_colors.get(color_number))
            attrs.append(font_color)
        else:
            attrs.append(bootstrap_colors.get(0))
            attrs.append(font_color)
        return attrs


    @api.model
    def enviar_notificacion_a_usuario(self, user, mensaje, tarea, subj):               
        
        enlace_tarea = f"<p style='padding-top:24px; padding-bottom:16px'><a style='background-color:#875A7B; padding:10px; text-decoration:none; color:#fff; border-radius:5px' href='/web#id={tarea.id}&view_type=form&model=project.task'>Ver Tarea</a></p>"

        mensaje_con_enlace = f"{mensaje}<br> Ver la tarea aquí: <br> {enlace_tarea}"

        user.partner_id.sudo().message_post(body=mensaje_con_enlace, partner_ids=user.partner_id.ids, subject=subj)