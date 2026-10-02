from odoo import api, fields, models


class SchoolFeeStructure(models.Model):
    _name = 'school.fee.structure'
    _description = 'Fee Structure'

    name = fields.Char(required=True)
    grade_id = fields.Many2one('school.grade', required=True)
    term_id = fields.Many2one('school.term', required=True)
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id')
    line_ids = fields.One2many('school.fee.structure.line', 'structure_id')
    total_amount = fields.Monetary(
        string='Compulsory Total', compute='_compute_total')

    _sql_constraints = [
        ('grade_term_uniq', 'unique(grade_id, term_id)',
         'There is already a fee structure for this grade and term.'),
    ]

    @api.depends('line_ids.amount', 'line_ids.is_addon')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(
                rec.line_ids.filtered(lambda l: not l.is_addon).mapped('amount'))


class SchoolFeeStructureLine(models.Model):
    _name = 'school.fee.structure.line'
    _description = 'Fee Structure Line'
    _order = 'sequence, id'

    structure_id = fields.Many2one(
        'school.fee.structure', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    product_id = fields.Many2one(
        'product.product', string='Fee Item', required=True,
        domain=[('type', '=', 'service')])
    name = fields.Char(string='Description')
    amount = fields.Monetary(required=True)
    is_addon = fields.Boolean(
        string='Add-on',
        help='Only charged to students who have this item ticked as an add-on.')
    currency_id = fields.Many2one(
        'res.currency', related='structure_id.currency_id')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            if not self.amount:
                self.amount = self.product_id.list_price
