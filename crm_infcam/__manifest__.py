# -*- coding: utf-8 -*-
{
    'name': "infcam-crm",

    'summary': """
        Customizações do módulo de CRM para a Infcam""",

    'description': """
        Módulo para as customizações no módulo de CRM da Infcam.
    """,

    'author': "Outbox Sistemas",
    'website': "http://www.outboxsistemas.com",
    'category': '',
    'version': '1.0',
    'depends': ['base', 'crm', 'stock', 'mrp_repair', 'mail', 'contacts'],
    'data': [
        'views/crm_lead_form.xml',
        #'views/report_nota_devolucao.xml',
    ],
}