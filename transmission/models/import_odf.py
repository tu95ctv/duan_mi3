# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re
def convert_float_location_(v,n):
    if isinstance(v, float):
        v= str(int(v))
    if  v != False and isinstance(v, int):
        v = str(v)
    return v
def sheet_for_ltk_(self,wb, gen_model_dict_kargs):

    return [wb.sheet_names()[0]]


def func_after_func_thiet_bi_(v, needdata,self,obj):
    rs = re.search('(.*) \(',v)
    if rs:
        return rs.group(1)
    else:
        return v


def odf_ids_(v,n,self):
    odf_ids_ptr = n['vof_dict']['odf_ids_ptr']['val']
    if odf_ids_ptr and v:
        odf_ids_ptr_2 = odf_ids_ptr[0][2]
        v[0][2].extend(odf_ids_ptr_2)
#         v.extend(odf_ids_137)
    return v

new = {u'import_soi': 
               {
                'title_rows' : [1,2], 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':sheet_for_ltk_,
                'model':'tran.tbtdan',
                'set_is_largest_map_row_choosing':True,
                'fields' : [
                        ('soi_or_thiet_bi', {'set_val':'soi', 'required':True,'key':True } ),
                        ('stt_soi', {'func':convert_float_location_,'xl_title':u'SOI', 'required':True,'key':True } ),#'func_de_tranh_empty':lambda r:  len(r) > 2
                        ( 'tuyen_cap',{'func':lambda v,n,self: n['sheet_name'], 'key':True,'required':True,'func_after_func': func_after_func_thiet_bi_}),
                        ('odf_ids_ptr',{'key':False,
                                    'required':False ,
                                    'remove_all_or_just_add_one_x2m': 'remove_all',
                                    'for_excel_readonly':True,
                                    'model':'tran.odf',
                                    'fields':[
                                             ('odf_rack',{'xl_title':u'odf 2',  'key':True, 'required': True}),    
                                             ('toa_do',{'xl_title':u'tọa độ 2',  'key':True, 'required': True,'st_is_x2m_field':True, 'func':convert_float_location_}),     
                                              ]
                                    }
                         ),
                        
                        ('odf_ids',{'key':False,
                                    'required':False ,
                                    'remove_all_or_just_add_one_x2m': 'remove_all',
                                    'func':odf_ids_,
                                    'fields':[
                                             ('odf_rack',{'xl_title':u'odf',  'key':True, 'required': True}),    
                                             ('toa_do',{'xl_title':u'tọa độ',  'key':True, 'required': True,'st_is_x2m_field':True, 'func':convert_float_location_}),     
                                              ]
                                    }
                         ),
                                    
                                    
                                    
                      ]
                }
               
               
             
              
              
              }

def gen_import_soi_func():
    return new