# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.osv import expression

class ProjectTemplate(models.Model):

    _inherit = 'project.project'

    x_custom_filter = fields.Boolean(string="Fecha fin teórica &lt; Fecha fin estimada", default=False)
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if ['x_custom_filter', '=', 1] in args:
            _index = args.index(['x_custom_filter', '=', 1])
            query = '''
                SELECT id FROM project_project WHERE x_theoretical_end_date < x_estimated_end_date
            '''
            self.env.cr.execute(query)
            query_result = self.env.cr.dictfetchall()
            ids = list(data['id'] for data in query_result)
            args[_index] = ['id', 'in', ids] # expression.AND([[('id', 'in', ids)], args])
        return super(ProjectTemplate, self).search(args, offset=offset, limit=limit, order=order, count=count)

    #[['x_custom_filter', '=', 1]]
    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     if ['x_custom_filter', '=', 1] in domain:
    #         query = '''
    #             SELECT id FROM project_project WHERE x_theoretical_end_date < x_estimated_end_date
    #         '''
    #         self.env.cr.execute(query)
    #         query_result = self.env.cr.dictfetchall()
    #     return super(ProjectTemplate, self).search_read(domain, fields, offset, limit, order)
