# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.dai_tgg.models.import_excel_model_dict_folder.model_dict_tvcv import  gen_tvcv_model_dict
from odoo.addons.dai_tgg.models.import_excel_model_dict_folder.model_dict_user_department import  gen_user_department_model_dict

class ImportExcel(models.Model):
    _inherit = 'importexcel.importexcel' 
#     type_choose = fields.Selection(selection_add = [('test_abc','test abc')])

    def set_parameter_tonkho(self):
        self.env['res.config.settings'].create({'group_stock_production_lot':True, 'group_uom':True})
    def gen_model_dict(self):
        rs = super(ImportExcel, self).gen_model_dict()
        rs.update(gen_tvcv_model_dict())
        rs.update(gen_user_department_model_dict())
        return rs