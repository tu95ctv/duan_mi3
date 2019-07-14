# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.tonkho.models.import_excel_model_dict_folder.model_dict import gen_model_dict_for_stock_move_line
from odoo.addons.tonkho.models.import_excel_model_dict_folder.model_dict_categ_and_location_partner import gen_model_dict_categ_and_location_partner
class importexcel(models.Model):
    _inherit = 'importexcel.importexcel' 
    def gen_model_dict(self):
        rs = super(importexcel, self).gen_model_dict()
        new = {u'stock.inventory.line.tong.hop.ltk.dp.tti.dp': gen_model_dict_for_stock_move_line, 
              }
        rs.update(new)
        rs.update(gen_model_dict_categ_and_location_partner())
        return rs