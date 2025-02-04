from odoo import api, fields, models



class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_names_search = ['reference','patient_id']
    _rec_name = 'patient_id'

    reference = fields.Char(string='Reference',default='New', tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient Name", tracking=True, required=False, ondelete='restrict')#restrict without delete or set null delete with patient without appointment #cascade with appointment
    partner_id = fields.Many2one('res.partner', string="Sales Partner Name", tracking=True)
    date_appointment = fields.Date(string="Date Appointment", tracking=True)
    note = fields.Text(string="Note", tracking=True)
    state = fields.Selection([
        ('draft','Draft'),('confirmed','Confirmed'),('ongoing','Ongoing'),
        ('done','Done'),('cancel','Cancelled')
    ], default='draft', tracking=True)
    appointment_line_ids = fields.One2many('hospital.appointment.line','appointment_id', string="Lines")
    total_qty = fields.Float(compute='_compute_total_qty',string="Total Quantity", store=True)
    total_amount = fields.Float(compute='_compute_total_amount',string="Total Amount", store=True)
    total_tax_amount = fields.Float(compute='_compute_total_tax',string="Tax Amount", store=True)
    #line_total_amount = fields.Float(compute='_compute_line_total_amount',string="Total Amount", store=True)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals.get('reference') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
            #total_qty = 0
            #for line in rec.appointment_line_ids:
                #total_qty += line.qty
            #rec.total_qty = total_qty
            rec.total_qty = sum(rec.appointment_line_ids.mapped('qty'))

    @api.depends('appointment_line_ids')
    def _compute_total_amount(self):
        for rec in self:
            total_amount = 0
            for line in rec.appointment_line_ids:
                total_amount += (line.line_total_amount *(line.tax/100) ) + line.line_total_amount
            rec.total_amount = total_amount

    @api.depends('appointment_line_ids')
    def _compute_total_tax(self):
        for rec in self:
            total_tax_amt = 0
            for line in rec.appointment_line_ids:
                total_tax_amt += (line.line_total_amount * (line.tax/100))
            rec.total_tax_amount = total_tax_amt


    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}]{rec.patient_id.name}"

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    qty = fields.Float(string="Quantity")
    price = fields.Float(string="Price")
    discount = fields.Float(string="Disc %")
    line_total_amount = fields.Float(compute='_compute_line_total',string="Line Total Amount", store=True)
    tax = fields.Float(string="Tax")

    @api.depends('qty','price','discount')
    def _compute_line_total(self):
        for rec in self:
            line_total = 0
            line_total = (rec.qty * rec.price) *(1-(rec.discount/100))
            rec.line_total_amount = line_total
    
