from odoo import api, models,fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'    
    
    #INTERCEPTAR EL GUARDADO DE LA LINEA PARA REMOVER EL PRODUCTO AL PRINCIPIO DEL NOMBRE COMO EN ODOO 17
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_id = vals.get('product_id')
            name = vals.get('name')

            if not product_id or not name:
                continue

            product = self.env['product.product'].browse(product_id)

            if not product.exists() or not product.name:
                continue

            product_name = product.name

            if name.startswith(product_name):
                vals['name'] = name[len(product_name):].lstrip(' \n\r\t')

        return super().create(vals_list)


    def get_print_name(self):
        self.ensure_one()

        if not self.product_id:
            return self.name

        if not self.name:
            return self.product_id.name

        product_names = {
            self.product_id.name,
            self.product_id.display_name,
        }

        for product_name in product_names:
            if self.name == product_name:
                return self.name

            if self.name.startswith(product_name):
                return self.name[len(product_name):].lstrip()

        return self.name