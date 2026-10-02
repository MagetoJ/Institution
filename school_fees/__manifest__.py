{
    'name': 'School Fees',
    'version': '18.0.1.0.0',
    'summary': 'Fee structures, term invoicing, discounts and balances',
    'depends': ['school_base', 'account', 'product'],
    'data': [
        'security/school_fees_security.xml',
        'security/ir.model.access.csv',
        'data/fee_products.xml',
        'views/school_term_views.xml',
        'views/fee_structure_views.xml',
        'views/student_views.xml',
        'wizard/invoice_wizard_views.xml',
        'views/menus.xml',
    ],
    'license': 'LGPL-3',
}
