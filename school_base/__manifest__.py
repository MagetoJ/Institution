{
    'name': 'School Base',
    'version': '18.0.1.0.0',
    'summary': 'Students, classes, academic years',
    'category': 'Education',
    'depends': ['base', 'contacts', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}