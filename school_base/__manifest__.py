{
    'name': 'School Base',
    'version': '18.0.1.0.0',
    'summary': 'Students, classes, academic years',
    'depends': ['base', 'contacts', 'mail', 'hr', 'account'],
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'views/school_views.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
