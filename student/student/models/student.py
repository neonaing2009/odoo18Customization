from odoo import models, fields, api

class School(models.Model):
    _name = 'school.list'
    _description = "This is school profile."

    name = fields.Char(string="Name")
    student_list = fields.One2many('student.list','school_id',string="Student List")
    ref_field_id = fields.Reference(
        [
            ('student.list','Student'),
            ('school.list','Schools'),
            ('student.hobby','Hobby'),
            ('sale.order','Sale'),
            ('account.move','Invoice'),
            ('purchase.order','Purchase')
        ]
    )

    invoice_id = fields.Many2one('account.move')
    invoice_user_id = fields.Many2one('res.users', related='invoice_id.invoice_user_id', store=True)
    invoice_date = fields.Date(related='invoice_id.invoice_date')
    base_id = fields.Integer("Student ID")

    # def create(self, vals):
    #     print(self)
    #     print(vals)
    #     rtn = super(School, self).create(vals)
    #     print(rtn)
    #     return rtn

    #@api.model
    @api.model_create_multi
    #@api.model_create_single
    def create(self, vals):
        print(self)
        print(vals)
        rtn = super(School, self).create(vals)
        print(rtn)
        return rtn

class Student(models.Model):
     _name = 'student.list'
     _inherit = ['mail.thread']
     _description = 'student.list'

     name = fields.Char(string="Name", required=True)
     address = fields.Text(string="Address")

     hobby_list = fields.Many2many('student.hobby','student_hobby_listrelation','student_id','hobby_id')
     school_id = fields.Many2one('school.list',string='School Name')
     gender = fields.Selection([('male', "Male"), ('female', "Female")], string='Gender')
     address_html = fields.Html(string="Address Html")
     location_html = fields.Html(string="Location Html")
     is_paid = fields.Boolean(string="Paid")
     product_id = fields.Many2one('product.product', string="Product", domain="[('default_code','!=','')]",required=True)
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

     ######Create New School Copy to Create###
     s_name = fields.Char(string="School NewName")
     s_student_list = fields.One2many('student.list', 'school_id', string="School Student List")
     s_ref_field_id =fields.Reference(
         [
             ('student.list', 'Student'),
             ('school.list', 'Schools'),
             ('student.hobby', 'Hobby'),
             ('sale.order', 'Sale'),
             ('account.move', 'Invoice'),
             ('purchase.order', 'Purchase')
         ]
     )

     s_invoice_id = fields.Many2one('account.move')
     #s_iv_id = fields.Many2one(related='s_invoice_id.id')
     s_invoice_user_id = fields.Many2one('res.users', related='s_invoice_id.invoice_user_id', store=True)
     s_invoice_date = fields.Date(related='s_invoice_id.invoice_date')

     ######End ####


     @api.depends('product_tmp_id.list_price')
     def _compute_price(self):
         for rec in self:
             rec.otherprice = rec.product_tmp_id.list_price

     def _compute_dummy(self):
         pass

     def json_data_store(self):
         self.student_data =[{"name":self.name,
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
                             }]

     def check_reference(self):

       for record in self:
           model_name, record_id = record.s_ref_field_id.split(',')
           referenced_record = self.env[model_name].browse(int(record_id))
           records = referenced_record
           return  records



     def custom_method(self):
         print("Hello Click")
         s_id = self.s_student_list.id
         s_ref_o = self.s_ref_field_id._name #Model Name
         s_ref = self.s_ref_field_id.id
         ref_val = f"{s_ref_o},{s_ref}"



         #print(s_ref_o)
         data = {"name":self.s_name,
                 "ref_field_id": ref_val,
                 "student_list": s_id,
                 "invoice_id": self.s_invoice_id.id,
                 "invoice_user_id": self.s_invoice_user_id.id,
                 "invoice_date": self.s_invoice_date,
                 "base_id": self.id
                 }
         print(data)
         self.env['school.list'].create(data)

         # select * from student where shcool_id = 1;
         # search_read(
         #     domain,
         #     fields[id, name, student_id],
         #     offset=101,
         #     limit=100,
         #     order="",
         #     load=None
         # )

         # sale_obj = self.env['sale.order.line']
         # total_sales_based_on_state = sale_obj.read_group([("order_id.state","=","sale")],
         #                                                  ["product_id","product_uom_qty:avg"],
         #                                                  ["product_id"])
         # for sale in total_sales_based_on_state:
         #     print(sale)
         # sales_obj = self.env['sale.order']
         # total_sales_based_on_state = sales_obj.read_group([("state","=","sale")],
         #                                                   ["partner_id","amount_total:sum"],
         #                                                   ["partner_id"])
         # for sale in total_sales_based_on_state:
         #     print(sale)

         # total_sales_based_on_partner = sales_obj.read_group([("state","=","sales")],
         #                                                     ["user_id","id:count"],
         #                                                     ["user_id"])
         # for partner in total_sales_based_on_partner:
         #     print(partner)

         #select * from student where student_id =1
         #search_read(
         #     domain,
         #     fields [id, name, student_id]
         #    offset=101,
         #    limit=100,
         #    order="",
         #    load=None
         # )
         #stud_obj = self.env["student.list"]
         #stud_list = stud_obj.search_read([],["id","name","gender"])
         #print(stud_list)
         #print(self.read())
         #print(self.env['student.list'].read())
         #total_records = self.env['student.list'].search_count([('id','>',10)])
         #print(total_records)
         #print(self.search([], limit=5, offset=0))
         #print(self.search([])) #Current Model Search
         #print(self.env["student.list"].search([])) #custom model or difference model
         #print(self.search([], order="name"))
         #self.json_data_store()
         #records = self.search([("amount","=",3000)])
         #self.print_table(records)
         #in operator
         #=("a","b","c","d")
         #records = self.search([("name","in",("Wah","wah","Khine"))])
         #self.print_table(records)
         # search(domain, limit, offset, order)
         #[condition, more conditions]

     def create(self, vals):
         print(self)
         print(vals)
         rtn = super(Student, self).create(vals)
         print(rtn)
         return rtn


     def duplicate_records(self):
         duplicate_record = self.copy()

     def copy(self, default=None):
        rtn = super(Student, self).copy(default=default)
        return rtn

     def print_table(self, records):
         print(f"Total Records Found :- {len(records)}")
         print("ID      Name        Amount")
         for rec in records:
             print(f"{rec.id}       {rec.name}      {rec.amount}")
         print("")
         print("")
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Hobby(models.Model):
    _name = "student.hobby"
    _description = "This is student hobbies."

    name = fields.Char("Name")