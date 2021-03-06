# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
from odoo import models, fields, api, _
try:
    # Python 3
    from urllib import parse as urlparse
except:
    from urlparse import urlparse


class AddUrlWizard(models.TransientModel):
    _name = 'ir.attachment.add_url'

    name = fields.Char('Name', required=True)
    url = fields.Char('URL', required=True)

    @api.multi
    def action_add_url(self):
        """Adds the URL with the given name as an ir.attachment record."""

        if not self._context.get('active_model'):
            return
        attachment_obj = self.env['ir.attachment']
        for form in self:
            url = urlparse(form.url)
            if not url.scheme:
                url = urlparse('%s%s' % ('http://', form.url))
            for active_id in self._context.get('active_ids', []):
                attachment = {
                    'name': form.name,
                    'type': 'url',
                    'url': url.geturl(),
                    'res_id': active_id,
                    'res_model': self._context.get('active_model')
                }
                attachment_obj.create(attachment)
        return False