# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.addons.tsbd.models.tool import  request_html
from bs4 import BeautifulSoup




class BXH(models.Model):
    _name = 'tsbd.bxh'
    _order = 'diem desc, hsbt desc, score_sum desc'
    leech_ids = fields.Many2many('tsbd.leech','leech_bxh_rel', 'bxh_id', 'leech_id')
    team_id = fields.Many2one('tsbd.team')
    stt = fields.Integer()
    cate_id = fields.Many2one('tsbd.cate',ondelete = 'cascade')
    home_t = fields.Integer()
    home_h = fields.Integer()
    home_b = fields.Integer()
    def cach_4_18(self, next_stt,diem):
        try:
            if next_stt:
                next_stt_bxh_id = self.env['tsbd.bxh'].search([('cate_id','=',self.cate_id.id),('stt','=',next_stt)])[0]
                next_stt =next_stt_bxh_id.diem
                next_offset = diem - next_stt
            else:
                next_offset = 'L'
        except IndexError:
            next_offset = 'E'
        return next_offset
               
    def take_name(self, is_name_gon = False):
        r =self
        stt =r.stt 
        diem=r.diem
        previous_stt = stt -1
        next_stt = stt + 1
        if next_stt > r.cate_id.no_match:
            next_stt = 0
        try:
            if previous_stt:
                previous_stt_bxh_id = self.env['tsbd.bxh'].search([('cate_id','=',r.cate_id.id),('stt','=',previous_stt)])[0]
                previous_diem =previous_stt_bxh_id.diem
                previous_offset = previous_diem - diem
            else:
                previous_offset = 'F'
        except IndexError:
            previous_offset = 'E'   
        try:
            if next_stt:
                next_stt_bxh_id = self.env['tsbd.bxh'].search([('cate_id','=',r.cate_id.id),('stt','=',next_stt)])[0]
                next_stt =next_stt_bxh_id.diem
                next_offset = diem - next_stt
            else:
                next_offset = 'L'
        except IndexError:
            next_offset = 'E'
        cach_4 = r.cach_4_18(4,diem)  
        cach_18 = r.cach_4_18( 18,diem)  
                            
#         names = ''
#         names += r.team_id.name + ' | '
#         names += u'%s'%stt  + ' | '
#         names += u'%s'%diem + u'(%s-%s-[C%s C%s])'%(previous_offset,next_offset,cach_4,cach_18)
#         names += '|BT%s|BB%s|HS%s'%(r.score_sum,r.lost_score_sum,r.hsbt)

#         stt_bet = self.env['tsbd.betbxh'].search([('team_id','=',self.team_id.id)])
#         stt_bet = u'[%s%%%s]'%(stt_bet[0].diem_phan_tram, stt_bet[0].stt) if stt_bet else ''

#         stt_bet = self.env['tsbd.betbxh'].search([('team_id','=',self.team_id.id)])
        stt_bet = u'[%s%%, %s]'%(self.diem_phan_tram, self.bet_stt) if self.bet_stt else ''

#        
#         
        over_bet =u'(%s%%, %s, %s, %s)'%(self.bet_over_pc, self.average_sum_score, self.average_score, self.average_lost_score)
        if is_name_gon:
            template = u'%s( ST:%s, Đ:%s, B:%s, A:%s, C:%s, D:%s)%s %s'
        else:
            template = u'%s, STT:%s, Điểm: %s, Before: %s, After:%s, Champ:%s, Drop:%s %s %s'
        names = template%(r.team_id.name, stt, diem,previous_offset,next_offset,cach_4,cach_18, over_bet, stt_bet )
        
        return names
    @api.multi
    def name_get(self):
        rs = []
        for r in self:
            names = r.take_name()
            rs.append((r.id,names))
        return rs
    @api.depends('home_match_number','home_t','home_h')
    def home_b_(self):
        for r in self:
            r.home_b = r.home_match_number - r.home_t -  r.home_h
            
    home_over = fields.Integer()
    home_under = fields.Integer()
    home_ou_draw = fields.Integer()
    
    away_over = fields.Integer()
    away_under = fields.Integer()
    away_ou_draw = fields.Integer()
    
    bet_home_over = fields.Integer(compute='bet_home_over_', store=True)
    @api.depends('home_over','home_under')
    def bet_home_over_(self):
        for r in self:
            r.bet_home_over = r.home_over -  r.home_under
        
    bet_away_over = fields.Integer(compute='bet_away_over_', store= True)
    @api.depends('away_over','away_under')
    def bet_away_over_(self):
        for r in self:
            r.bet_away_over = r.away_over -  r.away_under
            
    bet_over = fields.Integer(compute='bet_over_', store= True)
    bet_over_pc = fields.Integer(compute='bet_over_', store= True)
    @api.depends('bet_home_over','bet_away_over', 'match_number')
    def bet_over_(self):
        for r in self:
            bet_over = r.bet_home_over +  r.bet_away_over
            bet_over_pc = 100*bet_over/r.match_number
            r.bet_over = bet_over
            r.bet_over_pc = bet_over_pc
    stt_bet_over = fields.Integer()        
    
    home_tg = fields.Integer()
    home_th = fields.Integer()
    home_match_number =  fields.Integer()
    
    away_t = fields.Integer()
    away_h = fields.Integer()
#     away_b = fields.Float(compute='away_b_', store=True)
    away_b = fields.Integer()
    @api.depends('away_match_number','away_t','away_h')
    def away_b_(self):
        for r in self:
            r.away_b = r.away_match_number - r.away_t -  r.away_h
            
    away_tg = fields.Integer()
    away_th = fields.Integer()
    away_match_number =  fields.Integer()
#     diem = fields.Integer(compute='diem_', store=True)
    diem = fields.Integer()
    diem_dd = fields.Integer()
    score_sum = fields.Integer(compute='score_sum_',store=True)
    lost_score_sum = fields.Integer(compute='score_sum_',store=True)
    @api.depends('away_tg','home_tg')
    def score_sum_(self):
        for r in self:
            r.score_sum = r.away_tg + r.home_tg
            r.lost_score_sum = r.away_th + r.home_th
            
    hsbt = fields.Integer(compute='hsbt_', store=True)
    @api.depends('away_tg','home_tg','away_th','home_th')
    def hsbt_(self):
        for r in self:
            r.hsbt =  r.away_tg + r.home_tg - r.away_th - r.home_th
            
    match_number =  fields.Integer(compute='match_number_',store=True)
    
    @api.depends('home_match_number', 'away_match_number')
    def match_number_(self):
        for r in self:
            r.match_number = r.home_match_number + r.away_match_number
    average_score = fields.Float(digits=(6,2), compute='average_score_', store=True)  
    average_lost_score = fields.Float(digits=(6,2), compute='average_lost_score_', store=True)
    average_sum_score = fields.Float(digits=(6,2), compute='average_sum_score_', store=True)
    @api.depends('average_score','average_lost_score','trig' )
    def average_sum_score_(self):
        for r in self:
            r.average_sum_score = r.average_score + r.average_lost_score
    @api.depends('score_sum','match_number', 'trig')
    def average_score_(self):
        for r in self:
            r.average_score = r.score_sum/r.match_number
    @api.depends('lost_score_sum','match_number', 'trig')
    def average_lost_score_(self):
        for r in self:
            r.average_lost_score = r.lost_score_sum/r.match_number
            
            
    home_average_score = fields.Float(compute='home_average_score_', store=True,string=u'home as')      
    home_lost_average_score = fields.Float(compute='home_average_score_', store=True, string=u'home las')      
    trig = fields.Boolean()
    @api.depends('home_tg', 'home_th', 'home_match_number')
    def home_average_score_(self):
        for r in self:
            if r.home_match_number:
                r.home_average_score = r.home_tg/r.home_match_number
                r.home_lost_average_score = r.home_th/r.home_match_number
            
    away_average_score = fields.Float(compute='away_average_score_', store=True, string=u'away as')      
    away_lost_average_score = fields.Float(compute='away_average_score_', store=True, string=u'away las')      
    @api.depends('away_tg', 'away_th', 'away_match_number')
    def away_average_score_(self):
        for r in self:
            if r.away_match_number:
                r.away_average_score = r.away_tg/r.away_match_number
                r.away_lost_average_score = r.away_th/r.away_match_number
            
 
    
    
    
            
#     @api.depends('home_t','home_h', 'away_t', 'away_h')
#     def diem_(self):
#         for r in self:
#             r.diem = (r.home_t + r.away_t) *3 + (r.home_h + r.away_h)
class BETBXH(models.Model):
    _inherit = 'tsbd.bxh'
#     _name = 'tsbd.betbxh'
    
    
    bet_away_h = fields.Float()
    bet_home_h = fields.Float()
    bet_home_b = fields.Float()
    bet_away_b = fields.Float()
    bet_diem = fields.Float()
    bet_home_t = fields.Float()
    bet_away_t = fields.Float()
    
    
    bet_money = fields.Float()
    diem_phan_tram = fields.Integer(compute='diem_phan_tram_',string=u'Phần trăm thắng độ')
    @api.depends('diem','match_number')
    def diem_phan_tram_(self):
        for r in self:
            r.diem_phan_tram = 100*r.bet_diem/r.match_number
            
    bet_diem_no = fields.Integer(string=u'Hiệu số thắng thua kèo')
    bet_stt = fields.Integer()

#     bet_cate_id = fields.Many2one('tsbd.cate',ondelete = 'cascade')     
    
  
    