# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_
import sys
from odoo.exceptions import UserError
import datetime
VERSION_INFO   = sys.version_info[0]

def het_time(r,TIME_ALLOW_SECONDS):
    TIME_ALLOW = datetime.timedelta(seconds=TIME_ALLOW_SECONDS)
    create_date =  fields.Datetime.from_string(r.create_date)
    delta_time =  datetime.datetime.now() - create_date
    return  delta_time>TIME_ALLOW   


def get_value_of_one_setting(self,fname,tien_to = 'dai_tgg.'):
    if VERSION_INFO==2:
        return self.env['ir.values'].get_default('ltk.config.settings', tien_to+ fname)
    else:
        return self.env['ir.config_parameter'].sudo().get_param(tien_to + fname)
class CamSua(models.Model):
    _name = 'camsua'
    _auto = False
    cam_sua = fields.Boolean(compute='cam_sua_',string=u'cấm sửa')
    cam_sua_do_time =  fields.Boolean(compute='cam_sua_do_time_')
    cam_sua_do_diff_user =  fields.Boolean(compute='cam_sua_do_diff_user_')
    ly_do_cam_sua_do_time = fields.Char(compute='cam_sua_do_time_')
    ly_do_cam_sua_do_diff_user = fields.Char(compute='cam_sua_do_diff_user_')
    is_admin = fields.Boolean(compute='is_admin_')

    @api.multi
    def is_admin_(self):
        for r in self:
            if self.user_has_groups('base.group_erp_manager'):
                r.is_admin = True
    @api.multi
    def cam_sua_(self):
        for r in self:
            r.cam_sua = r.cam_sua_do_time or r.cam_sua_do_diff_user
    @api.multi
    def cam_sua_do_time_(self):
        for r in self:
            if not r.id:
                r.ly_do_cam_sua_do_time = u'Không cấm sửa do new'
                r.cam_sua_do_time = False
            elif get_value_of_one_setting(self,'is_cam_sua_truoc_ngay'):
                cam_sua_truoc_ngay = get_value_of_one_setting(self,'cam_sua_truoc_ngay')
                if fields.Date.from_string(r.ngay_bat_dau) < fields.Date.from_string(cam_sua_truoc_ngay):
                    r.cam_sua_do_time = True
                    r.ly_do_cam_sua_do_time = u'cấm sửa do trước ngày'
            elif not get_value_of_one_setting(self,'is_cam_sua_do_time'):
                r.ly_do_cam_sua_do_time = u'Không cấm sửa do is_cam_sua_do_time = False'
            else:
                TIME_ALLOW_SECONDS = get_value_of_one_setting(self,'allow_edit_time')
                cam_sua = het_time(r,TIME_ALLOW_SECONDS)
                r.cam_sua_do_time =  cam_sua
                if cam_sua:
                    r.ly_do_cam_sua_do_time = u'cấm sửa do hết thời gian' 
                else:
                    r.ly_do_cam_sua_do_time = u'Không cấm sửa do chưa hết thời gian' 
    @api.multi
    def cam_sua_do_diff_user_(self):
        for r in self:
            if not r.id:
                r.ly_do_cam_sua_do_diff_user = u'Ko Cấm do new'
                cam_sua_do_diff_user =  False
            elif self.user_has_groups('base.group_erp_manager'):
                r.ly_do_cam_sua_do_diff_user = u'Ko Cấm do user là admin'
                cam_sua_do_diff_user =  False
            else:
                cam_sua_do_diff_user = r.create_uid != self.env.user and r.user_id != self.env.user
                if cam_sua_do_diff_user:
                    r.ly_do_cam_sua_do_diff_user = u'Cấm do khác user'
                else:
                    r.ly_do_cam_sua_do_diff_user = u'Không cấm do cùng User'
            r.cam_sua_do_diff_user =  cam_sua_do_diff_user
    
    
#     def cam_xoa(self):
#         if self.cam_sua:
#             return True
        
    @api.multi
    def unlink(self):
        for r in self:
            if r.cam_sua:
                raise UserError(u'Không được xóa do cấm sửa')
#             else:
#                 if r.state != 'mark_delete' : #and not (r.is_sep or r.is_admin)
#                     raise UserError(u'Muốn Xóa thì phải Đánh Dấu Xóa trước đã')
        res = super(CamSua, self).unlink()
        return res 
    
    
    