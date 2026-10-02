from odoo import Command, fields, models
from odoo.exceptions import UserError


class SchoolFeeInvoiceWizard(models.TransientModel):
    _name = 'school.fee.invoice.wizard'
    _description = 'Generate Fee Invoices'

    term_id = fields.Many2one('school.term', required=True)
    class_ids = fields.Many2many(
        'school.class', string='Classes',
        help='Leave empty to invoice every class.')
    invoice_date = fields.Date(
        required=True, default=fields.Date.context_today)
    due_date = fields.Date()

    def action_generate(self):
        self.ensure_one()
        domain = [('state', '=', 'enrolled')]
        if self.class_ids:
            domain.append(('class_id', 'in', self.class_ids.ids))
        else:
            domain.append(('class_id', '!=', False))
        students = self.env['school.student'].search(domain)
        if not students:
            raise UserError(
                "No enrolled students found. Students must have a class "
                "and the status 'Enrolled' to be invoiced.")

        Structure = self.env['school.fee.structure']
        Move = self.env['account.move']
        created = Move
        no_structure = set()
        already_billed = 0

        for student in students:
            grade = student.class_id.grade_id
            structure = Structure.search([
                ('grade_id', '=', grade.id),
                ('term_id', '=', self.term_id.id)], limit=1)
            if not structure:
                no_structure.add(grade.name)
                continue
            if Move.search_count([
                    ('student_id', '=', student.id),
                    ('school_term_id', '=', self.term_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('state', '!=', 'cancel')]):
                already_billed += 1
                continue
            lines = []
            for line in structure.line_ids:
                if line.is_addon and line.product_id not in student.addon_product_ids:
                    continue
                lines.append(Command.create({
                    'product_id': line.product_id.id,
                    'name': line.name or line.product_id.name,
                    'quantity': 1,
                    'price_unit': line.amount,
                    'discount': student.discount_percent,
                }))
            if not lines:
                continue
            created |= Move.create({
                'move_type': 'out_invoice',
                'partner_id': student.billing_partner_id.id,
                'student_id': student.id,
                'school_term_id': self.term_id.id,
                'invoice_date': self.invoice_date,
                'invoice_date_due': self.due_date or self.invoice_date,
                'ref': '%s - %s' % (student.admission_no or student.name,
                                    self.term_id.name),
                'invoice_line_ids': lines,
            })

        if not created:
            msg = "No invoices were created."
            if no_structure:
                msg += " No fee structure for: %s." % ", ".join(sorted(no_structure))
            if already_billed:
                msg += " %s student(s) already have an invoice for this term." % already_billed
            raise UserError(msg)

        action = self.env['ir.actions.act_window']._for_xml_id(
            'school_fees.action_school_fee_invoices')
        action['domain'] = [('id', 'in', created.ids)]
        return action
