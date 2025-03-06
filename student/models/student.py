# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Student(models.Model):
    _name = 'wb.student'
    _description = 'Student'

    #id = fields.Char(string='id')
    name = fields.Char(string='name')
    address = fields.Char(string='Address')

