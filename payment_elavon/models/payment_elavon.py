# -*- coding: utf-8 -*-
import logging

from openerp import models, fields, api, _
_logger = logging.getLogger(__name__)


class AcquirerElavon(models.Model):
    _inherit = 'payment.acquirer'

    def _get_elavon_urls(self, environment):
        """ Elavon URLs
        """
        if environment == 'prod':
            return {
                'elavon_form_url':
                'https://hpp.santanderelavontpvvirtual.es/pay',
            }
        else:
            return {
                'elavon_form_url':
                'https://hpp.prueba.santanderelavontpvvirtual.es/pay',
            }

    @api.model
    def _get_providers(self):
        providers = super(AcquirerElavon, self)._get_providers()
        providers.append(['elavon', 'Elavon'])
        return providers

    elavon_merchant_id = fields.Char(
        string='Merchant ID', required_if_provider='elavon', size=50)
    elavon_account = fields.Char(string='Account', size=30)
    elavon_currency = fields.Char(
        string='Currency', required_if_provider='elavon', size=3,
        default='EUR')
    elavon_auto_settle_flag = fields.Boolean(
        string='Auto Settle', default=True)
    elavon_return_tss = fields.Boolean(string='Return TSS')
    elavon_secret_key = fields.Char(
        string='Secret Key', required_if_provider='elavon')

