# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_
import re
from odoo.addons.importexcel.models.model_dict_folder.tao_instance_new import importexcel_func
from odoo.addons.tonkho.models.import_excel_model_dict_folder.model_dict import default_import_xl_setting
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_round
# from odoo.addons.importexcel.models.model_dict_folder.recursive_func import export_all_no_pass_dict_para



class CommonSetting(models.Model):
    _name = 'importexcel.commonsetting'
    _auto = False
    st_allow_func_map_database_existence = fields.Boolean(default = default_import_xl_setting['default_st_allow_func_map_database_existence'])
    st_is_allow_write_existence  = fields.Boolean(default = default_import_xl_setting['default_st_is_allow_write_existence'])
    st_allow_check_if_excel_is_same_existence  = fields.Boolean(string=u'Cho phép đối chiếu product excel obj với product exist object',default = default_import_xl_setting['default_st_allow_check_if_excel_is_same_existence'])
    st_is_allow_empty_xldata_pn_is_unique_same_name_product  = fields.Boolean(default = default_import_xl_setting['default_st_is_allow_empty_xldata_pn_is_unique_same_name_product'],
                                                                              string='Cho phép sản phẩm có pn trống ờ file tương ứng với sản phẩm cùng tên và duy nhất')
    st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr  = fields.Boolean(default = default_import_xl_setting['default_st_is_allow_nonempty_pn_xldata_pr_is_empty_pn_same_name_pr'], 
                                                                                 string='Cho phép sản phẩm ở file excel có pn tương ứng với sản phẩm có cùng tên nhưng pn trống'
                                                                                 )
    
    
    
    dong_test = fields.Integer(default=0)#0 la initify vô hạn
    begin_row = fields.Integer(default=0)
    file = fields.Binary()
    filename = fields.Char()
    
class Importexcel(models.Model):
    _name = 'importexcel.importexcel' 
    _inherit = 'importexcel.commonsetting'
    _auto = True
    setting= fields.Char()
    import_key = fields.Selection([
        (u'stock.inventory.line.tong.hop.ltk.dp.tti.dp',u'stock.inventory.line.tong.hop'),
        (u'Product',u'Product'),
        (u'Thư viện công việc',u'Thư viện công việc'),
        (u'User',u'User')
        ,(u'Department',u'Department')
        ,(u'Partner',u'Partner')
        ,(u'location partner',u'location partner')
        ,(u'categ',u'Product Category')
        ,(u'cvi',u'Công việc')
         ,(u'thuebaoline',u'Thuê bao')
         ,(u'bds.poster',u'bds.poster'),
         (u'Loại sự cố, sự vụ', u'Loại sự cố, sự vụ')
                                    ],required = True,default=u'stock.inventory.line.tong.hop.ltk.dp.tti.dp')
    sheet_name_select = fields.Selection([
                                   (u'Vô tuyến',u'Vô tuyến'),
                                   (u'Chuyển Mạch (IMS, Di Động)',u'Chuyển Mạch (IMS, Di Động)'),
                                   (u'Truyền dẫn',u'Truyền dẫn'),
                                   (u'IP (VN2, VNP)',u'IP (VN2, VNP)'),
                                   (u'GTGT',u'GTGT'),(u'XFP, SFP các loại',u'XFP, SFP các loại')  ],rejquired=True)
    sheet_name =  fields.Char()
    key_tram =  fields.Selection([('key_ltk','key_ltk'),
                                  ('key_tti','key_tti'),
                                  ('key_137','key_137'),
                                  ('key_tti_dc','key_tti_dc'),
                                  ('key_ltk_dc','key_ltk_dc'),
                                  ('key_ltk_dc2','key_ltk_dc2'),
                                  ],default='key_ltk')

#     department_id = fields.Many2one('hr.department')
#     update_number=fields.Integer()
#     create_number=fields.Integer()
#     skipupdate_number=fields.Integer()
#     thong_bao_khac = fields.Char()
    trigger_model = fields.Selection([(u'kiemke',u'kiemke'),
                                    (u'vattu',u'vattu'),
                                    (u'kknoc',u'kknoc'),
                                    (u'cvi',u'cvi'),
                                    (u'stock.production.lot',u'stock.production.lot')
                                    ])
    log = fields.Text()

    imported_number_of_row = fields.Integer()

#     line_not_has_quant =  fields.Text()

    
    cach_tim_location_goc = fields.Selection([(u'find_origin_location_by_key_tram',u'mode 1 (tim location goc bằng key)'),(u'find_origin_location_by_column_named_tram',u'mode 2 ( tìm location góc bằng cột trạm)')])
    all_field_attr_dict = fields.Text()
    def gen_model_dict(self):
       
        return {}
    
    
    @api.onchange('sheet_name_select')
    def sheet_name_select_oc_(self):
        if self.sheet_name_select:
            self.sheet_name = self.sheet_name_select
    
    
    def importexcel(self):
        importexcel_func(self)
        return True
    
    def check_file(self):
        return {
             'type' : 'ir.actions.act_url',
             'url': '/web/binary/download_model?download_model=importexcel.importexcel&download_model_id=%s&download_key=%s'%(self.id, 'importexcel.checkfile'),
             'target': 'new',
             }
    
   
    def import_all(self):
        importexcel_func(self, import_key=u'Department')
        importexcel_func(self, import_key=u'Partner')
        importexcel_func(self, import_key=u'location partner')
        importexcel_func(self, import_key=u'Loại sự cố, sự vụ')
        importexcel_func(self, import_key=u'thuebaoline')
        importexcel_func(self, import_key=u'categ')
        return True
    
    def check_stt_inventory_line_old(self):
        rs = self.env['stock.inventory.line'].search([('inventory_id','=',self.inventory_id.id)], order='stt asc')
        rs2 = self.env['stock.inventory.line'].search([('inventory_id','=',self.inventory_id.id)], order='stt desc',limit=1)
        last_stt = rs2.stt
        kq = set(rs.mapped('stt'))
        self.test_result_1  = kq
        set_2 = set(range(1,last_stt))
        self.test_result_2= last_stt
        rs3 = set_2 - kq
        self.test_result_3 = sorted(rs3) 
    def check_line_khong_co_quant_va_khong_co_qty(self):
        rs1 = self.inventory_id.line_ids
        khong_co_so_luong =  sorted( rs1.filtered(lambda r: not  r.product_qty ).mapped('stt'))
        co_so_luong_but_khong_co_quant = sorted( rs1.filtered(lambda r: r.product_qty and not r.quant_ids).mapped('stt'))
        self.test_result_3 ='co_so_luong_but_khong_co_quant' + '\n%s'%co_so_luong_but_khong_co_quant
        self.test_result_2= 'khong_co_so_luong \n%s'%khong_co_so_luong
    def check_stt_inventory_line(self):
        rs1 = self.inventory_id.line_ids
        rs2 = rs1.mapped('quant_ids').filtered(lambda r: r.location_id.usage=='internal')
        rs3 = sorted(rs2.mapped('stt'))
#         rs2 =sorted( rs1.filtered(lambda r: r.product_qty and not r.quant_ids).mapped('stt'))
        self.test_result_1 =len(rs1)
        self.test_result_2 =len(rs2)
        self.test_result_3= rs3
        
    def test_code(self):
#         t = self.env['tvcv'].create({'name':'aa','diem':None,'code':None})
#         print (t.name, t.diem, t.code)
            t = self.env['tvcv']
            print ('t.department_id, t.diem, t.name,t.id',t.department_id, t.diem, t.name, t.id)
#         fl =  float_compare(1.667, 1.67, precision_rounding=2)
#         fl2 =  float_compare(1.7, 1.67, precision_rounding=2)
#         rs =  float_compare(1.767, 1.67, precision_rounding=0.01)
#         fl3= float_round(1.6667, precision_rounding=0.01)
#         fl4= float_round(1.67, precision_rounding=0.01)
#         raise UserError(u'%s-%s, %s-rs:%s'%(fl4,fl3, fl3==fl4,rs))


    def test_code1(self):
#         sql_multi_2 = '''select date_trunc('day',create_date) from stock_quant'''
         
        sql_multi_2 = "select create_date at time zone 'UTC' at time zone 'ICT'  from stock_quant where cast(create_date at time zone 'UTC' at time zone 'ICT' as date) = date '2018-08-31 '"
        self.env.cr.execute(sql_multi_2)
        result_2 = self.env.cr.dictfetchall()
        self.test_result_1 = result_2
        print ('self._context',self._context)

#         self.env['stock.inventory'].browse([13]).line_ids.unlink()
    def trigger(self):
        if self.trigger_model:
            count = 0
            self.env[self.trigger_model].search([]).write({'trig_field':'ok'})

        else:
            raise UserWarning(u'Bạn phải chọn trigger model')
  
    
    def import_strect(self):
        pass
        return True


class ImportCVI(models.Model):
    _name='importexcel.importcvi'
    _inherit = 'importexcel.importexcel'
    user_id = fields.Many2one('res.users',default= lambda self:self.env.uid)
    is_admin = fields.Boolean(compute='is_admin_')
    
    @api.depends('import_key')
    def is_admin_(self):
        for r in self:
            r.is_admin = self.user_has_groups('base.group_erp_manager')
    @api.model
    def default_get(self, fields):
        rs = super(ImportCVI, self).default_get(fields)
        rs['type_choose'] = u'cvi'
        return rs

    