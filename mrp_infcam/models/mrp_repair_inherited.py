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
            ('novo', 'Novo/Aguardando Avaliação do Técnico'),
            ('analise', 'Em Análise'),
            ('draft', 'Orçamento Pronto'),
            ('aguardando_aprovacao', 'Aguardando Aprovação'),
            ('cancel', 'Cancelado/Não Aprovado'),
            ('confirmed', 'Aprovado'),
            ('aguardando_retorno', 'Avisado Aguardando Retorno'),
            ('condenado', 'Sem Reparo/Condenado'),
            ('under_repair', 'Em Reparo'),
            ('waiting_stock', 'Aguardando Peças'),
            ('waiting_withdrawal', 'Pronto/Aguardando Retirada'),
            ('done', 'Reparado/Entregue'),
            ('devolvido', 'Devolvido/Sem Reparo'),
            ('montar_devolver', 'Montar P/ Devolver'),
            ('descartado', 'Equipamento Descartado'),
            ('garantia', 'Em Garantia'),
            ('contato_sem_sucesso', 'Tentativa de Contato S/ Sucesso'),
            ('2binvoiced', 'Para ser Faturado'),
            ('invoice_except', 'Exceção de Faturamento')
        ],
        required=True,
        readonly=False,
        track_visibility="onchange"
    )

    lot_id = fields.Many2one(
        domain="[('cliente', '=', partner_id)]"
    )

    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsavel',
        help='Responsável pelo suporte',
        track_visibility='onchange')

    @api.one
    def get_mrp_repair_state(self):

        state_list = {
            'novo': 'Novo/Aguardando Avaliação do Técnico',
            'analise': 'Em Análise',
            'draft': 'Orçamento Pronto',
            'aguardando_aprovacao': 'Aguardando Aprovação',
            'cancel': 'Cancelado/Não Aprovado',
            'confirmed': 'Aprovado',
            'aguardando_retorno': 'Avisado Aguardando Retorno',
            'condenado': 'Sem Reparo/Condenado',
            'under_repair': 'Em Reparo',
            'waiting_stock': 'Aguardando Peças',
            'waiting_withdrawal': 'Pronto/Aguardando Retirada',
            'done': 'Reparado/Entregue',
            'devolvido': 'Devolvido/Sem Reparo',
            'montar_devolver': 'Montar P/ Devolver',
            'descartado': 'Equipamento Descartado',
            'garantia': 'Em Garantia',
            'contato_sem_sucesso': 'Tentativa de Contato S/ Sucesso',
            '2binvoiced': 'Para ser Faturado',
            'invoice_except': 'Exceção de Faturamento'
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
