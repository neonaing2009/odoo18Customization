from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    reference = fields.Char(string='Reference',default='New', tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", tracking=True)
    date_appointment = fields.Date(string="Date Appointment", tracking=True)
    note = fields.Text(string="Note", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals.get('reference') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)
