# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_
from odoo.addons.tutool.mytools import  convert_utc_native_dt_to_gmt7,name_compute,convert_odoo_datetime_to_vn_datetime,convert_vn_datetime_to_utc_datetime,Convert_date_orm_to_str
from odoo.exceptions import UserError
import datetime
from copy import copy


def skip_depends_if_not_congviec_decorator(depend_func):
    def wrapper(*args,**kargs):
        self = args[0]
        for r in self:
            if r.loai_record ==u'Công Việc':
                depend_func(r)
    return wrapper
def skip_depends_if_not_congviec_decorator_valid_diemtc(depend_func):
    def wrapper(*args,**kargs):
        self = args[0]
        for r in self:
            if not r.id:
                pass
            elif r.loai_record !=u'Công Việc':
                r.valid_diemtc =True
            else:
                depend_func(r)
    return wrapper
class Cvi(models.Model):
    _name = 'cvi'
    _inherit = ['cvisuco','camsua']
    _auto = True
    _order = "id desc"
    state = fields.Selection([
                              ('mark_delete',u'Đánh Dấu Để Xóa'),
                              ('draft',u'Khởi tạo'),
                              ('confirmed',u'Nhân viên xác nhận'),
                              ('approved',u'Lãnh Đạo đã duyệt'),
                          ],default='draft', required=True, string=u'Trạng thái')
    @api.multi
    def action_mark_delete(self):
        for r in self:
            r.state = 'mark_delete'
    
    @api.multi
    def action_draft(self):
        for r in self:
            r.state = 'draft'
            
    @api.multi
    def action_confirmed(self):
        for r in self:
            r.state = 'confirmed'
    @api.multi
    def action_approved(self):
        for r in self:
            r.state = 'approved'

  
    is_your = fields.Boolean(compute='is_your_')  
    @api.depends('user_id')
    def is_your_(self):
        for r in self:
            r.is_your = r.user_id == self.env.user
        
        
    ti_le_chia_diem = fields.Float(digits=(6,2),string=u'Tỉ lệ chia điểm',default=100)
    tvcv_id_name = fields.Char(related='tvcv_id.name', string=u'Thư Viện Công Việc',store=True,readonly=True)
    code= fields.Char(related='tvcv_id.code', string=u'Mã Công Việc',store=True, readonly=True)
    diem_tvcv = fields.Float(digits=(6,2),related='tvcv_id.diem', string=u'Điểm Thư Viện',store=True,readonly=True)# 
    don_vi = fields.Many2one(related='tvcv_id.don_vi', string=u'Đơn vị tính',store=True, readonly=True)
    so_luong = fields.Float(string=u'Số Lượng',default = 1,required=True,digit=(6,2))
    so_lan = fields.Integer(string=u'Số Lần',default = 1,required=True)
    tree_view_ref = fields.Char(compute='tree_view_ref_',default='dai_tgg.tvcv_list')
    search_view_ref = fields.Char(compute='tree_view_ref_',default='dai_tgg.tvcv_search')
    @api.depends('loai_record')
    def tree_view_ref_(self):
        for r in self:
            if r.loai_record ==u'Công Việc':
                r.tree_view_ref = 'dai_tgg.tvcv_list'
                r.search_view_ref = 'dai_tgg.tvcv_search'
            else:
                r.tree_view_ref = 'dai_tgg.loai_suco_suvu_list'
                r.search_view_ref = 'dai_tgg.loai_suco_suvu_search'
                
    cd_parent_id = fields.Many2one('cvi',string=u'Công Việc Chia Điểm Cha',ondelete='cascade',copy=False)# ondelete='restrict' #ondelete='cascade', ondelete='set null'
    cd_children_ids = fields.One2many('cvi','cd_parent_id',string=u'Các CV Chia Điểm Con',copy=False)
    hd_parent_id = fields.Many2one('cvi',string=u'Công Việc Hưởng điểm Cha',ondelete='cascade')# ondelete='restrict' #ondelete='cascade', ondelete='set null'
    hd_children_ids = fields.One2many('cvi','hd_parent_id',string=u'Các CV Hưởng Điểm Con')
    diem_goc = fields.Float(digits=(6,2),string=u'Điểm Góc',compute='diem_goc_',store=True)# 
    diemtc = fields.Float(digits=(6,2),compute='diemtc_',string=u'Điểm Nhân Viên',store=True)
    slncl = fields.Integer(compute='slncl_',store=True,string=u'Số lượng người chia điểm')
    percent_diemtc = fields.Integer(default=100,string=u'Điểm LĐ/Điểm Nhân Viên (%)')
    diemld = fields.Float(digits=(6,2),compute='diemld_',string=u'Điểm Lãnh Đạo Chấm',store=True)
    valid_diemtc = fields.Boolean(compute='valid_diemtc_', string=u'Valid Điểm Nhân Viên',store=True)#
    loai_cvi = fields.Selection([(u'Single',u'Công Việc Đơn'),
                                 (u'Chia Điểm Cha',u'Chia Điểm Cha'),(u'Chia Điểm Con',u'Chia Điểm Con'),
                                 (u'Chung Điểm Cha',u'Chung Điểm Cha'),(u'Chung Điểm Con',u'Chung Điểm Con'),
                                 (u'Giai Đoạn Cha',u'Giai Đoạn Cha'), (u'Giai Đoạn Con',u'Giai Đoạn Con'),
                                 (u'Giai Đoạn Con và Chia Điểm Cha',u'Giai Đoạn Con và Chia Điểm Cha'),
                                 (u'Giai Đoạn Con và Giai Đoạn Cha',u'Giai Đoạn Con và Giai Đoạn Cha')
                                        ],compute='valid_diemtc_',store=True,string=u'Loại công việc')
    valid_cd = fields.Boolean(compute='valid_cd_',store=True)    
    valid_diemtc_conclusion = fields.Selection([(u'Chia điểm không đủ 100%',u'Chia điểm không đủ 100%'),
                                  (u'Thiếu giai đoạn con',u'Thiếu giai đoạn con'),
                                  (u'Thiếu giai đoạn',u'Thiếu giai đoạn'),
                                  (u'Thiếu giai đoạn và Chia điểm không đủ 100%',u'Thiếu giai đoạn và Chia điểm không đủ 100%'),
                                  (u'Kiểm tra điểm OK',u'Kiểm tra điểm OK'),         
                                                           ],compute='valid_diemtc_',store=True,string=u'Kiểm tra điểm')
    sum_cd_con = fields.Float(digits=(6,2),compute='sum_cd_con_',store=True)
    is_sep = fields.Boolean(compute='is_sep_')


    
    
    @api.onchange('loai_record','tvcv_id')
    def tvcv_id_oc_(self):
        member_ids = self._context.get('member_ids')
        if self.loai_record==u'Công Việc':
            if member_ids:
                member_ids = member_ids[0][2]#[[6, False, [1, 46]]]
            member_ids = member_ids or ([self.env.user.chung_ca_user_id] if self.env.user.chung_ca_user_id else [])
#             if member_ids !=None:
            if member_ids:
                if not self.cd_children_ids:
                    member_ids = [member_id for member_id in member_ids if member_id != self.user_id.id]
                    if member_ids:
                        defaults = self.default_get(self._fields)
                        cd_children_ids  = []
                        for m in member_ids:
                            a_defaults = defaults.copy()
                            a_defaults['user_id']= m
                            a_cd_children_id = (0,0,a_defaults)
                            cd_children_ids.append(a_cd_children_id)
                        return {'value':
                                {'cd_children_ids':cd_children_ids
                                 }
                                }
        else:
            return {'value':
                            {'cd_children_ids':[]
                             }
                            }

    @api.multi
    def cam_sua_do_diff_user_(self):
        for r in self:
            if not r.id:
                r.ly_do_cam_sua_do_diff_user = u'Ko Cấm do new'
                cam_sua =  False
            elif self.user_has_groups('base.group_erp_manager'):
                r.ly_do_cam_sua_do_diff_user = u'Ko Cấm do user là admin'
                cam_sua =  False
            else:

                if ( r.user_id == self.env.user) or (r.create_uid == self.env.user):
                    cam_sua = False
                else:
                    cam_sua = True
                if cam_sua:
                    r.ly_do_cam_sua_do_diff_user = u'Cấm do khác user'
                else:
                    r.ly_do_cam_sua_do_diff_user = u'Không cấm do cùng User'
            r.cam_sua_do_diff_user =  cam_sua
#     @api.depends('name')
#     def is_admin_(self):
#         rs = super(Cvi,self).is_admin_()
#         return rs
  
    @api.multi
    def cam_sua_(self):
        for r in self:
            cam_sua = r.cam_sua_do_time or (r.cam_sua_do_diff_user and not r.is_sep) or (r.state =='approved' and not r.is_sep)
            r.cam_sua = cam_sua and not r.is_admin

    @api.multi
    @skip_depends_if_not_congviec_decorator
    def is_sep_(self): 
        cac_linh_ids = self.env.user.cac_linh_ids
        for r in self:
            if self.env.uid in r.user_id.cac_sep_ids.mapped('id') or (self.user_has_groups('dai_tgg.group_cham_diem_cvi') and r.department_id == r.env.user.department_id)\
            or (cac_linh_ids and (r.create_uid == r.env.user or r.user_id == r.env.user)) \
            or  self.user_has_groups('base.group_erp_manager'):# +  r.user_id.cac_sep_ids.cac_sep_ids.mapped('id'):
                r.is_sep = True
            else:
                r.is_sep = False
    ################# DEPEND##########################
    
    
    
    @api.depends(
                'cd_children_ids',# dành cho CHIA ĐIỂM CHA
                'cd_parent_id.cd_children_ids', # Trigger cho slncl CHIA ĐIỂM CON
#                 'len_gd_child',#moi add
                )      # khi form thay đổi bất cứ field nào thì chắc chắn cd_children_ids thay đổi vì ta sẽ luôn thay nó trong hàm write()
    @skip_depends_if_not_congviec_decorator
    def slncl_(self):
        for r in self:
            if r.cd_children_ids:
                r.slncl = len(r.cd_children_ids) + 1
            elif r.cd_parent_id:#CHIA ĐIỂM CON
                r.slncl = len(r.cd_parent_id.cd_children_ids) + 1

            else:
                r.slncl = 1
                

    @api.depends('so_luong','so_lan','loai_record')
    @skip_depends_if_not_congviec_decorator
    def diem_goc_(self):
        for r in self:
            if r.cd_parent_id:#Điểm góc CHIA ĐIỂM CON
                r.diem_goc = r.cd_parent_id.tvcv_id.diem * r.cd_parent_id.so_luong * r.cd_parent_id.so_lan
            else:
                r.diem_goc = r.so_luong * r.so_lan * r.tvcv_id.diem
    @api.depends( 'slncl', 'diem_goc','cd_parent_id.diem_goc','ti_le_chia_diem')
    @skip_depends_if_not_congviec_decorator
    def diemtc_(self):
        for r in self:
                if r.cd_parent_id:#cv chia diem con
                    r.diemtc = r.cd_parent_id.diem_goc*r.ti_le_chia_diem/100
                else: 
                    r.diemtc = r.diem_goc*r.ti_le_chia_diem/100

    @api.depends('ti_le_chia_diem','slncl','cd_children_ids.ti_le_chia_diem')
    @skip_depends_if_not_congviec_decorator
    def sum_cd_con_(self):
        for r in self:
            if r.slncl > 1:
                sum_phan_tram = r.ti_le_chia_diem + sum(r.cd_children_ids.mapped('ti_le_chia_diem'))
                r.sum_cd_con =sum_phan_tram
    
    def valid_cd_chung_cha_con(self,r):
        abs_cd = abs(r.sum_cd_con - 100 )
        if  abs_cd <= 0.01*r.slncl:
            valid_cd = True
        else:
            valid_cd = False
        return valid_cd
    
    @api.depends('sum_cd_con','cd_parent_id.sum_cd_con')
    @skip_depends_if_not_congviec_decorator
    def valid_cd_(self):
        for r in self:
            if r.cd_parent_id:
                r.valid_cd = self.valid_cd_chung_cha_con(r.cd_parent_id)
            elif r.slncl > 1:
                r.valid_cd = self.valid_cd_chung_cha_con(r)

    
    @api.depends('valid_cd','hd_children_ids','loai_record')
    @skip_depends_if_not_congviec_decorator_valid_diemtc
    def valid_diemtc_(self):
        for r in self:
            if not r.id:
                pass
            else:
                if r.cd_parent_id:# CD CON
                    r.loai_cvi = u'Chia Điểm Con'
                    r.valid_diemtc = r.valid_cd
                    if not r.valid_diemtc:
                        r.valid_diemtc_conclusion =  u'Chia điểm không đủ 100%'
                elif  r.slncl > 1: # CD CHA
                    r.loai_cvi =u'Chia Điểm Cha'
                    r.valid_diemtc = r.valid_cd
                    if not r.valid_diemtc:
                        r.valid_diemtc_conclusion =  u'Chia điểm không đủ 100%'
                elif r.hd_parent_id:
                    r.loai_cvi = u'Chung Điểm Con'
                    r.valid_diemtc = True
                elif r.hd_children_ids:
                    r.loai_cvi = u'Chung Điểm Cha'
                    r.valid_diemtc = True
                else: # SINGLE
                    r.loai_cvi = u'Single'
                    r.valid_diemtc = True
                if r.valid_diemtc ==True:
                    r.valid_diemtc_conclusion = u'Kiểm tra điểm OK'
    @api.depends('percent_diemtc','diemtc')
    @skip_depends_if_not_congviec_decorator
    def diemld_(self):
        for r in self:
            r.diemld = r.diemtc * r.percent_diemtc /100
    def copy_vals_for_cd_or_hd_children_ids(self,vals ,fields_not_copy=['cd_children_ids','ti_le_chia_diem','user_id' ] ):
        copy_vals = copy(vals)
        for f in fields_not_copy:
            if f in copy_vals:
                del copy_vals[f]
        return copy_vals
    
#     @api.constrains('cd_parent_id')
#     def cd_children_constrains(self):
#         for r in self:
#             if r.cd_parent_id:
#                 update_field_list = ['tvcv_id','so_luong','gio_ket_thuc','gio_bat_dau','so_lan', 'department_ids','noi_dung']
#                 update_dict = self.get_parent_value_for_child(r,update_field_list,'cd_parent_id')
#                 r.write(update_dict)
#                 
#     @api.constrains('hd_parent_id')
#     def hd_children_constrains(self):
#         try:
#             for r in self:
#                 if r.hd_parent_id:
#                     update_field_list = ['tvcv_id','so_luong','gio_ket_thuc','gio_bat_dau','so_lan', 'department_ids','noi_dung']
#                     update_dict = self.get_parent_value_for_child(r,update_field_list,'hd_parent_id')
#                     r.write(update_dict)
#         except exceptions as e:
#             raise ValueError(e)
        
    def get_parent_value_for_child(self,r,update_field_list,cd_parent_id_or_gd_parent_id):
        update_dict = {}
        for field in update_field_list:
            parent_id = getattr(r,cd_parent_id_or_gd_parent_id)
            fields = r._fields
            if fields[field].type=='many2one':
                update_dict[field] = getattr(parent_id,field).id
            elif fields[field].type=='many2many' or fields[field].type=='one2many':
                update_dict[field] =[(6, False,  getattr(parent_id,field).ids)]
            else:
                update_dict[field] =getattr(parent_id,field)
        return update_dict
    def adapt_field_type(self,field,val):
        fields = self._fields
        if fields[field].type=='many2one':
            rs = val.id
        elif fields[field].type=='many2many' or fields[field].type=='one2many':
            rs =[(6, False,  val.ids)]
        else:
            rs = val
        return rs
        
    def write_cd_or_hd_childrends_depends_parent(self, parent_id, vals):
        for r in parent_id:
            if r.loai_record==u'Công Việc':
                if 'cd_children_ids' in vals:
                    cd_children_ids = vals['cd_children_ids']
                    is_adding_cd_children_ids = list(filter(lambda i:i[0]==0 or i[0]==2, cd_children_ids)) # thêm hoặc xóa đi cvi chia điểm
                    if bool(is_adding_cd_children_ids):
                        cd_parent_and_childs = r.cd_children_ids + r
                        ti_le_chia_diem = 100.0/r.slncl
                        cd_parent_and_childs.write({'ti_le_chia_diem':ti_le_chia_diem})
                
               
                            
                            
#                     adding_cd_children_ids = cd_children_ids.filtered(lambda i:i[0]==0)
                if r.cd_children_ids:
                    copy_vals = self.copy_vals_for_cd_or_hd_children_ids(vals)
                    r.cd_children_ids.write(copy_vals)
                if r.hd_children_ids:
                    copy_vals = self.copy_vals_for_cd_or_hd_children_ids(vals, ['hd_children_ids'])
                    r.hd_children_ids.write(copy_vals)
    @api.model
    def create(self, vals):
        cv = super(Cvi, self).create(vals)
        if vals.get('loai_record') == u'Công Việc':
            self.write_cd_or_hd_childrends_depends_parent(cv, vals)
        return cv
    @api.multi
    def write(self, vals):
        cd_or_hd_children_ids = vals.get('cd_children_ids') or vals.get('hd_children_ids')
        adding_cd_or_hd_children_ids = list(filter(lambda i:i[0]==0, cd_or_hd_children_ids)) if cd_or_hd_children_ids else []
        if adding_cd_or_hd_children_ids:
            for new in adding_cd_or_hd_children_ids:
                data = new[2]
                update_field_list = ['tvcv_id','so_luong','gio_ket_thuc','gio_bat_dau','so_lan', 'department_ids','noi_dung']
                for fname in update_field_list:
                    data[fname] = self.adapt_field_type(fname, getattr(self[0], fname))
        res = super(Cvi, self).write(vals)
        self.write_cd_or_hd_childrends_depends_parent(self, vals)
        return res    
    
    @api.multi
    def unlink(self):
        for r in self:
            if r.state != 'mark_delete' : 
                raise UserError(u'Muốn Xóa thì phải Đánh Dấu Xóa trước đã')
        res = super(Cvi, self).unlink()
        return res 
    
    
    

    
