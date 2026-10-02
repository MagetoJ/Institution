from odoo import api, fields, models


class SchoolStudent(models.Model):
    _inherit = 'school.student'

    discount_percent = fields.Float(
        string='Discount %', help='Scholarship or bursary, applied to every fee line.')
    addon_product_ids = fields.Many2many(
        'product.product', 'school_student_addon_rel',
        'student_id', 'product_id', string='Add-ons',
        domain=[('type', '=', 'service')])
    billing_partner_id = fields.Many2one(
        'res.partner', compute='_compute_billing_partner',
        string='Billed To')
    fee_invoice_ids = fields.One2many('account.move', 'student_id')
    fee_currency_id = fields.Many2one(
        'res.currency', compute='_compute_fee_currency')
    fee_balance = fields.Monetary(
        compute='_compute_fee_balance', currency_field='fee_currency_id')

    @api.depends('guardian_ids', 'partner_id')
    def _compute_billing_partner(self):
        for rec in self:
            rec.billing_partner_id = rec.guardian_ids[:1] or rec.partner_id

    def _compute_fee_currency(self):
        for rec in self:
            rec.fee_currency_id = self.env.company.currency_id

    @api.depends('fee_invoice_ids.amount_residual_signed',
                 'fee_invoice_ids.state')
    def _compute_fee_balance(self):
        for rec in self:
            moves = rec.fee_invoice_ids.filtered(
                lambda m: m.state == 'posted'
                and m.move_type in ('out_invoice', 'out_refund'))
            rec.fee_balance = sum(moves.mapped('amount_residual_signed'))

    def action_view_fee_invoices(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'school_fees.action_school_fee_invoices')
        action['domain'] = [('student_id', '=', self.id)]
        action['context'] = {
            'default_move_type': 'out_invoice',
            'default_student_id': self.id,
            'default_partner_id': self.billing_partner_id.id,
        }
        return action
