# -*- coding: utf-8 -*-
{
    'name': "infcam-sale",

    'summary': """
        Customizações do módulo de Sale para a Infcam""",

    'description': """
        Módulo para as customizações no módulo de Sale da Infcam.
    """,

    'author': "Outbox Sistemas",
    'website': "http://www.outboxsistemas.com",
    'category': '',
    'version': '1.0',
    'depends': ['base', 'sale_management', 'mail', 'contacts'],
    'data': [
        'views/report_saleorder_document.xml'
    ],
}