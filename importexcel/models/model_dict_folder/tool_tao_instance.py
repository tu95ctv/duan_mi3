 # -*- coding: utf-8 -*-
import sys
import xlrd
VERSION_INFO   = sys.version_info[0]
import xlwt
import re
MAP_TYPE = {
                      'integer':[int,float],
                      'float':float, 
                      'many2one':int,
                      'char':str,
                      'selection':str,
                      'text':str, 
                      'boolean':bool,
                      'many2many':list,
                      'one2many':list,
                      
                      
                      }

def get_width(num_characters):
    return int((1+num_characters) * 256)
# not_horiz_center_border_style = xlwt.easyxf("font:  name Times New Roman, height 240 ;align: wrap on , vert centre; borders: left thin,right thin, top thin, bottom thin")
# header_bold_style = xlwt.easyxf("font: bold on, name Times New Roman, height 240 ; align:  vert centre;  pattern: pattern solid, fore_colour gray25;borders: left thin, right thin, top thin, bottom thin")

EMPTY_CHAR = [u'',u' ',u'\xa0',u'#N/A',u'N/A',u'NA']
def check_is_string_depend_python_version(val):
    if VERSION_INFO==2:
        check_str = isinstance(val,unicode) or isinstance(val,str)
    else:
        check_str =  isinstance(val,str)
    return check_str
    
def empty_string_to_False(readed_value):
    if VERSION_INFO==2:
        check_str = isinstance(readed_value,unicode) or isinstance(readed_value,str)
    else:
        check_str =  isinstance(readed_value,str)
    
    if check_str :
        if readed_value  in EMPTY_CHAR:
            return False
        rs = re.search('\S',readed_value)
        if not rs:
            return False
    return readed_value
# def active_function(val):
#     return False if val ==u'na' else True
def read_merge_cell(sheet,row,col,merge_tuple_list):
    for crange in merge_tuple_list:
        rlo, rhi, clo, chi = crange
        if row>=rlo and row < rhi and col >=clo and col < chi:
            row = rlo
            col = clo
            break
    ctype = sheet.cell(row, col).ctype
    if  ctype==5:
        return False
    if   ctype == xlrd.XL_CELL_EMPTY:
#         raise ValueError(u'kkaka')
        print ('row,col',row,col)
        return False
    else:
        val = sheet.cell_value(row,col)
        return val
def read_excel_cho_field(sheet, row, col_index,merge_tuple_list):
    #print 'row','col',row, col_index,sheet
    val = read_merge_cell(sheet, row ,col_index,merge_tuple_list)
    if VERSION_INFO==2:
        check_str = isinstance(val,unicode) or isinstance(val,str)
    else:
        check_str =  isinstance(val,str)
    if check_str:
        val = val.strip()
    val = empty_string_to_False(val)
    return val
### Xong khai bao
def get_key(field_attr, attr,default_if_not_attr=None):
    return field_attr.get(attr,default_if_not_attr)
#     value = field_attr.get(attr,default_if_not_attr)
#     if isinstance(value, dict) and key_tram:
#         value =  value.get(key_tram,default_if_not_attr) if key_tram in value else value.get('all_key_tram',default_if_not_attr)
#     return value

def get_by_key_tram(field_attr, attr, key_tram,default_if_not_attr=None):
    value = field_attr.get(attr,default_if_not_attr)
    if isinstance(value, dict) and key_tram:
        value =  value.get(key_tram,default_if_not_attr) if key_tram in value else value.get('all_key_tram',default_if_not_attr)
    return value

def check_type_of_val(field_attr, val, field_name, model_name):        
    if field_attr.get('bypass_check_type'):
        return True
    field_type = field_attr.get('field_type')
    if field_type:
        type_allow = field_attr.get('type_allow',[])
        if val != False and val != None:
            try:
                type_tuong_ung_voi_char_field_type = MAP_TYPE[field_type]
            except:
                return True
                raise UserError(u'không có field_type:%s này'%field_type)
            if field_attr.get('is_x2m_field'):
                type_tuong_ung_voi_char_field_type = list
            if isinstance( type_tuong_ung_voi_char_field_type,list):
                type_allow.extend(type_tuong_ung_voi_char_field_type)
            else:
                type_allow.append(type_tuong_ung_voi_char_field_type)
            pass_type_check = False
            for a_type_allow in type_allow:
                if isinstance(val, a_type_allow):
                    pass_type_check = True
                    continue
            if not pass_type_check:
                raise UserError(u'model: %s- field:%s có giá trị: %s, đáng lẽ là field_type:%s nhưng lại có type %s'%(model_name, field_name,val,field_type,type(val)))
            
            
############### end small func ##################
