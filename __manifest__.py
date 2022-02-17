# -*- coding: utf-8 -*-
{
    'name': "Tickets FHOI",

    'summary': """
        Generar tickets para los pacientes""",

    'description': """
        Generates tickets for patiences
    """,

    'author': "Joel Rivas",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','board'],

    # always loaded
    'data': [
        'security/tickets_fhoi_security.xml',
        'security/ir.model.access.csv',
        'views/admin_view.xml',
        'views/ticket_view.xml',
        'views/agent_view.xml',
        'views/doctor_view.xml',
        'views/screen_view.xml',
        'views/dashboard_view.xml',
        'report/ticket_template.xml',
        'report/tickets_fhoi_report.xml',
        'automation/cron_job.xml'
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'assets': {
        'web.assets_backend': [
            'tickets_fhoi/static/src/css/styles.css',
        ]
    },
    'license': 'LGPL-3',
}
