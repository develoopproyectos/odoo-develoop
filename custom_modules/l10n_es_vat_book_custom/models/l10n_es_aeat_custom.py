# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.tools import ormcache

_logger = logging.getLogger(__name__)

class log_view_custom(models.AbstractModel):

    _inherit = 'res.partner'

    @ormcache("self.vat, self.country_id")
    def _parse_aeat_vat_info(self):
        """Return tuple with split info (country_code, identifier_type and
        vat_number) from vat and country partner
        """
        if self:
            self.ensure_one()
            vat_number = self.vat or ""
            prefix = vat_number[:2].upper()
            if self._map_aeat_country_code(prefix) in self._get_aeat_europe_codes():
                country_code = prefix
                vat_number = vat_number[2:]
                identifier_type = "02"
            else:
                if self.country_id.code:
                    country_code = self.country_id.code
                elif self.env["res.country"].search([("code", "=", prefix)]):
                    country_code = prefix
                else:
                    country_code = ""
                if (
                    self._map_aeat_country_code(country_code)
                    in self._get_aeat_europe_codes()
                ):
                    identifier_type = "02"
                else:
                    country_code = self._map_aeat_country_code(country_code, extended=True)
                    identifier_type = "04"
            if country_code == "ES":
                identifier_type = ""
            return (
                country_code,
                self.aeat_identification_type or identifier_type,
                self.aeat_identification if self.aeat_identification_type else vat_number,
            )
        else:
            return "", "", "" 
