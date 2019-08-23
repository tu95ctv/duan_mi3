# -*- coding: utf-8 -*-
from odoo.addons.importexcel.models.model_dict_folder.tao_instance_new import importexcel_func

def check_imported_file_sml(dl_obj, is_in_transfer = None):
    workbook = importexcel_func(dl_obj,
                             import_key=u'stock.inventory.line.tong.hop.ltk.dp.tti.dp',
#                              key_tram='key',
                             check_file=True,
                             is_in_transfer = True
                             )
    filename = 'check_file_of_%s-%s'%(dl_obj.filename,dl_obj.id)
    name = "%s%s" % (filename, '.xls')
    return workbook,name
