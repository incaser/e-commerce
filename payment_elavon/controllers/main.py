# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale

_logger = logging.getLogger(__name__)


class ElavonController(http.Controller):
    _return_url = '/payment/elavon/return'
    _cancel_url = '/payment/elavon/cancel'
    _exception_url = '/payment/elavon/error'
    _reject_url = '/payment/elavon/reject'

    @http.route([
        '/payment/elavon/return',
        '/payment/elavon/cancel',
        '/payment/elavon/error',
        '/payment/elavon/reject',
    ], type='http', auth='none')
    def elavon_return(self, **post):
        """ Elavon."""
        _logger.info('Elavon: entering form_feedback with post data %s',
                     pprint.pformat(post))
        if post:
            request.registry['payment.transaction'].form_feedback(
                request.cr, SUPERUSER_ID, post, 'elavon',
                context=request.context)
        return_url = post.pop('return_url', '')
        if not return_url:
            return_url = '/shop'
        return werkzeug.utils.redirect(return_url)


class website_sale(website_sale):
    @http.route(['/shop/payment/transaction/<int:acquirer_id>'], type='json',
                auth="public", website=True)
    def payment_transaction(self, acquirer_id):
        tx_id = super(website_sale, self).payment_transaction(acquirer_id)
        cr, context = request.cr, request.context
        acquirer_obj = request.registry.get('payment.acquirer')
        acquirer = acquirer_obj.browse(
            cr, SUPERUSER_ID, acquirer_id, context=context)
        if acquirer.provider == 'elavon':
            request.website.sale_reset(context=request.context)
        return tx_id
