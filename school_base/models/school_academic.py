from odoo import fields, models


class SchoolAcademicYear(models.Model):
    _name = 'school.academic.year'
    _description = 'Academic Year'
    _order = 'date_start desc'

    name = fields.Char(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    active = fields.Boolean(default=True)


class SchoolGrade(models.Model):
    _name = 'school.grade'
    _description = 'Grade / Level'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class / Section'

    name = fields.Char(required=True)
    grade_id = fields.Many2one('school.grade', required=True)
    academic_year_id = fields.Many2one('school.academic.year', required=True)
    teacher_id = fields.Many2one('res.partner', string='Class Teacher')
    student_ids = fields.One2many('school.student', 'class_id')
