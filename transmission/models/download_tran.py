# -*- coding: utf-8 -*-
from odoo import models, fields, api
# -*- coding: utf-8 -*-
from odoo.addons.downloadwizard.models.dl_models.dl_model import  download_model
from openerp.http import request
import xlwt
from odoo.exceptions import UserError
from copy import deepcopy
# 
# def stt_(v,needdata): 
#     v = needdata['a_instance_dict']['stt_not_model']['val']  +1   
#     return v  
# def cac_sep_ids_(v,n):
#     if v:
#         return ','.join(v.mapped('login'))
#     else:
#         return ''

def odf_tg_toa_do_(val,needdata):
    if val:
        double_count = needdata['double_count']
        vals= val.split(',')
        return vals[double_count]
    return val
def download_dcquang_(dl_obj,append_domain = []):

    FIELDNAME_FIELDATTR_quants = [
          ('huong',{}),
          ('thiet_bi',{}),
          ('he_thong',{}),
          ('stt_he_thong',{}),
          ('odf_tg',{'allow_write_merge':False,  'double_merge':True}),
          ('odf_tg_toa_do',{'func':odf_tg_toa_do_}),
          ('odf_line',{}),
          ('odf_line_toa_do',{}),
          ('chay_chinh_hay_du_phong',{}),
          ('cap',{}),
          
                    ]
    Export_Para_quants = {
        'exported_model':'dcquang.dcquang',
        'FIELDNAME_FIELDATTR':FIELDNAME_FIELDATTR_quants,
        'search_para':{'order': 'stt_he_thong asc, chay_chinh_hay_du_phong asc'},#desc
        }
    
    filename = 'users'
    name = "%s%s" % (filename, '.xls')
    workbook =  download_model(dl_obj,
                         Export_Para=Export_Para_quants,
                         append_domain=append_domain
                        )
    return workbook,name
        
 


class Download(models.TransientModel):
    _inherit = "downloadwizard.download"
    
    @api.multi
    def gen_pick_func(self): 
        rs = super(Download, self).gen_pick_func()
        rs.update({'dcquang.dcquang':download_dcquang_})
        return rs
    
    