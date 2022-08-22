
from odoo import api, fields, models

class SprintStageTemplate(models.Model):
    _name = "project.sprint.stage"
    _order = 'sequence,id'
    _description = 'Etapa del sprint'


class ProjectSprintType(models.Model):
    _name = 'project.sprint.type'
    _description = 'Sprint Stage'
    _order = 'sequence, name, id'

    sequence = fields.Integer(string='Sequence', default=1)
    name = fields.Char(string="Nombre de la Etapa")

    def _get_default_project_ids(self):
        default_project_id = self.env.context.get('default_project_id')
        return [default_project_id] if default_project_id else None

    project_ids = fields.Many2many('project.project', 'project_sprint_type_rel', 'type_id', 'project_id', string='Projects',
        default=_get_default_project_ids)
    description = fields.Text(translate=True)
    fold = fields.Boolean(string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    auto_validation_kanban_state = fields.Boolean('Automatic kanban status', default=False,
        help="Automatically modify the kanban state when the customer replies to the feedback for this stage.\n"
            " * A good feedback from the customer will update the kanban state to 'ready for the new stage' (green bullet).\n"
            " * A medium or a bad feedback will set the kanban state to 'blocked' (red bullet).\n")

    def unlink(self):
        stages = self
        default_project_id = self.env.context.get('default_project_id')
        if default_project_id:
            shared_stages = self.filtered(lambda x: len(x.project_ids) > 1 and default_project_id in x.project_ids.ids)
            tasks = self.env['project.sprint'].with_context(active_test=False).search([('project_id', '=', default_project_id), ('stage_id', 'in', self.ids)])
            if shared_stages and not tasks:
                shared_stages.write({'project_ids': [(3, default_project_id)]})
                stages = self.filtered(lambda x: x not in shared_stages)
        return super(ProjectSprintType, stages).unlink()

