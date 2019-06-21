 # -*- coding: utf-8 -*-
from odoo.exceptions import UserError
import datetime

def gen_model_dict_categ_and_location_partner():
    user_model_dict = {
               
        u'location partner': {
                'title_rows' : [0], 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names': [u'Location Partner'],
                'model':'stock.location',
                'fields' : [
                         ('name',{'func':None,'xl_title':u'Name','key':True,'required':True}),
                         ('usage',{'set_val':'supplier'}),
                         ('is_kho_cha',{'set_val':True}),
                         ('department_id',{'set_val':False}),
                         ('cho_phep_khac_tram_chon',{'set_val':True}),
                         ('not_show_in_bb',{'func':lambda v,n: True if v else False,'xl_title':u'not_show_in_bb','for_excel_readonly':True}),
                         ('partner_id_of_stock_for_report',{
                             'fields':[('name',{'func': lambda v,n:not n['vof_dict']['not_show_in_bb']['val'] and n['vof_dict']['name']['val'], 'key':True,'required':True}),
                                                       ]
                                            }
                         ),
                      ]
                },#location partner
                       
        u'categ': {
                'title_rows' : [0], 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names': [u'categ'],
                'model':'product.category',
                'fields' : [
                         ('name',{'func':None,'xl_title':u'Name','key':True,'required':True}),
                         ('stt_for_report',{'func':None,'xl_title':u'stt_for_report','required':True,'type_allow':[float]}),
#                          ('usage',{'set_val':'supplier'}),
#                          ('is_kho_cha',{'set_val':True}),
#                          ('cho_phep_khac_tram_chon',{'set_val':True}),
#                          ('partner_id_of_stock_for_report',{'fields':[('name',{'func': lambda v,n:n['vof_dict']['name']['val'], 'key':True,'required':True}),
#                                                        ]
#                                             }
#                          ),
                      ]
                },#location partner
                       
        
     
                              
                   }
                   
    return user_model_dict
    

                