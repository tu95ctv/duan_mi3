 # -*- coding: utf-8 -*-
from odoo.exceptions import UserError
import datetime
# from odoo.addons.importexcel.mytools import convert_float_to_ghi_chu_ngay_xuat,lot_name_
 
from odoo.addons.importexcel.models.model_dict_folder.model_dict import convert_float_to_ghi_chu_ngay_xuat

def gen_product_model_dict():
    user_model_dict = {
         u'Product':
              {
                   'title_rows' : [0], 
                   'begin_data_row_offset_with_title_row' :1,
                   'sheet_names': lambda self:[u'Tá»•ng há»£p']if not self.sheet_name else [self.sheet_name],
                   'model':'product.product',
                   'for_create_another' :True,
                   'fields' : [
                           ('stt',{'func':None,'xl_title':u'STT','key':True,'required':True,'skip_field_if_not_found_column_in_some_sheet':True,'for_excel_readonly' :True}),
                           ('prod_lot_id_excel_readonly',{'empty_val':[u'N/C',u'-',u'--',u'NA',u'N/A',u'chÆ°a Ä‘á»�c Ä‘Æ°á»£c SN'],'func':lambda val,needdata: int(val) if isinstance(val,float) else val,'xl_title':[u'Sá»‘ serial (S/N)',u'serial number'],'for_excel_readonly' :True}),
                           ('barcode_for_first_read',{'empty_val':[u'NA',u"'",u"`"],'func':lambda val,needdata: str(int(val)) if isinstance(val,float) else val,'xl_title':[u'Barcode'],'for_excel_readonly' :True}),
                           ('product_id',{ 'for_excel_readonly' :True,'model':'product.product',
                            'fields':[   
                           ('name',{'func':None,'xl_title':[u'Loáº¡i card'],'key':True,'required':True,'empty_val':[]}),
                           ('type',{'set_val':'product'}),
                              
                           ('dang_chay_tao',{'set_val':True}),
                           ('tram_ltk_tao',{'set_val':True}),
                              
                           ('tracking',{'func':lambda val,needdata: 'serial' if (needdata['vof_dict']['prod_lot_id_excel_readonly']['val'] or needdata['vof_dict']['barcode_for_first_read']['val']) !=False else False,'bypass_this_field_if_value_equal_False':True}),
                           ('thiet_bi_id',{'model':'tonkho.thietbi', 'fields':[('name',{'func':None,'xl_title':u'TÃªn há»‡ thá»‘ng thiáº¿t bá»‹', 'key':True,'required': True}),]}),
                           ('categ_id',{'model':'product.category','fields':[('name',{'func':lambda val,needdata: needdata['sheet_name'], 'key':True,'required': True}),]}),
                           ('uom_id',  {'model':'product.uom', 'fields': [ #'func':uom_id_,'default':1,
                                       ('name',{'set_val':u'CÃ¡i','key':True}),#'set_val':u'CÃ¡i',
                                                ('category_id', {'func': lambda n,v,self:self.env['product.uom.categ'].search(['|',('name','=','Unit'),('name','=',u'Ä�Æ¡n vá»‹')])[0].id
                                                                           }
                                                    ),
                            
                                                          ]
                                               }
                            ),
                               ]
                            }),
                                  
                                  
                           ('prod_lot_id_readexcel', {'for_excel_readonly' :True,'model':'stock.production.lot',
                     'fields':[
                       ('name',{'func':lot_name_ ,'key':True,'required':True}),
                       ('barcode_sn',{'func':lambda v,n:n['vof_dict']['barcode_for_first_read']['val'] ,'key':True}),
                       ('product_id',{'func':lambda v,n:n['vof_dict']['product_id']['val'] ,'key':True,'required':True}),
#                        ('pn_id',{'model':'tonkho.pn',
#                                                      'fields':[
#                                                                ('name',{'empty_val':[u'NA',u'-',u'--'],'xl_title':[u'MÃ£ card (P/N)',u'part number'],'key':True, 'required':True}),
#                                                                ('product_id',{'func':lambda v,n:n['vof_dict']['product_id']['val'] , 'key':True  }),
# #                                                                ('import_location_id',{'set_val':lambda self:self.import_location_id.id}),
#                                                                ('dang_chay_tao',{'set_val':True}),
#                                                                ('tram_ltk_tao',{'set_val':True}),
#                                                                   
#                                                                ]
#                                                      }),
                       ('ghi_chu_ngay_nhap',{'xl_title':[u'NÄƒm sá»­ dá»¥ng'], 'func':lambda v,n: convert_float_to_ghi_chu_ngay_xuat(v)}),
                       ('ghi_chu_ban_dau',{'xl_title':[u'Ghi chÃº - MÃ´ táº£ thÃªm'], 'func':lambda v,n: convert_float_to_ghi_chu_ngay_xuat(v)}),
#                        ('pn',{'empty_val':[u'NA','-','--'],'xl_title':[u'MÃ£ card (P/N)']}),
                         ]
                     }),
                                  
                         ]
                   },#End product
                       
                       
        
                   }
    return user_model_dict
    

                