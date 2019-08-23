# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re
def convert_float_location_(v,n):
    if isinstance(v, float):
        v= str(int(v))
    if  v != False and isinstance(v, int):
        v = str(v)
    return v

def convert_st_to_int_(v,n, self):
    try:
        return int(v)
    except:
        return False
def func_in_write_handle_(orm_field_val, val):
    if orm_field_val and val:
        orm_field_val_split = orm_field_val.split(',')
        if val not in orm_field_val_split:
            orm_field_val_split.append(val)
            orm_field_val_split = u','.join(orm_field_val_split)
            return orm_field_val_split
    return val

def odf_tg_(v,n,self):
    if v:
        rs = re.search('.*', v)
        return rs.group(0)
    return v
def func_after_func_thiet_bi_(v, needdata,self,obj):
    if v:
        rs = re.search('(.*)', v)
        if rs:
            return rs.group(1)
        else:
            return v
    return v
def func_after_func_replace_enter_(v, needdata, self, obj):
    if v:
        v = re.sub('\n', ' ', v)
    return v

class importexcel(models.Model):
    _inherit = 'importexcel.importexcel' 
    def gen_model_dict(self):
        rs = super(importexcel, self).gen_model_dict()
        new = {u'do_cap_quang': 
               {
                'title_rows' : [1,2], 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':['Kết quả đo hàng ngày'],
                'model':'dcquang.dcquang',
                'fields' : [
                        ('huong', {'func':None,'xl_title':u'HƯỚNG', 'required':True,'key':True } ),#'func_de_tranh_empty':lambda r:  len(r) > 2
                        ( 'stt_he_thong',{'func':None,'xl_title':u'stt Hệ THỐNG', 'key':True,'required':True, 'func':convert_st_to_int_}),
                        ( 'he_thong',{'func':None,'xl_title':u'Hệ THỐNG', 'key':True}),
                        ( 'thiet_bi',{'func':lambda v,n,self: n['vof_dict']['he_thong']['val'], 'key':False,'func_after_func':func_after_func_thiet_bi_}),
                        
                        ( 'odf_tg',{'func':odf_tg_,'xl_title':u'ODF-TG NODE2 odf', 'key':False}),
                        ( 'odf_tg_toa_do',{'func':None,'xl_title':u'ODF-TG NODE2 tọa độ', 'key':False, 'func':convert_float_location_, 'func_in_write_handle':func_in_write_handle_}),
                        
                        ( 'odf_line',{'func':None,'xl_title':u'ODF-LINE NODE2 odf', 'key':False}),
                        ( 'odf_line_toa_do',{'func':None,'xl_title':u'ODF-LINE NODE2 tọa độ', 'key':False, 'func':convert_float_location_, 'func_in_write_handle':func_in_write_handle_}),
                        
                        ( 'chay_chinh_hay_du_phong',{'func':None,'xl_title':u'Chạy chính', 'key':False, 'func_after_func':func_after_func_replace_enter_}),
                        ( 'cap',{'func':None,'xl_title':u'CÁP HOẠT ĐỘNG/DỰ PHÒNG', 'key':True}),
                      ]
                }
               
               , 
             
              
              
              
              }
        rs.update(new)
#         rs.update(gen_model_dict_categ_and_location_partner())
        return rs