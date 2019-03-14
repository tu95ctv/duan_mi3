# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import  timedelta
from odoo.addons.tsbd.models.tool import  request_html, get_or_create_object_sosanh
from bs4 import BeautifulSoup
from odoo.exceptions import UserError
import re
import datetime
from odoo.addons.tsbd.models.leech_tool import  get_update_dict, get_soup, get_fix_id,GethtmlError, get_events
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
    
    all_match_link_select= fields.Selection([('http://bongdaso.com/_PlayedMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1','http://bongdaso.com/_PlayedMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1'),
                                                                ('http://bongdaso.com/Everton-Leicester_City-2019_01_01-_Fix_55956.aspx.aspx?LeagueID=1&SeasonID=106&Data=stat','http://bongdaso.com/Everton-Leicester_City-2019_01_01-_Fix_55956.aspx.aspx?LeagueID=1&SeasonID=106&Data=stat mode 2'),
                                                                ('http://bongdaso.com/_ComingMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1&Odd=1','http://bongdaso.com/_ComingMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1&Odd=1'),
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
        for count, ss in enumerate(range (0,7)):
            print ('season', count)
            aml = re.sub('Period=\d+','Period=%s'%ss,link)
            self.leech_all_match_function(aml, IS_GET_STATISTICS_MATCH  =  False)
    @api.multi
    def bxh(self):
        pass
    def leech_all_match(self):
        m_ids = self.with_context({'leech_all_match_function':True}).leech_all_match_function( self.all_match_link, self.count, IS_GET_STATISTICS_MATCH = self.is_get_statistics_match )
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
                self.leech_all_match_function(l, IS_GET_STATISTICS_MATCH  =  False)

                    
     
 
    
    def leech_a_match(self):
        match_id = self.leeching_a_match_function(self.link, is_get_events = self.is_get_events)
        self.match_ids = [(4,match_id)]
        
    def leeching_a_match_function(self,match_link, IS_GET_STATISTICS_MATCH  = False, add_update_dict = {}, is_get_events = False):
        print ('get_team_and_date>>>>')
        team_and_begintime,match_date, str_time, home, away, match_soup  = get_team_and_date(self,match_link, add_update_dict)
        search_dict =team_and_begintime
        print ('get_update_dict>>>>')
        update_dict, score_odd_lst_strows = get_update_dict (self,match_link,match_date,
                                                              IS_GET_STATISTICS_MATCH =  IS_GET_STATISTICS_MATCH, add_update_dict=add_update_dict,str_time = str_time, match_soup=match_soup )
        match_id = get_or_create_object_sosanh(self,'tsbd.match', search_dict, update_dict)
        
        if is_get_events:
            print ('get_events>>>>')
            fix_id = get_fix_id(match_link)
            event_link = 'http://bongdaso.com/_CastingInfo.aspx?FixtureID=%s&SeasonID=112&Flags=&Home={}&Away={}'.format(home,away)%fix_id
            events = get_events(fix_id, match_id, home, away)
#             except GethtmlError:
#                 self.env['tsbd.errorlog'].create({'link': event_link})
#                 raise GethtmlError('loi khi get html***%s'%event_link)
            match_id.write({'event_ids': [(6,0,events)]})
            
            
        bet_ScoreLines = update_score_odds(self, score_odd_lst_strows, match_id.id)
        return match_id.id
    
   
    def leech_all_match_function(self, all_match_link, break_count=0,IS_GET_STATISTICS_MATCH = False):
        soup = get_soup(all_match_link)
        if '_PlayedMatches' in all_match_link:
            #http://bongdaso.com/_PlayedMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1
            mode = '_PlayedMatches'  #1
        elif 'Data=stat' in all_match_link:
            #http://bongdaso.com/Everton-Leicester_City-2019_01_01-_Fix_55956.aspx.aspx?LeagueID=1&SeasonID=106&Data=stat
            mode = 'stat' #2
        elif '_ComingMatches' in all_match_link:
        #http://bongdaso.com/_ComingMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1&Odd=1
            mode = '_ComingMatches' #4
        elif 'AsianCupSchedule' in all_match_link:
            mode = 'AsianCupSchedule'
        else:
            #http://bongdaso.com/LeagueSchedule.aspx?LeagueID=1&SeasonID=106&CountryRegionID=-1&Period=5
            mode = 'SeasonID' #3
            
        match_link_list = get_list_of_match_dict(self,soup,mode)
        if self.is_not_get_chua_bat_dau:
            match_link_list = list(filter(lambda i: i.get('state') != u'Chưa bắt đầu', match_link_list))
        if self.range_2:
            range_1 = self.range_1 -1
            range_2 = self.range_2
            
            len_match_link_list = len(match_link_list)
            
            if range_1 > len_match_link_list - 1:
                raise UserError('range_1 > len_match_link_list - 1')
            if range_2 > len_match_link_list :
                range_2 = len_match_link_list
            match_link_list = match_link_list[range_1:range_2]
            
            
        
#         raise UserError(u'%s'%match_link_list)
            
            
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
                                                           add_update_dict=add_update_dict, 
                                                           is_get_events = self.is_get_events
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
        self.log = u'số lượng trận đấu trong trang %s \n Số trận thành công: %s'%(len_match_ids, succeed_count)
        return m_ids
   
    
    
    
    
   
#         self.match_ids = [(5,0)]
    def test(self):
        away =u'Việt Nam'
        away = quote(away)
        link ='http://bongdaso.com/_CastingInfo.aspx?FixtureID=56032&SeasonID=112&Flags=&Home=Bournemouth&Away=%s'%away
        
        print ('link', link)
        raise UserError(u'%s'%(request_html(link)))
        
        
