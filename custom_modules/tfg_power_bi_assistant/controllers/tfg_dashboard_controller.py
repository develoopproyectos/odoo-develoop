from odoo import http
from odoo.http import request


class TfgDashboardController(http.Controller):
    @http.route('/show_tfg_dashboard', type='http', auth='user', website=False)
    def show_qweb(self):
        return request.render('tfg_power_bi_assistant.tfg_dashboard_template', {})