# -*- coding: utf-8 -*-
from odoo import models, fields, api
import mercadopago
import json

"""
Herda o módulo account invoice para customização de funcionalidades.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2019, Edson Junior"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"


class AccountInvoice(models.Model):
    """
        Classe Account Invoice herda da classe da OCA e customiza para integrar com o Mercado Pago.
    """
    _name = 'account.invoice'
    _inherit = ['account.invoice']

    mercado_pago_init_point = fields.Char(
        string='Init Point',
        track_visibility='onchange')

    mercado_pago_sandbox_init_point = fields.Char(
        string='Sandbox Init Point',
        track_visibility='onchange')

    mercado_pago_id_preferencia = fields.Char(
        string='ID Preferência',
        track_visibility='onchange')

    mercado_pago_status = fields.Selection(
        string='Status no Mercado Pago',
        track_visibility='onchange',
        selection=[('APRO', 'Pagamento aprovado'),
                   ('CONT', 'Pagamento pendente'),
                   ('OTHE', 'Recusado por erro geral'),
                   ('CALL', 'Recusado com validação para autorizar'),
                   ('FUND', 'Recusado por quantia insuficiente'),
                   ('SECU', 'Recusado por código de segurança inválido'),
                   ('EXPI', 'Recusado por problema com a data de vencimento'),
                   ('FORM', 'Recusado por erro no formulário'),
        ]
    )

    def criar_preferencia(self, cr, mp, cliente, context=None):
        '''
        Criar uma ordem de pagamento
        :param mp:
        :param cliente:
        :param kwargs:
        :return:
        '''
        itens_fatura = []

        for item in self.invoice_line_ids:
            linha_fatura = {
                "title": item.name,
                "quantity": item.quantity,
                "currency_id": "BRL",
                "unit_price": item.price_unit,
                'payment_method_id': "ticket",
            }

            itens_fatura.append(linha_fatura)

        preference = {
            "items": itens_fatura,
            "payer": cliente,
            "external_reference": "{}".format(self.id)
        }

        preference_result = mp.create_preference(preference)

        return preference_result

    def gerar_checkout(self, cr, context=None):
        if not self.mercado_pago_id_preferencia:
            mp = mercadopago.MP(self.company_id.mercado_pago_access_token)

            response = mp.get("/v1/customers/search", {
                "email": self.partner_id.email
            })

            cliente = None

            if response["status"] == 200:
                if len(response['response']['results']) > 0:
                    cliente = response['response']['results'][0]

            if not cliente:
                if self.partner_id.company_type == 'person':
                    type = "CPF"
                else:
                    type = "CNPJ"

                cliente = mp.post("/v1/customers", {
                    "name": self.partner_id.name,
                    "email": self.partner_id.email,
                    "identification": {
                        "type": type,
                        "number": self.partner_id.vat
                    }
                })

            preferencia = self.criar_preferencia(cr, mp, cliente)

            if preferencia['status'] == 201:
                self.write({
                    'mercado_pago_init_point': preferencia['response']['init_point'],
                    'mercado_pago_sandbox_init_point': preferencia['response']['sandbox_init_point'],
                    'mercado_pago_id_preferencia': preferencia['response']['id']
                })

            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.mercado_pago_init_point,
            }
        else:
            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.mercado_pago_init_point,
            }

    def criar_preferencia_boleto(self, cr, mp, cliente, context=None):
        '''
        Criar uma ordem de pagamento
        :param mp:
        :param cliente:
        :param kwargs:
        :return:
        '''
        itens_fatura = []

        for item in self.invoice_line_ids:
            linha_fatura = {
                "title": item.name,
                "quantity": item.quantity,
                "currency_id": "BRL",
                "unit_price": item.price_unit,
                'payment_method_id': "ticket",
            }

            itens_fatura.append(linha_fatura)

        preference = {
            "items": itens_fatura,
            "payer": cliente,
            "payment_methods": {
                "excluded_payment_methods": [
                    {
                        "id": "master"
                    }
                ],
                "excluded_payment_types": [
                    {
                        "id": "credit_card"
                    }
                ],
                "installments": 12,
                "default_payment_method_id": None,
                "default_installments": None
            },
            "external_reference": "{}".format(self.id)
        }

        preference_result = mp.create_preference(preference)

        return preference_result

    def gerar_checkout_boleto(self, cr, context=None):
        if not self.mercado_pago_id_preferencia:
            mp = mercadopago.MP(self.company_id.mercado_pago_access_token)

            response = mp.get("/v1/customers/search", {
                "email": self.partner_id.email
            })

            cliente = None

            if response["status"] == 200:
                if len(response['response']['results']) > 0:
                    cliente = response['response']['results'][0]

            if not cliente:
                if self.partner_id.company_type == 'person':
                    type = "CPF"
                else:
                    type = "CNPJ"

                cliente = mp.post("/v1/customers", {
                    "name": self.partner_id.name,
                    "email": self.partner_id.email,
                    "identification": {
                        "type": type,
                        "number": self.partner_id.vat
                    }
                })

            preferencia = self.criar_preferencia_boleto(cr, mp, cliente)

            if preferencia['status'] == 201:
                self.write({
                    'mercado_pago_init_point': preferencia['response']['init_point'],
                    'mercado_pago_sandbox_init_point': preferencia['response']['sandbox_init_point'],
                    'mercado_pago_id_preferencia': preferencia['response']['id']
                })

            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.mercado_pago_init_point,
            }
        else:
            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.mercado_pago_init_point,
            }

    def consultar_pagamento(self, context=None):
        if self.mercado_pago_id_preferencia:

            mp = mercadopago.MP(self.company_id.mercado_pago_access_token)

            response = mp.get("/v1/payments/search", {
                "external_reference": "{}".format(self.id)
            })

            if response['status'] == 200:
                for pagamento in response['response']['results']:
                    self.registrar_pagamento(pagamento)
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def registrar_pagamento(self, pagamento):
        if pagamento['status'] == 'approved':
            valores = {
                'invoice_ids': [[4, self.id, 'None']],
                'default_invoice_ids': [[4, self.id, 'None']],
                'amount': pagamento['transaction_amount'],
                'journal_id': 10,
                'payment_date': pagamento['date_approved'],
                'partner_id': self.partner_id.id,
                'payment_method_id': 3,
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'has_invoices': True,
            }

            pagamento = self.env['account.payment'].create(valores)

            pagamento.action_validate_invoice_payment()

            return pagamento

    @api.multi
    def consultar_pagamento_cron(self, context=None):
        """
        Função para buscar pagamentos no mercado pago.
        Função a ser executada de hora em hora com o intuido de verificar novos pagamentos efetuados no mercado pago e
        efetuar a baixa da fatura correspondente.
        :param context: Contexto da aplicação. Default None
        :return: Null
        """
        faturas_pendentes = self.env['account.invoice'].search([
            ('state', '=', 'open'),
            ('mercado_pago_id_preferencia', '!=', False)
        ])

        for fatura in faturas_pendentes:
            fatura.consultar_pagamento()
