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
                'url': self.mercado_pago_sandbox_init_point,
            }
        else:
            return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': self.mercado_pago_sandbox_init_point,
            }