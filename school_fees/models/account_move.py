from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    student_id = fields.Many2one(
        'school.student', index=True, copy=False, ondelete='set null')
    school_term_id = fields.Many2one('school.term', copy=False)
