from odoo import fields, models


class SchoolTerm(models.Model):
    _name = 'school.term'
    _description = 'Academic Term'
    _order = 'academic_year_id desc, sequence, date_start'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    academic_year_id = fields.Many2one('school.academic.year', required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
