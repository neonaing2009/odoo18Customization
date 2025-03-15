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
     product_default_code = fields.Char(string="Refer", related='product_id.default_code')
     #price = fields.Float(string="Sale Price", related='product_tmp_id.list_price', readonly=False, store=True,)
     price = fields.Float(string="Origin Price", related='product_tmp_id.list_price', store=True)
     otherprice = fields.Float(string="Sale Price", compute='_compute_price',readonly=False, store=True)
     default_code = fields.Char(string="DCode", related='product_tmp_id.default_code')
     ref_field_id = fields.Reference([('sale.order','Sale'),
                                ('account.move','Invoice'),
                                ('purchase.order','Purchase'),
                                ('product.template','Product Template'),
                                ('product.product','Product Information')])

     binary_field = fields.Binary('Binary Field')
     binary_field_name = fields.Char('Binary Field Name')
     binary_field_many = fields.Many2many('ir.attachment', string='Muti Files')
     my_currency_id = fields.Many2one('res.currency', string='(My Currency)')
     #currency_id = fields.Many2one('res.currency', string='Currency')
     amount = fields.Monetary(string='Amount', currency_field='my_currency_id')

     student_image = fields.Image(string='Student Image', max_width=128, max_height=128)


     @api.depends('product_tmp_id.list_price')
     def _compute_price(self):
         for rec in self:
             rec.otherprice = rec.product_tmp_id.list_price

     def _compute_dummy(self):
         pass

     def json_data_store(self):
         self.student_data ={"name":self.name,
                             "address":self.address,
                             "gender":self.gender,
                             "address_html":self.address_html,
                             "location_html":self.location_html,
                             "is_paid":self.is_paid,
                             "product_id":self.product_id,
                             "prices":self.price,
                             "otherprice":self.otherprice,
                             "ref_field_id":self.ref_field_id,
                             "binary_field":self.binary_field,
                             "binary_field_name":self.binary_field_name,
                             "my_currency_id":self.my_currency_id,
                             "amount":self.amount,
                             "student_image":self.student_image
                             }
     def custom_method(self):
         print(self.json_data_store())

#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

