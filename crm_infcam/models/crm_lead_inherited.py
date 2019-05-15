# -*- coding: utf-8 -*-
from odoo import models, fields, api

"""
Módulo que herda os leads do CRM para customizações da Infcam.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2019, Edson Junior"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"


class CrmLead(models.Model):
    """
        Classe CRM Lead herda dos leads do CRM e customiza de acordo com as necessidades da Infcam.
    """
    _name = 'crm.lead'
    _inherit = ['crm.lead']

    produto = fields.Many2one(
        comodel_name='product.product',
        string='Produto',
        help='Produto do cliente para orçamento',
        track_visibility='onchange')

    serie = fields.Many2one(
        comodel_name='stock.production.lot',
        string='Lote/Série',
        help='Número de série do produto para orçamento',
        domain="[('product_id', '=', produto)]",
        track_visibility='onchange')

    reparo = fields.Many2one(
        comodel_name='mrp.repair',
        string='Reparo',
        help='Reparo aberto através dessa oportunidade',
        track_visibility='onchange')

    def abrir_reparo(self, cr, context=None):
        valores = {
            'product_id': self.produto.id,
            'partner_id': self.partner_id.id,
            'lot_id': self.serie.id,
            'product_qty': 1.0,
            'product_uom': self.produto.uom_id.id,
            'invoice_method': 'after_repair',
            'state': 'confirmed',
            'responsavel': self.user_id.id,
            'location_id': 9,
            'location_dest_id': 9
        }

        reparo = self.env['mrp.repair'].create(valores)

        self.write({'reparo': reparo.id})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.model
    def create(self, values):
        """Override default Odoo create function and extend."""
        # Do your custom logic here
        record = super(CrmLead, self).create(values)

        template = self.env.ref('crm_infcam.email_template_mudanca_responsavel')
        self.env['mail.template'].browse(template.id).send_mail(record.id)

        template2 = self.env.ref('crm_infcam.email_template_notificacao_cliente')
        self.env['mail.template'].browse(template2.id).send_mail(record.id)

        return record

    @api.multi
    def write(self, values):
        record = super(CrmLead, self).write(values)

        if 'user_id' in values:
            template = self.env.ref('crm_infcam.email_template_mudanca_responsavel')
            self.env['mail.template'].browse(template.id).send_mail(self.id)

        if 'stage_id' in values:
            template2 = self.env.ref('crm_infcam.email_template_notificacao_cliente')
            self.env['mail.template'].browse(template2.id).send_mail(self.id)

        return record