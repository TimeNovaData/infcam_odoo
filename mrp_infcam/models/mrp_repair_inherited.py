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


from odoo.exceptions import UserError, ValidationError


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
            ('teste', 'Em Teste'),
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
        default='novo',
        track_visibility="onchange"
    )

    lot_id = fields.Many2one(
        domain="[('cliente', '=', partner_id)]"
    )

    location_id = fields.Many2one(
        default=9
    )

    location_dest_id = fields.Many2one(
        default=9
    )

    invoice_method = fields.Selection(
        default='after_repair'
    )

    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsavel',
        help='Responsável pelo suporte',
        track_visibility='onchange')

    def abrir_whatsapp(self, cr, context=None):
        url = 'https://api.whatsapp.com/send?phone=55{}&text=Ol%C3%A1%2C%20Somos%20da%20INFCAM%20SOLU%C3%87%C3%95ES%20TECNOL%C3%93GICAS.%20Nosso%20contato%20%C3%A9%20sobre%20uma%20Ordem%20de%20Servi%C3%A7o%20que%20voc%C3%AA%20tem%20conosco%20com%20N%C2%BA%20{}.'.format(
            self.partner_id.mobile,
            self.name
        )
        res = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }

        return res

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
            'teste': 'Em Teste',
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

        self.env['res.company'].browse(1).enviar_sms(
                telefone="55{}".format(record.partner_id.mobile.replace(" ", "")),
                mensagem="Olá! Informamos que a sua OS, {}, teve seu status atualizado e agora se encontra no "
                         "estágio de {}. Infcam".format(
                    record.name, record.get_mrp_repair_state())
            )

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

            self.env['res.company'].browse(1).enviar_sms(
                telefone="55{}".format(self.partner_id.mobile.replace(" ", "")),
                mensagem="Olá! Informamos que a sua OS, {}, teve seu status atualizado e agora se encontra no "
                         "estágio de {}. Infcam".format(
                    self.name, self.get_mrp_repair_state())
            )

        return record

    @api.multi
    def action_repair_end(self):
        """ Writes repair order state to 'To be invoiced' if invoice method is
        After repair else state is set to 'Ready'.
        @return: True
        """
        if self.filtered(lambda repair: repair.state != 'under_repair'):
            raise UserError(_("Repair must be under repair in order to end reparation."))
        for repair in self:
            repair.write({'repaired': True})
            vals = {'state': 'done'}
            vals['move_id'] = repair.action_repair_done().get(repair.id)
            if not repair.invoiced and repair.invoice_method == 'after_repair':
                vals['state'] = 'waiting_withdrawal'
            repair.write(vals)
        return True
