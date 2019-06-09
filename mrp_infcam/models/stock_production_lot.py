# -*- coding: utf-8 -*-
from odoo import models, fields, api

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2019, Edson Junior"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"


class StockProductionLot(models.Model):
    """
        Classe MRP Repair herda da classe da OCA e customiza de acordo com as necessidades da Infcam.
    """
    _name = 'stock.production.lot'
    _inherit = ['stock.production.lot']

    cliente = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        help='Cliente',
        track_visibility='onchange')
