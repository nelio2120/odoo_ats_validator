{
    'name': 'ATS Validator',
    'version': '18.0.1.0.0',
    'summary': 'Validación del Anexo Transaccional Simplificado (ATS) vía servicio externo',
    'category': 'Accounting/Accounting',
    'author': 'Custom',
    'depends': ['account', 'base_setup', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/res_config_settings_views.xml',
        'views/ats_validation_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
