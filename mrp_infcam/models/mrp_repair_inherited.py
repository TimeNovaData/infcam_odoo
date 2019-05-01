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

    @api.one
    def get_mrp_repair_state(self):

        state_list = {
            'draft': 'Cotação',
            'cancel': 'Cancelado',
            'confirmed': 'Confirmado',
            'under_repair': 'Em Reparo',
            'ready': 'Pronto para Reparar',
            '2binvoiced': 'Para ser Faturado',
            'invoice_except': 'Exceção de Faturamento',
            'waiting_stock': 'Aguardando Peças',
            'waiting_withdrawal': 'Aguardando Retirada',
            'done': 'Reparado'
        }

        return "{}".format(state_list[self.state])

    @api.model
    def create(self, values):
        """Override default Odoo create function and extend."""
        # Do your custom logic here
        record = super(MrpRepair, self).create(values)

        template = self.env.ref('mrp_infcam.email_template_mudanca_responsavel')
        self.env['mail.template'].browse(template.id).send_mail(record.id)

        template2 = self.env.ref('mrp_infcam.email_template_notificacao_cliente')
        self.env['mail.template'].browse(template2.id).send_mail(record.id)

        return record

    @api.multi
    def write(self, values):
        record = super(MrpRepair, self).write(values)

        if 'responsavel' in values:
            template = self.env.ref('mrp_infcam.email_template_mudanca_responsavel')
            self.env['mail.template'].browse(template.id).send_mail(self.id)

        if 'state' in values:
            template2 = self.env.ref('mrp_infcam.email_template_notificacao_cliente')
            self.env['mail.template'].browse(template2.id).send_mail(self.id)

        return record
