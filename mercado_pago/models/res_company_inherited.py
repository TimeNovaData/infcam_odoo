# -*- coding: utf-8 -*-
from odoo import models, fields, api

"""
Herda o módulo res company para customização de funcionalidades.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2019, Edson Junior"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"


class ResCompany(models.Model):
    """
        Classe Res Company herda da classe da OCA e customiza para integrar com o Mercado Pago.
    """
    _name = 'res.company'
    _inherit = ['res.company']

    mercado_pago_public_key = fields.Char(
        string='Mercado Pago - Public Key',
        track_visibility='onchange')

    mercado_pago_access_token = fields.Char(
        string='Mercado Pago - Access Token',
        track_visibility='onchange')

    mercado_pago_client_id = fields.Char(
        string='Mercado Pago - Client ID',
        track_visibility='onchange')

    mercado_pago_client_secret = fields.Char(
        string='Mercado Pago - Client Secret',
        track_visibility='onchange')
