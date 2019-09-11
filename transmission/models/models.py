# -*- coding: utf-8 -*-

from odoo import models, fields, api



    
    
    
class Truyendan(models.Model):
    _name = 'tran.truyendan'
    name = fields.Char()
    diem_ids = fields.One2many('tran.diem','truyendan_id')
class PortThietbi(models.Model):
    _name = 'tran.porttb'
    name = fields.Char()
class Luong(models.Model):
    _name = 'tran.luong'
    name = fields.Char()
    
class Diem(models.Model):
    _name = 'tran.diem'
    name = fields.Char()
    stt = fields.Integer()
    truyendan_id = fields.Many2one('tran.truyendan')
    porttb_id = fields.Many2one('tran.porttb')
    luong_id = fields.Many2one('tran.luong')
    


################################
class ODF(models.Model):
    _name = 'tran.odf'
    trig_field = fields.Boolean()
    name = fields.Char(compute = 'name_',store=True)
    
    @api.depends('toa_do','odf_rack', 'phong_may','trig_field' )
    def name_(self):
        for r in self:
            toa_do = r.toa_do
            odf_rack=r.odf_rack
            if toa_do and odf_rack and r.phong_may:
                r.name = toa_do + ' ' +  odf_rack  + ' ' + r.phong_may
                
                
    stt_odf = fields.Integer()
    toa_do = fields.Char()
    odf_rack = fields.Char()
#     soi_id = fields.Many2one('tran.soi')
    thiet_bi_id = fields.Many2one('tran.tbtdan')
    department_id = fields.Many2one('hr.department')
    phong_may = fields.Char()
    luong = fields.Char()


# class LuongLine(models.Model):
#     _name = 'tran.luongline'
#     name = fields.Char()
#     stt = fields.Integer()
# #     soi_id = fields.Many2one('tran.soi')
#     thiet_bi_id = fields.Many2one('tran.tbtdan')

#     @api.depends('soi_id','trig_field')
#     def luongline_ids_(self):
#         luongline_ids = self.env['tran.luongline']
#         for r in self:
#             thiet_bi_id = None
#             thiet_bi_id = r.soi_id
#             field_name = 'soi_id'
#             if thiet_bi_id:
#                 stt = 0
#                 if thiet_bi_id.luongline_ids:
#                     stt = max(thiet_bi_id.luongline_ids.mapped('stt'))
#                 luongline_id_id = self.env['tran.luongline'].search([(field_name,'=', thiet_bi_id.id)])
#                 if not luongline_id_id:
#                     luongline_id_id = self.env['tran.luongline'].create({field_name: thiet_bi_id.id, 'stt':stt + 1})
#                 luongline_ids |=luongline_id_id
#                 if thiet_bi_id.luongline_ids:
#                     luongline_ids |=thiet_bi_id.luongline_ids
#                
#                 r.luongline_ids = luongline_ids


    

    
    
    


