# -*- coding: utf-8 -*-
from odoo import models, fields, api

"""
Módulo que herda os parceiros para customizações da Infcam.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2019, Edson Junior"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"


class ResPartner(models.Model):
    """
        Classe CRM Lead herda dos leads do CRM e customiza de acordo com as necessidades da Infcam.
    """
    _name = 'res.partner'
    _inherit = ['res.partner']

    def abrir_whatsapp(self, cr, context=None):
        url = 'https://api.whatsapp.com/send?phone=55{}&text=Ol%C3%A1!%20Tudo%20bem%3F'.format(self.mobile)
        res = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }

        return res
