from odoo import models, fields, api

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'




    u_warehouse_location = fields.Char(string='Location')


    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            #if rec.code and rec.name:
            rec.display_name = f"{rec.code} - {rec.name}"

            #else:
                #rec.display_name = f"{rec.name},{rec.id}"

    #combination = fields.Char(string='Combine', compute='_compute_display_name')

    # def name_get(self):
    #     res = []
    #
    # def _compute_display_name(self):
    #     res = []
    #     for warehouse in self:
    #         name = warehouse.code
    #         res.append((warehouse.id,name))
    #     return res


