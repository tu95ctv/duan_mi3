 # -*- coding: utf-8 -*-
import re
import xlrd
from odoo.exceptions import UserError
import base64
from copy import deepcopy
from xlutils.copy import copy
from odoo.addons.importexcel.models.model_dict_folder.tool_tao_instance import read_excel_cho_field, check_is_string_depend_python_version, empty_string_to_False#,get_width,header_bold_style,VERSION_INFO
from odoo.addons.downloadwizard.models.dl_models.dl_model  import wrap_center_vert_border_style
from odoo.addons.importexcel.models.model_dict_folder.get_or_create_func import get_or_create_object_has_x2m
from odoo.addons.importexcel.models.model_dict_folder.recursive_func import export_all_key_list_vals_key_list_type_of_val,rut_gon_key,ordereddict_fields, check_val_of_attrs_is_true_type, add_more_attrs_to_field_MD,define_col_index_common,check_compatible_col_index_and_xl_title,write_get_or_create_title, convert_dict_to_order_dict_string, export_some_key_value_of_fields_MD 
from odoo.tools.float_utils import  float_round

def importexcel_func(odoo_or_self_of_wizard, import_key=False, key_tram=False, check_file = False, gen_model_dict_kargs= {}):
    gen_model_dict_kargs['check_file'] = check_file
    self = odoo_or_self_of_wizard
    key_tram =  getattr(self,'key_tram',False) or key_tram
    new_dict = self.env['importexcel.importexcel'].gen_model_dict()
    import_key = import_key or self.import_key
    MD = new_dict[import_key]
#     if 'cach_tim_location_goc' not in gen_model_dict_kargs:
    cach_tim_location_goc = getattr(self, 'cach_tim_location_goc', 'find_origin_location_by_key_tram' )
    if cach_tim_location_goc:
        gen_model_dict_kargs['cach_tim_location_goc'] = cach_tim_location_goc

    if callable(MD):
        MD = MD(self=self, key_tram=key_tram, gen_model_dict_kargs=gen_model_dict_kargs)
    key_allow = MD.get('key_allow',False)
    key_tram = key_allow and key_tram
    if key_allow and not key_tram:
        raise UserError(u'ban phai chon key_tram')
    
#     rs = self.env['importexcel.importexcel'].gen_model_dict()
#     out_dict = {}
#     type_out_dict = {}
#     for k,MD_test in rs.items():
#         if callable(MD_test):
#             MD_test = MD_test(self=self, key_tram=key_tram, gen_model_dict_kargs=gen_model_dict_kargs)
#         key_allow = MD_test.get('key_allow',False)
#         export_all_key_list_vals_key_list_type_of_val(MD_test, output_key_list_vals_dict=out_dict, output_key_list_type_of_vals_dict=type_out_dict)
#     raise UserError(u'%s%s%s'%(str(out_dict), '***'*8, convert_dict_to_order_dict_string(type_out_dict)))

    if not self.file:
        raise UserError(u'Bạn phải upload file để import')
    file_content = base64.decodestring(self.file)
    formatting_info = False if '.xlsx' in self.filename else True
    xl_workbook = xlrd.open_workbook(file_contents = file_content, formatting_info=formatting_info)
    noti_dict = {}
    
    #R1
    rut_gon_key(MD,key_tram)
    #R2
    ordereddict_fields( MD)
    #R2A
    check_val_of_attrs_is_true_type(MD)
    
    setting = MD.get('setting',{})
    setting.setdefault('allow_write', MD.get('allow_write', True))
    setting.setdefault('st_write_false', MD.get('st_write_false', False))
    setting2 = MD.get('setting2',{})
    if setting2:
        setting.update(setting2)
    self.setting = convert_dict_to_order_dict_string(setting)
    #R3
    add_more_attrs_to_field_MD(self, MD, setting = setting)
   
    imported_model = self.env[MD.get('model')]
    rs = imported_model.default_get([])#imported_model._fields)
    all_field_attr_dict, dict_of_att_vs_set_vals = export_some_key_value_of_fields_MD(MD, exported_attrs_list = ['field_type','xl_title'], dict_of_att_vs_set_vals = {})
    self.all_field_attr_dict = all_field_attr_dict
#     raise UserError(u'%s-%s'%(a,b))
    sheet_names=gen_sheet_names(self,MD, xl_workbook, gen_model_dict_kargs)
    needdata = {}
    needdata['self'] = self
    needdata['sheet_names'] = sheet_names
    needdata['key_tram'] = key_tram
    needdata['check_file'] = check_file

    sh_names = xl_workbook.sheet_names()
    if check_file:
        workbook_copy = copy(xl_workbook)
    for sheet_name in sheet_names:
        COPIED_MD = deepcopy(MD)
        needdata['vof_dict'] = COPIED_MD.get('fields') 
        needdata['sheet_name'] = sheet_name
        sheet = xl_workbook.sheet_by_name(sheet_name)
        set_is_largest_map_row_choosing = MD.get( 'set_is_largest_map_row_choosing')#set_is_largest_map_row_choosing  is boolean
        nrows = sheet.nrows
        title_rows = xac_dinh_title_rows(self, MD, set_is_largest_map_row_choosing, nrows, sheet_name)
        #R4
        row_title_index, largest_map_row, new_title_rows = define_col_index_common(title_rows, sheet, COPIED_MD, set_is_largest_map_row_choosing)
        if set_is_largest_map_row_choosing:
            row_title_index = largest_map_row
#         raise UserError(str(new_title_rows))

        #R5
        check_compatible_col_index_and_xl_title (self, COPIED_MD, needdata)
        
        
        #tim kiem first_row,last_row
        
        dong_test_in_MD = MD.get('dong_test')
        first_row,last_row = gen_first_and_last_row(self, MD, row_title_index, nrows, dong_test_in_MD)
        
        if check_file:
            index = sh_names.index(sheet_name)
            sheet_of_copy_wb = workbook_copy.get_sheet(index)
            write_get_or_create_title(MD,sheet,sheet_of_copy_wb, row_title_index)
        else:
            workbook_copy = None
            sheet_of_copy_wb = None
        merge_tuple_list =  sheet.merged_cells
        for number_row_count,row in enumerate(range(first_row, last_row)):
            print ('sheet_name*******',sheet_name,'row',row)
            create_instance (self, COPIED_MD, 
                                              sheet, 
                                              row, 
                                              merge_tuple_list, 
                                              needdata, 
                                              noti_dict,
                                              check_file = check_file,
                                              sheet_of_copy_wb = sheet_of_copy_wb,
                                              setting=setting,
                                              sheet_of_copy_wb_para = {'sheet_of_copy_wb':sheet_of_copy_wb,'row':row,'sheet':sheet },
                               )
        
    if number_row_count:
        self.imported_number_of_row = number_row_count + 1
    self.log= noti_dict
    
    return workbook_copy
################# CREATE INSTANCE
def create_instance (self,
                    MD,
                    sheet,
                    row,
                    merge_tuple_list,
                    needdata,
                    noti_dict, 
                    check_file = False,
                    sheet_of_copy_wb = False,
                    setting={},
                    sheet_of_copy_wb_para = None,
                    ):
    
    search_dict = {}
    update_dict = {}
    model_name = MD.get( 'model')
    empty_object = self.env[model_name] 
    collection_dict = {}
    needdata['collection_dict'] = collection_dict
    is_create, is_write, is_search, exist_val, is_go_loop_fields = \
    before_ci(self, MD, setting, check_file, needdata)
#     collection_dict['break_field'] = None
    if is_go_loop_fields:
        for field_name,field_attr  in MD['fields'].items():
            a_field_code = get_a_field_val(self,
                                           field_name,
                                           field_attr,
                                           needdata,
                                           row,
                                           sheet,
                                           check_file,
                                           sheet_of_copy_wb,
                                           merge_tuple_list,
                                           model_name,
                                           noti_dict,
                                           search_dict,
                                           update_dict,
                                           collection_dict,
                                           setting, 
                                           sheet_of_copy_wb_para,
                                           )
            
            if a_field_code =='break_loop_fields_because_one_required_field':
                if field_attr.get('raise_if_False') and not check_file:
                    raise UserError('raise_if_False field: %s'%field_name)
                break
        if a_field_code =='break_loop_fields_because_one_required_field':
            this_model_notice = noti_dict.setdefault(model_name,{})
            skip_because_required = this_model_notice.setdefault('skip_because_required',0)
            this_model_notice['skip_because_required'] = skip_because_required + 1
            
            break_condition_func_for_main_instance  = MD.get('break_condition_func_for_main_instance')
            if break_condition_func_for_main_instance:
                break_condition_func_for_main_instance(needdata)
            obj = empty_object
            obj_val = False
            is_instance_ton_tai = None
            is_instance_ton_tai = u'Không tồn tại do required Field  = False'
            searched_obj= None
        elif collection_dict.get('instance_is_None_in_check_file_mode_becaused_a_required_field_in_imported_mode'):# có 1 field = false and required ==> instance đó = False
            obj, obj_val, is_instance_ton_tai =  empty_object, False, u'Không tồn tại do required Field  = False'
            searched_obj= None
        else:
            obj, obj_val, searched_obj, is_duoc_tao, a_row_instance_build_noti_dict =\
                         get_or_create_object_has_x2m(self,
                                                                    model_name,
                                                                    search_dict, 
                                                                    update_dict,
                                                                    MD=MD,
                                                                    exist_val=exist_val,
                                                                    setting=setting,
                                                                    check_file=check_file,
                                                                    is_search = is_search,
                                                                    is_create = is_create,
                                                                    is_write = is_write,
                                                                    sheet_of_copy_wb_para = sheet_of_copy_wb_para
                                                                    )
            this_model_not_dict = noti_dict.setdefault(model_name,{})
            for k,v in a_row_instance_build_noti_dict.items():
                this_model_not_dict[k] = this_model_not_dict.get(k,0) + v

            if exist_val:
                func_check_if_excel_is_same_existence =   setting.get('st_allow_check_if_excel_is_same_existence') and  MD.get('func_check_if_excel_is_same_existence')
                if  func_check_if_excel_is_same_existence:# and not get_or_create:,not st_is_allow_write_existence and
                    func_check_if_excel_is_same_existence(bool(searched_obj), searched_obj, obj)
                is_instance_ton_tai = True
                this_model_notice = noti_dict.setdefault(model_name,{})
                this_model_notice['exist_val'] = this_model_notice.get('exist_val',0) + 1
            else:
                is_instance_ton_tai = bool(searched_obj)
    if check_file:
        offset_write_xl = MD.get('offset_write_xl')
        if offset_write_xl !=None:
            if is_instance_ton_tai:
                get_or_create_display = u'Đã Có' 
            elif is_instance_ton_tai == u'Không tồn tại do required Field  = False':
                get_or_create_display = u'Break do field(cell) trống:%s'%collection_dict['break_field']
            elif is_instance_ton_tai == False:# searched_obj is null obj
                get_or_create_display = u'Chưa'
            sheet_of_copy_wb.write(row, sheet.ncols + offset_write_xl, get_or_create_display )
            
#         offset_write_xl_2 = MD.get('offset_write_xl_2')
#         if offset_write_xl_2 !=None:
#             searched_obj_show = str(searched_obj)
#             sheet_of_copy_wb.write(row, sheet.ncols + offset_write_xl_2, searched_obj_show, wrap_center_vert_border_style)
        
        check_file_write_more =  MD.get('check_file_write_more')
        if check_file_write_more:
            for offset_col, write_more_func, write_more_title in check_file_write_more:
                write_more_val = write_more_func(self, MD, searched_obj, collection_dict)
                sheet_of_copy_wb.write(row, sheet.ncols + offset_col, write_more_val, wrap_center_vert_border_style)

    return obj, obj_val 

#F1 
def get_a_field_val(self,
                                   field_name,
                                   field_attr,
                                   needdata,
                                   row,
                                   sheet,
                                   check_file,
                                   sheet_of_copy_wb,
                                   merge_tuple_list,
                                   model_name,
                                   noti_dict,
                                   search_dict,
                                   update_dict,
                                   collection_dict,
                                   setting,
                                   sheet_of_copy_wb_para,
                                   
                           ):
    skip_this_field = field_attr.get('skip_this_field', False)
    if callable(skip_this_field):
            skip_this_field = skip_this_field(self)
    if skip_this_field:
        return True
    col_index = field_attr.get('col_index')
    func = field_attr.get('func')
    obj = False
    set_val = field_attr.get('set_val')
    if set_val != None:
        val = set_val
    elif col_index !=None: # đọc file exc
        xl_val = read_excel_cho_field(sheet, row, col_index, merge_tuple_list)
        xl_val = empty_string_to_False(xl_val)
        field_attr['excel_val'] = xl_val
        val = empty_string_to_False(xl_val)
        if field_attr.get('partern_empty_val'):
            val = empty_string_to_False(val, pt = field_attr.get('partern_empty_val'))
        if val != False and field_attr.get('st_is_x2m_field'):
            val = val.split(',')
            val = list(map(lambda i: empty_string_to_False(i.strip()),val))
            if False in val:
                    raise UserError(u'Không được có phần tử = False')
    elif field_attr.get('fields') :
        obj,val   = create_instance (self,
                                                field_attr,
                                                sheet, 
                                                row, 
                                                merge_tuple_list,
                                                needdata, 
                                                noti_dict,
                                                check_file = check_file ,
                                                sheet_of_copy_wb = sheet_of_copy_wb,
                                                setting=setting,
                                                sheet_of_copy_wb_para = sheet_of_copy_wb_para
                                                               )
    else:
        val = False
    try:
        field_attr['before_func_val'] = val
    except Exception as e:
        raise UserError(u'%s-%s-%s'%(field_name, field_attr, row))
    # func
    karg = field_attr.get('karg',{})
    if karg ==None:
        karg ={}
        
    func_pre_func = field_attr.get('func_pre_func')
    if func_pre_func:
        val = func_pre_func(val, needdata,self)
        
        
    if func:
        try:
            val = func(val, needdata,**karg)
        except TypeError:
            try:
                val = func(val, needdata,self,**karg)
            except TypeError:
                val = func(val,**karg)
        if isinstance(val,tuple):
            obj,val = val
#         print ('func read model_name:%s field_name:%s'%(model_name,field_name),'val',val)
    
    val = replace_val_for_ci (field_attr,val,needdata)
    field_attr['val_goc'] = val
    
    
    if val == False:
        if field_name =='uom_id':
            print ('kakakaka',val)
        default_val = field_attr.get('default_val')
        if  default_val!=None:
            val = default_val
            
            
    if field_attr.get('field_type') =='float':
        try:
            val = float_round(val, precision_rounding=0.01)
        except:
            raise UserError(u'%s-%s'%(val,type(val)))
        
        
    
    field_attr['val'] = val
    field_attr['obj'] = obj
    if check_file:     
        required_when_normal  = field_attr.get('required', False)   
#         required = field_attr.get('required_when_check_file', required_when_normal) 
        required = False
        if (required_when_normal and val==False) and required ==False:
            collection_dict['instance_is_None_in_check_file_mode_becaused_a_required_field_in_imported_mode'] = True
            break_field = collection_dict.setdefault('break_field',[])
            break_field.append( field_name)
    else:
        required = field_attr.get('required', False)  

   
    key_or_not = field_attr.get('key')
    a_field_code = True
    if '2many' in field_attr.get('field_type','' ) and val == False: # khong add field 2many neu field do bang False
        return a_field_code
    if required and (val==False ):# val ==False <==> val ==0, val ==0 <==> val =False
        a_field_code = 'break_loop_fields_because_one_required_field' 
        break_field = collection_dict.setdefault('break_field',[])
        break_field.append( field_name)        
        return  a_field_code#sua 5
    elif not field_attr.get('for_excel_readonly'):
        if key_or_not==True:
            search_dict [field_name] = val
        elif key_or_not == 'Both':
            search_dict [field_name] = val
            update_dict [field_name] = val
        else:
            update_dict [field_name] = val
    valid_field_func = field_attr.get('valid_field_func')
    if valid_field_func:
        valid_field_func(val,obj,needdata,self)
    print ("row: ", row,'model_name: ',model_name,'-field: ', field_name, '-val: ', val)
    check_type_of_val(field_attr, val, field_name, model_name)
    return a_field_code        

            
def replace_val_for_ci(field_attr, val, needdata):
    
    
    
    #### deal replace string ####
    replace_string = field_attr.get('replace_string')
    if  replace_string and check_is_string_depend_python_version(val):
        for pattern,repl in replace_string:
            pattern = pattern.replace('(','\(').replace(')','\)')
            val = re.sub(pattern, repl, val)
    #### end  deal replace string ####
    
    
    
    #### deal empty val ###
#     empty_val = field_attr.get('empty_val')
#      
#     if empty_val and val in empty_val:
#         val = False   
    #### !!!deal empty val ###
    #### deal  replace val#####
    replace_val = field_attr.get('replace_val')
    if replace_val:
        replace_val_tuple = replace_val.get(needdata['sheet_name']) or replace_val.get('all')
        if replace_val_tuple:
            for k,v in replace_val_tuple:
                if val ==k:
                    val = v
                    break
    return val


def check_notice_dict_co_create_or_get(model_name,noti_dict,check_file):
    adict = noti_dict.get(model_name,{})
    if not adict.get('create') and not adict.get('update') and not check_file :
        raise UserError(u'các row bị bỏ qua hết không có dòng nào được tạo hoặc được update')
    
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
def check_type_of_val(field_attr, val, field_name, model_name):        
    if field_attr.get('bypass_check_type'):
        return True
    char_field_type = field_attr.get('field_type')
    if char_field_type:
        type_allow = field_attr.get('type_allow',[])
        if val != False and val != None:
            try:
                map_type_of_char_field_type = MAP_TYPE[char_field_type]
            except:
                return True
                raise UserError(u'không có field_type:%s này trong MAP_TYPE '%char_field_type)
            if field_attr.get('st_is_x2m_field'):
                map_type_of_char_field_type = list
            if isinstance( map_type_of_char_field_type, list):
                type_allow.extend(map_type_of_char_field_type)
            else:
                type_allow.append(map_type_of_char_field_type)
            type_of_val = type(val)
            is_pass_type_check =  type_of_val in type_allow
            if not is_pass_type_check:
                raise UserError(u'model: %s- field:%s có giá trị: %s, đáng lẽ là field_type:%s nhưng lại có type %s'%(model_name, field_name,val,char_field_type,type(val)))
            
def xac_dinh_is_search_is_create_is_write(field_MD, check_file, exist_val, st_is_allow_write_existence, func_check_if_excel_is_same_existence  ):
    if check_file:
        is_search = True
        is_create = False
        is_write = False
    else:
        if exist_val:
            if st_is_allow_write_existence:
                is_create = False
                is_write = True
            else:
                is_create = False
                is_write = False
            if func_check_if_excel_is_same_existence :
                is_search = True
            else:
                is_search = False
        else:
            is_create = True
            is_write = True
            is_search =True
    return is_create, is_write, is_search
                
    
def before_ci(self, field_MD, setting, check_file, needdata):
    func_map_database_existence = setting.get('st_allow_func_map_database_existence') and field_MD.get('func_map_database_existence')
    if func_map_database_existence:
        exist_val = func_map_database_existence(needdata,self) 
    else:
        exist_val = None
        
        
    if exist_val:
        st_is_allow_write_existence = setting['st_is_allow_write_existence']
        func_check_if_excel_is_same_existence =   setting.get('st_allow_check_if_excel_is_same_existence') and  field_MD.get('func_check_if_excel_is_same_existence') 
    else:
        st_is_allow_write_existence = None
        func_check_if_excel_is_same_existence = None
    is_go_loop_fields = not exist_val or (exist_val and (func_check_if_excel_is_same_existence or st_is_allow_write_existence)) or check_file
    if is_go_loop_fields:
        is_create, is_write, is_search = xac_dinh_is_search_is_create_is_write(field_MD, check_file, exist_val, st_is_allow_write_existence, func_check_if_excel_is_same_existence  )
        
    return is_create, is_write, is_search, exist_val, is_go_loop_fields
                

                
def gen_first_and_last_row(self, MD, row_title_index,nrows, dong_test_in_MD):
            off_set_row = MD.get('begin_data_row_offset_with_title_row', 1)
            min_row = row_title_index + off_set_row
            first_row = min_row + getattr(self,'begin_row',0)
            print ('first_row','min_row',first_row,min_row)
            dong_test = getattr(self,'dong_test',None) or dong_test_in_MD
            if not dong_test:
                last_row = nrows
            else:
                last_row = first_row + dong_test
            if last_row > nrows:
                last_row =  nrows
            if first_row >  last_row :
                raise UserError(u'first_row >  last_row')
            return first_row,last_row

def xac_dinh_title_rows(self,MD,set_is_largest_map_row_choosing, nrows, sheet_name):
            range_1 = getattr(self, 'range_1',None)
            range_2 = getattr(self, 'range_2',None)
            if range_1 or range_2:
                title_rows = range(range_1,range_2)
            else:
                if set_is_largest_map_row_choosing:
                    title_rows = range(0,nrows)
                else:
                    title_rows_some_sheets = MD.get('title_rows_some_sheets',{})
                    if title_rows_some_sheets:
                        title_rows_some_sheets=title_rows_some_sheets.get(sheet_name)
                    if title_rows_some_sheets:
                        title_rows = title_rows_some_sheets
                    else:
                        title_rows = MD.get('title_rows')  # MODEL_DICT['title_rows']
            return title_rows
        
def gen_sheet_names(self,MD, xl_workbook, gen_model_dict_kargs):
        sheet_names = MD.get('sheet_names')
        if callable(sheet_names):
            try:
                sheet_names = sheet_names(self)
            except TypeError as e:
                if 'required positional argument' in u'%s'%e:
                    try:
                        sheet_names = sheet_names(self,xl_workbook)
                    except TypeError as e:
                        if 'required positional argument' in u'%s'%e:
                            sheet_names = sheet_names(self,xl_workbook, gen_model_dict_kargs )
                        else:
                            raise UserError(u'có 1 lỗi ở hàm sheet_names: %s '%e)
                else:
                        raise UserError(u'có 1 lỗi ở hàm sheet_names: %s '%e)    
        return sheet_names
    
    
