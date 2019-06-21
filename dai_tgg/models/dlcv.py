# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_
from odoo.osv import expression
from odoo.osv.query import Query
import datetime
from odoo.addons.dai_tgg.mytools import  convert_utc_native_dt_to_gmt7
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

import os,sys,inspect
# from odoo.addons.dai_tgg.controllers.controllers import download_cvi
# def download_cvi(a):
#     pass
class DLCV(models.TransientModel):
    _name = 'dlcv'
    ngay_bat_dau_filter = fields.Date(string=u'Ngày Bắt Đầu')
    ngay_ket_thuc_filter = fields.Date(string=u'Ngày Kết Thúc')
    is_show_diem_nhan_vien = fields.Boolean(string=u'Có show cột điểm nhân viên không?')
    chon_thang = fields.Selection([(u'Tháng Trước',u'Tháng Trước'),(u'Tháng Này',u'Tháng Này')],string = u'Chọn tháng')
    department_ids = fields.Many2many('hr.department')

    @api.multi
    def download_cvi_binh(self):
        pass
#         download_cvi(self)
#         workbook = download_cvi(self)
#         currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#         dir_tmp = os.path.dirname(currentdir) + '/static/'
#         
#         workbook.save(dir_tmp + 'abc.xls')
#         return {
#             'type' : 'ir.actions.act_url',
#             'url': '/dai_tgg/static/%s' % ('abc.xls'),
#             'target': 'blank',
#         }
#         
        
    def check_department_(self):   
        if not self.department_ids:
                self.department_ids = [self.env.user.department_id.id]
        else:
            if len(self.department_ids) > 1:
                    raise UserError(u'Bạn chỉ được chọn 1 đơn vị download')
            else:
                if not self.user_has_groups('base.group_erp_manager'):
                    select_department_id = self.department_ids[0].id
                    user_department_id = self.env.user.department_id.id
                    child_department_of_user_ids = self.env['hr.department'].search([('id','child_of',user_department_id)]).ids
                    if select_department_id not in child_department_of_user_ids :
                        raise UserError(u'Đơn vị bạn chọn phải cùng  hoặc là con với đơn vị của bạn')
    @api.multi
    def download_cvi_o(self):
        self.check_department_()
        return {
             'type' : 'ir.actions.act_url',
             'url': '/web/binary/download_cvi?model=dlcv&id=%s&more=abc'%(self.id),
             'target': 'new',
        }
    @api.multi
    def download_cvi_by_userlist(self):
        return {
             'type' : 'ir.actions.act_url',
             #'url': '/web/binary/download_document?model=importbd&field=file&id=%s&filename=product_stock.xls'%(self.id),
             'url': '/web/binary/download_cvi_by_userlist?model=dlcv&id=%s&more=abc'%(self.id),
             'target': 'new',
        }
        
        
        
    def cvi_filter(self):
        sql_cmd = '''select cvi.user_id,sum(diemtc),u.login,p.name from cvi inner join res_users as u on cvi.user_id = u.id inner join res_partner as p on u.partner_id = p.id group by cvi.user_id ,u.login,p.name'''
        self.env.cr.execute(sql_cmd)
        rsul = self.env.cr.fetchall()
        self.log = rsul
        

        