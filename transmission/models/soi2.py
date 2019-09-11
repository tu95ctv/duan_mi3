# -*- coding: utf-8 -*-

from odoo import models, fields, api
class TBandSoi(models.Model):
    _name = 'tran.tbsoi'
    _auto = False
    name = fields.Char()
    trig_field = fields.Boolean()
    soi_id = fields.Many2one('tran.soi')
    thiet_bi_id = fields.Many2one('tran.tbtdan')
    
#     partner_odf_id = fields.Many2one('tran.odf', compute='partner_odf_id_', store = True)
#     @api.depends('soi_id', 'number_partner_odf')
#     def partner_odf_id_(self):
#         for r in self:
#             partner_odf_id = r.soi_id.odf_ids.filtered(lambda odf:odf.stt_odf==r.number_partner_odf)
#             r.partner_odf_id =partner_odf_id
#     number_partner_odf = fields.Integer(default=1)
    thiet_bi_phia_truoc_id = fields.Many2one('tran.tbtdan')
    file_name = fields.Char()
    luong = fields.Char()
class TBTD(models.Model):
    _name = 'tran.tbtdan'
    _auto = True
    _inherit = ['tran.tbsoi']
    name = fields.Char(compute = 'tbtdan_name_',store=True)
    
    @api.depends('trig_field','ten_he_thong','port')
    def tbtdan_name_(self):
        for r in self:
            if r.port and r.ten_he_thong:
                r.name = r.port +', ' + r.ten_he_thong

    trig_field = fields.Boolean()
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
    soi_or_thiet_bi = fields.Selection([('thiet_bi','thiet_bi'),('soi','soi')],default='thiet_bi')
    
    @api.depends('name', 'soi_id','thiet_bi_id','trig_field', 'soi_id.luong_txt','thiet_bi_id.luong_txt')
    def luong_txt_(self):
        for r in self:
            thiet_bi_id = None
            if r.thiet_bi_id:
                thiet_bi_id = r.thiet_bi_id
            else:
                thiet_bi_id = r.soi_id
            
            r.luong_txt = luong_txt_func(r, thiet_bi_id)

                    
    nhan_txt = fields.Text(compute ='nhan_txt_', store = True)   
    @api.depends('thiet_bi_id', 'soi_id','thiet_bi_id.odf_ids.name' )
    def nhan_txt_(self):
        for r in self:
                self_odf = r.odf_ids
                nhans = []
                if len(self_odf)==1 and self_odf.name :
                    nhan_1 = r.name + '<-->' + self_odf.name 
                    nhans.append(nhan_1)
                    
                if self_odf:
                    thiet_bi = r.thiet_bi_id or r.soi_id
                    thiet_bi_odf =thiet_bi.odf_ids
                    for selfodf in self_odf:
                        for thietbiodf in thiet_bi_odf:
                            if (selfodf.phong_may == thietbiodf.phong_may) and thietbiodf.name and selfodf.name:
                                nhan_2 = selfodf.name +  '<-->'  +  thietbiodf.name
                                nhans.append(nhan_2)
                r.nhan_txt = '\n'.join(nhans)                
              
              
              
    ### soi move qua ###
    
    
    
def luong_txt_func(r, thiet_bi_id):
        luong_txt =  False
        if r.name:
            rs = [r.name]
            if thiet_bi_id:   
                if thiet_bi_id.luong_txt:
                    rs.append(thiet_bi_id.luong_txt)
            luong_txt = u'-->'.join(rs)
        
        return luong_txt

    


                
                
class SOI(models.Model):
    _name = 'tran.soi'
    _auto = True
    _inherit = ['tran.tbsoi']
    trig_field = fields.Boolean()
    
    
    
    name = fields.Char(compute='soi_name_',store=True)
    @api.depends('tuyen_cap','stt_soi','trig_field')
    def soi_name_(self):
        for r in self:
            if r.stt_soi and r.tuyen_cap:
                r.name = r.stt_soi + ' ' + r.tuyen_cap
    soi_or_thiet_bi = fields.Selection([('thiet_bi','thiet_bi'),('soi','soi')],default='soi')
    tuyen_cap = fields.Char()
    stt_soi = fields.Char()
    odf_ids = fields.One2many('tran.odf','soi_id')
    odf_dau = fields.Char(compute='odf_dau_cuoi_')
    odf_cuoi = fields.Char(compute='odf_dau_cuoi_')
    odf_cuoi_khac_tram = fields.Char()
    odf_cuoi_khac_tram_toa_do = fields.Char()
    des_1 = fields.Char()
    des_2 = fields.Char()
    ten = fields.Char()
    chi_tiet_dau_noi = fields.Char()
    
    
    
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
                    
    
    
    
    nhan_txt = fields.Text(compute ='nhan_txt_', store = True)   
    @api.depends('thiet_bi_id', 'soi_id','thiet_bi_id.odf_ids.name' )
    def nhan_txt_(self):
        for r in self:
                self_odf = r.odf_ids
                nhans = []
                if len(self_odf)==1 and self_odf.name :
                    nhan_1 = r.name + '<-->' + self_odf.name 
                    nhans.append(nhan_1)
                    
                if self_odf:
                    thiet_bi = r.thiet_bi_id or r.soi_id
                    thiet_bi_odf =thiet_bi.odf_ids
                    for selfodf in self_odf:
                        for thietbiodf in thiet_bi_odf:
                            if (selfodf.phong_may == thietbiodf.phong_may) and thietbiodf.name and selfodf.name:
                                nhan_2 = selfodf.name +  '<-->'  +  thietbiodf.name
                                nhans.append(nhan_2)
                r.nhan_txt = '\n'.join(nhans)                     

    luong_txt = fields.Char(compute='luong_txt_', store=True)
    @api.depends('name', 'soi_id','thiet_bi_id','trig_field', 'soi_id.luong_txt','thiet_bi_id.luong_txt')
    def luong_txt_(self):
        for r in self:
            if r.name:
                thiet_bi_id = None
                if r.thiet_bi_id:
                    thiet_bi_id = r.thiet_bi_id
                else:
                    thiet_bi_id = r.soi_id
                
                r.luong_txt = luong_txt_func(r, thiet_bi_id)
                
                
class HeThong(models.Model):
    _name = 'tran.hethong'
    name = fields.Char()


#     


