# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectUpdate(http.Controller):
#     @http.route('/project_update/project_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_update/project_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_update.listing', {
#             'root': '/project_update/project_update',
#             'objects': http.request.env['project_update.project_update'].search([]),
#         })

#     @http.route('/project_update/project_update/objects/<model("project_update.project_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_update.object', {
#             'object': obj
#         })
