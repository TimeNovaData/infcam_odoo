# -*- coding: utf-8 -*-
{
    'name': "infcam-mrp",

    'summary': """
        Customizações do módulo de MRP para a Infcam""",

    'description': """
        Módulo para as customizações no módulo de MRP da Infcam.
    """,

    'author': "Outbox Sistemas",
    'website': "http://www.outboxsistemas.com",
    'category': '',
    'version': '1.0',
    'depends': ['base', 'mrp_repair', 'mail', 'contacts'],
    'data': [
        'views/mrp_repair_kanban.xml',
        'views/mrp_repair_form.xml',
        'views/email_template_mudanca_responsavel.xml',
        'views/email_template_notificacao_cliente.xml'
    ],
}