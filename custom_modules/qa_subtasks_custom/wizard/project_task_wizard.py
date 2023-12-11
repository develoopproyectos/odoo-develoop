from odoo import fields, models, api

class YourModelWizard(models.TransientModel):
    _name = 'project.task.wizard' 
    task_ids = fields.Many2many('project.task', string='Tareas Exist.')

   
    def action_add_existing_tasks(self):
        # Realiza las acciones necesarias para asociar las tareas existentes a la tarea actual
        self.ensure_one()
        # Código para asociar tareas, por ejemplo:
        self.env['project.task'].browse(self._context.get('default_test_parent_id')).write({
            'test_child_ids': [(4, task.id) for task in self.task_ids],
        })
        return {'type': 'ir.actions.act_window_close'}
