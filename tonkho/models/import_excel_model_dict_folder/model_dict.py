# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
import datetime
from odoo.addons.tutool.mytools import pn_replace


def gen_model_dict_for_stock_move_line(self=None, key_tram=None, gen_model_dict_kargs= {}):  
       
#     mode =      getattr(self, 'mode',None)     or mode
    check_file = gen_model_dict_kargs.get('check_file')
    cach_tim_location_goc = gen_model_dict_kargs.get('cach_tim_location_goc', 'find_origin_location_by_key_tram') or 'find_origin_location_by_key_tram'
    mode = u'1' if cach_tim_location_goc =='find_origin_location_by_key_tram' else u'2'
    if key_tram == sml:
        mode = u'2'
    write_field_categ_id = self.env['ir.config_parameter'].sudo().get_param('tonkho.' + 'write_field_categ_id')
    not_use_default_excel_import_setting = self.env['ir.config_parameter'].sudo().get_param('tonkho.' + 'not_use_default_excel_import_setting')
#     use_default = not not_use_default_excel_import_setting
    use_default = False
    admin_to_user = False
    user_to_admin = self.user_has_groups('tonkho.group_write_field_when_import_excel')
    is_admin = self.user_has_groups('base.group_erp_manager')
    is_user = not self.user_has_groups('base.group_erp_manager')
    is_admin_cal = False
    if is_user:
        if user_to_admin:
            is_admin_cal = True
    if is_admin:
        if admin_to_user:
            is_admin_cal = False
        else:
            is_admin_cal = True
    import_from_inventory =self._context.get('import_from_inventory') # ở đây thì get context được vào trong fields thì mất
    ALL_MODELS_DICT = {
     u'stock.inventory.line.tong.hop.ltk.dp.tti.dp': {
    'key_allow':True,
    'set_is_largest_map_row_choosing':{sml:True,
                                       all_key_tram:False},                      
    'title_rows':{
        'key_ltk':range(0,6),
        'key_tti':[3,4],
        key_ltk_dc:[0],
        key_tti_dc:[0,1],
        key_ltk_dc2:[7,8],
        sml:[0],
        key_137: range(3,5)
        },
    'title_rows_some_sheets':{'key_ltk':{u'XFP, SFP các loại':[2,3]}},
    'begin_data_row_offset_with_title_row' :{all_key_tram:1,
                                             key_tti_dc:2},
    'offset_write_xl':{all_key_tram:1}, 
    'string':u'Dong dieu chuyen',
    'sheet_names':{
        'key_ltk':sheet_for_ltk_,
        'key_tti':lambda self,wb: wb.sheet_names() if not self.sheet_name else if_self_sheet_name(self.sheet_name,wb),
        'key_ltk_dc':lambda self:[u'Tổng hợp'] if not self.sheet_name else [self.sheet_name],
        key_tti_dc:lambda self:[u'TTI-TS co'],
        sml:  lambda self,wb: [wb.sheet_names()[0]] if not self.sheet_name else if_self_sheet_name(self.sheet_name,wb),
        'key_137':lambda self,wb: wb.sheet_names() if not self.sheet_name else if_self_sheet_name(self.sheet_name,wb),
        key_ltk_dc2:lambda self,wb: [wb.sheet_names()[0]],
                   } ,
    'model':{all_key_tram: 'stock.inventory.line',sml:'stock.move.line'},
    'st_write_false':False,
    'setting':{all_key_tram: {
                   'st_is_allow_write_existence':default_import_xl_setting['default_st_is_allow_write_existence'] if use_default else self.st_is_allow_write_existence,
                   'st_allow_check_if_excel_is_same_existence':default_import_xl_setting['default_st_allow_check_if_excel_is_same_existence'] if use_default else self.st_allow_check_if_excel_is_same_existence,
                   'st_is_allow_empty_xldata_pn_is_unique_same_name_product':default_import_xl_setting['default_st_is_allow_empty_xldata_pn_is_unique_same_name_product'] if use_default else self.st_is_allow_empty_xldata_pn_is_unique_same_name_product,
                   'st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr':default_import_xl_setting['default_st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr'] if use_default else  self.st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr,
                   'st_allow_func_map_database_existence':default_import_xl_setting['default_st_allow_func_map_database_existence'] if use_default else self.st_allow_func_map_database_existence,
                               }},
    'setting2': {sml: {'allow_check_excel_obj_is_exist_raise_or_break':'break', 
                            'allow_write':True if  is_admin_cal else False},
                    all_key_tram:{'allow_check_excel_obj_is_exist_raise_or_break':'raise',
                                        'allow_write': True if is_admin_cal else False}
                 },
    'break_condition_func_for_main_instance':{all_key_tram:break_condition_func_for_main_instance_,
                                                                key_137:None},
    'fields': [
    
    ('barcode_for_first_read',{'empty_val':[u'NA',u"'",u"`"],
                                        'skip_this_field':{key_ltk_dc:False,
                                                                'all_key_tram':True},
                                        'func':lambda val,*n: str(int(val)) if isinstance(val,float) else val,'xl_title':[u'Barcode'],'for_excel_readonly' :True}),
    ('prod_lot_id_excel_readonly',{'empty_val':{'key_ltk':[u'N/C'],
                                                                'key_tti':[u'N/C',u'N/a',u'n/a',u'N/A'],
                                                                'key_ltk_dc':[u'N/C',u'-',u'--',u'NA',u'N/A',u'chưa đọc được SN'],
                                                                 all_key_tram:[u'N/C',u'-',u'--',u'NA',u'N/A',u'chưa đọc được SN',u'N/C',u'N/a',u'n/a',u'N/A']},
                                                'func':lambda val, *n: str(int(val)) if isinstance(val,float) else val,
                                                'xl_title':{all_key_tram:[u'Lot/Serial Number',u'Seri Number',u'Số serial (S/N)',u'Serial Number',u'Serial',u'S/N',u'SERI',u'Số S/N',u'''SERI
S/N'''],
                                                            key_tti_dc: None,},
                                                'for_excel_readonly' :True,
                                                'required':{key_137:True},
                                                'col_index':{'all_key_tram':None,
                                                                key_tti_dc:20}
                                                }),
    ('prod_lot_id_excel_readonly_for_search',{'for_excel_readonly' :True,
                                                            'func':prod_lot_id_excel_readonly_for_search_}),
    ('ma_vat_tu_readonly',{'for_excel_readonly' :True,
                                    'skip_this_field': {'key_137':False, all_key_tram:True},
                                    'xl_title':{'key_137':[u'Mã vật tư']}}),
    ('product_id_name_readonly',{'for_excel_readonly' :True,
                                             'col_index':{all_key_tram:None,
                                                                        key_tti_dc:11,
                                                                  },
                                            'xl_title':{'key_ltk':[u'TÊN VẬT TƯ',u'Module quang',u'Product'],
                                                        'key_ltk_dc':[u'Loại card'],
                                                        'key_tti':[u'TÊN VẬT TƯ'],
                                                        sml:[u'TÊN VẬT TƯ', u'Tên Vật Tư',u'Danh mục hàng hóa',u'Tên – Qui cách hàng hóa'],
                                                        key_137:[u'TÊN TIẾNG VIỆT',u'TÊN THIẾT BỊ',u'Tên vật tư'],
                                                        key_ltk_dc2:[u'Tên tài sản'],
                                                        key_tti_dc:u'''Tên
                                                        
    chi tiết
    thiết bị
    (card)'''
                                                        },
                                            'empty_val':{'key_ltk':[u'TỔNG ĐÀI IMS',u'JUNIPER ERX 1400; T1600 ; T4000',u'HDD 300G 10K SAS'],
                                                              'sml':[u'TỔNG ĐÀI IMS',u'JUNIPER ERX 1400; T1600 ; T4000',u'HDD 300G 10K SAS'],
                                                              all_key_tram:None}}) ,
    ('stt',{'func':stt_, 
            'xl_title':{'key_ltk':[u'STT'],
                        'key_tti':u'STT',
                        'key_ltk_dc':u'STT',
                         key_tti_dc: [u'Stt',u'Stt '],
                         sml:u'STT',
                         key_137:[u'SỐ'],
                         key_ltk_dc2:u'STT'},
            'skip_this_field':{key_137: True, all_key_tram:getattr(self,'skip_stt', False)},
            'allow_not_match_xl_title':True ,
            'key':{all_key_tram:True},
            'required_force':{all_key_tram:True},
      }
    ), 
    ('product_id',{'string':u'Tên Vật tư',
                       'search_func':search_func_for_product_id_,
                       'offset_write_xl':{all_key_tram:2}, 
#                        'offset_write_xl_2':{sml:4}, 
                       'check_file_write_more':{sml:[(4, check_file_write_more_check_searched_obj_product_, u'Searched OBJ'),\
                                                     (5, check_file_write_more_check_name_product_, u'Name of Product'),
                                                     (6,check_file_write_more_check_PN_product_, 'PN of Product'),
                                                     (7, check_file_write_more_check_name_and_PN_product_, 'Name and PN of Product')]},
                       'key':'Both',
                       'required':{all_key_tram:True},
                       'required_when_check_file':False,
                       'func':{all_key_tram:None,
                                 key_137: product_id_,
                               },
                       'func_map_database_existence':func_map_database_existence_for_product_,
                       'func_check_if_excel_is_same_existence':{all_key_tram: func_check_if_excel_is_same_existence_for_product_id_},#,sml:None
                       'fields':[('pn',{'type_allow':[int,float],
                                            'func':def_pn_,
                                            'empty_val':[u'NA',u'-',u'--'],
                                            'xl_title':[u'Part-Number',u'Part Number',u'Partnumber',u'Mã card (P/N)', u'mã vật tư'],
                                            'write_false':False,
                                            'allow_not_match_xl_title':{sml:True,all_key_tram:None},
                                            'write_field':True}),
                                ('pn_replace',{'type_allow':[int,float],
                                               'func':pn_replace_, 
                                                'for_excel_readonly':True}),
                                ('name',{'func': {all_key_tram: product_id_name_, 'key_137':product_id_137_},
                                             'key':False,
                                             'required':True,
                                             'write_field':True if is_admin_cal else False}),
                                ('type', {'set_val':'product'}),
                                ('categ_id',{
                                                'write_false':False,
                                                'write_field':{all_key_tram: write_field_categ_id if is_admin_cal else False, sml:False},
                                                'key':False,
                                                'only_get':{all_key_tram:True if  not is_admin_cal else False},
                                                'raise_if_diff':False,
                                                'set_val':{key_ltk_dc2:1,key_ltk_dc: 1},
                                                'fields':[('name',{'key':True,
                                                                        'required':True,
                                                                        'allow_not_match_xl_title':{sml:True, all_key_tram:False},
                                                                        'replace_string':{all_key_tram:[(u'Chuyển Mạch (IMS, Di Động)',u'Chuyển mạch'),(u'IP (VN2, VNP)',u'IP'),(u'XFP, SFP các loại',u'XFP, SFP')]},
                                                                        'func':{all_key_tram:(lambda val,needdata: needdata['sheet_name']) if mode!=u'2' else None,
                                                                                'key_tti':categ_id_tti_convert_to_ltk_, key_tti_dc: None, sml:None}, 
                                                                        'karg':{'key_tti':{'tram':'TTI'}},
                                                                        'xl_title':{all_key_tram:None, key_tti_dc:[u'Phân hệ'], sml:[u'Nhóm'],'key_ltk':[u'Nhóm'] if mode ==u'2' else None}
                                                                        })]
                                                 }
                                 ),
                                ('toc_do_id', {'skip_this_field':{all_key_tram:True,'key_ltk':False},
                                                    'write_false':False,
                                                    'fields':[('name',{'allow_not_match_xl_title':True,'key':True,'xl_title':[u'Tốc độ']})]}),
                                ('brand_id',{'empty_val':[u'NA'],
                                                'write_false':False,
                                                'fields':[('name',{'func':lambda v,n: v.upper() if isinstance(v,str) else v,
                                                                        'allow_not_match_xl_title':{sml:True,all_key_tram:False},
                                                                        'xl_title':{all_key_tram: [u'Hãng sản xuất',u'Hãng / Model']},
                                                                        'key':True,
                                                                        'required': True}),
                                                              ]
                                                }
                                 ),
                                 ('thiet_bi_id',{
                                                    'write_false':False,
                                                    'write_field':None if is_admin_cal else False,
                                                    'fields':[('name',{'key':True,
                                                                           'required': True,
                                                                           'func':{all_key_tram:lambda v,n: str(int(v)) if isinstance(v,float) else v,  key_137: lambda v,n:n['sheet_name'],},
                                                                           'allow_not_match_xl_title':{sml:True,all_key_tram:None,'key_ltk': True if mode ==u'1' else None},
                                                                           'xl_title':{ 'all_key_tram':[u'Thiết bị', u'Tên hệ thống thiết bị'],
                                                                                       key_tti_dc:u'''Tên
            thiết bị'''
                                                                                       }, 
                                                                           }),
                                                            ('categ_id',{'key':False,
                                                                            'requried':True,
                                                                            'raise_if_False':True,
                                                                            'write_field':write_field_categ_id if is_admin_cal else False,
                                                                            'write_false':False,
                                                                            'func': lambda v,n:n['vof_dict']['product_id']['fields']['categ_id']['val']}
                                                             ),
                                                            ('brand_id',{
                                                                         'write_field':None if is_admin_cal else False,
                                                                         'key':False,
                                                                         'write_false':False,
                                                                         'func': lambda v,n:n['vof_dict']['product_id']['fields']['brand_id']['val']}),                                                               
                                                          ]}
                                ), 
                                ('uom_id',{'write_field':None if is_admin_cal else False, # required = True
                                                'write_false':False,
#                                                 'default_val':1,
                                                'offset_write_xl_diff':12, 
                                                'fields': [('name',{'set_val':{all_key_tram:None, key_ltk_dc:u'Cái',  key_ltk_dc2:u'Cái',  key_tti_dc:u'Cái' },
                                                                        'func':{all_key_tram:name_of_uom_id_,},
                                                                        'operator_search':'=ilike',
                                                                        'xl_title':{all_key_tram:[u'Đơn vị tính',u'ĐVT',u'Đơn vị'], key_ltk_dc2:None },
                                                                        'key':True,
                                                                        'required':True,
                                                                        'replace_string':{'key_ltk':[('Modunle','module'),('CARD','Card'),('module','Module')],
                                                                                                'key_tti':[('CARD','Card'),('module','Module'),(u'bộ',u'Bộ')]},
                                                                        'sheet_allow_this_field_not_has_exel_col':{'key_ltk':[u'XFP, SFP các loại']}}
                                                            ),
                                                            ('category_id', {'func': lambda n,v,self:self.env['product.uom.categ'].search(['|',('name','=','Unit'),('name','=',u'Đơn vị')])[0].id}),
                                                           ]
                                                }
                                 )]
    }),  
    ('product_qty',{'required':True,
                        'type_allow':[int],
                        'transfer_name':{sml:'qty_done'},
                        'func':qty_,
                        'replace_val':{'key_ltk':{u'XFP, SFP các loại':[(False,1)]}},
                        'set_val':{'all_key_tram':None, 'key_ltk_dc':1, key_tti_dc:1, key_ltk_dc2:1},
                         'xl_title':{'all_key_tram':[u'Tồn kho cuối kỳ',u'Số lượng'],
                                    'key_ltk':[u'Tồn kho cuối kỳ',u'Số lượng',u'Tồn kho cuối kỳ',u'Quantity',u'Số lượng',u'Số lượng điều chỉnh'],
                                    'key_tti':[u'Tồn kho cuối kỳ',u'Số lượng',u'Tồn kho cuối kỳ'],
                                    sml:[u'Số lượng',u'Số lượng',u'S/L',u'Tồn kho cuối kỳ',u'Quantity',u'Số lượng điều chỉnh']},
                        'sheet_allow_this_field_not_has_exel_col':{'key_ltk':[u'XFP, SFP các loại']}}),
    ('location_id_goc', {'model':'stock.location',
                                'for_excel_readonly' :True,
                                'required': {all_key_tram:True, sml:False},
                                'only_get': mode ==u'2',
                                'valid_field_func':{sml:check_location_id_is_same_in_bb_,
                                                        all_key_tram:  check_if_your_depart_of_lc_goc_ if (mode==u'2' and not is_admin_cal) else None},
                                'func':{all_key_tram:None if  mode ==u'2'  else location_goc_},
                                'fields': [('name',{'xl_title': u'Trạm',
                                                        'allow_not_match_xl_title':True,
                                                        'key':True,'required':True})] if mode == u'2' else [] ,
                                'only_get':True,
                                'raise_if_False':True, 
                         }),  
    
    ('department_id_for_excel_readonly',{'for_excel_readonly':True,
                                                         'key':False,
                                                         'raise_if_False':True,
                                                         'func':{all_key_tram: department_for_sml_and_mode2_ if mode ==u'2' else look_department_from_key_tram_}}),
    ('inventory_id', {'skip_this_field':{sml:True},
                            'key':True,
                            'func': inv_id_,
                            'karg':{'key_ltk':{'import_from_inventory':import_from_inventory}},
                            'fields':[('name',{'key':True, 'required': True,
                                                    'func': gen_inventory_name
                                                    }),
                                       ('location_id',{'func':lambda v,needdata: needdata['vof_dict']['location_id_goc']['val']})
                                    ] if not import_from_inventory  else None}
    ),
    ('location_id1',{'only_get': {sml:True}, 'model':'stock.location', 'for_excel_readonly':True, 
                       'fields':[
                                ('location_id',{'key':True,'required':True, 'func':lambda v, n: n['vof_dict']['location_id_goc']['val']}),
                                ('name',{'key':True, 'required':True,
                                            'allow_not_match_xl_title':{sml:True, all_key_tram:False},
                                            'sheet_allow_this_field_not_has_exel_col':{'key_ltk':[u'XFP, SFP các loại']},
                                            'func_pre_func':{'key_ltk': func_pre_func_location_id_1_ltk_dp_xfp_ if  mode ==u'1' else None},
                                            'func':convert_float_location_,
                                            'col_index':{all_key_tram:None, key_tti_dc:22 },
                                            'xl_title':{
                                                     all_key_tram:[u'Phòng',u'Phòng máy'],
                                                     'sml':[u'Phòng',u'Phòng máy'],
                                                     'key_ltk':[u'Phòng',u'Phòng máy'],
                                                     'key_tti':u'Phòng',
                                                      key_ltk_dc:[u'Vị trí lắp đặt'],
                                                      key_ltk_dc2:[u'Vị trí lắp đặt'],
                                                      key_tti_dc:[u'''Vị trí
đặt'''],
                                                     },
                                            
                                            }
                                 ),
                                ('department_id',{'key':True, 'required':True, 'model':'hr.department',
                                                         'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val']}
                                 ),
                                ('stock_type',{'set_val':'phong_may','key':True}),
                                ]
                       }), 
    ('location_id2',{'only_get': {sml:True},
                        'model':'stock.location',
                        'for_excel_readonly':True,
                        'fields':[
                                ('location_id',{'required':True,'func':lambda val,needdata: needdata['vof_dict']['location_id1']['val'] or  needdata['vof_dict']['location_id_goc']['val']  , 'key':True}),
                                ('name',{'func':convert_float_location_,
                                            'xl_title':{all_key_tram:[u'Tủ/Kệ',u'Tủ'],
                                                        'sml':[u'Tủ/Kệ',u'Tủ',u'Tủ/cabinet'],
                                                        'key_ltk':[u'Tủ/Kệ',u'Tủ',u'Tủ/cabinet'],
                                                        'key_tti':[u'Tủ/Kệ',u'Tủ'],
                                                        key_ltk_dc:[u'Tên tủ (Cabinet / rack)',u'Tủ'],
                                                        key_ltk_dc2:[u'Tên tủ (Cabinet / rack)',u'Tủ'],
                                                        key_tti_dc:None,
                                                     },
                                            'allow_not_match_xl_title':{sml:True, all_key_tram:False},
                                          'key':True,'required': True}),
                                ('department_id',{'key':True,'model':'hr.department', 'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val'],'required':True,'raise_if_False':True}),
                                ('stock_type',{'set_val':'tu','key':True})]
                        }
     ),                                           
    ('location_id3',{
                     'only_get': {sml:True},
                      'model':'stock.location', 'for_excel_readonly':True,
                                           'fields':[
                                                    ('location_id',{'required':True,
                                                                    'func':lambda val,needdata: needdata['vof_dict']['location_id2']['val'] or needdata['vof_dict']['location_id1']['val'] or  needdata['vof_dict']['location_id_goc']['val'], 'key':True}),
                                                    ('name',{'func':convert_float_location_,
                                                             'xl_title':{
                                                                            all_key_tram:[u'Ngăn',u'Ngăn/Kệ'],
                                                                            'sml':[u'Ngăn',u'Ngăn/Kệ',u'Shelf/ngăn/kệ'],
                                                                            'key_ltk':[u'Ngăn',u'Ngăn/Kệ',u'Shelf',u'Shelf/ngăn/kệ'],
                                                                            'key_tti':[u'Ngăn',u'Ngăn/Kệ'],
                                                                             key_ltk_dc:[u'Ngăn (shelf)',u'Ngăn'],
                                                                             key_ltk_dc2:[u'Ngăn (shelf)',u'Ngăn'],
                                                                             key_tti_dc:None},
                                                              'allow_not_match_xl_title':{sml:True,all_key_tram:False},
                                                              'key':True,'required': True}),
                                                  
    #                                                                     ('department_id',{'key':False,'model':'hr.department', 'set_val':lambda self: self.department_id.id,'required':True }),
                                                    ('department_id',{'key':True,'model':'hr.department', 'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val'],'required':True,'raise_if_False':True}),
                                                    ('stock_type',{'set_val':'shelf','key':True}),
                                                    
                                                    ]
                                           }),         
    ('location_id4',{
                     'only_get': {sml:True},
                      'model':'stock.location', 'for_excel_readonly':True,
                                           'fields':[
                                                    ('location_id',{'required':True,'func':lambda val,needdata: needdata['vof_dict']['location_id3']['val'] or needdata['vof_dict']['location_id2']['val'] or needdata['vof_dict']['location_id1']['val'] or  needdata['vof_dict']['location_id_goc']['val'], 'key':True}),
                                                    ('name',{'func':convert_float_location_,
                                                             'xl_title':{
                                                                            'sml':[u'Số thùng',u'STT trong shelf',u'STT trong shelf/số thùng',u'Hộp'],
                                                                            'key_ltk':[u'Số thùng',u'STT trong shelf',u'STT trong shelf/số thùng',u'Hộp'],
                                                                            'key_tti':[u'Số thùng'],
                                                                             key_ltk_dc:[u'Số thứ tự (trong shelf)'],
                                                                             key_ltk_dc2:[u'Số thứ tự (trong shelf)'],
                                                                             key_tti_dc:None,
                                                                            },   
                                                              'allow_not_match_xl_title':{sml:True,all_key_tram:False},
                                                      'key':True,'required': True,'allow_not_match_xl_title':True}),
                                                    ('department_id',{'key':True,'model':'hr.department', 'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val'],'required':True,'raise_if_False':True}),
                                                    ('stock_type',{'set_val':'stt_trong_self','key':True}),
                                                    ]
                                           }),  
    ('location_id5',{
                    'only_get': {sml:True},
                    'model':'stock.location', 
                    'for_excel_readonly':True,
                               'fields':[
                                      ('location_id',{'required':True,
                                                        'func':lambda val,needdata: needdata['vof_dict']['location_id4']['val'] or needdata['vof_dict']['location_id3']['val'] or needdata['vof_dict']['location_id2']['val'] or needdata['vof_dict']['location_id1']['val'] or  needdata['vof_dict']['location_id_goc']['val'],
                                                        'key':True}),
                                        ('name',{
                                                'func':convert_float_location_,
                                                'xl_title':{
                                                            'sml':[u'Slot'],
                                                            'key_ltk':[u'Slot'] if mode ==u'2' else None ,
                                                            'key_tti':None,
                                                            key_ltk_dc:[u'Khe (Slot)'],
                                                            key_ltk_dc2:[u'Khe (Slot)'],
                                                            key_tti_dc:None,
                                                            },        
                                                 
                                                'key':True,'required': True,
                                                'allow_not_match_xl_title':True,
                                                }),
                                      
                                        ('stock_type',{'set_val':'slot',
                                                             'key':True,
                                                       
                                                       }),
                                        ('department_id',{'key':True,'model':'hr.department', 'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val'],'required':True,'raise_if_False':True}),
                                        ]
                               }),     
                    
                    
    ('location_id6',{'skip_this_field':{sml:True},'model':'stock.location',
                        'for_excel_readonly':True,
                        'fields':[('name',{'key':True,'required': True,'func':location_id6_chua_ro_}),
                                ('location_id',{'required':True,'func':lambda val,needdata: needdata['vof_dict']['location_id5']['val']  or needdata['vof_dict']['location_id4']['val'] or needdata['vof_dict']['location_id3']['val'] or needdata['vof_dict']['location_id2']['val'] or needdata['vof_dict']['location_id1']['val'] or  needdata['vof_dict']['location_id_goc']['val'], 'key':True}),
                                ('department_id',{'key':True,'model':'hr.department', 'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val'],'required':True})]
                        }),
     ('location_id', {'skip_this_field':{all_key_tram:False},
                    'func':{ 'sml':location_id_for_sml_,
                                all_key_tram: or_7_location_id_ },
                    'key':False}
     ),
            
        
               
                  
    ('location_id_goc_dc',{'for_excel_readonly':True, 'model':'stock.location',
                                 'key':False, 
                                 'for_excel_readonly' :True,
                                 'func':None,
                                 'only_get':True,
                                 'valid_field_func':{sml:check_location_id_is_same_in_bb_dc_},
                                 'fields':[('name',{'xl_title':u'Trạm điều chuyển',
                                                        'key':True,
                                                        'required':True,
                                                        'allow_not_match_xl_title':True}),
                                           ], 
                                 'skip_this_field':{sml:False, all_key_tram:True},
    
                         }),  
    
    
    ('location_id1_dc',{'skip_this_field':{sml:False, all_key_tram:True}, 
                            'model':'stock.location', 
                            'for_excel_readonly':True, 
                                           'fields':[
                                                    ('name',{'func':convert_float_location_,
                                                                  'col_index':{all_key_tram:None,
                                                                                    key_tti_dc:22,
                                                                              },
                                                             'xl_title':{
                                                                          'sml':u'Phòng máy điều chuyển',
                                                                          'key_ltk':[u'Phòng',u'Phòng máy'],
                                                                         'key_tti':u'Phòng',
                                                                          key_ltk_dc:[u'Vị trí lắp đặt'],
                                                                          key_ltk_dc2:[u'Vị trí lắp đặt'],
                                                                          key_tti_dc:[u'''Vị trí
    đặt'''],
                                                                         },
                                                              'key':True,'required': True,
                                                              'sheet_allow_this_field_not_has_exel_col':{'key_ltk':[u'XFP, SFP các loại']},
                                                              'allow_not_match_xl_title':True,
                                                              }),
                                                    ('location_id',{'required':True,
                                                                    'func':lambda val,needdata: needdata['vof_dict']['location_id_goc_dc']['val'],
                                                                     'key':True}),
                                                    
                                                    ('department_id',{
                                                                      'valid_field_func':None if is_admin_cal else check_if_your_department_in_location_1_2_3_4_5_ ,
                                                                      'key':True,
                                                                      'model':'hr.department', 
                                                                      'func':lambda v,n,self: n['vof_dict']['location_id_goc_dc']['obj'].department_id.id,
                                                                      'required':True}),
    #                                                                 ('department_id',{'key':True,'model':'hr.department', 'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val'],'required':True,'raise_if_False':True}),
                                                   
                                                    ('stock_type',{'set_val':'phong_may'}),
                                                    ]
                                           }), 
    ('location_id2_dc',{'skip_this_field':{sml:False, all_key_tram:True}, 
                        'model':'stock.location', 'for_excel_readonly':True,
                                               'fields':[
                                                        ('name',{'func':convert_float_location_,
                                                                 'xl_title':{
                                                                                 sml:[u'Tủ điều chuyển']
                                                                             },
                                                                  'key':True,'required': True,'allow_not_match_xl_title':True,}),
                                                        ('location_id',{'required':True,'func':lambda val,needdata: needdata['vof_dict']['location_id1_dc']['val'] or  needdata['vof_dict']['location_id_goc_dc']['val']  , 'key':True}),
                                                        ('department_id',{
                                                                      'valid_field_func':None if is_admin_cal else check_if_your_department_in_location_1_2_3_4_5_,
                                                                      'key':True,
                                                                      'model':'hr.department', 
                                                                      'func':lambda v,n,self: n['vof_dict']['location_id_goc_dc']['obj'].department_id.id,
                                                                      'required':True}),
                                                        ('stock_type',{'set_val':'tu'}),
                                                        
                                                        ]
                                               }),                                           
    ('location_id3_dc',{'skip_this_field':{sml:False, all_key_tram:True},
                         'model':'stock.location', 'for_excel_readonly':True,
                                           'fields':[
                                                    ('name',{'func':convert_float_location_,
                                                             'xl_title':{
                                                                             sml:[u'Shelf điều chuyển']
                                                                             },
                                                              'key':True,'required': True,'allow_not_match_xl_title':True,}),
                                                    ('location_id',{'required':True,
                                                                    'func':lambda val,needdata: needdata['vof_dict']['location_id2_dc']['val'] or needdata['vof_dict']['location_id1_dc']['val'] or  needdata['vof_dict']['location_id_goc_dc']['val'], 'key':True}),
                                                    ('department_id',{
                                                                       'valid_field_func':None if is_admin_cal else check_if_your_department_in_location_1_2_3_4_5_,
                                                                      'key':True,
                                                                      'model':'hr.department', 
                                                                      'func':lambda v,n,self: n['vof_dict']['location_id_goc_dc']['obj'].department_id.id,
                                                                      'required':True}),
                                                    ('stock_type',{'set_val':'shelf'}),
                                                    
                                                    ]
                                           }),         
    ('location_id4_dc',{'skip_this_field':{sml:False,all_key_tram:True},
                        'model':'stock.location', 'for_excel_readonly':True,'allow_not_match_xl_title':True,
                                           'fields':[
                                                    ('name',{'func':convert_float_location_,
                                                             'xl_title':{
                                                                             sml:[u'STT trong shelf điều chuyển']
                                                                            },   
                                                      'key':True,'required': True,'allow_not_match_xl_title':True}),
                                                    ('location_id',{'func':lambda val,needdata: needdata['vof_dict']['location_id3_dc']['val'] or needdata['vof_dict']['location_id2_dc']['val'] or needdata['vof_dict']['location_id1_dc']['val'] or  needdata['vof_dict']['location_id_goc_dc']['val'], 'key':True}),
    #                                                                 ('department_id',{'required':True,'key':True,'model':'hr.department', 'func': lambda v,n:n['vof_dict']['department_id_for_excel_readonly']['val'],'required':True,'raise_if_False':True}),
                                                    
                                                    ('department_id',{
                                                                       'valid_field_func':None if is_admin_cal else check_if_your_department_in_location_1_2_3_4_5_,
                                                                      'key':True,
                                                                      'model':'hr.department', 
                                                                      'func':lambda v,n,self: n['vof_dict']['location_id_goc_dc']['obj'].department_id.id,
                                                                      'required':True}),         
                                                    ('stock_type',{'set_val':'stt_trong_self'}),
                                                    ]
                                           }),  
    ('location_id5_dc',{'skip_this_field':{sml:False, all_key_tram:True},
                       'model':'stock.location', 
                       'for_excel_readonly':True,
                               'fields':[
                                        ('name',{
                                                'func':convert_float_location_,
                                                'xl_title':{
                                                            sml:[u'Slot điều chuyển']
                                                            },        
                                                'key':True,'required': True,
                                                'allow_not_match_xl_title':True,
                                                }),
                                        ('location_id',{'required':True,
                                                         'valid_field_func':None if is_admin_cal else check_if_your_department_in_location_1_2_3_4_5_,
                                                        'func':lambda val,needdata: needdata['vof_dict']['location_id4_dc']['val'] or needdata['vof_dict']['location_id3_dc']['val'] or needdata['vof_dict']['location_id2_dc']['val'] or needdata['vof_dict']['location_id1_dc']['val'] or  needdata['vof_dict']['location_id_goc_dc']['val'], 'key':True}),
                                        ('stock_type',{'set_val':'slot',
                                                       
                                                       }),
                                        ('department_id',{
                                                                      'key':True,
                                                                      'model':'hr.department', 
                                                                      'func':lambda v,n,self: n['vof_dict']['location_id_goc_dc']['obj'].department_id.id,
                                                                      'required':True}),
                                        ]
                               }),     
                    
                    
                    
                    
#     ('location_id_dc',{'for_excel_readonly':True, 'skip_this_field':{sml:False, all_key_tram:True}, 
#                             'func':lambda v,needdata: needdata['vof_dict']['location_id5_dc']['val'] or
#                                                                 needdata['vof_dict']['location_id4_dc']['val'] or \
#                                                                 needdata['vof_dict']['location_id3_dc']['val'] or \
#                                                                 needdata['vof_dict']['location_id2_dc']['val'] or \
#                                                                 needdata['vof_dict']['location_id1_dc']['val'] or \
#                                                                 needdata['vof_dict']['location_id_goc_dc']['val']
#                             }
#      ),
    ('location_dest_id',{'skip_this_field':{sml:False, all_key_tram:True}, 
                                'func':lambda v,needdata: needdata['vof_dict']['location_id5_dc']['val'] or
                                                                needdata['vof_dict']['location_id4_dc']['val'] or \
                                                                needdata['vof_dict']['location_id3_dc']['val'] or \
                                                                needdata['vof_dict']['location_id2_dc']['val'] or \
                                                                needdata['vof_dict']['location_id1_dc']['val'] or \
                                                                needdata['vof_dict']['location_id_goc_dc']['val'] or \
                                                                self.location_dest_id.id }),
    ('picking_id',{'skip_this_field':{sml: False,
#                                             sml:True if check_file else False,
                                            all_key_tram:True},
                        'key':True,'required':True,
                        'func':lambda v,n:n['self'].id,
                   }),
    ('product_uom_id',{'skip_this_field':{sml:False,all_key_tram:True}, 
                       'required_when_check_file':{sml:False},
                        'func':product_uom_id_,
                       }),
    
    ('tinh_trang',{'skip_this_field':{sml:False, all_key_tram:True},
                    'set_val': {all_key_tram:u'tot',  sml:None},'xl_title':  {all_key_tram:None,  sml:[u'T/T',u'Tình trạng']},
                   'allow_not_match_xl_title':True,
                   'func':tinh_trang_}),
    ('ghi_chu',{
                'xl_title':u'ghi chú',
                'func': {'sml':ghi_chu_cho_sml_,
                         all_key_tram:convert_float_to_ghi_chu_cho_sml_ngay_xuat,
                         },
                'allow_not_match_xl_title':True,
                 }),
    
    ('prod_lot_id', {'key':True,
                     'offset_write_xl':{all_key_tram:3},
                     'required_force':{all_key_tram:False, key_137:True},
                     'transfer_name':{sml:'lot_id'},
                     'string':u'Serial number',
                     'func_map_database_existence':func_map_database_existence_for_lot_id_,
                      'fields':[('name',{'key':True, 'type_allow':[int],
                                            'required':True,
                                            'required_when_check_file':False,
                                            'operator_search':'=ilike',
                                            'func':{all_key_tram:lambda v, needdata: needdata['vof_dict']['prod_lot_id_excel_readonly']['val'],
                                                     key_ltk_dc:lot_name_key_ltk_dc_,
                                                     }
                                             }),
                                    ('barcode_sn',{'skip_this_field':{key_ltk_dc:False, all_key_tram:True}, 'func':lambda v,n:n['vof_dict']['barcode_for_first_read']['val'], 'key':True}),
                                    ('id_ke_toan',{'skip_this_field':{key_ltk_dc2:False, all_key_tram:True}, 'key':False, 'xl_title':[u'ID - Không sửa cột này']}),
                                    ('the_tai_san',{'skip_this_field':{key_ltk_dc2:False, all_key_tram:True}, 'key':False,'xl_title':[u'Số thẻ']}),
                                    ('product_id',{'key': True, 'required':False, 'func':lambda v,n:n['vof_dict']['product_id']['val']}),
                                    ('tinh_trang',{'skip_this_field':{sml:True,all_key_tram:False},
                                                       'set_val': {all_key_tram:u'tot',  sml:None},
                                                       'xl_title':  {all_key_tram:None,  sml:[u'T/T',u'Tình trạng']},
                                                       'allow_not_match_xl_title':True,
                                                       'func': tinh_trang_
                                                   }),
                                    ('ngay_su_dung',{'skip_this_field':{all_key_tram:True,key_ltk_dc2:False},
                                        'xl_title':[u'Ngày đưa vào SD'],
                                        'func':lambda v,n: convert_float_to_ghi_chu_cho_sml_ngay_xuat_2(v)}),
                                    ('ghi_chu_ban_dau',{'write_field':False,'xl_title':[u'Ghi chú - Mô tả thêm',u'Ghi chú'], 'func':lambda v,n: convert_float_to_ghi_chu_cho_sml_ngay_xuat(v),'allow_not_match_xl_title':True}),
                                    ('ghi_chu_ngay_nhap',{'skip_this_field':{all_key_tram:False,key_137:False},'xl_title':[u'NHẬP',u'Ngày nhập'],'allow_not_match_xl_title':True,'func':lambda v,n: convert_float_to_ghi_chu_cho_sml_ngay_xuat(v),'allow_not_match_xl_title':True}),
                                    ('ghi_chu_ngay_xuat',{'skip_this_field':{all_key_tram:False,key_137:False},'xl_title':[u'XUẤT',u'Ngày xuất'],'allow_not_match_xl_title':True,'func':lambda v,n: convert_float_to_ghi_chu_cho_sml_ngay_xuat(v),'allow_not_match_xl_title':True}),
                          ]
                      }
     ),
   
                                     ]
                    },#End stock.inventory.line'
    }                        
    return ALL_MODELS_DICT[u'stock.inventory.line.tong.hop.ltk.dp.tti.dp']




def lot_name_key_ltk_dc_(val,needdata,self):
    product_id = needdata['vof_dict']['product_id']['obj']
    lot_name = needdata['vof_dict']['prod_lot_id_excel_readonly']['val'] or (needdata['vof_dict']['barcode_for_first_read']['val'] and  ('use barcode ' + needdata['vof_dict']['barcode_for_first_read']['val']))
    if  (lot_name ==False and  product_id.tracking=='serial'):
        lot_name = 'unknown ' + product_id.name + '  ' + str(int(needdata['vof_dict']['stt']['val']) )
    return lot_name
def convert_float_location_(v,n):
    if isinstance(v, float):
        v= str(int(v))
    if  v != False and isinstance(v, int):
        v = str(v)
    return v
def func_pre_func_location_id_1_ltk_dp_xfp_(v,n,self):
    if  n['sheet_name']== u'XFP, SFP các loại':
        return u'Phòng máy 3'
    else:
        return v
def convert_float_to_ghi_chu_cho_sml_ngay_xuat(val):
    if isinstance(val, float):
        seconds = (val - 25569) * 86400.0
        try:
            val= datetime.datetime.utcfromtimestamp(seconds).strftime('%d/%m/%Y')
        except ValueError:# year is out of range
            pass
    return val 

def convert_float_to_ghi_chu_cho_sml_ngay_xuat_2(val):
    if isinstance(val, float):
        seconds = (val - 25569) * 86400.0
        val= datetime.datetime.utcfromtimestamp(seconds).strftime('%d/%m/%Y')
    return val 
def name_of_uom_id_(v,n):
    v = u'Cái' if n['sheet_name']== u'XFP, SFP các loại' else v
    if isinstance(v,str):
        v = v.capitalize()
    return v
def uom_id_137_(v,n):
    if isinstance(v,str):
        v = v.capitalize()
    else:
        v = u'Cái'
    return v
SHEET_CONVERT = {'TTI':{u'CHUYỂN MẠCH':u'Chuyển Mạch (IMS, Di Động)',u'IP':u'IP (VN2, VNP)',u'TRUYỀN DẪN':u'Truyền dẫn',u'GTGT': u'GTGT',u'VÔ TUYẾN' :u'Vô tuyến'}}
SHEET_CONVERT_2_BC = {u'Chuyển Mạch (IMS, Di Động)':u'Chuyển mạch',u'IP (VN2, VNP)':u'IP'}
def categ_id_tti_convert_to_ltk_(v,n,tram=None):
    v =  n['sheet_name']
    tram_dict = SHEET_CONVERT.get(tram)
    if tram_dict:
        categ_theo_ltk =  tram_dict.get(v,v)
        return categ_theo_ltk
    else:
        return v
    
###them self

def location_from_key_tram(v,n,self):
    key_tram = n['key_tram']
    key_tram_split = key_tram.split('_')
    tram = key_tram_split[1]
    if 'dc'  in key_tram:
        stock_location_name = tram +u' đang chạy'
    else:
        stock_location_name = tram +u' dự phòng'
    
    stock_location_id =  self.env['stock.location'].search([('name','=ilike',stock_location_name)])
    if not stock_location_id:
        raise UserError ( u' Không tồn tại stock_location ')
    return stock_location_id
def look_department_from_key_tram_(v,n,self):
    key_tram = n['key_tram']
    key_tram_split = key_tram.split('_')
    tram = key_tram_split[1]
    stock_location_id =  self.env['hr.department'].search([('name','ilike',tram)])
    return stock_location_id.id
    
def location_goc_(v,n,self):
    obj = location_from_key_tram(v,n,self)
    return obj, obj.id

def check_location_id_is_same_in_bb_(val,obj,needdata,self):
    if obj:
        if obj != self.location_id:
            raise UserError(u'Kho nguồn ở file excel khác với kho nguồn ở biên bản ')
def check_if_your_depart_of_lc_goc_(val,obj,needdata,self):
    if obj:
        if obj.department_id != self.env.user.department_id:
                raise UserError(u'Kho kiểm kê không thuộc đơn vị của bạn')
def check_if_your_department_in_location_1_2_3_4_5_(v,o,n,self):
        if v != self.env.user.department_id.id:
            raise UserError (u'với users role, Muốn tạo  hay get địa điểm điều chuyển con của địa điểm gốc, thì department_id phải giống với user.department_id')

    
def check_location_id_is_same_in_bb_dc_(val,obj,needdata,self):
    if obj:
        if obj != self.location_dest_id:
            raise UserError(u'Kho đích trong excel không bằng  kho đích trong biên bản')
        
    
# def location_goc_sml_(v,n,self):
#     if v == False:
#         return self.location_id.id
#     else:
#         return v
#         
# def choose_inventory_id_name(v,n,self):
#     stock_location_id = location_from_key_tram(v,n,self)
#     return stock_location_id.name + '-' +  ','.join(n['sheet_names'])

def gen_inventory_name(v,n,self):
    if not n.get('saved_in_needdata_of_inventory_id') :
        stock_location_id_name = n['vof_dict']['location_id_goc']['obj'].name
        return stock_location_id_name + '-' +  ','.join(n['sheet_names'])
    else:
        return False



    
    
#copy ngoai
def convert_integer(val,needdata):
    try:
        return int(val)
    except:
        return 0
def qty_(val,n):
    if val:
        try:
            val = float(int(val))
            val=  1.0 if  (n['vof_dict']['prod_lot_id_excel_readonly']['val'] and val > 1) else val
        except ValueError as e:
            if n['check_file']:
                return 0
            else:
                raise ValueError(e)
    return val

def qty_137_(val,n):
    if val !=0:
        val =1
    return val


def stt_(v,n):
    if isinstance(v, str):
        try:
            v = int(v)
            return v
        except :
            return False
    else:
        return v
    
def tinh_trang_(v,n):
    if v ==None or v ==u'Tốt' or v==u'tot' or v ==False:
        return u'tot'
    else:
        return u'hong'
def ghi_chu_cho_sml_(v,n,self):
    if getattr(self, 'allow_cate_for_ghi_chu',False):
        return n.get('cate',False)#n['cate']#
    else:
        return v
# def name_replace_(v,n,self):
#     v = n['vof_dict']['prod_lot_id']['fields']['pn_id']['fields']['name']['val'] 
#     print ('val****',v)
#     if isinstance(v,str):
#         v = re.sub('[-_ \s]','',v)
#     return v
# def ghi_chu_cho_sml_cate_all_key_tram_(v,n,self):
#     if True:#getattr(self, 'allow_cate_for_ghi_chu',False):
#         return n.get('cate',False)
#     else:
#         return False
    
def def_pn_(val,n,self):
    print ('****************val of pn', val)
    dk = ( isinstance(val,float) or isinstance(val,int))
    if val and dk:
        val = str(int(val)) 
    return val
def pn_replace_(v,n,self):
    v = n['vof_dict']['product_id']['fields']['pn']['val'] 
    if isinstance(v,str):
        v = pn_replace(v)
    return v
def product_id_(v,n,self):
    if v==False:
        v = n['vof_dict']['product_id']
        v = v.get('val',False)
    return v
def break_condition_func_for_main_instance_(needdata):
    needdata ['cate'] = needdata['vof_dict']['product_id_name_readonly']['val']
def tracking_write_func_(**kargs):
    val =  kargs['val']
    if val =='none':
        return 'continue'


def prod_lot_id_excel_readonly_for_search_(v,n,self):
    prod_lot_id_excel_readonly_name = n['vof_dict']['prod_lot_id_excel_readonly']['val']
    lot_obj = self.env['stock.production.lot']
    if prod_lot_id_excel_readonly_name:
        prod_lot_id_excel_readonly_for_search = lot_obj.search([('name', '=', prod_lot_id_excel_readonly_name)])
    else:# False
        prod_lot_id_excel_readonly_for_search = None
    return prod_lot_id_excel_readonly_for_search
 

def func_map_database_existence_for_product_(n,self): 
    prod_lot_id_excel_readonly_for_search = n['vof_dict']['prod_lot_id_excel_readonly_for_search']['val']
    if prod_lot_id_excel_readonly_for_search:
        exist_product =  prod_lot_id_excel_readonly_for_search.product_id
    else:
        exist_product =  None
    return exist_product

def func_map_database_existence_for_lot_id_(n,self): 
    prod_lot_id_excel_readonly_for_search = n['vof_dict']['prod_lot_id_excel_readonly_for_search']['val']
    return prod_lot_id_excel_readonly_for_search
  
    
    
    
    
def func_check_if_excel_is_same_existence_for_product_id_(get_or_create, searched_obj, exist_val):#bool(searched_obj), searched_obj, obj
    if not get_or_create:
        raise UserError(u'Tồn tại existence nhưng excel data không khớp, tức là get_or_create = create')
    else:
        if exist_val not in searched_obj:
            raise UserError(u'Tồn tại existence, tồn tại excel data ( sau khi search) nhưng search(%s,%s) != existence (%s,%s)   '%(searched_obj.name, searched_obj.pn, exist_val.name, exist_val.pn))
    
def product_uom_id_(v,n,self):
    pr_id = n['vof_dict']['product_id']['val']
    if pr_id != None:
        uom_id = self.env['product.product'].browse(pr_id ).uom_id.id
    else:
        uom_id =None
    return uom_id
        
def product_id_name_(v,n,self):
    v= n['vof_dict']['product_id_name_readonly']['val'] 
    v = str(int(v)) if  isinstance(v, float) else v
    return v
def product_id_137_(v,n,self):
    v= n['vof_dict']['product_id_name_readonly']['val'] or n['vof_dict']['ma_vat_tu_readonly']['val']
    v = str(int(v)) if  isinstance(v, float) else v
    return v


def search_func_for_product_id_(self, model_dict, setting):
    PR = self.env['product.product']
    st_is_allow_empty_xldata_pn_is_unique_same_name_product = setting['st_is_allow_empty_xldata_pn_is_unique_same_name_product']
    st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr = setting['st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr']
    product_name =  model_dict['fields']['name']['val']
    pn_replace = model_dict['fields']['pn_replace']['val']
    print ('hahaaaaaaaaaaaa search func**** product_name:%s - pn_replace :%s- pn:%s'%(product_name, pn_replace, model_dict['fields']['pn']['val']))
    if not pn_replace:
#         raise UserError('not pn_replace')
        pr = self.env['product.product'].search([('name', '=', product_name),('pn', '=', False)])
        if pr:
            return pr
        if st_is_allow_empty_xldata_pn_is_unique_same_name_product:
            pr = self.env['product.product'].search([( 'name', '=', product_name)])
            if len(pr)==1 :
                return pr
        return PR
    else:
        pr = self.env['product.product'].search([('pn_replace','=',pn_replace)])
        print ('**** pr :%s'%pr)
        if pr:
            return pr
        if st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr:
            pr = self.env['product.product'].search([('name','=',product_name), ('pn','=',False)])
            if pr:
                return pr
        return PR
    
        
        

        
def location_id6_chua_ro_(v,needdata,self):    
    v_all = needdata['vof_dict']['location_id5']['val'] \
                or needdata['vof_dict']['location_id4']['val'] or \
                needdata['vof_dict']['location_id3']['val'] or \
                needdata['vof_dict']['location_id2']['val'] or \
                needdata['vof_dict']['location_id1']['val']
    if  v_all ==False:
        return u'Chưa rõ'
    else:
        return False
def or_7_location_id_(v,needdata):
    return needdata['vof_dict']['location_id6'].get('val') or \
                needdata['vof_dict']['location_id5']['val'] or \
                needdata['vof_dict']['location_id4']['val'] or \
                needdata['vof_dict']['location_id3']['val'] or \
                needdata['vof_dict']['location_id2']['val'] or \
                needdata['vof_dict']['location_id1']['val'] or \
                needdata['vof_dict']['location_id_goc']['val']

def location_id_for_sml_(v,n,self):
    lc_id =  or_7_location_id_(v,n)
    if lc_id == False:
        return self.location_id.id
    else:
        return lc_id

    
def inv_id_(v, n, self, import_from_inventory=None):       
    if  import_from_inventory:
        return self.id
    return n.setdefault('saved_in_needdata_of_inventory_id',v)

def department_for_sml_and_mode2_(v,n,self):
    return self.env['stock.location'].browse(n['vof_dict']['location_id_goc']['val']).department_id.id
#     return n['vof_dict']['location_id_goc']['obj'].department_id.id

def sheet_for_ltk_(self,wb, gen_model_dict_kargs):
    if gen_model_dict_kargs.get('cach_tim_location_goc',u'find_origin_location_by_key_tram') == u'find_origin_location_by_key_tram':
        return [u'Truyền dẫn',u'IP (VN2, VNP)',u'GTGT',u'Chuyển Mạch (IMS, Di Động)',u'Vô tuyến',u'XFP, SFP các loại']if not self.sheet_name else [self.sheet_name]
    else:
        sheet_name = getattr(self, 'sheet_name',None)
        if sheet_name ==u'all' or sheet_name ==u'All':
            return wb.sheet_names()
        elif sheet_name:
            return [self.sheet_name]
        else:
            return [wb.sheet_names()[0]]
            
def if_self_sheet_name(sheet_name,wb):
    if sheet_name ==u'all' or sheet_name ==u'All':
        return wb.sheet_names()
    return [sheet_name]

def check_file_write_more_check_searched_obj_product_(self,field_MD,searched_obj,*arg,**kargs):
    collection_dict = arg[0]
#     break_field = needdata['collection_dict']['break_field']
    rs = searched_obj
    
    print ('***rs', rs)
    show_val = common_show_write_searched_obj(rs, u'No searched_obj', collection_dict)
    return show_val
def common_show_write_searched_obj(rs, no_obj_show, collection_dict):
    if rs:
        show_val = str(rs.mapped('id'))
    elif rs == None:
        break_field = collection_dict['break_field']
        show_val = u'break do cell trống:%s'%break_field
    else:
        show_val = no_obj_show
    return show_val


def common_show_write(rs, no_obj_show ):
    if rs:
        show_val = str(rs.mapped('id'))
    elif rs == False:
        show_val = u'Empty cell'
    elif rs == None:
#         show_val = u'không thấy obj do có searched field == None'
        show_val = u'break do cell trống'
    else:
        show_val = no_obj_show
    return show_val
    
def check_file_write_more_check_name_product_(self, field_MD,*arg, **kargs):
    name = field_MD['fields']['name']['val']
    if name:
        rs = self.env['product.product'].search([('name', '=ilike', name)])
    else:
        rs = False
    show_val = common_show_write(rs, u'No pr has name' )
    return show_val

def check_file_write_more_check_PN_product_(self, field_MD,*args, **kargs):
    pn_replace = field_MD['fields']['pn_replace']['val']
    if pn_replace:
        rs = self.env['product.product'].search([('pn_replace', '=ilike', pn_replace)])
    else:
        rs = False
    show_val = common_show_write(rs, u'No pr has pn' )
    return show_val

def check_file_write_more_check_name_and_PN_product_(self, field_MD,*arg, **kargs):
    name = field_MD['fields']['name']['val']
    pn_replace = field_MD['fields']['pn_replace']['val']
    rs = self.env['product.product'].search([('name', '=ilike', name), ('pn_replace', '=ilike', pn_replace)])
    show_val = common_show_write(rs, u'No pr has name and pn')
    return show_val



    
default_import_xl_setting = {
            'default_st_allow_func_map_database_existence':True,
             'default_st_is_allow_write_existence':True,
             'default_st_allow_check_if_excel_is_same_existence':False,
             'default_st_is_allow_empty_xldata_pn_is_unique_same_name_product':False,
             'default_st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr':False,
             }


all_key_tram = 'all_key_tram'
key_ltk_dc = 'key_ltk_dc'
key_ltk_dc2 = 'key_ltk_dc2'
key_tti_dc = 'key_tti_dc'
key_137 = 'key_137'
write_xl = 'write_xl'
sml = 'sml'
key = 'key',
required = 'required' 
