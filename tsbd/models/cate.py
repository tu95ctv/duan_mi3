# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.addons.tsbd.models.tool import  request_html
# from odoo.addons.tsbd.models.leech import  detail_match
from odoo.addons.tsbd.models.tool import   get_or_create_object_sosanh

from bs4 import BeautifulSoup

class Period(models.Model):  
    _name = 'tsbd.period' 
    name = fields.Char()
#     cate_id = fields.Many2one('tsbd.cate')
class Cate(models.Model):  
    _name = 'tsbd.cate' 
    name = fields.Char()
    cate_id = fields.Many2one('tsbd.cate')
    match_ids = fields.One2many('tsbd.match', 'cate_id')
    bang_match_ids = fields.One2many('tsbd.match', 'bang_id')
    cate_ids = fields.One2many('tsbd.bxh','cate_id')
    no_match =  fields.Integer(compute='no_match_', store=True)
    large_cate =  fields.Boolean()
    team_ids = fields.Many2many('tsbd.team','cate_team_rel','cate_id', 'team_id')
    
#     bet_bxh_ids = fields.One2many('tsbd.betbxh','cate_id')
    match_number = fields.Integer()
    avg_score1 = fields.Float()
    avg_score2 = fields.Float()
    avg_score = fields.Float()
    
    ou_bxh_ids = fields.Many2many('tsbd.bxh','cate_oubxh_relate','cate_id','bxh_id', compute='ou_bxh_ids_')
    
    @api.depends('name')
    def ou_bxh_ids_(self):
        for r in self:
            bxh_ids = self.env['tsbd.bxh'].search([('cate_id', '=', r.id)])
            r.ou_bxh_ids= [(6,0,bxh_ids.ids)]
            
    @api.multi
    def gen_round(self):     
        for team in self.team_ids:
            team_id =team.id
            match_ids = self.env['tsbd.match'].search([('cate_id','=',self.id),'|', ('team1','=',team_id),('team2','=',team_id)],order='date asc')
            for count, match in enumerate(match_ids):
                match.round = count +1
        self.log = u'match_ids len per team:%s '%len(match_ids)
        
    @api.multi
    def find_late_soon_match(self):
        sql_query =  "select time,count(id), time::timestamp::date as date  from tsbd_match where cate_id = %s and round = %s group by time"%(self.id,1)
        self.env.cr.execute(sql_query)
        rs = self.env.cr.dictfetchall()
        adict = {}
        date_adict = {}
        
        for i in rs:
            gio_dict = {}
            gio = i['time']
            dt_gio = fields.Datetime.from_string(gio)
            count = i['count']
            gio_dict['count'] = count
            date = i['date']
            date_dict = date_adict.setdefault(date,{})
            
            min_time = date_dict.setdefault('min_time',dt_gio)
            str_min_time = date_dict.setdefault('str_min_time',gio)
            
            max_time = date_dict.setdefault('max_time',dt_gio)
            str_max_time = date_dict.setdefault('str_max_time',gio)
            
            
            
            if dt_gio < min_time:
                date_dict['min_time'] = dt_gio
                date_dict['str_min_time'] = str_min_time
                
            if dt_gio > max_time:
                date_dict['max_time'] = dt_gio
                date_dict['str_max_time'] = str_max_time
                
                
            gio_dict['date'] = date
            adict[gio]= gio_dict
        
        for k,v in adict.items():
            if k == date_adict[v['date']]['str_min_time'] and v['count']==1:
                is_min_time = True
#                 v['is_min_time'] =True
            else:
                is_min_time = False
                
            if k == date_adict[v['date']]['str_max_time'] and v['count']==1:
                is_max_time = True
#                 v['is_min_time'] =True
            else:
                is_max_time = False
            if is_max_time and is_min_time:
                pass
            
                
                
                
#                 v['is_min_time'] =False
                
        
        
        
        matchs = self.env['tsbd.match'].search([('cate_id','=',self.id),('round','=', 1)])
        for match in matchs:
            if adict[match.time]['is_min_time'] == True:
                is_min_time =True
#                 raise UserError('akakaka')
            else:
                is_min_time =False
           
            match.is_min_time = is_min_time
#         rs = self.env['tsbd.match'].read_group([('cate_id','=',self.id),('round','=',1)],['time'],['time:date'])
#         raise UserError(u'%s ==%s'%(adict,date_adict))
        
        
                
                
            
    @api.multi
    def gen_team(self):
        if u'ảng' not in self.name:
            cate_id = 'cate_id'
        else:
            cate_id = 'bang_id'
        domain = [(cate_id,'=', self.id)]
        match_ids = self.env['tsbd.match'].search(domain)
        home_teams = match_ids.mapped('team1.id')
        away_teams = match_ids.mapped('team2.id')
        cate_teams = home_teams + away_teams
        cate_teams = set(cate_teams)
        self.team_ids = [(6,0,cate_teams)]
#     no_match =  fields.Integer()
    @api.multi
    def avg_button(self):
#         self.env['tsbd.match'].search([('cate_id','=')])
        rs = self.env['tsbd.match'].read_group([('cate_id','=', self.id)],['score1', 'score2'],[])
        rs = rs[0]
        self.match_number = rs['__count']
        self.avg_score1 =rs['score1']/rs['__count']
        self.avg_score2 =rs['score2']/rs['__count']
        self.avg_score = self.avg_score1 + self.avg_score2

#         raise UserError(u'%s'%rs)
    @api.multi
    def name_get(self):

        result = []
        for r in self:
            name = u'%s%s'%(r.name, u'(%s Team)'%r.no_match if r.no_match else '')
            result.append((r.id,name))
        return result
        
        
    @api.depends('cate_ids', 'large_cate')
    def no_match_(self):
        for r in self:
            r.no_match = len(r.cate_ids)
    @api.multi
    def clear_bxh(self):
        self.cate_ids = [(6,0,[])]
#         self.bet_bxh_ids = [(6,0,[])]
    @api.multi
    def trig(self):
        matchs= self.env['tsbd.match'].search([])
        matchs.write({'trig':True})

    
#     
    def gen_bxh_dict(self, cate_teams, domain, for_bet=False):
        rt_goal = {}
        if 1:
            ad_map = {'team1':{'name':'home', 'score_tg':'score1', 'score_th':'score2'},'team2':{'name':'away', 'score_tg':'score2', 'score_th':'score1'}}
            for team1_or_2,ad in ad_map.items() :
                read_group_rs = self.env['tsbd.match'].read_group(domain,[team1_or_2,'score1', 'score2'],[team1_or_2], lazy=False)
                for ateam in read_group_rs:
                    team_id = ateam[team1_or_2][0]
                    ateams = rt_goal.setdefault(team_id, {})
                    ateams['%s_match_number'%ad['name']] = ateam['__count']
                    ateams['%s_tg'%ad['name']] = ateam[ad['score_tg']]
                    ateams['%s_th'%ad['name']] = ateam[ad['score_th']]
                    rt_goal[team_id] = ateams   
        rt_ou = {}  
        ad = {'team1':'home','team2':'away'}
        for team1_or_2,home_or_away in ad.items() :
            read_group_rs = self.env['tsbd.match'].read_group(domain, [team1_or_2,'over_or_under'],[team1_or_2, 'over_or_under'], lazy=False)
            for ateam in read_group_rs:
                team_id = ateam[team1_or_2][0]
                ateams = rt_ou.setdefault(team_id, {})
                if ateam['over_or_under'] == 'over':
                    ateams['%s_over'%home_or_away] = ateam['__count']
                elif  ateam['over_or_under'] == 'under':
                    ateams['%s_under'%home_or_away] = ateam['__count']
                else:
                    ateams['%s_ou_draw'%home_or_away] = ateam['__count']
        rt_winlost = {}        
        
        
#         if not for_bet :
        ad_map = {'team1':{'name':'home', 't': 'doi_nha', 'b': 'doi_khach', 'h': 'hoa' },'team2':{'name':'away', 't': 'doi_khach', 'b': 'doi_nha', 'h': 'hoa' }}
        for team1_or_2,ad in ad_map.items() :
            read_group_rs = self.env['tsbd.match'].read_group(domain, [team1_or_2, 'winner','score1', 'score2'],[team1_or_2, 'winner'], lazy=False)
            for ateam in read_group_rs:
                team_id = ateam[team1_or_2][0]
                ateams = rt_winlost.setdefault(team_id, {})
                if ateam['winner'] == ad['t']:
                    ateams['%s_t'%ad['name']] = ateam['__count']
                elif ateam['winner'] == ad['b']:
                    ateams['%s_b'%ad['name']] = ateam['__count']
                else:
                    ateams['%s_h'%ad['name']] = ateam['__count']
#         else:
        ad_map = {'team1':{'name':'home', 't': 'team1', 'b': 'team2', 'h': 'hoa','handicap_wl1or2':'handicap_wl1', 'handicap_wl_amount1or2':'handicap_wl_amount1'  },
                  'team2':{'name':'away', 't': 'team2', 'b': 'team1', 'h': 'hoa', 'handicap_wl1or2':'handicap_wl2','handicap_wl_amount1or2':'handicap_wl_amount2' }}
        for team1_or_2,ad in ad_map.items() :
            read_group_rs = self.env['tsbd.match'].read_group(domain, [team1_or_2, 'handicap_bet_winner','score1', 'score2', ad['handicap_wl1or2'], ad['handicap_wl_amount1or2']],[team1_or_2, 'handicap_bet_winner',], lazy=False)
            handicap_wl1or2 = ad['handicap_wl1or2']
            handicap_wl_amount1or2 = ad['handicap_wl_amount1or2']
            for ateam in read_group_rs:
                team_id = ateam[team1_or_2][0]
                ateams = rt_winlost.setdefault(team_id, {})
                if ateam['handicap_bet_winner'] == ad['t']:
                    ateams['bet_%s_t'%ad['name']] = ateam[handicap_wl1or2]
                    ateams['bet_%s_t_no'%ad['name']] = ateam['__count']
                    ateams['bet_%s_win_amount'%ad['name']] = ateam[handicap_wl_amount1or2]
                elif ateam['handicap_bet_winner'] == ad['b']:
                    ateams['bet_%s_b'%ad['name']] = ateam[handicap_wl1or2]
                    ateams['bet_%s_b_no'%ad['name']] = ateam['__count']
                    ateams['bet_%s_lose_amount'%ad['name']] = ateam[handicap_wl_amount1or2]
                else:
                    ateams['bet_%s_h'%ad['name']] = ateam['__count']
        bxh_dict = {}
        for team in cate_teams:
            adict = {}
            ateam_rt_ou = rt_ou.get(team,{})
            ateam_rt_goal = rt_goal.get(team,{})
            ateam_rt_winlost = rt_winlost.get(team,{})
            
            adict.update(ateam_rt_ou)
            adict.update(ateam_rt_goal)
            adict.update(ateam_rt_winlost)
            
#             if not for_bet:
            home_t = ateam_rt_winlost.get('home_t' ,0)
            away_t = ateam_rt_winlost.get('away_t' ,0)
            home_h = ateam_rt_winlost.get('home_h' ,0)
            away_h = ateam_rt_winlost.get('away_h' ,0) 
            diem = (home_t +  away_t ) *3 + ( home_h + away_h)
            money = False

#             else:
#                
                
            bet_home_t = ateam_rt_winlost.get('bet_home_t' ,0)
            bet_away_t = ateam_rt_winlost.get('bet_away_t' ,0) 
            
            bet_home_b = ateam_rt_winlost.get('bet_home_b' ,0)
            bet_away_b = ateam_rt_winlost.get('bet_away_b' ,0) 
            
            
            bet_diem = (bet_home_t + bet_away_t )  +   bet_home_b + bet_away_b
           
            
            
            bet_home_t_no = ateam_rt_winlost.get('bet_home_t_no' ,0)
            bet_away_t_no = ateam_rt_winlost.get('bet_away_t_no' ,0) 
            bet_home_b_no = ateam_rt_winlost.get('bet_home_b_no' ,0)
            bet_away_b_no = ateam_rt_winlost.get('bet_away_b_no' ,0) 
            
            bet_diem_no = (bet_home_t_no + bet_away_t_no ) 
            
            
            
            home_win_amount =  ateam_rt_winlost.get('bet_home_win_amount',0)
            away_win_amount  = ateam_rt_winlost.get('bet_away_win_amount',0)
            home_lose_amount =  ateam_rt_winlost.get('bet_home_lose_amount',0)
            away_lose_amount  = ateam_rt_winlost.get('bet_away_lose_amount',0)
            bet_money = home_win_amount + away_win_amount + home_lose_amount + away_lose_amount
            
            adict.update({'bet_money':bet_money, 'bet_diem_no': bet_diem_no, 'bet_diem':bet_diem})
                
                
                
            
            score_sum = ateam_rt_goal.get('home_tg',0) + ateam_rt_goal.get('away_tg',0)
            lost_score_sum = ateam_rt_goal.get('home_th',0) + ateam_rt_goal.get('away_th',0)
            hsbt = score_sum - lost_score_sum
            update_dict = {
                              'score_sum':score_sum,
                              'lost_score_sum':lost_score_sum,
                              'diem':diem,
                              'hsbt':hsbt,
                               }
            adict.update(update_dict)
            bxh_dict[team] =adict
        return bxh_dict
    
    

    @api.multi
    def bxh(self):
        for_bet = self._context.get('for_bet')
        if for_bet:
            cate_id = 'bet_cate_id'
            model = 'tsbd.betbxh'
        else:
            model ='tsbd.bxh'
            
        
        if u'ảng' not in self.name:
            cate_id = 'cate_id'
        else:
            cate_id = 'bang_id'
            
        domain = [(cate_id,'=', self.id),('state','!=', u'Chưa bắt đầu')]
        match_ids = self.env['tsbd.match'].search(domain)
        home_teams = match_ids.mapped('team1.id')
        away_teams = match_ids.mapped('team2.id')
        cate_teams = home_teams + away_teams
        cate_teams = set(cate_teams)
#         len_cate_teams = len(cate_teams)
#         raise UserError(len_cate_teams)
        
        bxh_dict = self.gen_bxh_dict(cate_teams, domain,for_bet=for_bet)
        for team,ateam_bxh_dict in bxh_dict.items():
#             new_ateam = {}
#             new_ateam['home_t'] =ateam_bxh_dict['home_t']
#             new_ateam['away_t'] = ateam_bxh_dict['away_t']
#             new_ateam['home_b'] =ateam_bxh_dict['home_b']
#             new_ateam['away_b'] = ateam_bxh_dict['away_b']
#             
#             new_ateam['home_h'] = ateam_bxh_dict['home_h']
#             new_ateam['away_h'] = ateam_bxh_dict['away_h']
#             new_ateam['home_tg'] = ateam_bxh_dict['home_tg']
#             new_ateam['home_th'] =  ateam_bxh_dict['home_th']
#             new_ateam['diem'] = ateam_bxh_dict['diem']
#             new_ateam['away_tg'] = ateam_bxh_dict['away_tg']
#             new_ateam['away_th'] = ateam_bxh_dict['away_th']
#             new_ateam['home_match_number'] = ateam_bxh_dict['home_match_number']
#             new_ateam['away_match_number'] = ateam_bxh_dict['away_match_number']
#             
            
            ateam_bxh_dict['cate_id'] = self.id
            
            get_or_create_object_sosanh(self,model, {'team_id':team, 'cate_id':self.id
                                                          }, ateam_bxh_dict, is_must_update = True)
        
        
#         if not for_bet:
        rg_rs = self.env['tsbd.bxh'].read_group([('cate_id','=', self.id)],['team_id','diem'],['diem'],lazy=False)
        rg_rs =  list(filter(lambda i: i['__count']>1,rg_rs))
        for ateam_rg in rg_rs:
            diem = ateam_rg['diem']
            team_ids = self.env['tsbd.bxh'].search([('diem','=', diem),('cate_id','=',self.id)]).mapped('team_id.id')
            domain = [(cate_id,'=', self.id),('state','!=', u'Chưa bắt đầu'),('team1','in',team_ids),('team2','in',team_ids)]
            doi_dau_bxh_dict = self.gen_bxh_dict(team_ids, domain)
            for team, ex_team_bxh_dict in doi_dau_bxh_dict.items():
                ex_search_dict = {'team_id':team, 'cate_id':self.id}
                ex_update_dict = {'diem_dd':ex_team_bxh_dict['diem']}
                get_or_create_object_sosanh(self,'tsbd.bxh', ex_search_dict,  ex_update_dict, is_must_update = True)
       
        bxh_ids = self.env['tsbd.bxh'].search([('cate_id','=',self.id)],order='diem desc, hsbt desc, score_sum desc')
#         else:
        
        
        
        for stt,r in enumerate(bxh_ids) :
            r.stt = stt +1
        for stt,r in enumerate(bxh_ids.sorted(key=lambda r: r.bet_over, reverse=True)):
            r.stt_bet_over = stt + 1
        
        bxh_ids = self.env['tsbd.bxh'].search([('cate_id','=',self.id)],order='bet_diem desc')
        for stt,r in enumerate(bxh_ids) :
            r.bet_stt = stt +1
            
        
        
