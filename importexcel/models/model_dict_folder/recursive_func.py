 # -*- coding: utf-8 -*-
from odoo.addons.importexcel.models.model_dict_folder.tool_tao_instance import get_key,get_width,VERSION_INFO
from odoo.addons.downloadwizard.models.dl_models.dl_model  import header_bold_style
from collections import  OrderedDict
from odoo.exceptions import UserError
import re
import operator
from odoo import _
   

ATT_TYPE_LIST ={
  'fields':['collections.OrderedDict'],
  'default_val':[],
  'begin_data_row_offset_with_title_row': ['int'],
  'break_condition_func_for_main_instance': ['NoneType', 'function'],
  'bypass_this_field_if_value_equal_False': ['bool'],
  'inactive_include_search': ['bool'],
  'st_is_x2m_field': ['bool'],
  'remove_all_or_just_add_one_x2m': ['bool','str'],
  'bypass_this_field_if_value_equal_False_default': ['bool'],
  'st_write_false':['bool'], 
  'write_false':['bool'], 
  'col_index': ['int', 'NoneType'],
  'empty_val': ['list', 'NoneType'],
  'for_excel_readonly': ['bool'],
  'func': ['function', 'NoneType'],
  'func_check_if_excel_is_same_existence': ['function'],
  'func_map_database_existence': ['function'],
  'func_pre_func': ['function'],
  'karg': ['dict'],
  'key': ['bool', 'str'],
  'key_allow': ['bool'],
  'last_import_function': ['NoneType', 'function'],
  'last_record_function': ['NoneType', 'function'],
  'model': ['str'],
  'offset_write_xl': ['int'],
  'offset_write_xl_2': ['int'],
  'offset_write_xl_diff': ['int'],
  'offset_write_xl_for_searched_obj': ['int'],
  'check_file_write_more': ['list'],

  'only_get': ['bool'],
  'operator_search': ['str'],
#   'prepare_func': ['function'],
  'required_pre': ['bool'],
  'print_if_write': ['bool'],
  'print_write_dict_new': ['bool'],
  'raise_if_False': ['bool'],
  'raise_if_diff': ['bool'],
  'replace_string': ['list'],
  'replace_val': ['dict'],
  'required': ['bool'],
  'required_force': ['bool'],
  'required_when_check_file': ['bool'],
  'requried': ['bool'],
  'search_func': ['function'],
  'remove_out_item_func': ['function'],
  'set_is_largest_map_row_choosing': ['bool'],
  'set_val': ['str', 'function', 'int', 'NoneType'],
  'setting': ['dict'],
  'setting2': ['dict'],
  'sheet_allow_this_field_not_has_exel_col': ['list'],
  'sheet_names': ['function','list'],
  'allow_not_match_xl_title': ['bool', 'NoneType'],
  'skip_this_field': ['bool'],
  'BreakRowException_if_raise_only_get': ['bool'],
  'string': ['str'],
  'title_rows': ['range', 'list'],
  'title_rows_some_sheets': ['dict'],
  'transfer_name': ['str'],
  'type_allow': ['list'],
  'valid_field_func': ['function', 'NoneType'],
  'write_field': ['bool', 'NoneType'],
  'xl_title': ['list', 'NoneType', 'str']
}


  
def export_all_key_list_vals_key_list_type_of_val(MD, output_key_list_vals_dict = {}, output_key_list_type_of_vals_dict = {} , key_allow= False):
    for key,val in MD.items():
        if isinstance(val, dict) and key_allow:
            for key_tram,v in val.items():
                append_val_type_n_val_of_key (output_key_list_vals_dict, output_key_list_type_of_vals_dict,key, v)
        else:
            append_val_type_n_val_of_key (output_key_list_vals_dict, output_key_list_type_of_vals_dict,key, val)
        if key == 'fields':
            for fname, field_MD in val:
                export_all_key_list_vals_key_list_type_of_val(field_MD, output_key_list_vals_dict = output_key_list_vals_dict, output_key_list_type_of_vals_dict=output_key_list_type_of_vals_dict, key_allow=key_allow)
    return output_key_list_vals_dict, output_key_list_type_of_vals_dict

def append_val_type_n_val_of_key (output_key_list_vals_dict, output_key_list_type_of_vals_dict, key, val):
    output_key_list_vals_dict.setdefault(key,[]).append(val)
    type_of_val = str(type(val))
    rs = re.search("<class '(.*)'>",type_of_val)
    if rs:
        type_of_val = rs.group(1)
    else:
        print ('type_of_val', type_of_val)
        raise UserError('search theo partern khong ra %s'%type_of_val)
    list_of_type_of_val = output_key_list_type_of_vals_dict.setdefault(key,[])
    if type_of_val not in list_of_type_of_val:
        list_of_type_of_val.append(type_of_val)
        
def convert_name_class_to_string(val):
    type_of_val = str(type(val))
    rs = re.search("<class '(.*?)'>",type_of_val)
    if rs:
        type_of_val = rs.group(1)
    else:
        print ('type_of_val **', type_of_val)
        raise UserError(u"RE không ra dạng  <class '(.*?)'>"%type_of_val)
    return type_of_val


def convert_dict_to_order_dict_string(x):
    sorted_x = sorted(x.items(), key=lambda kv: kv[0])
    new = map(lambda kv:u"'%s':%s"%(kv[0],kv[1]),sorted_x)
    new = u', '.join(new)
    new = '{%s}'%new
    return new

###########!R0###############



# R1
def rut_gon_key(MD, key_tram): 
    for key, val in MD.items():
        
        if isinstance(val, dict) and key_tram:
            val =  val.get(key_tram) if key_tram in val else val.get('all_key_tram')
        
        MD[key] = val
        if key == 'fields' :
            for fname, field_MD in val: 
                rut_gon_key(field_MD, key_tram)
                    
# def convert_val_depend_key_tram(value, key_tram):
#     if isinstance(value, dict) and key_tram:
#         value =  value.get(key_tram) if key_tram in value else value.get('all_key_tram')
#     return value

###R2
def ordereddict_fields(MD):
    for fname, field_MD in MD['fields']:
        if 'fields' in field_MD :
            ordereddict_fields (field_MD)
    MD['fields']=OrderedDict(MD['fields'])
    
    
#R2A             
def check_val_of_attrs_is_true_type(MD):
    for attr, val in MD.items():
        if attr == 'fields':
            for field_MD in val.values():
                check_val_of_attrs_is_true_type(field_MD)
        if not check_set_val_is_true_type(attr, val):
            raise UserError (u'attr %s val %s không thỏa hàm check_set_val_is_true_type'%(attr,val))
            
            
            
#R2A1
STRING_TYPE_DICT = {str:'str' ,bool:'bool', list:'list',dict:'dict',int:'int', }       
def check_set_val_is_true_type(attr, val):
    allow_type_list = ATT_TYPE_LIST.get(attr)
    if  allow_type_list==None:
        raise UserError(u'attr:%s chưa có liệt kê  trong ATT_TYPE_LIST'%attr)
    if allow_type_list ==[]:
        return True
    if  callable(val):
        str_val_type = 'function'
    elif val == None :
        return True
    else:
        str_val_type =convert_name_class_to_string(val)
    if str_val_type not in allow_type_list:
        raise UserError (u'attr %s val %s, type:%s, không đúng dữ liệu %s'%(attr,val, str_val_type, allow_type_list))
        return False
    else:
        return True    
#R3
def add_more_attrs_to_field_MD(self, MD, field_stt = 0, setting={}):# add x2m_fields
    model_name = get_key(MD, 'model')
    OBJ = self.env[model_name]
    fields= OBJ._fields
    default_dict = OBJ.default_get(fields)
    
    for f_name, field_MD in MD.get('fields').items():
        field_stt +=1
        f_name = get_key(field_MD, 'transfer_name') or  f_name
        skip_this_field = get_key(field_MD, 'skip_this_field',False)
        if not skip_this_field:
            if f_name not in fields and not field_MD.get('for_excel_readonly'):
                raise UserError(u'f_name:"%s" không nằm trong fields, phải thêm thược tính for_excel_readonly-field_attr:%s'%(f_name, field_MD))
            st_write_false = setting['st_write_false']
            write_false = field_MD['write_false'] if 'write_false' in field_MD else st_write_false
            field_MD['write_false'] = write_false
            field_MD['field_stt'] = field_stt
            
            if not field_MD.get('for_excel_readonly') :# and not skip_this_field
                field = fields[f_name]
                field_MD['field_type'] = field.type
                if field.comodel_name:
                    field_MD['model'] = field.comodel_name
                
                if 'required' not in field_MD:
                    required_from_model = field.required
                    required_force = field_MD.get('required_force', None)
                    required = required_force or required_from_model
                    field_MD['required']= required
            
            if f_name in default_dict and field_MD.get('default_val') ==None:
                default_val = default_dict[f_name]
                field_MD['default_val']=  default_val
            
            if field_MD.get('empty_val'):
                partern_empty_val =  '^('+  '|'.join(field_MD.get('empty_val')) +')$'
                field_MD['partern_empty_val'] = partern_empty_val
            
            
            if 'st_is_x2m_field' in field_MD:
                x2m_fields = MD.setdefault('x2m_fields',[])
                x2m_fields.append(f_name)
                
            if field_MD.get('fields'):
                    field_stt = add_more_attrs_to_field_MD(self, field_MD, field_stt =  field_stt, setting=setting)
            
            
    return field_stt


 # R4        
def define_col_index_common(title_rows, sheet, COPY_MODEL_DICT, set_is_largest_map_row_choosing = False):
    if not set_is_largest_map_row_choosing:
        is_write= True
    else:
        is_write = False
    row_title_index, largest_map_row = define_col_index(title_rows, sheet, COPY_MODEL_DICT, is_write = is_write)
   
    if set_is_largest_map_row_choosing:
        lowest_row = largest_map_row -2 
        if lowest_row < 0:
            lowest_row = 0
        title_rows = range(lowest_row,largest_map_row+3)
        row_title_index, largest_map_row = define_col_index(title_rows, sheet, COPY_MODEL_DICT)
    return row_title_index, largest_map_row, title_rows
def define_col_index(title_rows, sheet, COPY_MODEL_DICT, is_write = True):
    row_title_index =None
    number_map_dict = {}
    for row in title_rows:
        if row >= sheet.nrows:
            break
        for col in range(0,sheet.ncols):
            read_excel_value = str(sheet.cell_value(row,col))
            is_read_excel_value_map_xl_title = look_up_col_index( COPY_MODEL_DICT, read_excel_value, col, is_write = is_write)
            if is_read_excel_value_map_xl_title:
                row_title_index = row
                number_map_dict[row] =number_map_dict.get(row,0) + 1
    if not number_map_dict:
        raise UserError(u'number_map_dict rỗng')
    largest_map_row = max(number_map_dict.items(), key=operator.itemgetter(1))[0]
    return row_title_index, largest_map_row

# R4-1
def look_up_col_index(MD, read_excel_value, col, is_write = True):
    is_read_excel_value_match_with_xl_title_of_MD = False
    for fname, field_MD in MD.get('fields').items():
        is_a_field_match_excel = False
        xl_title = field_MD.get('xl_title')
        col_index = field_MD.get('col_index')
#         if xl_title != None and col_index !=None:
#             raise UserError("xl_title != None and col_index !=None, fname:%s, %s"%(fname,field_MD))
        if field_MD.get('set_val') != None:
            continue
        if  col_index !=None:
            continue
        elif field_MD.get('fields'):
            is_a_field_match_excel = look_up_col_index(field_MD, read_excel_value, col, is_write = is_write)
        elif xl_title:
            xl_title_s =  xl_title if isinstance(xl_title, list) else [xl_title]
            for xl_title in xl_title_s:
                xl_title_partern = u'^%s$'%xl_title
                xl_title_partern = xl_title_partern.replace('\\','\\\\').replace('(','\(').replace(')','\)') #không thể thể hiện chuổi \ nên thể hiện bằng \\
                rs = re.search(xl_title_partern, read_excel_value, re.IGNORECASE)
                if rs:
                    if is_write:
                        field_MD['col_index'] = col
                    is_a_field_match_excel = True 
                    break    
           
        is_read_excel_value_match_with_xl_title_of_MD = is_read_excel_value_match_with_xl_title_of_MD or is_a_field_match_excel
        if is_a_field_match_excel:
            break
    return is_read_excel_value_match_with_xl_title_of_MD #or is_map_xl_title_foreinkey



#R3
def add_more_attrs_to_field_MD_after_add_col_index(self, MD, field_stt = 0, setting={}):# add x2m_fields
    for f_name, field_MD in MD.get('fields').items():
#         f_name = get_key(field_MD, 'transfer_name') or  f_name
        skip_this_field = get_key(field_MD, 'skip_this_field',False)
        if not skip_this_field:
            set_col_index = field_MD.get('set_col_index')
            if set_col_index != None:
                field_MD['col_index'] = set_col_index
            if field_MD.get('fields'):
                    field_stt = add_more_attrs_to_field_MD(self, field_MD, field_stt =  field_stt, setting=setting)
            
            




# def define_col_index(title_rows, sheet, MD):
#     title_col_dict = {}
#     for row in title_rows:
#         if row >= sheet.nrows:
#             break
#         for col in range(0, sheet.ncols):
#             read_excel_value = str(sheet.cell_value(row,col))
#             title_col_dict[read_excel_value] = {'col':col, 'row':row}
#     look_col_index_for_field_md(MD, title_col_dict)
#     
# 
# def look_col_index_for_field_md(MD, title_col_dict):
#     for field_MD in MD['fields'].values():
#         xl_titles = field_MD.get('xl_title')
#         if xl_titles and field_MD.get( 'col_index') != None:
#             if isinstance(xl_titles, str):
#                 xl_titles = [xl_titles]
#             field_map = False
#             for xl_title in xl_titles:
#                 xl_title_partern = u'^%s$'%xl_title
#                 xl_title_partern = xl_title_partern.replace('\\','\\\\').replace('(','\(').replace(')','\)') #không thể thể hiện chuổi \ nên thể hiện bằng \\                for xl_read_val, col in title_col_dict.items():
#                 for read_excel_val, col_dict in title_col_dict.items():
#                     rs = re.search(xl_title_partern, read_excel_val, re.IGNORECASE)
#                     if rs:
#                         field_map = True
#                         break
#                 if field_map:
#                     break
#             if field_map:
#                 field_MD['col_index'] = col_dict['col']
#         if 'fields' in field_MD:
#             look_col_index_for_field_md(field_MD, title_col_dict)
            
        

#R5           
def check_compatible_col_index_and_xl_title(self, MD, needdata):
    for fname, field_MD in MD.get('fields').items():
        skip_this_field = get_key(field_MD, 'skip_this_field', False)
        if not skip_this_field: 
            col_index = get_key(field_MD, 'col_index', None)
            xl_title = get_key(field_MD, 'xl_title')#moi them , moi bo field_attr.get('xl_title')
            set_val = get_key( field_MD,'set_val')
            func = field_MD.get('func')
            check_compatible_col_index_and_xl_title_for_a_field( field_MD, xl_title, col_index, set_val, needdata, fname, func)
            if field_MD.get('fields'):
                check_compatible_col_index_and_xl_title(self, field_MD, needdata)
#R51
def check_compatible_col_index_and_xl_title_for_a_field(field_attr, xl_title, col_index, set_val, needdata, field_name, func):
#         if col_index or set_val or func:
#             pass
        if xl_title and set_val:
            raise UserError("xl_title and set_val")
        if set_val != None:
            return True
        if col_index==None:
            if xl_title : # có kê xl_title nhưng mà không match
                sheet_allow_this_field_not_has_exel_col = get_key( field_attr,'sheet_allow_this_field_not_has_exel_col')
                allow_not_match_xl_title = get_key(field_attr,'allow_not_match_xl_title')
                skip_if_not_match =  allow_not_match_xl_title or (sheet_allow_this_field_not_has_exel_col and needdata['sheet_name'] in sheet_allow_this_field_not_has_exel_col)
                if not skip_if_not_match:
                    raise UserError(_(u'Excel has not column, which in %s of %s, please change column name match with them') %(xl_title, field_name))
            else:
                if field_attr.get('model'):
                    if not func and not field_attr.get('fields'):
                        raise UserError(u'model thì phải có ít nhất func và fields: %s-%s'%(field_name,field_attr))
                else:
                    if not func:
                        raise UserError (u'Sao không có col_index và không có func luôn field %s attrs %s'%(field_name,u'%s'%field_attr))
#R5A

def asmall_func(MD, fname,  sheet_ncols, offset_write_xl, sheet_of_copy_wb, title_row, surfix =u' sẵn hay tạo'):
    if offset_write_xl !=None:
        col =  sheet_ncols + offset_write_xl 
        title = 'Check ' + MD.get('string', fname)  + surfix
        sheet_of_copy_wb.col(col).width =  get_width(len(title))
        sheet_of_copy_wb.write(title_row, col, title, header_bold_style)
    
def write_get_or_create_title(MD, sheet, sheet_of_copy_wb, title_row, fname=None):
    offset_write_xl = get_key(MD, 'offset_write_xl')
    offset_write_xl_diff = get_key(MD, 'offset_write_xl_diff')
    offset_write_xl_for_searched_obj = get_key(MD, 'offset_write_xl_for_searched_obj')
    check_file_write_more = get_key(MD, 'check_file_write_more')
    fname = fname or MD.get('model')
    sheet_ncols = sheet.ncols
    for k,v in [(offset_write_xl, u' có sẵn hay phải tạo'),(offset_write_xl_for_searched_obj, u'theo cách tìm'), (offset_write_xl_diff,  u'ở excel giống hay khác trong database')]:
        asmall_func(MD, fname,  sheet_ncols, k, sheet_of_copy_wb, title_row, v)
    
#     if offset_write_xl !=None:
#         asmall_func(MD, fname,  sheet_ncols, offset_write_xl, sheet_of_copy_wb, title_row)
#     if offset_write_xl_for_searched_obj !=None:
#         col =  sheet.ncols + offset_write_xl_for_searched_obj 
#         title = MD.get('string', fname)  + u' for searched obj'
#         sheet_of_copy_wb.col(col).width =  get_width(len(title))
#         sheet_of_copy_wb.write(title_row, col, title, header_bold_style)
#     if offset_write_xl_diff != None:
#         col =  sheet.ncols + offset_write_xl_diff 
#         title = MD.get('string', fname)  + u' Diff'
#         sheet_of_copy_wb.col(col).width =  get_width(len(title))
#         sheet_of_copy_wb.write(title_row, col, title, header_bold_style)
    
    
    if check_file_write_more:
        for more_offset, func, more_title in check_file_write_more:
            col =  sheet.ncols + more_offset 
            title = more_title
            sheet_of_copy_wb.col(col).width =  get_width(len(title))
            sheet_of_copy_wb.write(title_row, col, title, header_bold_style)
            
        
    if MD.get('fields'):
        for fname, field_MD in MD.get('fields').items():
            write_get_or_create_title(field_MD, sheet, sheet_of_copy_wb, title_row, fname)
#R7        
def export_some_key_value_of_fields_MD(MD, exported_attrs_list = ['field_type','xl_title'], dict_of_att_vs_set_vals = {}):
    fields = MD['fields']
    all_field_attr_dict = {}
    for fname, field_MD in fields.items():
        attr_dict = {}
        for exported_key in exported_attrs_list:
            if exported_key in field_MD:
                val = field_MD.get(exported_key)
                attr_dict[exported_key] = val
                alist = dict_of_att_vs_set_vals.setdefault( exported_key, [])
                if val not in alist:
                    alist.append(val)
        if field_MD.get('fields') :
            all_field_attr_dict_child, dict_of_att_vs_set_vals  = export_some_key_value_of_fields_MD(field_MD, exported_attrs_list, dict_of_att_vs_set_vals)
            attr_dict['fields'] = all_field_attr_dict_child
        all_field_attr_dict[fname] = attr_dict 
    return all_field_attr_dict, dict_of_att_vs_set_vals

                   
                   



                

            
            
            

                
                        
            
            







                    
                    
                    



            

                                    
    
        
        











                

    

                
                




