# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import  timedelta, datetime
from odoo.addons.tsbd.models.tool import  request_html, get_or_create_object_sosanh
from bs4 import BeautifulSoup
from odoo.exceptions import UserError
import re

from odoo.addons.tsbd.models.leech_tool import  get_update_dict, get_soup, get_fix_id,GethtmlError, get_events, get_soup_of_events
from odoo.addons.tsbd.models.leech_tool import  get_team_and_date, update_score_odds, get_list_of_match_dict, get_soup_ajax_link
from urllib.parse import quote

    
class Leech(models.Model):
    _name = 'tsbd.leech'
    log = fields.Text()
    log1 = fields.Text()
    parse_log = fields.Text()
    link = fields.Char()
    all_match_link = fields.Char()
    match_ids = fields.Many2many('tsbd.match')
    count = fields.Integer()
    is_get_statistics_match = fields.Boolean()
    is_get_events = fields.Boolean()
    is_not_get_chua_bat_dau= fields.Boolean()
    
    range_1 = fields.Integer(default =1)
    range_2 = fields.Integer(default = 0)
    
    all_match_link_select= fields.Selection([
                                                                ('http://bongdaso.com/_PlayedMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1',u'Đã đá'),
                                                                ('http://bongdaso.com/_LiveMatches.aspx?LeagueID=-1&SeasonID=-1&AjaxCheck=1',u'Đang đá'),
                                                                ('http://bongdaso.com/Everton-Leicester_City-2019_01_01-_Fix_55956.aspx.aspx?LeagueID=1&SeasonID=106&Data=stat','http://bongdaso.com/Everton-Leicester_City-2019_01_01-_Fix_55956.aspx.aspx?LeagueID=1&SeasonID=106&Data=stat mode 2'),
                                                                ('http://bongdaso.com/_ComingMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1&Odd=1',u'Sắp đá'),
                                                                ('http://bongdaso.com/LeagueSchedule.aspx?LeagueID=1&SeasonID=106&CountryRegionID=-1&Period=6',u'Ngoại hạng anh tháng 2'),
                                                                ('http://bongdaso.com/LeagueSchedule.aspx?LeagueID=3&SeasonID=111&CountryRegionID=-1&Period=5',u'Seria tháng 1'),
                                                                ('http://bongdaso.com/LeagueSchedule.aspx?LeagueID=4&SeasonID=110&CountryRegionID=-1&Period=5',u'Laliga tháng 1'),
                                                                ('http://bongdaso.com/LeagueSchedule.aspx?LeagueID=5&SeasonID=109&CountryRegionID=-1&Period=5',u'Đức tháng 1'),
                                                                ('http://bongdaso.com/LeagueSchedule.aspx?LeagueID=6&SeasonID=108&CountryRegionID=-1&Period=5',u'Pháp tháng 1'),
                                                                ('http://bongdaso.com/LeagueSchedule.aspx?LeagueID=2&SeasonID=104&Period=4',u'C1 vòng bảng 17'),
                                                                ('http://bongdaso.com/LeagueSchedule.aspx?LeagueID=2&SeasonID=112&Period=5',u'C1 vòng bảng 18'),
                                                                ('http://bongdaso.com/AsianCupSchedule.aspx',u'Asian cup'),
                                             
                                             ])
    cate_id = fields.Many2one('tsbd.cate')
    bxh_ids = fields.Many2many('tsbd.bxh','leech_bxh_rel','leech_id', 'bxh_id')
    @api.multi
    def trig(self):
        matchs= self.env['tsbd.match'].search([])
        matchs.write({'trig':True})
    def trig_team(self):
        matchs= self.env['tsbd.team'].search([])
        matchs.write({'trig':True})
        
    def trig_predict(self):
        matchs= self.env['tsbd.predict'].search([])
        matchs.write({'trig':True})
        
        
    def xoa_bxh_not_cate(self):
        bxh = self.env['tsbd.bxh'].search([('cate_id','=',False)]).unlink()
#         matchs.write({'trig':True})
        
    @api.onchange('all_match_link_select')
    def all_match_link_select_oc_(self):
        self.all_match_link = self.all_match_link_select
    @api.multi
    def clean_match(self):
        self.match_ids = [(5,False,False)]

            
    @api.multi
    def leech_all_season(self):
        link = self.all_match_link
        for count, ss in enumerate(range (0,8)):
            print ('season', count)
            aml = re.sub('Period=\d+','Period=%s'%ss,link)
            self.leech_all_match_function(aml, IS_GET_STATISTICS_MATCH  =  False)
    @api.multi
    def bxh(self):
        pass
    def leech_all_match(self):
        rts = self.leech_all_match_function( self.all_match_link, self.count,
                                                IS_GET_STATISTICS_MATCH = self.is_get_statistics_match,
                                                is_not_get_chua_bat_dau= self.is_not_get_chua_bat_dau, range_1 = self.range_1, range_2 = self.range_2,
                                                is_get_events = self.is_get_events, 
                                                 )
        
        m_ids = rts[0]
        for m_id in m_ids:
            self.write( {'match_ids': [(4,m_id)]})
    
    @api.multi
    def leech_all_season_auto_get_period(self):
        link = self.all_match_link
        self.leech_all_season_auto_get_period_f(link)
        
    @api.multi
    def leech_all_season_auto_get_period_f(self,link):
        soup = get_soup(link)
        period = soup.select('div.periods_table td')
        links = []
        for p in period:
            a = p.select('a')
            txt=p.get_text()
            if txt and (u'Vòng loại' not in txt and u'Vòng sơ loại' not in txt ):
                if a:
                    links.append(('http://bongdaso.com/'  + a[0]['href'],txt))
                else:
                    links.append((link,txt))
        for l,t in links:
                self.leech_all_match_function(l, IS_GET_STATISTICS_MATCH  =  False, is_get_events = True)

    def leech_a_match(self):
        match_id = self.leeching_a_match_function(self.link, is_get_events = self.is_get_events)
        self.match_ids = [(4,match_id)]
        
        
        
#     def gen_lineup(self, html):
#         thong_ke_dict = {}
#         for patern in [("'_HomeLineup_','(.*?)'", '1'),("'_AwayLineup_','(.*?)'",'2')]:
#             rs=re.search("'_HomeLineup_','(.*?)'",html)
#             rs =  'http://bongdaso.com/' + rs.group(1)
#             
#             
#             rs=re.search(patern[0],html)
#             rs =  'http://bongdaso.com/' + rs.group(1)
#             rs = request_html(rs)
#             soup = BeautifulSoup(rs, 'html.parser')
#             rs = soup.select('div.squad_table table tr')
#             da_chinhs =[]
#             da_phus =[]
#             alist = da_chinhs
#             for count, tr in enumerate(rs):
#                 if count != 0:
#                     if tr.get('class') == ['fixture_separator']:
#                         alist =da_phus
#                         continue
#                     gt = tr.get_text()
#                     number = tr.select('td:nth-of-type(1)')[0].get_text()
#                     tr2 = tr.select('td:nth-of-type(2) div')[0]
#                     name = tr2.get_text()
#                     player_id = tr2['id']
#                     player_id = player_id.replace('player_','player_tip_')
#                     player_id_soup = soup.select('div#%s'%player_id)[0]
#                     trs = player_id_soup.select('div.boxBody > table > tr:nth-of-type(1) > td:nth-of-type(2) tr')#[0].get_text()
#     #                 raise UserError(ngay_sinh)
#     #                 ngay_sinh = player_id_soup.select('div.boxBody>table td:nth-of-type(2) table tr:nth-of-type(2) ')[0].get_text()
#                     adict_search  = {'number':int(number),'name': name}
#                     adict_update = {}
#                     for count, tr in enumerate(trs):
#                         if count ==1:
#                             td2 = tr.select('td:nth-of-type(2)')[0].get_text()
#                             print ('td2',td2)
#                             dt = datetime.strptime(td2,'%d/%m/%Y')
#                             adict_update['birthday']= fields.Date.to_string(dt)
#                     alist.append((adict_search,adict_update))
#             players = []   
#             
#             
#             
#             for adict_search,adict_update  in da_phus:
#                 player_id = get_or_create_object_sosanh(self,'tsbd.player',adict_search, adict_update).id
#                 players.append(player_id)
#                 
#             for da_chinh_or_du_bi  in [(da_chinhs,'da_chinh_players%s_ids'%patern[1]), (da_phus,'du_bi_players%s_ids'%patern[1])]:
#                 players = map(lambda i: get_or_create_object_sosanh(self,'tsbd.player',i[0], i[1]).id, da_chinh_or_du_bi[0])
#                 thong_ke_dict[da_chinh_or_du_bi[1]] = [(6,0,players)]
    
    
    def gen_lineup_new(self, match_link, search_dict, match_id):
        match_link =  match_link.replace('Data=Odds', 'Data=lineup').replace('Data=Casting','Data=lineup' )
        if 'Data=lineup' not in match_link:
            match_link = match_link + '&Data=lineup'
        html = request_html(match_link)
        lineup_dict = {}
        playerlines = []
        
        
        for patern in [("'_HomeLineup_','(.*?)'", search_dict['team1'], 'home'),("'_AwayLineup_','(.*?)'",search_dict['team2'], 'away')]:
            rs=re.search(patern[0], html)
            rs =  'http://bongdaso.com/' + rs.group(1)
            rs = request_html(rs)
            soup = BeautifulSoup(rs, 'html.parser')
            rs = soup.select('div.squad_table table tr')
            da_chinhs =[]
            da_phus =[]
            alist = da_chinhs
            for count, tr in enumerate(rs):
                if count != 0:
                    if tr.get('class') == ['fixture_separator']:
                        alist =da_phus
                        continue
                    gt = tr.get_text()
                    number = tr.select('td:nth-of-type(1)')[0].get_text()
                    try:
                        number = int(number)
                    except:
                        number = False
                    print ('tr**', tr)
#                     player_name_tr = tr.select('td:nth-of-type(2) div')[0]
                    player_name_tr = tr.select('td:nth-of-type(2)')[0]
                    name = player_name_tr.get_text()
                    
                    if number:
                        adict_search  = {'number':int(number),'name': name}
                    else:
                        adict_search  = {'name': name}
                    adict_update = {}
                    
                    
                    player_id = player_name_tr.get('id')
                    if player_id:
                        player_id = player_id.replace('player_','player_tip_')
                        player_id_soup = soup.select('div#%s'%player_id)[0]
                        image_soup = player_id_soup.select('div.boxBody > table > tr:nth-of-type(1) > td:nth-of-type(1) img')#[0].get_text()
                        if image_soup:
                            image_soup = image_soup[0]
                            image_link = image_soup['src']
                            image_link = image_link.replace('&amp;','&')
                            image_link = 'http://bongdaso.com/' + image_link
                        else:
                            image_link = False
                        trs = player_id_soup.select('div.boxBody > table > tr:nth-of-type(1) > td:nth-of-type(2) tr')#[0].get_text()
                       
                        if image_link:
                            adict_update['image_link'] = image_link
                        for count, tr in enumerate(trs):
                            if count == 0:
                                continue
                            if count ==1:
                                td2 = tr.select('td:nth-of-type(2)')[0].get_text()
                                dt = datetime.strptime(td2,'%d/%m/%Y')
                                adict_update['birthday']= fields.Date.to_string(dt)
                    alist.append((adict_search,adict_update))
            for da_chinh_or_du_bi  in [(da_chinhs, 'da_chinh'), (da_phus,'du_bi')]:
                players = map(lambda i: get_or_create_object_sosanh(self,'tsbd.player',i[0], i[1]).id, da_chinh_or_du_bi[0])
                a_playerlines = map(lambda i: get_or_create_object_sosanh(self,'tsbd.playerline',{'player_id':i, 'team_id':patern[1],
                                                                                                 'home_or_away': patern[2],'da_chinh_hay_du_bi':da_chinh_or_du_bi[1],'match_id': match_id
                                                                                                }).id, players)
                playerlines += list(a_playerlines)
        lineup_dict['playerline_ids'] = [(6,0,playerlines)]
        return lineup_dict
    
    def get_tk(self, fix_id, home, away):
        event_soup = get_soup_of_events(fix_id, home, away )
        possesion = event_soup.select('div.fixture_stats table tr')
        rs = []
        for count, tr in enumerate(possesion):
            if count in (0,2,3):
                try:
                    tieu_chi_tk1= int(float(tr.select('td:nth-of-type(1)')[0].get_text().replace('%','')))
                    tieu_chi_tk2 = int(float(tr.select('td:nth-of-type(3)')[0].get_text().replace('%','')))
                    rs.append((tieu_chi_tk1 ,tieu_chi_tk2 ))
                except:
                    return {}
        thong_ke_dict = {'possession1':rs[0][0], 'possession2':rs[0][1],
                                    'shots_on_target1':rs[1][0], 'shots_on_target2':rs[1][1],
                                    'shots_off_target1':rs[2][0], 'shots_off_target2':rs[2][1],
                                    }
        return thong_ke_dict
                
    def leeching_a_match_function(self,match_link, IS_GET_STATISTICS_MATCH  = False, add_update_dict = {}, is_get_events = False):
        fix_id = get_fix_id(match_link)
        team_and_begintime,match_date, str_time, home, away, match_soup, html  = get_team_and_date(self, match_link, add_update_dict)
        search_dict =team_and_begintime


       
        
        thong_ke_dict = self.get_tk(fix_id, home, away)
        update_dict, score_odd_lst_strows = get_update_dict (self, match_link,match_date,
                                                               IS_GET_STATISTICS_MATCH =  IS_GET_STATISTICS_MATCH,
                                                               add_update_dict= add_update_dict,
                                                               str_time = str_time,
                                                               match_soup=match_soup,
                                                               thong_ke_dict=thong_ke_dict
                                                                )
        
        
        match_id = get_or_create_object_sosanh(self,'tsbd.match', search_dict, update_dict)
        
        
        
        lineup_dict = self.gen_lineup_new(match_link, search_dict, match_id.id)
        
        
        match_id.write(lineup_dict)
        if is_get_events:
            events = get_events(fix_id, match_id, home, away)
            match_id.write({'event_ids': [(6,0,events)]})
            
            
        bet_ScoreLines = update_score_odds(self, score_odd_lst_strows, match_id.id)
        return match_id.id
    
   
    def leech_all_match_function(self, all_match_link, break_count=0, IS_GET_STATISTICS_MATCH = False,
                                  is_not_get_chua_bat_dau= None,range_1 =1, range_2 = 0, is_get_events = False):
        
        
        match_link_list = get_list_of_match_dict(all_match_link)
        
        
        if is_not_get_chua_bat_dau:
            match_link_list = list(filter(lambda i: i.get('state') != u'Chưa bắt đầu', match_link_list))
        if range_2:
            range_1 = range_1 -1
            range_2 = range_2
            len_match_link_list = len(match_link_list)
            if range_1 > len_match_link_list - 1:
                raise UserError('range_1 > len_match_link_list - 1')
            if range_2 > len_match_link_list :
                range_2 = len_match_link_list
            match_link_list = match_link_list[range_1:range_2]
        count = 0 
        succeed_count = 0
        len_match_ids = len(match_link_list)
        m_ids = []
        for c, adict in enumerate(match_link_list):
            print (u'%s/%s>>>>>>>>'%(c+1, len_match_ids))
            add_update_dict = adict#{'cate': adict['cate']}
            match_link = adict['match_link']
            try:
                match_id = self.leeching_a_match_function(match_link,
                                                           IS_GET_STATISTICS_MATCH= IS_GET_STATISTICS_MATCH,
                                                           add_update_dict = add_update_dict, 
                                                           is_get_events = is_get_events
                                                           )
                m_ids.append(match_id)
                print ('%s/%s,%s'%(count, len_match_ids, add_update_dict))
                succeed_count +=1
            except GethtmlError as e:
                self.env['tsbd.errorlog'].create({'link': str(e)})
                print ('leech a math link but Error html get url:%s'%e)
                pass
            count+=1
            if break_count and break_count == count:
                break
#         self.log = u'số lượng trận đấu trong trang %s \n Số trận thành công: %s'%(len_match_ids, succeed_count)
        return m_ids,len_match_ids, succeed_count
   
    
    
    
    
   
#         self.match_ids = [(5,0)]
    def test(self):
        away =u'Việt Nam'
        away = quote(away)
        link ='http://bongdaso.com/_CastingInfo.aspx?FixtureID=56032&SeasonID=112&Flags=&Home=Bournemouth&Away=%s'%away
        
        print ('link', link)
        raise UserError(u'%s'%(request_html(link)))
        
        
