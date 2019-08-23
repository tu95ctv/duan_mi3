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
    
    
    
    

