from odoo import models, fields, api


class Student(models.Model):
     _name = 'student.list'
     _description = 'student.list'

     name = fields.Char(string="Name", require=True)
     address = fields.Char(string="Address")

#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

