from odoo import models, fields

class ProjectTaskCustom(models.Model):    
    _inherit = 'project.task'

    qa_parent_id = fields.Many2one('project.task', string='Tarea QA padre', index=True)
    qa_child_ids = fields.One2many('project.task', 'qa_parent_id', string="QA-subtasks")
    test_parent_id = fields.Many2one('project.task', string='Tarea QA padre', index=True)
    test_child_ids = fields.One2many('project.task', 'test_parent_id', string="QA-testcases")
    test_state = fields.Selection([
        ('passed', 'Aprovado'),
        ('failed', 'Fallido'),
        ('blocked', 'Bloqueado'),
        ('not_run', 'No Corre')], 'Estado')
    severity = fields.Selection([
        ('high', 'Alta'),
        ('medium', 'Media'),
        ('low', 'Baja')], 'Severidad')    
    

    def action_add_existing_tasks(self):
        self.ensure_one()
        return {
            'name': 'Agregar Tareas Exist.',
            'view_mode': 'form',
            'res_model': 'project.task.wizard',  # Reemplaza 'your.model.wizard' con el nombre de tu modelo de asistente
            'type': 'ir.actions.act_window',
            'context': {
                'default_test_parent_id': self.id,
            },
            'view_id': self.env.ref('qa_subtasks_custom.view_add_existing_tasks_wizard').id,  # Reemplaza 'your_module' con el nombre de tu módulo
            'target': 'new',
        }


    def action_remove_child_task(self):
        for task in self:
            if task.test_parent_id:
                # Quitar la tarea actual de la relación con la tarea padre
                task.test_parent_id.test_child_ids -= task
                # Actualizar el campo test_parent_id de la tarea actual
                task.write({'test_parent_id': False})

    