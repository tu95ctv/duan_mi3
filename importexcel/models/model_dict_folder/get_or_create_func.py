 # -*- coding: utf-8 -*-
from odoo.addons.importexcel.models.model_dict_folder.tool_tao_instance import get_key
from odoo.osv import expression
import datetime
from odoo import  fields
from odoo.exceptions import UserError
from odoo.addons.downloadwizard.models.dl_models.dl_model  import wrap_center_vert_border_style
from odoo.tools.float_utils import float_compare, float_round

def get_or_create_object_has_x2m (self,
                                model_name, 
                                search_dict,
                                write_dict ={},
                                MD = {},
                                exist_val=False,
                                setting= {},
                                check_file = False,
                                is_search = True,
                                is_create = True,
                                is_write = True,
                                sheet_of_copy_wb_para = None
                                 ):
    x2m_fields = MD.get('x2m_fields')
    if x2m_fields:
        x2m_field = x2m_fields[0]
        x2m_values = search_dict[x2m_field]
        len_x2m = len(x2m_values)
        result = []
    else:
        len_x2m = 1
    instance_build_noti_dict = {}  
    for i in range(0,len_x2m):
        if x2m_fields:
            search_dict[x2m_field] = x2m_values[i] #
        obj, searched_obj, is_tao_moi, new_noti_dict = get_or_create_object_has_search(self, 
                                model_name, 
                                search_dict,
                                write_dict =write_dict,
                                MD = MD,
                                exist_val=exist_val,
                                setting = setting,
                                check_file = check_file,
                                is_search = is_search,
                                is_create = is_create,
                                is_write = is_write,
                                sheet_of_copy_wb_para = sheet_of_copy_wb_para
                                )
        for k,v in new_noti_dict.items():
            instance_build_noti_dict[k] = instance_build_noti_dict.get(k,0) + v
        if x2m_fields:
            result.append(obj.id)
            searched_obj |= searched_obj
    if x2m_fields:
        remove_all_or_just_add_one_x2m = MD.get('remove_all_or_just_add_one_x2m', 'add_one')
        if remove_all_or_just_add_one_x2m == 'remove_all':
            obj_id =  [(6,False,result)]
        else:
            obj_id  = list(map(lambda x: (4, x, False), result)) 
    else:
        if not obj:
            obj_id = None
        else:
            obj_id = obj.id
    if not check_file and not obj:
        raise UserError('not check_file and not obj')
        
            
   
#             raise UserError('akakak')
        
#         if obj != None :#and  obj != False
#             obj_id = obj.id
#             print ('hiccccccccccccccccccc',obj_id )
#         else:
#             obj_id = obj
#         obj_id = obj.id
#         if check_file and not obj_id:
# #             obj = None
#             obj_id = None
                
    return obj, obj_id, searched_obj, is_tao_moi, instance_build_noti_dict

def get_or_create_object_has_search(self, model_name,
                                search_dict,
                                write_dict ={},
                                MD = {},
                                exist_val= None,
                                setting = {},
                                check_file=False,
                                is_search = True,
                                is_create = True,
                                is_write = True,
                                sheet_of_copy_wb_para = None
                                ):
    is_tao_moi = False
    new_noti_dict = {} 
    empty_object  = self.env[model_name]
    if is_search:
        searched_obj = search_handle(self, MD, search_dict, check_file, model_name, setting, empty_object)
        new_noti_dict['search']=1
    else:
        searched_obj = None
    
    
    if exist_val:
        write_obj = exist_val
    else:
        write_obj = searched_obj
        
        
        
    return_obj = write_obj
    
    if write_obj and len(write_obj) > 1:
        try:
            mapped_name = write_obj.mapped('name')
        except:
            mapped_name = write_obj
        raise UserError (u'len_return_obj > 1 %s'%(mapped_name))
    if not write_obj and is_create:
        create_obj = create_handle(self, search_dict, write_dict, MD, model_name)
        return_obj = create_obj
        new_noti_dict['create'] =1
        is_tao_moi = True
    elif write_obj and (( is_write and  setting['allow_write']) or check_file):
        write_handle(self, write_obj, MD, write_dict, check_file, sheet_of_copy_wb_para, new_noti_dict )

    
    return return_obj , searched_obj, is_tao_moi, new_noti_dict# bool(searched_obj)



def search_handle(self, model_dict, search_dict, check_file, model_name, setting, empty_object):
    search_func = model_dict.get('search_func')
    if search_func:
        searched_obj = search_func(self, model_dict, setting)
    else:
        if search_dict :
            pass
        else:
            raise UserError(u'Không có search dict, model_name: %s-MD: %s'%(model_name, model_dict))
        if model_dict.get('inactive_include_search'):
            domain_not_active = ['|',('active','=',True),('active','=',False)]
        else:
            domain_not_active = []
        domain = []
        has_none_val_search_field = False
        for f_name in search_dict:
            field_attr = model_dict['fields'][f_name]
            val =  search_dict[f_name]
            if val == None:
                if check_file:
                    searched_obj = empty_object
                    searched_obj =  None
                    has_none_val_search_field = True
                    break
                else:
                    raise UserError(u'nếu không phải check_file, val không thể bằng None')
            f_name = get_key(field_attr, 'transfer_name') or f_name
            operator_search = field_attr.get('operator_search','=')
            tuple_in = (f_name, operator_search, val)
            domain.append(tuple_in)
        if not has_none_val_search_field:
            domain = expression.AND([domain_not_active, domain])
            searched_obj  = self.env[model_name].search(domain)
    return searched_obj
                
def create_handle(self, search_dict, write_dict, model_dict, model_name):
    search_dict_new ={}
    only_get = get_key(model_dict,'only_get')
    if only_get:
        raise UserError(u'Model %s này chỉ được get chứ không được tạo'%model_name)
    search_dict.update(write_dict)
    for f_name,val in search_dict.items():
        field_attr = model_dict['fields'][f_name]
        f_name = get_key(field_attr, 'transfer_name') or f_name
        search_dict_new[f_name]=val
    created_object = self.env[model_name].create(search_dict_new)
    return_obj = created_object
    return return_obj

def write_handle(self, return_obj, model_dict, write_dict, check_file, sheet_of_copy_wb_para, new_noti_dict ):
    write_dict_new = {}
    writed_object = return_obj
    for key_f_name, val in write_dict.items():
        field_MD= model_dict['fields'][key_f_name]
        offset_write_xl_diff = field_MD.get('offset_write_xl_diff')
        
        
        if check_file and   offset_write_xl_diff ==None:
            continue
        if not check_file and (field_MD.get('val_goc') ==False and not field_MD.get('write_false')):
            continue
        f_name = get_key(field_MD, 'transfer_name') or key_f_name
        if check_file:
            is_write_this_field = False
        else:
            is_write_this_field = field_MD.get('write_field', True)
        if not check_file and not is_write_this_field :
            continue
        orm_field_val = getattr(writed_object, f_name)
        diff = check_diff_write_val_with_exist_obj(orm_field_val, val, field_MD)
        if diff:
            if is_write_this_field:
                write_dict_new[f_name] = val
            if check_file:
                if hasattr(orm_field_val,'name'):
                    orm_field_val = getattr(orm_field_val,'name')
                    if val == None:
                        try:
                            val = field_MD['fields']['name']['val']
                        except:
                            pass
                            
                diff_show = u'Khác, db:%s- xl:%s'%(orm_field_val, val)
        else:
            if check_file:
                diff_show = u'Giống'
        if check_file:
            sheet_of_copy_wb = sheet_of_copy_wb_para['sheet_of_copy_wb']
            sheet_of_copy_wb.write(sheet_of_copy_wb_para['row'], sheet_of_copy_wb_para['sheet'].ncols + offset_write_xl_diff, diff_show, wrap_center_vert_border_style)
    
    if not check_file:
        if write_dict_new:
            writed_object.write(write_dict_new)
            new_noti_dict['update'] = 1
        else:#'not update'
            new_noti_dict['skipupdate'] = 1
        
        


def check_diff_write_val_with_exist_obj(orm_field_val, field_dict_val, field_attr):
    is_write = False
    if isinstance(orm_field_val, datetime.date):
        converted_orm_val_to_dict_val = fields.Date.from_string(orm_field_val)
    elif isinstance(orm_field_val, datetime.datetime):
        converted_orm_val_to_dict_val = fields.Datetime.from_string(orm_field_val)
    else:
        try:
            converted_orm_val_to_dict_val = getattr(orm_field_val, 'id', orm_field_val)
            if converted_orm_val_to_dict_val == None: #recorderset.id ==None when recorder set = ()
                converted_orm_val_to_dict_val = False
        except:
            converted_orm_val_to_dict_val = orm_field_val
    if field_attr.get('field_type')=='float':
        is_write = float_compare(orm_field_val, field_dict_val, precision_rounding=0.01)# 1 la khac, 0 la giong
    else:
        is_write =  converted_orm_val_to_dict_val != field_dict_val
    return is_write
    
                
                

