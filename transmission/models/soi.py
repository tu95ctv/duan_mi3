# -*- coding: utf-8 -*-

from odoo import models, fields, api
class TBandSoi(models.Model):
    _name = 'tran.tbsoi'
    _auto = False
    name = fields.Char()
    trig_field = fields.Boolean()
#     soi_id = fields.Many2one('tran.soi')
    thiet_bi_id = fields.Many2one('tran.tbtdan')
    thiet_bi_phia_truoc_id = fields.Many2one('tran.tbtdan')
    file_name = fields.Char()
    luong = fields.Char()
    
class DayNhay(models.Model):
    _name = 'tran.daynhay'
    tbtd_id = fields.Many2one('tran.tbtdan')
    name = fields.Char()
    
class TBTD(models.Model):
    _name = 'tran.tbtdan'
    _auto = True
    day_nhay_ids = fields.One2many('tran.daynhay','tbtd_id', compute='nhan_txt_', store=True)
    refect_thiet_bi_id = fields.Many2one('tran.tbtdan', compute='refect_thiet_bi_id_', store=True)
    refect_thiet_bi_ids = fields.One2many('tran.tbtdan', 'thiet_bi_id')
    @api.depends('refect_thiet_bi_ids')
    def refect_thiet_bi_id_(self):
        for r in self:
            if r.refect_thiet_bi_ids:
                r.refect_thiet_bi_id = r.refect_thiet_bi_ids[0]
#     _inherit = ['tran.tbsoi']
    
    
    #### Chung ############
    
    name = fields.Char()
    trig_field = fields.Boolean()
#     soi_id = fields.Many2one('tran.soi')
    thiet_bi_type = fields.Selection([('thiet_bi','thiet_bi'),('soi','soi')], default='thiet_bi',related='thiet_bi_id.soi_or_thiet_bi')
#     tree_view_ref = fields.Selection([('transmission.soi_list','transmission.soi_list'),('transmission.tbtd_list','transmission.tbtd_list')])
    thiet_bi_form_view_ref = fields.Selection([('transmission.soi_form','transmission.soi_form'),('transmission.tbtd_form','transmission.tbtd_form')],compute='thiet_bi_form_view_ref_')
    thiet_bi_tree_view_ref = fields.Selection([('transmission.soi_list','transmission.soi_list'),('transmission.tbtd_list','transmission.tbtd_list')])
#     thiet_bi_form_view_ref = fields.Selection([('transmission.soi_form','transmission.soi_form'),('transmission.tbtd_form','transmission.tbtd_form')])
    thiet_bi_search_view_ref = fields.Selection([('transmission.soi_search','transmission.soi_search'),('transmission.tbtd_search','transmission.tbtd_search')])
#     @api.onchange('thiet_bi_type')
#     def thiet_bi_type_onchange_(self):
#         if self.thiet_bi_type == 'soi':
#             self.thiet_bi_tree_view_ref,self.thiet_bi_form_view_ref,self.thiet_bi_search_view_ref = 'transmission.soi_list','transmission.soi_form','transmission.soi_search'
#         else:
#             self.thiet_bi_tree_view_ref,self.thiet_bi_form_view_ref,self.thiet_bi_search_view_ref = 'transmission.tbtd_list','transmission.tbtd_form','transmission.tbtd_search'
    @api.depends('thiet_bi_type')
    def thiet_bi_form_view_ref_(self):
        for r in self:
            if r.thiet_bi_type == 'soi':
                r.thiet_bi_form_view_ref = 'transmission.soi_form'
            else:
                r.thiet_bi_form_view_ref = 'transmission.tbtd_form'
            
#     @api.onchange('thiet_bi_form_view_ref')
#     def thiet_bi_type_onchange_for_list(self):
#         if self.thiet_bi_form_view_ref == 'transmission.soi_form':
#             self.thiet_bi_tree_view_ref = 'transmission.soi_list'
#         else:
#             self.thiet_bi_tree_view_ref = 'transmission.tbtd_list'
            
            


    thiet_bi_id = fields.Many2one('tran.tbtdan')
    thiet_bi_phia_truoc_id = fields.Many2one('tran.tbtdan')
    file_name = fields.Char()
    luong = fields.Char()
    soi_or_thiet_bi = fields.Selection([('thiet_bi','thiet_bi'),('soi','soi')], default='thiet_bi')
    ####################
    
    name = fields.Char(compute = 'tbtdan_name_',store=True)
    
    @api.depends('trig_field','ten_he_thong','port','soi_or_thiet_bi')
    def tbtdan_name_(self):
        for r in self:
            if r.soi_or_thiet_bi =='thiet_bi':
                if r.port and r.ten_he_thong:
                    r.name = r.port +', ' + r.ten_he_thong
            elif r.soi_or_thiet_bi =='soi':
                if r.stt_soi and r.tuyen_cap:
                    r.name = r.stt_soi + ' ' + r.tuyen_cap
                
                
                

    
    he_thong_id= fields.Many2one('tran.hethong')
    ten_he_thong = fields.Char()
    ten_card = fields.Char()
    slot = fields.Char()
    port = fields.Char()
    odf = fields.Char()
    port_odf = fields.Char()
    rate = fields.Char()
    ten = fields.Char()
    near = fields.Char()
    far = fields.Char()
    tb_or_cq = fields.Char()
    port_tb_or_cq = fields.Char()
   
    luong_txt = fields.Char(compute='luong_txt_', store=True)
    odf_ids = fields.One2many('tran.odf', 'thiet_bi_id')
    cap_quang = fields.Char()
    soi = fields.Char()
    test1 = fields.Char()
    test2 = fields.Char()
    
    
#     @api.depends('name', 'soi_id','thiet_bi_id','trig_field', 'soi_id.luong_txt','thiet_bi_id.luong_txt')
    @api.depends('name','thiet_bi_id','trig_field','thiet_bi_id.luong_txt')
    def luong_txt_(self):
        for r in self:
            thiet_bi_id = None
            if r.thiet_bi_id:
                thiet_bi_id = r.thiet_bi_id
#             else:
#                 thiet_bi_id = r.soi_id
            
            r.luong_txt = luong_txt_func(r, thiet_bi_id)

                    
    nhan_txt = fields.Text(compute ='nhan_txt_', store = True)   
    @api.depends('thiet_bi_id.nhan_txt', 'trig_field' )
    def nhan_txt_(self):
        for r in self:
            self_odf = r.odf_ids
            nhans = []
            if len(self_odf)==1 and self_odf.name :
                nhan_1 = r.name + '<-->' + self_odf.name 
                nhans.append(nhan_1)
            
            thiet_bi = r.thiet_bi_id   
            if self_odf:
                thiet_bi_odf =thiet_bi.odf_ids
                for selfodf in self_odf:
                    for thietbiodf in thiet_bi_odf:
                        if (selfodf.phong_may == thietbiodf.phong_may) and thietbiodf.name and selfodf.name:
                            nhan_2 = selfodf.name +  '<-->'  +  thietbiodf.name
                            nhans.append(nhan_2)
            if thiet_bi:
                if thiet_bi.nhan_txt:
                    nhans.append(thiet_bi.nhan_txt)
            r.nhan_txt = '\n'.join(nhans)
            
            for nhan in nhans:
#                 day_nhay_id_list = []
                day_nhay_id = self.env['tran.daynhay'].search([('name','=',nhan),('tbtd_id','=',r.id)])     
                if not day_nhay_id:
                    day_nhay_id =self.env['tran.daynhay'].create({'name':nhan, 'tbtd_id':r.id})
                    
#                 day_nhay_id_list.append(day_nhay_id.id)
#                 r.write({'day_nhay_ids':[(6,0,day_nhay_id_list)]})
              
              
              
    ### soi move qua ###
#     name = fields.Char(compute='soi_name_',store=True)
#     @api.depends('tuyen_cap','stt_soi','trig_field')
#     def soi_name_(self):
#         for r in self:
#             if r.stt_soi and r.tuyen_cap:
#                 r.name = r.stt_soi + ' ' + r.tuyen_cap
#     soi_or_thiet_bi = fields.Selection([('thiet_bi','thiet_bi'),('soi','soi')],default='soi')
    tuyen_cap = fields.Char()
    stt_soi = fields.Char()
#     odf_ids = fields.One2many('tran.odf','soi_id')
    odf_dau = fields.Char(compute='odf_dau_cuoi_')
    odf_cuoi = fields.Char(compute='odf_dau_cuoi_')
    @api.depends('odf_ids')
    def odf_dau_cuoi_(self):
        for r in self:
            odf_ids =r.odf_ids
            if odf_ids:
                odf_dau = odf_ids.filtered(lambda i: i.stt_odf ==1)
                if odf_dau:
                    r.odf_dau = odf_dau.name
                    
                odf_cuoi = odf_ids.filtered(lambda i: i.stt_odf ==2)
                if odf_cuoi:
                    r.odf_cuoi = odf_cuoi.name
                    
                    
    odf_cuoi_khac_tram = fields.Char()
    odf_cuoi_khac_tram_toa_do = fields.Char()
    des_1 = fields.Char()
    des_2 = fields.Char()
    ten = fields.Char()
    chi_tiet_dau_noi = fields.Char()
    
    
    
    
    
def luong_txt_func(r, thiet_bi_id):
        luong_txt =  False
        if r.name:
            rs = [r.name]
            if thiet_bi_id:   
                if thiet_bi_id.luong_txt:
                    rs.append(thiet_bi_id.luong_txt)
            luong_txt = u'-->'.join(rs)
        
        return luong_txt

    


                
                
# class SOI(models.Model):
#     _name = 'tran.soi'
#     _auto = True
#     _inherit = ['tran.tbsoi']
#     
#     
#     
#     
#     name = fields.Char(compute='soi_name_',store=True)
#     @api.depends('tuyen_cap','stt_soi','trig_field')
#     def soi_name_(self):
#         for r in self:
#             if r.stt_soi and r.tuyen_cap:
#                 r.name = r.stt_soi + ' ' + r.tuyen_cap
# #     soi_or_thiet_bi = fields.Selection([('thiet_bi','thiet_bi'),('soi','soi')],default='soi')
#     tuyen_cap = fields.Char()
#     stt_soi = fields.Char()
#     odf_ids = fields.One2many('tran.odf','soi_id')
#     odf_dau = fields.Char(compute='odf_dau_cuoi_')
#     odf_cuoi = fields.Char(compute='odf_dau_cuoi_')
#     @api.depends('odf_ids')
#     def odf_dau_cuoi_(self):
#         for r in self:
#             odf_ids =r.odf_ids
#             if odf_ids:
#                 odf_dau = odf_ids.filtered(lambda i: i.stt_odf ==1)
#                 if odf_dau:
#                     r.odf_dau = odf_dau.name
#                     
#                 odf_cuoi = odf_ids.filtered(lambda i: i.stt_odf ==2)
#                 if odf_cuoi:
#                     r.odf_cuoi = odf_cuoi.name
#                     
#                     
#     odf_cuoi_khac_tram = fields.Char()
#     odf_cuoi_khac_tram_toa_do = fields.Char()
#     des_1 = fields.Char()
#     des_2 = fields.Char()
#     ten = fields.Char()
#     chi_tiet_dau_noi = fields.Char()
#     
#     
#     
#     
#                     
#     
#     
#     
#     nhan_txt = fields.Text(compute ='nhan_txt_', store = True)   
#     @api.depends('thiet_bi_id', 'soi_id','thiet_bi_id.odf_ids.name' )
#     def nhan_txt_(self):
#         for r in self:
#                 self_odf = r.odf_ids
#                 nhans = []
#                 if len(self_odf)==1 and self_odf.name :
#                     nhan_1 = r.name + '<-->' + self_odf.name 
#                     nhans.append(nhan_1)
#                     
#                 if self_odf:
#                     thiet_bi = r.thiet_bi_id or r.soi_id
#                     thiet_bi_odf =thiet_bi.odf_ids
#                     for selfodf in self_odf:
#                         for thietbiodf in thiet_bi_odf:
#                             if (selfodf.phong_may == thietbiodf.phong_may) and thietbiodf.name and selfodf.name:
#                                 nhan_2 = selfodf.name +  '<-->'  +  thietbiodf.name
#                                 nhans.append(nhan_2)
#                 r.nhan_txt = '\n'.join(nhans)                     
# 
#     luong_txt = fields.Char(compute='luong_txt_', store=True)
#     @api.depends('name', 'soi_id','thiet_bi_id','trig_field', 'soi_id.luong_txt','thiet_bi_id.luong_txt')
#     def luong_txt_(self):
#         for r in self:
#             if r.name:
#                 thiet_bi_id = None
#                 if r.thiet_bi_id:
#                     thiet_bi_id = r.thiet_bi_id
#                 else:
#                     thiet_bi_id = r.soi_id
#                 
#                 r.luong_txt = luong_txt_func(r, thiet_bi_id)
                
                
class HeThong(models.Model):
    _name = 'tran.hethong'
    name = fields.Char()


#     


