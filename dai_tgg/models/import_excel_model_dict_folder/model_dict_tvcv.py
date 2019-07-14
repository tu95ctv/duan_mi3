 # -*- coding: utf-8 -*-
def convert_integer(val,needdata):
    try:
        return int(val)
    except:
        return 0
def int_catch_error_(v,n):
    try:
        v = int(v)
    except:
        v = False
    return v

def float_catch_error_(v,n):
    try:
        v = float(v)
    except:
        v = False
    return v
def gen_tvcv_model_dict():
    tvcv_dict = {
          u'Thư viện công việc': {
                'inactive_include_search':True,
                'title_rows' : range(1,4), 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':lambda self,wb: wb.sheet_names(),
                'model':'tvcv',
                'offset_write_xl':1,
                'string':'TVCV da co chua',
                'fields' : [
                        ('stt', {'xl_title': u'stt','for_excel_readonly':True, 'required':True}),
                    
                        ( 'code',{'func':None,'xl_title':u'Mã CV', 'key':True ,'required':True}),
                        ('name', {'func':None,'xl_title':u'Công việc',
                               'required':True,
                               } ),
                        ('don_vi',{'offset_write_xl_diff':2, 'fields':[
                                                ('name',{'key':True, 'required':True, 'xl_title':u'Đơn vị' }),
                                                ],'key' : False, 'required' : False}),
                            
                        ('do_phuc_tap',{'func':convert_integer,'xl_title':u'Độ phức tạp','key':False,'func':int_catch_error_, 'offset_write_xl_diff':3,}),
                        ('thoi_gian_hoan_thanh',{'offset_write_xl_diff':4, 'func':convert_integer, 'xl_title':u'Thời gian hoàn thành','key':False, 'func':int_catch_error_}),
                        ('diem',{'func':None,
                                 'xl_title':u'Điểm',
                                 'key':False,
                                 'func':float_catch_error_,
                                 'offset_write_xl_diff':5,
                                 'default_val':1,
                                 }),
                        ('dot_xuat_hay_dinh_ky',{'offset_write_xl_diff':6,'offset_write_xl':7, 'fields':[
                                                ('name',{'key':True, 'required':True,'col_index':7}),
                                                ],'key' : False,'required' : False}),  
                        ('ghi_chu',{'offset_write_xl_diff':8, 'func':None,'xl_title':u'Ghi chú','key':False}),
                                               ( 'loai_record',{'func':None,'set_val':u'Công Việc', 'key':False }),
#                         ('department_id',{'key':True,'model':'hr.department',
#                                            'func': lambda self: self.env['hr.department'].search([('name','=ilike',u'Đài HCM')]).id,
#                                            'required':True,'raise_if_False':True
#                                                                   }),
                        ( 'state',{'set_val':'confirmed'}),
                        ( 'cong_viec_cate_id',
                          {
                            'key':False,
                            'fields':[('name',{
                                'key':True,
                                'required':True,
                                'replace_string':[('Quan_ly',u'Quản lý'),('Vanhanh',u'Vận hành'),('Van_thu_hanh_chinh',u'Văn thư hành chính'),('Baocao',u'Báo cáo'),('Khac',u'Khác')],
                                'func': lambda v,n,self:n['sheet_name']})]
                            
                             }),
                            

                        ('active',{'func':lambda val, n: False if val ==u'na' else True,
                                     'xl_title':u'active','key':False,
                                     'allow_not_match_xl_title':True}),
                      ]
                },#End stock.inventory.line'   
        
         u'Loại sự cố, sự vụ': {
                'title_rows' : [0], 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':['Loại sự cố sự vụ'],
                'model':'tvcv',
                'fields' : [
                        ('name', {'func':None,'xl_title':u'Loại', 'required':True,'key':True } ),#'func_de_tranh_empty':lambda r:  len(r) > 2
                        ( 'loai_record',{'func':None,'xl_title':u'loai_record', 'key':True,'required_force':True, 'raise_if_False':True}),
                        ( 'is_bc',{'set_val':True}),
                      ]
                },#End stock.inventory.line'   
        }
    return tvcv_dict