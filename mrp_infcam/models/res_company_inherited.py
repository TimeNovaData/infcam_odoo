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
        Classe Res Company herda da classe da OCA e customiza de acordo com as necessidades da Infcam.
    """
    _name = 'res.company'
    _inherit = ['res.company']

    sms_credencial = fields.Char(
        string='Credencial SMS',
        help='Credencial para envio de SMS',
        track_visibility='onchange')

    sms_token = fields.Char(
        string='Token SMS',
        help='Token para envio de SMS',
        track_visibility='onchange')

    def enviar_sms(self, telefone, mensagem, context=None):
        import requests

        payload = {
            'Credencial': self.sms_credencial,
            'Token': self.sms_token,
            'Principal_User': 'FF',
            'Aux_User': 'F1',
            'Mobile': telefone,
            'Send_Project': 'N',
            'Message': mensagem
        }

        r = requests.get("http://www.pw-api.com/sms/v_3_00/smspush/enviasms.aspx", params=payload)

        print(r)
