# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.addons.tsbd.models.tool import  request_html
# from odoo.addons.tsbd.models.leech import  detail_match
from odoo.addons.tsbd.models.tool import   get_or_create_object_sosanh

from bs4 import BeautifulSoup

from odoo.addons.tsbd.models.bet import handicap_winning_ 
import re

# import re
# from odoo.osv import expression

from odoo.addons.tsbd.models.leech_tool import  get_events

    
    

        
        
class BetScore(models.Model):
    _name ='tsbd.betscore'
    betscore1 = fields.Integer()
    betscore2 = fields.Integer()
    @api.multi
    def name_get(self):
        rs = []
        for r in self:
            name_show = u'%s-%s'%(r.betscore1, r.betscore2)
            rs.append((r.id,name_show))
        return rs
            
        
class BetScoreLine(models.Model):
    _name ='tsbd.betscoreline'
    betscore_id = fields.Many2one('tsbd.betscore')
    match_id = fields.Many2one('tsbd.match')
    odd = fields.Float()
    
#     @api.constrains('betscore_id','match_id','odd')
#     def scoreline(self):
#         for r in self:
#             if (r.match_id.score1 == r.betscore_id.betscore1) and  (r.match_id.score2 == r.betscore_id.betscore2):
#                 r.match_id.score_odd = r.odd
def adecorator(func):
    def awrapper(*arg,**karg):  
        self = arg[0]
        for r in self:
            if r.state != u'Chưa bắt đầu':
                func(r)
    return awrapper

def h1decorator(func):
    def awrapper(*arg,**karg):  
        self = arg[0]
        for r in self:
            if r.co_ti_so_h1 :
                func(r)
    return awrapper
        
sign = lambda x: (-1, 1)[x > 0]
      
class Match(models.Model):
    _name = 'tsbd.match'
    _order = 'time asc'
    
    
    @api.multi
    def leeching_a_match(self):
        Leech_obj = self.env['tsbd.leech']
        Leech_obj.leeching_a_match_function(self.match_link, is_get_events=True)
    
    
    @api.multi
    def get_events(self):
        
        get_events('59387',self,'team1', 'team2')
    
    @api.multi
    def create_match_for_test(self):
        m = self.env['tsbd.match'].create({'team1':1,'score1':False})
        print ('match',m)
        
        
    @api.multi
    def trig_button(self):
        self.write({'trig':True})
        
    @api.multi
    def test(self):
        ratio,amount = handicap_winning_(None, bet_kind='eu1',mode='predict', match_id =self, skip_tinh_tien=False)
        ratio2,amount2 = handicap_winning_(None, bet_kind='eu2',mode='predict', match_id =self, skip_tinh_tien=False)
        raise UserError(u'%s-%s- %s-%s'%(ratio,amount, ratio2,amount2 ))
        
        
        
    @api.multi
    def get_infor_test(self):
        large_bxh_id_of_team2 = self.team2.large_bxh_id
        stt_2 = large_bxh_id_of_team2.stt 
        cate_id = large_bxh_id_of_team2.cate_id
        
        team2range = list(filter(lambda i:i>0,range(stt_2-2,stt_2+3)))
        bxh_ids =  self.env['tsbd.bxh'].search([('cate_id','=', cate_id.id),('stt', 'in', team2range)]).mapped('team_id')
        raise UserError(u'%s'%bxh_ids)
    
    @api.multi
    def get_infor_test2(self):
        match_id = self
        betscore_id = self.env['tsbd.betscore'].search([('betscore1', '=',2 ),('betscore2', '=',1)])
        domain =  [('match_id','=',match_id.id),('betscore_id', '=',betscore_id.id )]
        print ('***domain',domain)
        bet_score_id = match_id.env['tsbd.betscoreline'].search(domain)
        print ('***bet_score_id',bet_score_id)
        raise UserError(u'%s'%bet_score_id)


  
    
        
        
    @api.multi    
    def detail_match_button(self):
        pass
#         search_dict,update_dict = detail_match(self, self.link)
#         search_dict.update(update_dict)
#         self.write(search_dict)
        
    def get_odds_button(self):
        rs= self.get_odds(self.link)
        raise UserError(u'%s'%rs)


    @api.multi
    def leech_button(self):
        rs  = request_html(self.link)
        file = open('/media/sf_C_DRIVE/D4/dl/testfile.html','w') 
        file.write(rs) 
        file.close() 
        self.log =rs
        
    def du_doan(self,soup):
        ct = soup.select('div#postContent')
        ct =  ct[0].get_text()
        rs = re.search('DỰ ĐOÁN:\s*?\d+\s*?-\s*?\d+', ct)
        ti_so =  rs.group(0)
        return ti_so
        
    @api.multi
    def parse_button(self):
        
        file = open('/media/sf_C_DRIVE/D4/dl/testfile.html','r') 
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        a_s = soup.select('a')
        hrefs = []
        for a in a_s:
            try:
                hrefs.append(a['href'])
            except:
                pass
        hrefs =  list(filter ( lambda a: 'nhan-dinh-bong-da-' in a, hrefs))
        du_doans = []
        for h in hrefs:
            link = 'http://bongdaplus.vn/' + h
            rs  = request_html(link)
            soup = BeautifulSoup(rs, 'html.parser')
            du_doan = self.du_doan(soup)
            du_doans.append(du_doan)
            
        self.parse_log =du_doans
    
    
    
    playerline_ids = fields.One2many('tsbd.playerline', 'match_id')
    away_main_playerline_ids = fields.One2many('tsbd.playerline', 'match_id', domain=[('home_or_away','=','away'), ('da_chinh_hay_du_bi','=','da_chinh')])
    away_standby_playerline_ids = fields.One2many('tsbd.playerline', 'match_id', domain=[('home_or_away','=','away'), ('da_chinh_hay_du_bi','=','du_bi')])
    round = fields.Integer()
    errorlog_ids = fields.One2many('tsbd.errorlog','match_id')
    cate_id_selection = fields.Selection('cate_id_selection_')
    def cate_id_selection_(self):
        rs = self.env['tsbd.cate'].search([('large_cate','=',True)])
        rs = list(map(lambda i:(i.name,i.name),rs))
#         print ('***cate****',rs)
        return rs    
    attr_match = fields.Selection([('single_match','tran don'), ('soon_match','tran son'), ('late_match','tran muon'), ('sametime_match','tran cung gio')])
    str_score = fields.Char(compute='str_score_',store=True)
    @api.depends('score1','score2','trig','state')
    @adecorator
    def str_score_(self):
        for r in self:
            r.str_score =u'%s-%s'%(r.score1, r.score2)
            
    log = fields.Text()
    parse_log = fields.Text()
    link = fields.Char()
    trig = fields.Boolean()
    betscoreline_ids = fields.One2many('tsbd.betscoreline', 'match_id')
   
    shots_on_target1 = fields.Integer()
    shots_off_target1 = fields.Integer()
    possession1 = fields.Integer()
    
    shots_on_target2 = fields.Integer()
    shots_off_target2 = fields.Integer()
    possession2 = fields.Integer()
    
    du_bi_players2_ids = fields.Many2many('tsbd.player','match_du_bi_players2_rel','match_id' 'player_id')
    da_chinh_players2_ids = fields.Many2many('tsbd.player','match_du_bi_players2_rel','match_id' 'player_id')
    is_min_time = fields.Boolean()
    time= fields.Datetime()#[('cate_id','=',self.id),
    date = fields.Date()
    is_copy_begin_to_curent = fields.Boolean()
    statictis_match_ids =  fields.Many2many('tsbd.match','match_statictis_match_rel','match_id', 'statictis_match_id')
    
    current_time =  fields.Float()
    state = fields.Char()
    cate_id = fields.Many2one('tsbd.cate')
    bxh1_id = fields.Many2one('tsbd.bxh', related='team1.large_bxh_id')
    bxh2_id = fields.Many2one('tsbd.bxh',  related='team2.large_bxh_id')
    
    bxh_ids = fields.Many2many('tsbd.bxh',compute='bxh_ids_')
    h1score1 = fields.Integer(compute='h1score1_',store=True)
    h1score2 = fields.Integer(compute='h1score1_',store=True)
    
    lat_keo = fields.Boolean(compute='lat_keo_', store=True)
    @api.depends('score1','score2','begin_handicap')
    def lat_keo_(self):
        for r in self:
            rs = ( r.score1 - r.score2 ) * r.begin_handicap
            r.lat_keo = rs < 0 
        
    
    sum_h1 = fields.Integer(compute='sum_h1_', store=True)
    @api.depends('h1score1','h1score2','trig')
    def sum_h1_(self):
        for r in self:
            r.sum_h1 = r.h1score1 + r.h1score2
    range_sum_h1 = fields.Selection([('0','0'), ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'),('gt5','gt5')], compute='range_sum_h1_', store=True)
    
    @api.depends('sum_h1','co_ti_so_h1') 
    def range_sum_h1_(self):
        for r in self:
            if r.co_ti_so_h1:
                sum_h1 = r.sum_h1
                if sum_h1 > 5:
                    rt = 'gt5'
                else:
                    rt = str(sum_h1)
                r.range_sum_h1 = rt
            else:
                r.range_sum_h1 = False
    sum_h2 = fields.Integer(compute='sum_h2_', store=True)
    range_sum_h2 = fields.Selection([('0','0'), ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'),('gt5','gt5')], compute='sum_h2_', store=True)
    @api.depends('sum_h1','score1', 'score2', 'co_ti_so_h1')
    @h1decorator
    def sum_h2_(self):
        for r in self:
            sum_h2 = r.score1 + r.score2 - r.sum_h1
            if sum_h2 > 5:
                range_sum_h2 = 'gt5'
            else:
                range_sum_h2 = str(sum_h2)
            r.range_sum_h2 = range_sum_h2
                
            
        
    sum_ft = fields.Integer(compute='sum_ft_', store=True)
    @api.depends('score1','score2')
    def sum_ft_(self):
        for r in self:
            r.sum_ft = r.score1 + r.score2
    range_sum_ft = fields.Selection([('0','0'), ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'),('gt5','gt5')], compute='range_sum_ft_', store=True)
    @api.depends('sum_ft') 
    def range_sum_ft_(self):
        for r in self:
            sum_h1 = r.sum_ft
            if sum_h1 > 5:
                rt = 'gt5'
            else:
                rt = str(sum_h1)
            r.range_sum_ft = rt
   
   
    first_per_full = fields.Float(compute='first_per_full_',store=True)
    @api.depends('sum_h1', 'sum_ft')
    def first_per_full_(self):
        for r in self:
            if r.sum_ft:
                r.first_per_full = r.sum_h1/r.sum_ft
    
    
    co_ti_so_h1 = fields.Boolean(compute='h1score1_',store = True)

    @api.depends('event_ids')
    def h1score1_(self):
        for r in self:
            event = self.env['tsbd.event'].search([('match_id','=', r.id),('event','=','h1_finish')])
            if event:
                r.h1score1 = event.score1
                r.h1score2 = event.score2
                r.co_ti_so_h1 = True
    
    def bxh_ids_(self):
        for r in self:
            r.bxh_ids = [(6,0,r.cate_id.cate_ids.ids)]
    
#     @api.depends('team1','team2')
#     def bxh_(self):
#         for r in self:
#             if r.team1:
#                 bxh_id = self.env['tsbd.bxh'].search ([('team_id','=',r.team1.id)])
#                 if bxh_id:
#                     r.bxh1_id = bxh_id[0]
#                     
#             if r.team2:
#                 bxh_id = self.env['tsbd.bxh'].search ([('team_id','=',r.team2.id)])
#                 if bxh_id:
#                     r.bxh2_id = bxh_id[0]
        
    bang_id = fields.Many2one('tsbd.cate')
    
    period_id = fields.Many2one('tsbd.period')
    name = fields.Char(compute='name_',store=True)
    @api.depends('team1','team2','time','score1','score2','state','trig')
    def name_(self):
        for r in self:
            if r.time:
                time_txt = (fields.Datetime.from_string(r.time) + timedelta(hours=7)).strftime('%d/%m/%Y %H:%M')
            else:
                time_txt = (fields.Date.from_string(r.date) ).strftime('%d/%m/%Y')
            state = r.state 
            if state ==u'Chưa bắt đầu':
                score_txt ='X-X'
            else:
                score_txt = str(r.score1)  +' - ' + str(r.score2)
            if  r.team1.name  and   r.team2.name:
                name = r.team1.name + '    ' + score_txt + '    ' + r.team2.name + '    ' + time_txt
                r.name = name
                
    @api.model
    def name_get(self):
        rs = []
        for r in self:
            if r.time:
                time_txt = (fields.Datetime.from_string(r.time) + timedelta(hours=7)).strftime('%d/%m/%Y %H:%M')
            else:
                time_txt = (fields.Date.from_string(r.date) ).strftime('%d/%m/%Y')
            state = r.state 
            if state ==u'Chưa bắt đầu':
                score_txt ='X-X'
            else:
                score_txt = str(r.score1)  +' - ' + str(r.score2)
            hd_ou = '(HD:%s, OU:%s)'%(r.begin_handicap,r.begin_ou)
#             if  r.team1.name  and   r.team2.name:
            name = r.team1.take_name() + '    ' + score_txt + '    ' + r.team2.take_name() + '    ' + time_txt + ' ' +hd_ou
            rs.append((r.id,name))
        return rs
                
                
     
    match_link = fields.Char()
    
    scoreodd = fields.Float(compute='score_odd_',store=True)
    
    @api.depends('score1','score2','betscoreline_ids','trig')
    @adecorator
    def score_odd_(self):
        for r in self:
            ratio,amount = handicap_winning_(None, bet_kind='exact_score',mode='predict', match_id =r)
            r.scoreodd = amount
    
    
    team1= fields.Many2one('tsbd.team')
    team2= fields.Many2one('tsbd.team')
    team1_stt = fields.Integer(related='team1.large_bxh_id.stt', store=True)
    team2_stt = fields.Integer(related='team2.large_bxh_id.stt', store=True)
    
    team1_bxh_ids = fields.Many2many('tsbd.bxh',compute='team1_bxh_ids_')
    team2_bxh_ids = fields.Many2many('tsbd.bxh',compute='team1_bxh_ids_')
    
    ou_team1_bxh_ids = fields.Many2many('tsbd.bxh',compute='team1_bxh_ids_')
    ou_team2_bxh_ids = fields.Many2many('tsbd.bxh',compute='team1_bxh_ids_')
    
    guest_score1 = fields.Integer()
    guest_score2 = fields.Integer()
    avg_sum_score = fields.Float(digits=(6,2), compute='avg_sum_score_',store = True,string=u'TB Bàn Thắng')
    du_doan_show = fields.Char( compute ='du_doan_show_')
    
    @api.depends('predict_ids')
    def du_doan_show_(self):
        for r in self:
            rs = []
            for new in r.predict_ids:
                if r.state =='can_read_du_doan':
                    ti_so =': x-x'
                else:
                    ti_so = ': %s-%s'%(new.predict_score1, new.predict_score2)
                astr = new.site_id.short or new.site_id.name +ti_so
                rs.append(astr)
            rs = u'*'.join(rs)
            r.du_doan_show = rs
                
    
    @api.depends('team1', 'team2')
    def avg_sum_score_(self):
        for r in self:
            if r.team1.large_bxh_id and r.team2.large_bxh_id :
                r.avg_sum_score = (r.team1.large_bxh_id.average_sum_score + r.team2.large_bxh_id.average_sum_score)/2
    
    
    @api.depends('team1')
    def team1_bxh_ids_(self):
        for r in self:
            r.team1_bxh_ids = [(6,0,[r.team1.large_bxh_id.id])]
            r.team2_bxh_ids = [(6,0,[r.team2.large_bxh_id.id])]
            
            r.ou_team1_bxh_ids = [(6,0,[r.team1.large_bxh_id.id])]
            r.ou_team2_bxh_ids = [(6,0,[r.team2.large_bxh_id.id])]
            
    hw_hl = fields.Char(compute= 'hw_hl_', store=True)
    hw_aw = fields.Char(compute= 'hw_hl_', store=True)
    al_aw = fields.Char(compute= 'hw_hl_', store=True)
    al_hl = fields.Char(compute= 'hw_hl_', store=True)
    
    @api.depends('team1','team2','trig')
    def hw_hl_(self):
        for  r in self:
            hw, hl = r.team1.large_bxh_id.home_average_score, r.team1.large_bxh_id.home_lost_average_score
            aw, al = r.team2.large_bxh_id.away_average_score, r.team2.large_bxh_id.away_lost_average_score
            
            r.hw_hl = '%.02f-%.02f (%.02f)'%(hw,hl,hw+hl)
            r.hw_aw = '%.02f-%.02f (%.02f)'%(hw, aw, hw + aw)
            
            r.al_aw = '%.02f-%.02f (%.02f)'%(al, aw, al + aw)
            r.al_hl = '%.02f-%.02f (%.02f)'%(al, hl,al + hl)


    nhan_dinh_txt = fields.Char(compute='nhan_dinh_txt_')
    @api.depends('team1', 'team2')
    def nhan_dinh_txt_(self):
        for r in self:
            r.nhan_dinh_txt = u'Nhận định %s %s %s'%(r.team1.name,r.team2.name, fields.Date.from_string(r.date).strftime('%d-%m-%Y'))
    score1 = fields.Integer(default=False)
    score2 = fields.Integer()
    sum_score12 = fields.Float(compute='sum_score12_', store=True, group_operator='avg')
    @api.depends('score1','score2')
    def sum_score12_(self):
        for r in self:
            r.sum_score12 = r.score1 + r.score2
    event_ids =  fields.One2many('tsbd.event','match_id')
    event_show = fields.Char(compute='event_show_')
    @api.depends('event_ids')
    def event_show_(self):
        for r in self:
            goal_event_ids = r.event_ids.filtered(lambda r: r.event == 'goal')
            event_shows = []
            for event in goal_event_ids:
                minute = u'%s%s'%(event.current_time, u'+%s'%event.adding_time if event.adding_time else '')
                a_show = u'%s:%s'%(minute, event.str_score)
                event_shows.append(a_show)
            event_show = u','.join(event_shows)
            r.event_show = event_show
    bet_ids =  fields.One2many('tsbd.bet','match_id')
    
    hd_ou_show = fields.Char(compute='hd_ou_show_')
    @api.depends('begin_handicap','begin_ou')
    def hd_ou_show_(self):
        for r in self:
            r.hd_ou_show =u'Handicap %s, Over/Under %s'%(r.begin_handicap, r.begin_ou)
    
    begin_handicap_money1 =  fields.Float(default=100,digit=(6,3))
    begin_handicap_money2 =  fields.Float(default=100,digit=(6,3))
    begin_handicap =  fields.Float(digit=(6,2))
    
    begin_ou_money1 =  fields.Float(default=100,digit=(6,3))
    begin_ou_money2 =  fields.Float(default=100,digit=(6,3))
    begin_ou =  fields.Float(digit=(6,2))
    
    curent_handicap_money1 =  fields.Float(default=100,digit=(6,3))
    curent_handicap_money2 =  fields.Float(default=100,digit=(6,3))
    curent_handicap = fields.Float(digit=(6,2))
    
    curent_ou_money1 =  fields.Float(default=100,digit=(6,3))
    curent_ou_money2 =  fields.Float(default=100,digit=(6,3))
    curent_ou =  fields.Float(digit=(6,2))
    
    predict_ids = fields.One2many('tsbd.predict','match_id')
    
    total_winning_amount = fields.Float(compute='total_winning_amount_',store=True)
    @api.depends('bet_ids')
    def total_winning_amount_(self):
        for r in self:
            r.total_winning_amount = sum(r.bet_ids.mapped('winning_amount'))
    

    winner = fields.Selection([('doi_nha',u'Đội nhà'), ('doi_khach',u'Đội khách'), ('hoa',u'Hai đội hòa')], compute='_match_winner', store= True)
    loser = fields.Selection([('doi_nha',u'Đội nhà'), ('doi_khach',u'Đội khách'), ('hoa',u'Hai đội hòa')], compute='_match_winner', store= True)
    @api.depends('score1','score2','trig','state')
    @adecorator
    def _match_winner(self):
        for r in self:
            if r.score1 > r.score2:
                r.winner = 'doi_nha'
                r.loser = 'doi_khach'
            elif r.score1< r.score2:
                r.winner = 'doi_khach'
                r.loser = 'doi_nha'    
            else:
                r.winner = 'hoa'
                r.loser = 'hoa'    
    # compute fields 
    keo_0_025_05 = fields.Float(compute='_keo_0_025_05', store=True)
    @api.depends('score1', 'score2', 'begin_handicap','state','trig')
    def _keo_0_025_05(self):
        for r in self:
            r.keo_0_025_05 = abs(r.begin_handicap - float(int(r.begin_handicap)))
    
    handicap_0_05_1 = fields.Float(compute='handicap_wl_compute_', store=True)
    
    cua_tren_hay_cua_duoi = fields.Selection([(u'cua_tren',u'Cửa trên'), (u'cua_duoi',u'Cửa dưới'), (u'hoa_tien',u'Hòa tiền'), (u'team1',u'team1'), (u'team2',u'team2')], 
                                       compute='handicap_wl_compute_', store=True)
    handicap_bet_winner = fields.Selection([('team1',u'Team1'), ('team2',u'Team 2'), ('hoa',u'Hòa')], compute='handicap_wl_compute_', store= True)
    handicap_bet_loser = fields.Selection([('team1',u'Team1'), ('team2',u'Team 2'), ('hoa',u'Hòa')], compute='handicap_wl_compute_', store= True)
    
    handicap_wl1 = fields.Float(compute='handicap_wl_compute_', store=True)
    handicap_wl2 = fields.Float(compute='handicap_wl_compute_', store=True)
    handicap_win_amount = fields.Float(compute='handicap_wl_compute_', store=True)
    handicap_lost_amount = fields.Float(compute='handicap_wl_compute_', store=True)
    handicap_wl_amount1 = fields.Float(compute='handicap_wl_compute_', store=True)
    handicap_wl_amount2 = fields.Float(compute='handicap_wl_compute_', store=True)
    
    eu1_odd = fields.Float()
    eu_draw_odd = fields.Float()
    eu2_odd= fields.Float()
    
    
    eu1_amount = fields.Float(compute='eu_amount_', store= True)
    eu_draw_amount = fields.Float(compute='eu_amount_', store= True)
    eu2_amount = fields.Float(compute='eu_amount_', store= True)
    
    @api.depends('score1', 'score2', 'eu1_odd', 'eu2_odd', 'eu_draw_odd','state', 'trig')
    @adecorator
    def eu_amount_(self):
        for r in self:
            if r. eu1_odd:
                ratio,amount = handicap_winning_(None, bet_kind='eu1',mode='predict', match_id =r)
                r.eu1_amount = amount
                
                ratio,amount = handicap_winning_(None, bet_kind='eu_draw',mode='predict', match_id =r)
                r.eu_draw_amount = amount
                
                ratio,amount = handicap_winning_(None, bet_kind='eu2',mode='predict', match_id = r)
                r.eu2_amount = amount
            
            
            
            
            
            
    
    
    @api.depends('score1', 'score2', 'begin_handicap','state', 'trig')
    @adecorator
    def handicap_wl_compute_(self):
        for r in self:
            if r.state != u'Chưa bắt đầu':
                ratio, amount = handicap_winning_(None, bet_kind='handicap1',mode='predict', match_id =r)
                r.handicap_wl1 = ratio
                r.handicap_wl2 = -ratio
                r.handicap_0_05_1 = abs(ratio)
                if ratio > 0:
                    doi_thang = 'team1'
                    r.handicap_bet_winner ='team1'
                    r.handicap_bet_loser = 'team2'
                    r.handicap_win_amount = amount
                    ratio_handicap_lost, handicap_lost_amount = handicap_winning_(None, bet_kind='handicap2',mode='predict', match_id =r)
                    r.handicap_lost_amount = handicap_lost_amount
                    r.handicap_wl_amount1 = amount
                    r.handicap_wl_amount2 = handicap_lost_amount
                elif ratio < 0:
                    doi_thang = 'team2'
                    r.handicap_bet_winner = 'team2'
                    r.handicap_bet_loser = 'team1'
                    ratio_handicap_win, handicap_win_amount = handicap_winning_(None, bet_kind='handicap2', mode='predict', match_id =r)
                    r.handicap_lost_amount = amount
                    r.handicap_win_amount = handicap_win_amount
                    r.handicap_wl_amount1 = amount
                    r.handicap_wl_amount2 = handicap_win_amount
                else:
                    doi_thang= 'hoa_tien'
                    r.handicap_bet_winner = 'hoa'
                    r.handicap_bet_loser = 'hoa'
                adict  ={}
                if r.begin_handicap > 0:
                    adict = {'team1':'cua_tren', 'team2':'cua_duoi'}
                elif r.begin_handicap < 0:
                    adict = {'team2':'cua_tren', 'team1':'cua_duoi'}
                rs = adict.get(doi_thang, doi_thang)
                r.cua_tren_hay_cua_duoi = rs    
                
                
                
                   
    context_team_handicap_wl = fields.Float(compute='context_team_handicap_wl_')
    @api.depends('team1','team2','handicap_wl1','handicap_wl2')
    @adecorator
    def context_team_handicap_wl_(self):
        team = self._context.get('team')
        if team:
            for r in self:
                if r.team1.id == team:
                    r.context_team_handicap_wl = r.handicap_wl1
                elif r.team2.id == team:
                    r.context_team_handicap_wl = r.handicap_wl2
                    
    context_begin_handicap = fields.Float(compute='context_begin_handicap_')
    @api.depends('team1','team2','handicap_wl1','handicap_wl2')
    @adecorator
    def context_begin_handicap_(self):
        team = self._context.get('team')
        if team:
            for r in self:
                if r.team1.id == team:
                    r.context_begin_handicap = r.begin_handicap
                elif r.team2.id == team:
                    r.context_begin_handicap = -r.begin_handicap
                    
                    
    
    sum_handicap_wl1 = fields.Float(compute='sum_handicap_wl1_2_')
    sum_handicap_wl2 = fields.Float(compute='sum_handicap_wl1_2_')
    @api.depends('team1', 'team2','team_match_limit','handicap_wl1','handicap_wl2','team_match_limit')
    def sum_handicap_wl1_2_(self):
        for r in self:
            team_match_limit = r.team_match_limit
            limit = team_match_limit and u'limit %s'%r.team_match_limit or ''
            for f_name in ['1','2']:
#                 team_id =r.team1.id
                team_id =getattr(r,'team%s'%f_name).id
                rs = 0
                for number_team in [1,2]:
                    where =  "(team1 = %(team_id)s or team2 = %(team_id)s) and state = 'Kết thúc' order by date desc"%{'team_id':team_id}
                    have =  'having A.team%(number_team)s= %(team_id)s'%{'number_team':number_team,'team_id':team_id}
                    sql_query = '''select A.team%(number_team)s,sum(A.handicap_wl%(number_team)s) from (select team%(number_team)s, handicap_wl%(number_team)s from tsbd_match  where %(where)s %(limit)s) A   group by team%(number_team)s %(have)s
        '''%{'number_team':number_team,'team_id':team_id, 'limit':limit,'where':where,'have':have}
                    self.env.cr.execute(sql_query)
                    rs2 = self.env.cr.dictfetchall()
                    if rs2:
                        rs2 = rs2[0]['sum']
                        rs +=rs2
                setattr(r,'sum_handicap_wl%s'%f_name,rs)
                
                
                
                
    over_or_under = fields.Selection([('over','Over'), ('under','Under'),('draw',u'Hòa')], compute='over_or_under_compute_', store=True)
    over_0_05_1 = fields.Float(compute='over_or_under_compute_', store=True)
    over_wl = fields.Float(compute='over_or_under_compute_', store=True)
    under_wl = fields.Float(compute='over_or_under_compute_', store=True)
    over_wl_amount = fields.Float(compute='over_or_under_compute_', store=True)
    under_wl_amount = fields.Float(compute='over_or_under_compute_', store=True)
    ou_win_amount = fields.Float(compute='over_or_under_compute_', store=True)
    ou_lost_amount = fields.Float(compute='over_or_under_compute_', store=True)
    @api.depends('score1','score2','begin_ou','trig')
    @adecorator
    def over_or_under_compute_(self):
        for r in self:
            ratio_over, over_amount = handicap_winning_(None, bet_kind='over',mode='predict', match_id =r)
            r.over_wl = ratio_over
            r.under_wl = -ratio_over
            r.over_0_05_1 = abs(ratio_over)
            if ratio_over > 0:
                r.over_or_under = 'over'
                ratio_under, under_amount = handicap_winning_(None, bet_kind='under',mode='predict', match_id =r)
                r.ou_win_amount = over_amount
                r.ou_lost_amount = under_amount
            elif ratio_over < 0:
                r.over_or_under = 'under'
                ratio_under, under_amount = handicap_winning_(None, bet_kind='under',mode='predict', match_id =r)
                r.ou_win_amount = under_amount
                r.ou_lost_amount = over_amount
            else:
                r.over_or_under = 'draw'
                under_amount = 0
            r.over_wl_amount = over_amount
            r.under_wl_amount = under_amount
            
    
    team1_over = fields.Integer(compute = 'team1_team_2_over_under_')
    team1_under = fields.Integer(compute = 'team1_team_2_over_under_')
    team2_over = fields.Integer(compute = 'team1_team_2_over_under_')
    team2_under = fields.Integer(compute = 'team1_team_2_over_under_')
    @api.depends('team1_match_ids','trig')
    def team1_team_2_over_under_(self):
        for r in self:
            teams =[('team1',r.team1.id), ('team2',r.team2.id)]
            for team_name, team in teams:
                rs1 = self.env['tsbd.match'].read_group(['|', ('team1', '=', team ), ('team2', '=', team )],['over_or_under'], ['over_or_under'], lazy=False )
                for adict in rs1:
                    over_or_under = adict['over_or_under']
                    if over_or_under =='over' or over_or_under =='under':
                        setattr(r, '%s_%s'%(team_name,over_or_under), adict['__count'])
    
    team1_match_ids = fields.Many2many('tsbd.match', 'match_match_rel', 'match_id', 'team1_match_id', compute='team1_match_ids_')
    team1_match_conclude = fields.Char(compute='team1_match_ids_')
    team2_match_ids = fields.Many2many('tsbd.match', 'match_matchofteam2_rel', 'match_id', 'team2_match_id', compute='team1_match_ids_', )
    team2_match_conclude = fields.Char(compute='team1_match_ids_')
    team_match_limit = fields.Integer(store=False)
    @api.depends('team1','team_match_limit','matchs_filter_by_cate','cate_id')
    def team1_match_ids_(self):
        for r in self:
            limit =5#r.team_match_limit or None# r.team_match_limit or None
            for no_team in ['1', '2']:
                team = getattr(r,'team%s'%no_team).id
                domain =['|', ('team1', '=',team ), ('team2', '=', team),('state','!=',u'Chưa bắt đầu')]
                if r.matchs_filter_by_cate:
                    domain.append(('cate_id','=',r.cate_id.id))
                rs = self.env['tsbd.match'].search(domain,order='date desc', limit= limit)
                setattr(r, 'team%s_match_ids'%no_team,[(6,0,rs.ids)])
                conclude = self.gen_handicap_and_over_array_str(rs, team)
                setattr(r, 'team%s_match_conclude'%no_team,conclude)
    
    
    related_team1_matchs = fields.Many2many('tsbd.match', 'match1_match_rel', 'matchr_id', 'team1_matchr_id', compute='related_team1_matchs_')
    all_related_team1_matchs = fields.Many2many('tsbd.match', 'all_match1_match_rel', 'all_matchr_id', 'all_team1_matchr_id', compute='related_team1_matchs_')
    related_team2_matchs = fields.Many2many('tsbd.match', 'match2_match_rel', 'matchr_id2', 'team1_matchr_id2', compute='related_team1_matchs_')
    all_related_team2_matchs = fields.Many2many('tsbd.match', 'all_match2_match_rel', 'all_matchr_id2', 'all_team1_matchr_id2', compute='related_team1_matchs_')
    
    related_team1_conclude = fields.Char(compute='related_team1_matchs_')
    all_related_team1_conclude = fields.Char(compute='related_team1_matchs_')
    related_team2_conclude = fields.Char(compute='related_team1_matchs_')
    all_related_team2_conclude = fields.Char(compute='related_team1_matchs_')
    
    hora_related_team1_matchs = fields.Many2many('tsbd.match', 'match1_match_rel', 'matchr_id', 'team1_matchr_id', compute='related_team1_matchs_')
    hora_related_team2_matchs = fields.Many2many('tsbd.match', 'match2_match_rel', 'matchr_id2', 'team1_matchr_id2', compute='related_team1_matchs_')
    hora_related_team1_conclude = fields.Char(compute='related_team1_matchs_')
    hora_related_team2_conclude = fields.Char(compute='related_team1_matchs_')
    matchs_filter_by_cate = fields.Boolean(default=True)
    number_team_relate = fields.Integer(default =4)
    
    
    @api.depends('number_team_relate')
    def related_team1_matchs_(self):
        for r in self:
            number_team_relate = r.number_team_relate
            map_dict = {'team1':{'op':'team2','team':r.team1.id}, 'team2':{'op':'team1', 'team':r.team2.id}}
            for all_relate_or_home_away in ['all_','', 'hora_']:
                for team, ad in map_dict.items():
                    op = ad['op']
                    large_bxh_id_of_team2 = getattr(r,op ).large_bxh_id
                    stt_2 = large_bxh_id_of_team2.stt
                    stt_1 =  getattr(r,team ).large_bxh_id.stt
                    cate_id = large_bxh_id_of_team2.cate_id
                    team2range = list(filter(lambda i:i>0 and i !=stt_1,range(stt_2-number_team_relate, stt_2+ number_team_relate + 1)))
                    team_ids =  self.env['tsbd.bxh'].search([('cate_id','=', cate_id.id),('stt', 'in', team2range)]).mapped('team_id')
                    if all_relate_or_home_away =='':
                        domain = [('state','!=',u'Chưa bắt đầu'),(team,'=',getattr(r,team).id), (op,'in', team_ids.ids)]
                    elif all_relate_or_home_away =='hora_':
                        domain = [('state','!=',u'Chưa bắt đầu'),(team,'=',getattr(r,team).id)]
                    else:
                        domain = [('state','!=',u'Chưa bắt đầu'),'&','|', ('team1','=',getattr(r,team).id),('team2','=',getattr(r,team).id), '|',('team1','in', team_ids.ids), ('team2','in', team_ids.ids)]
                   
                    team2_ids = self.env['tsbd.match'].search(domain, order='date desc')
                    setattr(r, '%srelated_%s_matchs'%(all_relate_or_home_away, team), [(6,0,team2_ids.ids)])
                    conclude = self.gen_handicap_and_over_array_str(team2_ids, ad['team'])
#                     conclude = u'%s--domain:%s'%(conclude,domain)
                    setattr(r, '%srelated_%s_conclude'%(all_relate_or_home_away, team), conclude)
    def same_or_change(self, al):
        i_pre = None
        sign_pre ,sign,  same,change,   = 0, 0,1,0
        wl_same_list, win_same_list,lose_same_list,change_list   =[],[],[], []
        for c, i in enumerate(al):
                if i !=0 or c == (len(al)-1) :
                    if i_pre ==None:
                        i_pre = i
                        continue
                    if i !=0:
                        sign = i*i_pre
                        sign_of_sign = sign * sign_pre
                    else:
                        sign_of_sign = 0
                    if i_pre > 0:
                        same_list = win_same_list
                    else:
                        same_list = lose_same_list
                    if sign < 0 :
                        if i !=0:
                            change +=1
                        if sign_of_sign < 0 :
                            same_list.append(same)
                            wl_same_list.append(same)
                            same = 1
                        if c == (len(al)-1):
                            change_list.append(change)
                    elif sign > 0:
                        if i !=0:
                            same +=1
                        if sign_of_sign< 0:
                            change_list.append(change)
                            change =0
                        if c == (len(al)-1):
                            same_list.append(same)
                            wl_same_list.append(same)
                    i_pre = i
                    sign_pre = sign
        return wl_same_list, win_same_list, lose_same_list,change_list      
#     def same_or_change(self, al):
#         i_pre = None
#         sign_pre = 0
#         same = 1
#         sign=0
#         wl_same_list =[]
#         win_same_list =[]
#         lose_same_list =[]
#         change = 0
#         change_list = []
#         for c, i in enumerate(al):
#          
#                 if i !=0 or (i==0 and c == (len(al)-1)) :
# #                     print ('c',c,'i_pre',i)
#                     if i_pre ==None:
#                         i_pre = i
#                         continue
#                     if i !=0:
#                         sign = i*i_pre
#                         sign_of_sign = sign * sign_pre
# #                         print ('sign_of_sign', sign_of_sign)
#                     if i_pre > 0:
#                         same_list = win_same_list
#                     else:
#                         same_list = lose_same_list
#         
#                     if sign < 0 :# change
#                         if i !=0:
#                             change +=1
#                         if sign_of_sign < 0 :
#                             same_list.append(same)
#                             append_list = same_list
#                             append_item = same
#                             wl_same_list.append(same)
#                         else:
#                             if c == (len(al)-1):
# #                                 print ('hahahah')
#                                 append_list = change_list
#                                 append_item = change
#                                 change_list.append(change)
#                         same = 1 
#     #                     i_pre =i
#     #                     sign_pre = sign
#                     elif sign > 0:
#                         if i !=0:
#                             same +=1
#                         if sign_of_sign< 0:
#                             change_list.append(change)
#                             append_list = change_list
#                             append_item = change
#                        
#                         else:
#                             if c == (len(al)-1):
# #                                 print ('ahahaha')
#                                 append_list = same_list
#                                 append_item = same
#                                 same_list.append(same)
#                                 wl_same_list.append(same)
#                         change =0
#                     i_pre = i
#                     sign_pre = sign
#         return wl_same_list, win_same_list, lose_same_list,change_list
       
    
    def gen_bet_handicap_array_str(self, rs, team):
        ad = {1:'W',-1: 'L', 0.5: 'W/2', -0.5:'L/2', 0:'D'}
        rs = rs.with_context(team=team).mapped('context_team_handicap_wl')
        wl_same_list, win_same_list, lose_same_list,change_list = self.same_or_change(rs)
        st_wl_list = map(lambda i: ad[i], rs)
        st_wl = u' '.join(st_wl_list)
        rs_win = list(filter(lambda i : i>0, rs))
        rs_losse = list(filter(lambda i : i<0, rs))
        rs_draw = list(filter(lambda i : i==0, rs))
        kluan = u'Hadicap %s (%s, %s, %s, %s) win_same_list: %s, lose_same_list: %s, change_list:%s '%(st_wl, len(rs_win),len(rs_draw),  len(rs_losse), sum(rs),win_same_list,lose_same_list, change_list)   
        return kluan
    
    def gen_over_under_array_str(self, rs, team):
        list_over_wl = rs.with_context(team=team).mapped('over_wl')
        rs_for_array = rs.with_context(team=team).mapped('over_or_under')
        rs_for_array = filter(lambda i:i,rs_for_array) # xem lại
        rs_for_array= map(lambda i:i[0].upper(),rs_for_array)
        rs_for_array = u' '.join(rs_for_array)
        rs_win = list(filter(lambda i : i>0, list_over_wl))
        rs_losse = list(filter(lambda i : i<0, list_over_wl))
        rs_draw = list(filter(lambda i : i==0, list_over_wl))
#         kluan = u'Over:%s - Draw:%s - Under:%s, Tổng %s'%(len(rs_win),len(rs_draw),  len(rs_losse), sum(rs))  
        kluan = u'Over Bet: %s  (%s, %s, %s, %s)'%(rs_for_array, len(rs_win),len(rs_draw),  len(rs_losse), sum(list_over_wl))   
        return kluan
    
    
    def get_context_begin_handicap_array_str(self,rs,team):
        match_len = len(rs)
        if match_len:
            handicap = rs.with_context(team=team).mapped('context_begin_handicap')
            ou =  rs.mapped('begin_ou')
            kluan = u'(AVG Handicap: %.02f, AVG O/U: %.02f, Số trận: %s)'%(sum(handicap)/match_len, sum(ou)/match_len, match_len)   
        else:
            kluan = ''
        return kluan
    
    def gen_winner_array_str(self, rs, team):
     
#         rs_goc = rs
        rs = rs.with_context(team=team).mapped('context_team_normal_wl')
        rs_win = list(filter(lambda i : i=='thang', rs))
        rs_losse = list(filter(lambda i : i=='bai', rs))
        rs_draw = list(filter(lambda i : i=='hoa', rs))
        
        convert_rs =  map(lambda i:i[0].upper(),rs)
        convert_rs = ' '.join(convert_rs)
                
        
        kluan = u'Thắng Thua %s (%s, %s, %s)'%(convert_rs, len(rs_win),len(rs_draw),  len(rs_losse))   
        return kluan
    
    
    
    def gen_handicap_and_over_array_str(self,rs,team):
        thang_thua = self.gen_winner_array_str(rs,team)
        general = self.get_context_begin_handicap_array_str( rs, team)
        hd = self.gen_bet_handicap_array_str( rs, team)
        ou = self.gen_over_under_array_str( rs, team)
        kl = u'%s***%s***%s***%s'%(general,thang_thua, hd,ou)
        return kl
    
    
    
            
    team1_winlost_txt = fields.Char(compute='team1_winlost_txt_')
    team2_winlost_txt = fields.Char(compute='team1_winlost_txt_')
    team1_winlost5_txt = fields.Char(compute='team1_winlost_txt_')
    team2_winlost5_txt = fields.Char(compute='team1_winlost_txt_')
    
    team1_ou_txt = fields.Char(compute='team1_winlost_txt_')
    team2_ou_txt = fields.Char(compute='team1_winlost_txt_')
    @api.depends('team1')
    def team1_winlost_txt_(self):
        for r in self:
            ad = {5:5,10:''}
            for limit in ad:
                apart_name = ad[limit]
                for  no_team in ['1', '2']:
                    team = getattr(r,'team%s'%no_team).id
                    rs = self.env['tsbd.match'].search(['|', ('team1', '=', team ), ('team2', '=', team ),('state','!=',u'Chưa bắt đầu')],limit=limit, order = 'date desc')
#                     rs = rs.with_context(team=team).mapped('context_team_handicap_wl')
#                     rs_win = list(filter(lambda i : i>0, rs))
#                     rs_losse = list(filter(lambda i : i<0, rs))
#                     rs_draw = list(filter(lambda i : i==0, rs))
#                     kluan = u'%s - %s - %s, Tổng %s'%(len(rs_win),len(rs_draw),  len(rs_losse), sum(rs))
                    
                    kluan = self.gen_bet_handicap_array_str(rs,team)
                    setattr(r, 'team%s_winlost%s_txt'%(no_team,apart_name),kluan)
                    if limit ==10:
                        kluan = self.gen_over_under_array_str(rs,team)
                        setattr(r, 'team%s_ou%s_txt'%(no_team,apart_name),kluan)
            
            
            
   
   
    context_team_normal_wl =  fields.Selection([('thang',u'Thắng'), ('hoa',u'Hoà'), ('bai',u'Bại')], compute='context_team_normal_wl_' )
    @api.depends('team1', 'team2')
    def context_team_normal_wl_(self):
        for r in self:
            team = self._context.get('team')
            if r.team1.id == team :
                if r.winner =='doi_nha':
                    rs = 'thang'
                elif r.winner =='doi_khach':
                    rs = 'bai'
                else:
                    rs ='hoa'
                r.context_team_normal_wl = rs
            elif r.team2.id == team:
                if r.winner =='doi_nha':
                    rs = 'bai'
                elif r.winner =='doi_khach':
                    rs = 'thang'
                else:
                    rs ='hoa'
                r.context_team_normal_wl = rs
            else:
                pass
                
                
            
    
    team1_nomal_winlost_txt = fields.Char(compute='team1_nomal_winlost_txt_')
    team2_nomal_winlost_txt = fields.Char(compute='team1_nomal_winlost_txt_')
    @api.depends('team1')
    def team1_nomal_winlost_txt_(self):
        for r in self:
            for  no_team in ['1', '2']:
                team = getattr(r,'team%s'%no_team).id
                rs = self.env['tsbd.match'].search(['|', ('team1', '=',team), ('team2', '=', team),('state','!=',u'Chưa bắt đầu')],limit=10, order = 'date desc')
                
                
#                 rs = rs.with_context(team=team).mapped('context_team_normal_wl')
#                 rs_win = list(filter(lambda i : i=='thang', rs))
#                 rs_losse = list(filter(lambda i : i=='bai', rs))
#                 rs_draw = list(filter(lambda i : i=='hoa', rs))
#                 
#                 convert_rs =  map(lambda i:i[0].upper(),rs)
#                 convert_rs = ' '.join(convert_rs)
#                 
#                 
#                 kluan = u'%s - %s -%s'%(len(rs_win),len(rs_draw),  len(rs_losse))
                kluan = self.gen_winner_array_str(rs,team)
                setattr(r, 'team%s_nomal_winlost_txt'%no_team, kluan)
                
           
   
   
   
    
   
    
    
    
    
    
    
    
    
    
    
    @api.onchange('current_time')
    def _oc_current_time(self):
        current_time = self.current_time
        current_time = current_time + 15 if current_time > 47 else current_time
        self.time = datetime.now() -  timedelta(minutes=current_time)
        
        
    @api.onchange('is_copy_begin_to_curent')
    def _oc_is_copy_begin_to_curent(self):
        if self.is_copy_begin_to_curent:
            for handicap_or_ou in ['handicap','ou']:
                for field in ['_money1','_money2','']:
                    field_name_get = 'begin_' + handicap_or_ou + field
                    field_name_set = 'curent_' + handicap_or_ou + field
                    setattr(self, field_name_set, getattr(self, field_name_get))
            
    
    @api.onchange('event_ids')
    def _oc_event_ids(self):
        if self.event_ids:
            self.score1=self.event_ids[-1].score1
            self.score2=self.event_ids[-1].score2