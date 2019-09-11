# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.transmission.models.import_odf import gen_import_soi_func

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


def sheet_for_ltk_(self,wb, gen_model_dict_kargs):
    if self.sheet_name:
        return [self.sheet_name]
    return [wb.sheet_names()[0]]
    return wb.sheet_names()


def func_after_func_soi_(v, needdata,self,obj):
    rs = re.search('(.*) \(',v)
    if rs:
        return rs.group(1)
    else:
        return v


def odf_ids_(v,n,self,obj):
    odf_ids_ptr = n['vof_dict'].get('odf_ids_ptr',{}).get('val',None)
    if odf_ids_ptr and v:
        odf_ids_ptr_2 = odf_ids_ptr[0][2]
        v[0][2].extend(odf_ids_ptr_2)
        ptr_obj = n['vof_dict']['odf_ids_ptr']['obj']
        obj.extend(ptr_obj)
#         v.extend(odf_ids_137)
    return v

def odf_rack_(v,n,self):
    if '6-ODF-NODE2 - 03 06 2019 (MTO-LAN-ALC-HUG-PM1)' in n['file_name']:
        return False
    else:
        return v
    
# tbtd #

def sheet_for_tbtd_(self,wb, gen_model_dict_kargs):
    return [wb.sheet_names()[0]]


def xac_dinh_pm(v,n,self, dau_hay_cuoi = 'dau'):
    sheet_name = n['sheet_name']
    rs = re.search('(pm\d)-(pm\d)',sheet_name ,re.I)
    if rs:
        pm_dau, pm_cuoi= rs.group(1),rs.group(2)
        if dau_hay_cuoi =='dau':
            return pm_dau
        else:
            return pm_cuoi
    else:
        return 'PM3'
def phong_may_(v,n,self):
    return xac_dinh_pm(v,n,self, dau_hay_cuoi = 'dau')
def phong_may_ptr_(v,n,self):   
    return xac_dinh_pm(v,n,self, dau_hay_cuoi = 'cuoi')
def phong_may_cho_thiet_bi_(v,n,self):
    sheet_name = n['sheet_name']
    return 'PM3'
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
             
             
             u'import_soi': 
               {
                'title_rows' : [1,2], 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':sheet_for_ltk_,
                'model':'tran.tbtdan',
                'set_is_largest_map_row_choosing':True,
                'fields' : [
                        ('soi_or_thiet_bi', {'set_val':'soi', 'required':True,'key':True } ),
                        ('stt_soi', {'func':convert_float_location_,'xl_title':[u'SOI',u'sợi'], 'required':True,'key':True } ),#'func_de_tranh_empty':lambda r:  len(r) > 2
                        ('file_name', {'func':lambda v,n,self: n['file_name'] } ),
                        ('des_1', {'func':convert_float_location_,'xl_title':[u'des 1'], 'col_index':3 } ),
                        ('des_2', {'func':convert_float_location_,'xl_title':[u'des 2'],  'col_index':6 } ),
                        ('ten', {'func':convert_float_location_,'xl_title':[u'Tên',u'ten',u'NAME'],  'col_index':7 } ),
                        ('chi_tiet_dau_noi', {'func':convert_float_location_,'xl_title':[u'CHI TIẾT ĐẤU NỐI LUỒNG'],  'col_index':8} ),
                        ( 'tuyen_cap',{'func':lambda v,n,self: n['sheet_name'], 'key':True,'required':True,'func_after_func': func_after_func_soi_}),
                        ('odf_cuoi_khac_tram', {'xl_title':u'odf 2', 'col_index':4, 'func':lambda v,n,self: str(v) if v else v} ),
                        ('odf_cuoi_khac_tram_toa_do', {'xl_title':u'tọa độ 2', 'col_index':5, 'func':convert_float_location_} ),
                        ('odf_ids_ptr',{
                                    'key':False,
                                    'required':False ,
                                    'remove_all_or_just_add_one_x2m': 'remove_all',
                                    'for_excel_readonly':True,
                                    'model':'tran.odf',
                                    'fields':[
                                            ('stt_odf',{'set_val':2}), 
                                            ('odf_rack',{'xl_title':u'odf 2',  'key':True, 'required': True ,'func':odf_rack_, 'col_index':4}),    
                                            ('toa_do',{'xl_title':u'tọa độ 2',  'key':True, 'required': True,'st_is_x2m_field':True, 'func':convert_float_location_, 'col_index':5}),     
                                            ('phong_may',{'func':phong_may_ptr_}),
                                            ('department_id',{'key':True, 
                                                                    'required': True,
                                                                    'allow_create':False,
                                                                    'fields':[('name', {'func': lambda v,n,self: u'trạm ltk' if not self.department_id else self.department_id.name, 'required': True,'key':True,  'operator_search':'=ilike' })]

          
                                                         }),     
                                              
                                              
                                                                                                       

                                              ]
                                    }
                         ),
                        
                        ('odf_ids',{'key':False,
                                    'required':False ,
                                    'remove_all_or_just_add_one_x2m': 'remove_all',
                                    'func':odf_ids_,
                                    'fields':[
                                             ('stt_odf',{'set_val':1}),    
                                             ('odf_rack',{'xl_title':u'odf',  'key':True, 'required': True, 'col_index':1}),    
                                             ('toa_do',{'xl_title':u'tọa độ',  'key':True, 'required': True,'st_is_x2m_field':True, 'func':convert_float_location_, 'col_index':2}),     
                                             ('phong_may',{'func':phong_may_}),
                                             ('department_id',{'key':True, 
                                                                    'required': True,
                                                                    'allow_create':False,
                                                                    'fields':[('name', {'set_val':u'trạm ltk', 'required': True,'key':True,  'operator_search':'=ilike' })]

          
                                                         }),      
                                              
                                              ]
                                    }
                         ),
                                    
                                    
                                    
                      ]
                }
               ,
               
               
               
               u'tbtdan': 
               {
                'title_rows' : [1,2], 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':sheet_for_tbtd_,
                'model':'tran.tbtdan',
                'set_is_largest_map_row_choosing':True,
                'fields' : [
                        ('soi_or_thiet_bi', {'set_val':'thiet_bi', 'required':True,'key':True } ),
                        ( 'ten_he_thong',{'func':lambda v,n,self: n['sheet_name'], 'key':True, 'required':True}),
                        ( 'he_thong_id',{'fields':[('name',{'func':lambda v,n,self: n['sheet_name'], 'key':True, 'required':True})]
                            }),

                        ( 'ten_card',{'xl_title':['card'], 'key':True, 'allow_not_match_xl_title':True}),
                        ( 'slot',{'xl_title':['slot'], 'key':True, 'allow_not_match_xl_title':True}),
                        ( 'port',{'xl_title':['port'], 'key':True,'required':True}),
                        ( 'rate',{'xl_title':['RATE/MODE',u'rate'], 'key':True}),
                        ( 'odf',{'xl_title':['ODF HW','odf'], 'key':True}),
                        ( 'port_odf',{'xl_title':['PORT ODF'], 'key':True, 'func':convert_float_location_,}),
                        ( 'ten',{'xl_title':['NAME'], 'key':True}),
                        ( 'near',{'xl_title':['NEAR'], 'key':True}),
                        ( 'far',{'xl_title':['FAR'], 'key':True}),
                        ( 'tb_or_cq',{'xl_title':['THIẾT BỊ ODF'], 'key':True}),
                        ( 'port_tb_or_cq',{'xl_title':['PORT Tx,Rx'], 'key':True}),
                        ( 'cap_quang',{'xl_title':[' Tên cáp quang'],   'allow_not_match_xl_title':True}),
                        ( 'soi',{'xl_title':['sợi'], 'allow_not_match_xl_title':True}),
                        
                        
                        ('file_name', {'func':lambda v,n,self: n['file_name'] } ),
                        ('odf_ids',{'key':False,
                                    'required':False ,
                                    'remove_all_or_just_add_one_x2m': 'remove_all',
                                    'fields':[
                                             ('stt_odf',{'set_val':1}),    
                                             ('odf_rack',{ 'key':True, 'required': True,'func': lambda v,n,self: n['vof_dict']['odf']['val']}),    
                                             ('toa_do',{ 'key':True, 'required': True,'st_is_x2m_field':True, 'func': lambda v,n,self: n['vof_dict']['port_odf']['val']}),     
                                             ('phong_may',{'func':phong_may_cho_thiet_bi_,'key':True}),
                                             ('department_id',{'key':True, 
                                                                    'required': True,
                                                                    'allow_create':False,
                                                                    'fields':[('name', {'set_val':u'trạm ltk', 'required': True,'key':True,  'operator_search':'=ilike' })]

          
                                                         }),      
                                              
                                              ]
                                    }
                         ),
                            
                            
                       
                        
                        
                                    
                                    
                                    
                      ]
                }
               
               
               
               
               
              
              
              
              }
#         new2 = gen_import_soi_func()
        rs.update(new)
#         rs.update(new2)
#         rs.update(gen_model_dict_categ_and_location_partner())
        return rs