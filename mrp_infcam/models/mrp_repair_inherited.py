# -*- coding: utf-8 -*-
from odoo import models, fields, api

"""
Módulo de Tarefas Recorrentes para as Tarefas padrões do módulo de Projetos.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2019, Edson Junior"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"


class MrpRepair(models.Model):
    """
        Classe MRP Repair herda da classe da OCA e customiza de acordo com as necessidades da Infcam.
    """
    _name = 'mrp.repair'
    _inherit = ['mrp.repair']

    state = fields.Selection(
        string="Status",
        selection=[
            ('draft', 'Cotação'),
            ('cancel', 'Cancelado'),
            ('confirmed', 'Confirmado'),
            ('under_repair', 'Em Reparo'),
            ('ready', 'Pronto para Reparar'),
            ('2binvoiced', 'Para ser Faturado'),
            ('invoice_except', 'Exceção de Faturamento'),
            ('waiting_stock', 'Aguardando Peças'),
            ('waiting_withdrawal', 'Aguardando Retirada'),
            ('done', 'Reparado')
        ],
        required=True,
        readonly=False,
        track_visibility="onchange"
    )

    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsavel',
        help='Responsável pelo suporte',
        track_visibility='onchange')