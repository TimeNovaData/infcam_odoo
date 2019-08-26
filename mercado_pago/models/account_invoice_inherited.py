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

    def criar_preferencia(self, cr, mp, cliente, context=None):
        '''
        Criar uma ordem de pagamento
        :param mp:
        :param cliente:
        :param kwargs:
        :return:
        '''
        preference = {
            "items": [
                {
                    "title": "Serviço de Testes",
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": 10.01,
                    'payment_method_id': "ticket",
                }
            ],
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

        print(preference_result["response"]["sandbox_init_point"])

        return json.dumps(preference_result, indent=4)

    def gerar_checkout(self, cr, context=None):
        # mp = mercadopago.MP("7099317734495678", "2Es81E92Wxrc5ACjKXEhLwig6WnZI2J0")
        mp = mercadopago.MP("TEST-7099317734495678-081714-5aef01acc34b8678d5ce305e1e3edf77-2093730")
        # tipos = mp.get("/v1/identification_types")
        # mp.sandbox_mode(True)

        response = mp.get("/v1/customers/search", {
            "email": "edson.junior@outboxsistemas.com"
        })

        cliente = None

        if response["status"] == 200:
            if len(response['response']['results']) > 0:
                cliente = response['response']['results'][0]

        if not cliente:
            cliente = mp.post("/v1/customers", {
                "name": "Edson",
                "surname": "Junior",
                "email": "edson.junior@outboxsistemas.com",
                "identification": {
                    "type": "CPF",
                    "number": "08887138435"
                }
            })

        preferencia = self.criar_preferencia(cr, mp, cliente)

        print(preferencia)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }