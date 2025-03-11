from odoo import models, fields, api


class Student(models.Model):
     _name = 'student.list'
     _inherit = ['mail.thread']
     _description = 'student.list'

     name = fields.Char(string="Name", required=True)
     address = fields.Text(string="Address")
     gender = fields.Selection([('male', "Male"), ('female', "Female")], string='Gender')
     address_html = fields.Html(string="Address Html")
     location_html = fields.Html(string="Location Html")
     is_paid = fields.Boolean(string="Paid")
     product_id = fields.Many2one('product.product', string="Product", required=True)
     product_tmp_id = fields.Many2one('product.template', string="Product Template Id")
     product_default_code = fields.Char(string="Default Code", related="product_tmp_id.default_code", store=True)





#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

