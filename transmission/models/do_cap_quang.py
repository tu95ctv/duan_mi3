# -*- coding: utf-8 -*-

from odoo import models, fields, api
class DoCapQuang(models.Model):
    _name = 'dcquang.dcquang'
    name = fields.Char()
    
    huong = fields.Char()
    stt = fields.Integer()
    stt_he_thong = fields.Integer()
    he_thong = fields.Char()
    thiet_bi = fields.Char()
    odf_tg = fields.Char()
    odf_tg_toa_do = fields.Char()
    
    odf_line = fields.Char()
    odf_line_toa_do = fields.Char()
    
    
    chay_chinh_hay_du_phong = fields.Char()
    cap = fields.Char()