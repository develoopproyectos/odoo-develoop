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
            SELECT task_id FROM planning_slot WHERE cast(end_datetime as date) >= cast(now() as date) and task_id in (SELECT id FROM project_task %s)
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
        #Crear notas a partir del cambio de tags
        if 'tag_ids' in vals:
            old_tags = self.tag_ids.ids
            new_tags = vals.get('tag_ids', [])[0][2]
            added_tags = list(set(new_tags)-set(old_tags))
            removed_tags = list(set(old_tags)-set(new_tags))
            # Creamos notas para las etiquetas agregadas
            if added_tags:
                tags = []
                for tag in added_tags:
                    tags.append(self.env['project.tags'].search([('id', '=', tag)]))
                added_notes = "Se agregaron las siguientes etiquetas:<ul style='list-style-position: inside;'>{}</ul>".format("".join(f"<li><div class='badge badge-pill mt-2' style='border-color: {self.get_bootstrap_color_class(tag.color)[0]}; background-color: {self.get_bootstrap_color_class(tag.color)[0]}; color: {self.get_bootstrap_color_class(tag.color)[1]} ;font-size: 11px; padding: 6px;'>{tag.name}</div></li>" for tag in tags))
                result.message_post(body=added_notes)

            # Creamos notas para las etiquetas eliminadas
            if removed_tags:
                tags = []
                for tag in removed_tags:
                    tags.append(self.env['project.tags'].search([('id', '=', tag)]))
                removed_notes = "Se quitaron las siguientes etiquetas:<ul style='list-style-position: inside;'>{}</ul>".format("".join(f"<li><div class='badge badge-pill mt-2' style='border-color: {self.get_bootstrap_color_class(tag.color)[0]}; background-color: {self.get_bootstrap_color_class(tag.color)[0]}; color: {self.get_bootstrap_color_class(tag.color)[1]} ;font-size: 11px; padding: 6px;'>{tag.name}</div></li>" for tag in tags))
                result.message_post(body=removed_notes)

        if 'stage_id' in vals:
            stage_name = self.env['project.task.type'].browse(vals.get('stage_id')).name.lower()
            if stage_name in task_type_validation:
                users_to_subscribe = self.env['res.users'].search([('id','=', 48)]).partner_id  # Puedes obtener el usuario actual o cualquier otro
                result.message_subscribe(partner_ids=users_to_subscribe.ids)
                self.enviar_notificacion_a_usuario(users_to_subscribe, f"Fuiste suscrito a la tarea <strong style='font-size:16px'>{result.name}</strong> que paso a la etapa de <strong style='font-size:16px'>{stage_name}</strong>", result, f"Tarea {result.name} Cambio de Estapa")                
                
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
                    
            if 'stage_id' in vals:
                stage_name = self.env['project.task.type'].browse(vals.get('stage_id')).name.lower()
                if stage_name in task_type_validation:
                    users_to_subscribe = self.env['res.users'].search([('id','=', 48)])  # Puedes obtener el usuario actual o cualquier otro
                    rec.message_subscribe(partner_ids=users_to_subscribe.partner_id.ids)
                    self.enviar_notificacion_a_usuario(users_to_subscribe, f"Fuiste suscrito a la tarea <strong style='font-size:16px'>{rec.name}</strong> que paso a la etapa de <strong style='font-size:16px'>{stage_name}</strong>", rec, f"Tarea {rec.name} Cambio de Estapa")                    
                    
                    
                else:
                    users_to_subscribe = self.env['res.users'].search([('id','=', 48)])
                    rec.message_unsubscribe(partner_ids=users_to_subscribe.partner_id.ids)           

        for rec2 in vals.get('child_ids', []):
            if len(rec2) == 3:
                if rec2[2]:
                    rec2[2]['display_project_id'] = rec2[2]['project_id']
        
        #Crear notas a partir del cambio de tags
        if 'tag_ids' in vals:
            old_tags = self.tag_ids.ids
            new_tags = vals.get('tag_ids', [])[0][2]
            added_tags = list(set(new_tags)-set(old_tags))
            removed_tags = list(set(old_tags)-set(new_tags))
            # Creamos notas para las etiquetas agregadas
            if added_tags:
                tags = []
                for tag in added_tags:
                    tags.append(self.env['project.tags'].search([('id', '=', tag)]))
                added_notes = "Se agregaron las siguientes etiquetas:<ul style='list-style-position: inside;'>{}</ul>".format("".join(f"<li><div class='badge badge-pill mt-2' style='border-color: {self.get_bootstrap_color_class(tag.color)[0]}; background-color: {self.get_bootstrap_color_class(tag.color)[0]}; color: {self.get_bootstrap_color_class(tag.color)[1]} ;font-size: 11px; padding: 6px;'>{tag.name}</div></li>" for tag in tags))
                self.message_post(body=added_notes)

            # Creamos notas para las etiquetas eliminadas
            if removed_tags:
                tags = []
                for tag in removed_tags:
                    tags.append(self.env['project.tags'].search([('id', '=', tag)]))
                removed_notes = "Se quitaron las siguientes etiquetas:<ul style='list-style-position: inside;'>{}</ul>".format("".join(f"<li><div class='badge badge-pill mt-2' style='border-color: {self.get_bootstrap_color_class(tag.color)[0]}; background-color: {self.get_bootstrap_color_class(tag.color)[0]}; color: {self.get_bootstrap_color_class(tag.color)[1]} ;font-size: 11px; padding: 6px;'>{tag.name}</div></li>" for tag in tags))
                self.message_post(body=removed_notes)
        old_users = self.user_ids
        result = super(Dev_ProjectTaskCustom, self).write(vals)
        if 'user_ids' in vals and self.stage_id.name.lower() in task_type_validation:
                users_to_notifi = self.env['res.users'].search([('id','=', 48)])
                self.enviar_notificacion_a_usuario(users_to_notifi, "La tarea <strong style='font-size:16px'>{}</strong> fue asignada a:  <strong style='font-size:16px'>{}</strong><div title='Cambiado' role='img' class='o_Message_trackingValueSeparator o_Message_trackingValueItem fa fa-long-arrow-right'></div><strong style='font-size:16px'>{}</strong>".format(rec.name, "".join(f" {user.name}," for user in old_users.user_ids),"".join(f" {user.name}," for user in self.user_ids)) , self, f"Tarea {self.name} Re Asignacion")
        return result

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

        user.partner_id.message_post(body=mensaje_con_enlace, partner_ids=user.partner_id.ids, subject=subj)
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self._context.get('search_by_id'):
            # Agregar lógica para buscar por ID
            args += [('id', '=', self._context.get('search', False))]

        return super(Dev_ProjectTaskCustom, self).search(args, offset=offset, limit=limit, order=order, count=count)