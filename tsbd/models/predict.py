# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.addons.tsbd.models.bet import handicap_winning_ 
import re
from odoo.addons.tsbd.models.tool import  get_or_create_object_sosanh
class Predictsite(models.Model):
    _name = 'tsbd.site'
    name = fields.Char()
    short = fields.Char(default = lambda self: self.name)

def adecorator(func):
    def awrapper(*arg,**karg):  
        self = arg[0]
        for r in self:
            if r.match_state and r.match_state != u'Chưa bắt đầu':
                func(r)
    return awrapper 
class Predict(models.Model):  
    _name =  'tsbd.predict'
    trig = fields.Boolean()
    match_state = fields.Char(related='match_id.state', store=True)
    match_id = fields.Many2one('tsbd.match')
    site_id = fields.Many2one('tsbd.site',string='web site')
    link = fields.Char()
    predict_score1 = fields.Integer()
    predict_score2 = fields.Integer()
    predict_handicap = fields.Selection([('handicap1','handicap1'),('handicap2','handicap2')],compute='predict_handicap_and_ou_',store=True)
    amount = fields.Float(default=1)
    predict_exact_score_winning_amount =  fields.Float(compute='predict_exact_score_winning_amount_',store=True)
    state =  fields.Selection([('nhap_tay',u'Nhập tay'),('tu_dong','Tự động'),('can_read_du_doan','Không đọc được dự đoán')],default = 'nhap_tay')
    
    time= fields.Datetime(related='match_id.time', store=True)
    date = fields.Date (related='match_id.date', store=True)
    
    team1= fields.Many2one('tsbd.team',related='match_id.team1', store=True)
    team2= fields.Many2one('tsbd.team',related='match_id.team2', store=True)
    begin_handicap =  fields.Float(digit=(6,2),related='match_id.begin_handicap', store=True)
    begin_ou=  fields.Float(digit=(6,2),related='match_id.begin_ou', store=True)
#     state_match = fields.Char(related = 'match_id.state',store=True)
    @api.onchange('link')
    def link_oc_(self):
        if self.link:
            rs = re.search('//(.+?)/',self.link)
            site_name = rs.group(1).replace('www.','')
            site_id = get_or_create_object_sosanh (self,'tsbd.site',{'name':site_name})
            self.site_id = site_id

    @api.depends('match_id.begin_ou','match_id.begin_handicap','predict_score1','predict_score2')
    def predict_handicap_and_ou_(self):
        for r in self:
            diff = (r.predict_score1 - r.predict_score2) - r.match_id.begin_handicap
            if diff > 0:
                predict_handicap = 'handicap1'
            else:
                predict_handicap = 'handicap2'
            r.predict_handicap = predict_handicap
            
            sum_score = r.predict_score1 + r.predict_score2
            if sum_score > r.match_id.begin_ou:
                predict_ou = 'over'
            else:
                predict_ou = 'under'
            r.predict_ou = predict_ou
    predict_ou = fields.Selection([('over','over'),('under','under')],compute='predict_handicap_and_ou_',store=True)
    predict_handicap_winning_mount = fields.Float(compute='predict_handicap_winning_mount_',store=True)
    predict_ou_winning_mount = fields.Float(compute='predict_ou_winning_mount_',store=True)
    
    
    @api.depends('predict_ou','trig', 'match_state')
    @adecorator
    def predict_ou_winning_mount_(self):
        for r in self:
            bet_kind = r.predict_ou
            winning_ratio,winning_amount = handicap_winning_(r,bet_kind,mode='predict')
            r.predict_ou_winning_mount = winning_amount
    
    @api.depends('predict_handicap','trig','match_state')
    @adecorator
    def predict_handicap_winning_mount_(self):
        for r in self:
            bet_kind = r.predict_handicap
            winning_ratio,winning_amount = handicap_winning_(r,bet_kind,mode='predict')
            r.predict_handicap_winning_mount = winning_amount
            
    @api.depends('predict_score1','predict_score2','trig','match_state')
    @adecorator
    def predict_exact_score_winning_amount_(self):
        for r in self:
            bet_kind = 'exact_score'
            winning_ratio,winning_amount = handicap_winning_(r,bet_kind,mode='predict')
            r.predict_exact_score_winning_amount = winning_amount
    
    

            
