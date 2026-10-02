from odoo import fields, models


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one(
        'res.partner', required=True, ondelete='restrict', auto_join=True)
    admission_no = fields.Char(string='Admission No.', copy=False)
    birth_date = fields.Date()
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    class_id = fields.Many2one('school.class', tracking=True)
    guardian_ids = fields.Many2many(
        'res.partner', 'school_student_guardian_rel',
        'student_id', 'guardian_id', string='Guardians')
    state = fields.Selection(
        [('draft', 'Applicant'), ('enrolled', 'Enrolled'),
         ('graduated', 'Graduated'), ('left', 'Left')],
        default='draft', tracking=True)
