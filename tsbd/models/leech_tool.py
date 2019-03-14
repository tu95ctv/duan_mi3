# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import  timedelta
import datetime
# from odoo.addons.tsbd.models.tool import  request_html
from bs4 import BeautifulSoup
import re
from odoo.addons.tsbd.models.tool import get_or_create_object_sosanh, GethtmlError
from odoo.addons.tsbd.models.tool import  request_html# as rh
from odoo.http import request
from urllib.parse import quote


# 
# def try_decorator_for_request_html(func):
#     def awrapper(*args,**kargs):
# #         try:
#         rs = func(*args,**kargs)
#         request.env['tsbd.errorlog'].create({'link':args[0]})
#         return rs
# #         except GethtmlError:
#     return awrapper
# 
# @try_decorator_for_request_html    
# def request_html(link):
#     return rh(link)
    
    
class GetOddsException(Exception):
    pass
def thapphan(td):
#     print ('td*** in thappan',td)
    if '/' in td:
        if ' ' in td:
            al = td.split(' ')
            td = float(al[0]) + thapphan(al[1])
        else:
            al = td.split('/')
            td = float(al[0])/float(al[1])
    else:
        try:
            td = float(td)
        except:
            td = False
    return td
def thap_phan_co_2_cham(td):
    td = td.get_text()
    if ':' in td:
        al = td.split(':')
        td = thapphan(al[1]) - thapphan(al[0])
    else:
        td = thapphan(td)
    return td

# 04/02
def get_soup(link):
    html  = request_html(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup
def get_fix_id(match_link):
        if not match_link:
            return None
        rs = re.search(r'Fix_(\d*?)\.aspx', match_link)
        fix_id = rs.group(1)
        return fix_id
def get_soup_ajax_link(fix_id,template_link):
#     fix_id = get_fix_id(match_link)
    score_link = template_link%fix_id
    html  = request_html(score_link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_team_and_date(self, match_link, add_update_dict, is_set_must_get_time = True):
        soup = None
        if is_set_must_get_time:
            check_time_for_get_soup = 'time' not in add_update_dict
        else:
            check_time_for_get_soup = 'time' not in add_update_dict and 'date' not in add_update_dict
       
        is_get_soup =    any(['home' not in add_update_dict, 'away' not in add_update_dict, check_time_for_get_soup])
        
        if is_get_soup:
            soup = get_soup(match_link)
        
        if  'home' not in add_update_dict:
            home = soup.select('div#scr_home a')[0].get_text()
            home = re.sub('\s+\[\d+\]', '', home)
        else:
            home = add_update_dict['home']
        if 'away' not in add_update_dict:
            away = soup.select('div#scr_away a')[0].get_text()
            away = re.sub('\[\d+\]\s+', '', away)
        else:
            away = add_update_dict['away']
        home = home.strip()
        away = away.strip()
        if 'time' in add_update_dict:
            begin_time = add_update_dict['time']
            dtime = datetime.datetime.strptime(begin_time,'%d/%m/%Y %H:%M') - timedelta(hours=7)
            str_time = fields.Datetime.to_string(dtime)
            match_date = dtime.date()
            str_date = fields.Date.to_string(dtime)
        else:
            if is_set_must_get_time:
                begin_time = soup.select('div#scr_start')[0].get_text()
                begin_time = begin_time[9:]
                dtime = datetime.datetime.strptime(begin_time,'%d/%m/%Y %H:%M') - timedelta(hours=7)
                str_time = fields.Datetime.to_string(dtime)
                match_date = dtime.date()
                str_date = fields.Date.to_string(match_date)
            else:
                match_date = datetime.datetime.strptime(add_update_dict['date'],'%d/%m/%Y')
                str_date = fields.Date.to_string(match_date)
                str_time = None
            
       
                
        
#         if 'time' not in add_update_dict and  'date' not in add_update_dict:
#             begin_time = soup.select('div#scr_start')[0].get_text()
#             begin_time = begin_time[9:]
#             dtime = datetime.datetime.strptime(begin_time,'%d/%m/%Y %H:%M') - timedelta(hours=7)
#             str_time = fields.Datetime.to_string(dtime)
#             match_date = dtime.date()
#             str_date = fields.Date.to_string(match_date)
#         else:
#             if 'time' in add_update_dict:
#                 begin_time = add_update_dict['time']
#                 dtime = datetime.datetime.strptime(begin_time,'%d/%m/%Y %H:%M') - timedelta(hours=7)
#                 str_time = fields.Datetime.to_string(dtime)
#                 match_date = dtime.date()
#                 str_date = fields.Date.to_string(dtime)
#             else:
#                 match_date = datetime.datetime.strptime(add_update_dict['date'],'%d/%m/%Y')
#                 str_date = fields.Date.to_string(match_date)
#                 str_time = None
                
                
        team1_id = get_or_create_object_sosanh(self,'tsbd.team',{'name':home})
        team2_id = get_or_create_object_sosanh(self,'tsbd.team',{'name':away})
        team_dict = {'team1': team1_id.id,
                            'team2': team2_id.id,
#                             'time':str_time,
                            'date':str_date,
                            
                    }
        return team_dict, match_date, str_time,home,away, soup
    
def get_score(fix_id, soup=None,add_update_dict = {}):
    if 'score1' in add_update_dict and 'score2' in add_update_dict and 'state' in add_update_dict and 'curent_time' in add_update_dict:
        score_dict = {'score1': add_update_dict['score1'],
                  'score2': add_update_dict['score2'],
                  'curent_time': add_update_dict['curent_time'],
                  'state': add_update_dict['state']
                  }
    elif 'state' in add_update_dict and add_update_dict['state']==u'Chưa bắt đầu':
        score_dict = {'state':u'Chưa bắt đầu',
                      'curent_time':False,
            }
    else:
        pass
        if not soup:
            template_link = u'http://bongdaso.com/_MatchScoreTable.aspx?FixtureID=%s'
            soup = get_soup_ajax_link(fix_id,template_link)
        div_scores = soup.select('div.score')
        if  not div_scores:
            div_scores = soup.select('span.sscore')
            span = True
        else:
            span =False
        txt_list_divodds = list(map(lambda td: td.get_text(),div_scores))
        try:
            score1 =  int(txt_list_divodds[0])
            score2 =  int(txt_list_divodds[2])
        except:
            score1,score2 =False,False
        if span == False:
            try:
                fixture_status = soup.select('div.fixture_status')[0].get_text().strip()
            except IndexError:
                fixture_status = False
            try:
                curent_time = int(fixture_status)
                state = u'process'
            except:
                curent_time = False
                state = fixture_status
        else:
            state_soups = soup.select('div div')
            state = state_soups[-1].get_text()
            curent_time = False
        score_dict = {'score1':score1,
                      'score2':score2,
                      'curent_time':curent_time,
                      'state':state
                      }
    return score_dict

def get_odds(fix_id):
#     txt_list_divodds = None
#     num_try_get_html = 0
#     while not txt_list_divodds and num_try_get_html < 5:
    template_link = u'http://bongdaso.com/_OddsInfo.aspx?FixtureID=%s&LeagueID=1&SeasonID=50&HomeClubID=14&AwayClubID=15001&HomePrimaryClubID=14&AwayPrimaryClubID=15001&HomeShortCode=NEW&AwayShortCode=WOV&Home=Newcastle&Away=Wolverhampton'
    soup = get_soup_ajax_link(fix_id,template_link)
    divodds = soup.select('div#ABOdds table  tr:nth-of-type(2) td')
    txt_list_divodds = list(map(lambda td: thap_phan_co_2_cham(td) ,divodds))
#     if not txt_list_divodds:
#             f = open("/media/sf_C_DRIVE/D4/dl/not_odds.html", "w")
#             f.write(str(soup))
#             num_try_get_html +=1
    if txt_list_divodds:
        odds_dict = {
            'begin_handicap_money1' : txt_list_divodds[0] -1  if  txt_list_divodds[0] else False,
            'begin_handicap_money2' : txt_list_divodds[2] -1 if  txt_list_divodds[2] else False,
            'begin_handicap' :  txt_list_divodds[1],
            'begin_ou_money1' :txt_list_divodds[4] -1.0 if txt_list_divodds[4] else False,
            'begin_ou_money2' : txt_list_divodds[5] -1.0 if txt_list_divodds[5] else False,
            'begin_ou' :txt_list_divodds[3],
            }
    else:
        raise UserError(u'không có txt_list_divodds')
    
        
    
    
    
    trow_soups = soup.select('tr table tr')
    score_odd_lst_strows = []
    print ('len(trow_soups)',len(trow_soups))
    for trow in trow_soups:
        score = trow.select('td')
#             td_odd_down = trow.select('td:nth-of-type(1)')
        if score:
            score = score[0].get_text()
            if ' - ' in score:
                a_score_odds = []
                scores  = score.split(' - ')
                a_score_odds.append(scores)
                td2 = trow.select('td:nth-of-type(2)')
                if td2:
                    td2 = td2[0].get_text()
                    a_score_odds.append(td2)
#                     score +=' ' + td2
                score_odd_lst_strows.append(a_score_odds)
#         txt_trows = u'\n'.join(score_odd_lst_strows)
    
    score_odd_lst_strows
    return odds_dict, score_odd_lst_strows
def get_cate(self,fix_id, league_season, match_date, soup = None):
    if not soup:
        template_link = u'http://bongdaso.com/_OtherMatches.aspx?FixtureID=%s&{}&CountryRegionID=-1&PlayingDate={}'.format(league_season, match_date.strftime('%d-%m-%Y'))
        soup = get_soup_ajax_link(fix_id,template_link)
    try:
        name = soup.select('table tr.ls')[0].get_text()
        name = name.strip()
    except:
        name = False
    if name:
        cate_id = get_or_create_object_sosanh(self,'tsbd.cate', {'name':name})
        cate_id = cate_id.id
    else:
        cate_id = False
    return cate_id




def gen_a_match_dict(self,adict, trow, mode='stat', cate_name = False,period=False):
    nth_datetime = 1
    date_format = '%d/%m/%y %H:%M'
    time_key = 'time'
    
    if mode =='stat' or mode =='SeasonID':
        if mode=='stat':
            offset = 0
            date_format = '%d/%m/%Y'
            time_key = 'date'
        elif mode =='SeasonID': # lịch thi đấu
            offset =1
            date_format = '%d/%m/%y %H:%M'
            time_key = 'time'
        elif mode =='AsianCupSchedule':
            offset =1
            date_format = '%d/%m/%y %H:%M'
            time_key = 'time'
        nth_home =3 - offset
        nth_away = 5 - offset
        nth_score = 4 - offset
        nth_match_link = 6 - offset
      
    elif mode == '_ComingMatches':
        date_format = '%d/%m %H:%M'
        time_key = 'time'
        nth_match_link = 6
        
    elif mode == '_PlayedMatches':
        date_format = '%d/%m %H:%M'
        time_key = 'time'
        nth_match_link = 5
        nth_home =2
        nth_away = 4
        nth_score =3
#         
#         match_link_td = trow.select('td:nth-of-type(5) a')
#         if not match_link_td:
#             continue
#         href =  'http://bongdaso.com/' + match_link_td[0]['href']
#         adict['match_link'] = href
#         adict['cate'] = cate_name
#         
#         begin_time =  trow.select('td:nth-of-type(1)')[0].get_text()
#         begin_times = begin_time.split(' ')
#         begin_time = begin_times[0] + '/' + str(fields.Date.from_string(fields.Date.context_today(self)).year) +' ' + begin_times[1]
#         adict['time']= begin_time
#         
#         begin_time =  trow.select('td:nth-of-type(2)')[0].get_text()
#         adict['home']= begin_time
#         begin_time =  trow.select('td:nth-of-type(4)')[0].get_text()
#         adict['away']= begin_time
        
    elif mode =='AsianCupSchedule':
        nth_home =4
        nth_away = 6
        nth_score = 5
        nth_match_link = 8
        nth_datetime=2
        
        
    datem =  trow.select('td:nth-of-type(%s)'%nth_datetime)
    if datem:
        datem = datem[0].get_text()
        if datem:
            try:
                datem_obj = datetime.datetime.strptime(datem, date_format)
                if mode == 'SeasonID' or mode =='AsianCupSchedule':
                    datem = datem_obj.strftime('%d/%m/%Y %H:%M')
                elif mode == '_ComingMatches' or mode == '_PlayedMatches' :
                    datems = datem.split(' ')
                    datem = datems[0] + '/' + str(fields.Date.from_string(fields.Date.context_today(self)).year) +' ' + datems[1]
            except Exception as e:
                return 'continue'
        else:
            return 'continue'
    else:
        return 'continue'
    
    if datem_obj:
        if mode !='_ComingMatches':
            home =  trow.select('td:nth-of-type(%s) a'%nth_home)
            away =  trow.select('td:nth-of-type(%s) a'%nth_away)
            home = home[0].get_text()
            away = away[0].get_text()
        else:
            home_away =  trow.select('td:nth-of-type(2)')[0].get_text()
            home, away =  home_away.split(' - ')
        
        adict['home']= home.strip()
        adict['away']= away.strip()
            
        if mode == 'stat':
            cate =  trow.select('td:nth-of-type(2) img')
            cate = cate[0]
            cate = cate['title']
        else:
            cate = cate_name
        
        if cate:
            cate = cate.strip()
            if cate:
                adict['cate']= cate
        if period:
            adict['period']= period
        
        adict[time_key]= datem
        match_link =  trow.select('td:nth-of-type(%s) a'%nth_match_link)
        if match_link:
            match_link = match_link[0]['href']
            match_link = 'http://bongdaso.com/' + match_link
        else:
            match_link = False
        adict['match_link']=match_link
        
        
        
        if mode !='_ComingMatches':
            score_soup =  trow.select('td:nth-of-type(%s)'%nth_score)[0].get_text()
            if '~' in score_soup:
                score_soup = score_soup.split('~')
            elif '*' in score_soup:
                score_soup = score_soup.split('*')
            elif '-' in score_soup:
                score_soup = score_soup.split('-')
            else:
                return 'continue'
                raise UserError(u'Sao tỷ số lại không có định dạn -, *,~')
            try:
                adict['score1'] = int(score_soup[0])
                adict['score2'] = int(score_soup[1])
                adict['state']= u'Kết thúc'
                adict['curent_time']= False
            except:
                adict['score1'] = False
                adict['score2'] = False
                adict['state']= u'Chưa bắt đầu'
                adict['curent_time']= False
                
        else:
            adict['state']= u'Chưa bắt đầu'
    else:
        return 'continue'
   
# if '_PlayedMatches' in all_match_link:
#     #http://bongdaso.com/_PlayedMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1
#     mode = '_PlayedMatches'  #1
# elif 'Data=stat' in all_match_link:
#     #http://bongdaso.com/Everton-Leicester_City-2019_01_01-_Fix_55956.aspx.aspx?LeagueID=1&SeasonID=106&Data=stat
#     mode = 'stat' #2
# elif '_ComingMatches' in all_match_link:
# #http://bongdaso.com/_ComingMatches.aspx?LeagueID=-1&SeasonID=-1&Period=1&Odd=1
#     mode = '_ComingMatches' #4
# else:
#     #http://bongdaso.com/LeagueSchedule.aspx?LeagueID=1&SeasonID=106&CountryRegionID=-1&Period=5
#     mode = 'SeasonID' #3
#    
    
    
def get_list_of_match_dict(self, soup, mode):
    match_link_list = []
    trows = soup.select('table  tr')
    cate_name = False
    period = False
    if mode == 'SeasonID': #r sửa 
        cate_soup = soup.select('div.season_info table tr:nth-of-type(1) td:nth-of-type(2)')
        cate_name = cate_soup[0].get_text()
        period= soup.select('div.periods_table td.ctbl_selected')[0].get_text()
    elif mode =='AsianCupSchedule':
        cate_name = 'Asian Cup 2019'
    for trow in trows:
        adict = {}
        if mode == '_PlayedMatches' or mode == '_ComingMatches':
            class_ = trow.get('class')
            if class_ ==['ls']:
                cate_name = trow.get_text()
                cate_name = cate_name.strip()
                continue
#         if mode == '_PlayedMatches' :
#             match_link_td = trow.select('td:nth-of-type(5) a')
#             if not match_link_td:
#                 continue
#             href =  'http://bongdaso.com/' + match_link_td[0]['href']
#             adict['match_link'] = href
#             adict['cate'] = cate_name
#             begin_time =  trow.select('td:nth-of-type(1)')[0].get_text()
#             begin_times = begin_time.split(' ')
#             begin_time = begin_times[0] + '/' + str(fields.Date.from_string(fields.Date.context_today(self)).year) +' ' + begin_times[1]
#             adict['time']= begin_time
#             begin_time =  trow.select('td:nth-of-type(2)')[0].get_text()
#             adict['home']= begin_time
#             begin_time =  trow.select('td:nth-of-type(4)')[0].get_text()
#             adict['away']= begin_time
#         else:
        rt = gen_a_match_dict(self,adict, trow,mode, cate_name,period)
        if rt =='continue':
            continue
        if 'home' not in adict:
            raise UserError(' not home in adict %s in get_list_of_match_dict'%adict)
        match_link_list.append( adict)
    return  match_link_list
def update_score_odds (self, txt_trows,match_id):  
    bet_ScoreLines = []
    for score_odd in txt_trows:
        betscore1 = int(score_odd[0][0])
        betscore2 = int(score_odd[0][1])
        odd = float(score_odd[1])
        bet_score_id = get_or_create_object_sosanh(self,'tsbd.betscore', {'betscore1':betscore1, 'betscore2':betscore2})[0].id
        bet_ScoreLine = get_or_create_object_sosanh(self,'tsbd.betscoreline', {'betscore_id':bet_score_id, 'match_id':match_id}, {'odd':odd})
        bet_ScoreLines.append(bet_ScoreLine)
    return bet_ScoreLines
def get_events(fix_id,self, home,away):
    home =  quote(home)
    away = quote(away)
    link = 'http://bongdaso.com/_CastingInfo.aspx?FixtureID={}&SeasonID=112&Flags=&Home={}&Away={}'.format(fix_id, home, away)
#     soup = get_soup_ajax_link(fix_id, link)
    html  = request_html(link)
    soup = BeautifulSoup(html, 'html.parser')
    rs = soup.select('div.fixture_casting table tr')
    events =[]
    for tr in rs:
        score_soup = tr.select('td:nth-of-type(3)')
        minute_soup = tr.select('td:nth-of-type(1)')
#         score_txt =  score[0].get_text()
        if score_soup:
            minute_str = minute_soup[0].get_text()
            minutes= minute_str.split('+')
            minute_str = minutes[0].replace("'",'')
            try:
                minute = int(minute_str)
                if len(minutes) ==2:
                    adding_minute_str = minutes[1].replace("'",'')
                    adding_time = int(adding_minute_str)
                else:
                    adding_time = False
            except:
                adding_time = False
                pass
            str_score = score_soup[0].get_text()
            if str_score:
                des  = tr.select('td:nth-of-type(4)')[0].get_text()
                str_scores = str_score.split(':')
                score1 = int(str_scores[0])
                score2 = int(str_scores[1])
                score_event = get_or_create_object_sosanh(self,'tsbd.event', {'event':'goal','match_id':self.id, 'score1':score1,'score2':score2},{'des':des,'current_time': minute,'adding_time':adding_time}).id
                events.append(score_event)
            event_soup = tr.select('td:nth-of-type(2) img')
            if event_soup:
                event_soup =event_soup[0]
                src = event_soup.get('src',None)
                if src == 'img/45.gif':
                    des  = tr.select('td:nth-of-type(4)')[0].get_text()
                    rs = re.search('(\d+):(\d+)', des)
                    score1,score2 =rs.group(1),rs.group(2)
                    haftime_event = get_or_create_object_sosanh(self,'tsbd.event', {'event':'h1_finish','match_id':self.id},{'des':des,'score1':score1,'score2':score2, 'current_time': minute,'adding_time':adding_time}).id
                    events.append(haftime_event)
    return events
                
def get_update_dict(self, match_link, match_date, IS_GET_STATISTICS_MATCH = False, add_update_dict = {},str_time=None, match_soup = None):
        update_dict = {}
        fix_id = get_fix_id(match_link)
        #         cate = add_update_dict['cate']
        cate_id = False
        if 'cate'  in add_update_dict :
            cate_id = get_or_create_object_sosanh(self,'tsbd.cate', {'name':add_update_dict['cate']}).id
        else:
            league_season = re.search(r'\?(.*$)',match_link).group(1)
            cate_id = get_cate(self, fix_id, league_season, match_date)
        if cate_id:
            update_dict['cate_id']  = cate_id    
        if not match_soup:
            match_soup = get_soup(match_link)
        grp_rnd_info = match_soup.select('div#grp_rnd_info')
        if grp_rnd_info:
            grp_rnd_info= grp_rnd_info[0].get_text()
            if u'ảng' in grp_rnd_info:
                update_dict['bang_id']  = get_or_create_object_sosanh(self,'tsbd.cate', {'name':grp_rnd_info, 'cate_id':cate_id}).id
        score_and_status_dict = get_score(fix_id, add_update_dict=add_update_dict)
        update_dict.update(score_and_status_dict)
        odds_adict, score_odd_lst_strows = get_odds(fix_id)
        update_dict.update(odds_adict)
        if 'period' in add_update_dict:
            update_dict['period_id']  = get_or_create_object_sosanh(self,'tsbd.period', {'name':add_update_dict['period']}).id
        update_dict['match_link']  = match_link or add_update_dict.get('match_link')
        if str_time:
            update_dict['time'] = str_time
        if IS_GET_STATISTICS_MATCH:
            match_link  = re.sub('&Data=(.*?)$','',match_link)
            statictis_link =match_link +'&Data=stat'
            statictis_match_ids = self.leech_all_match_function(statictis_link, is_write = False, break_count=6, IS_GET_STATISTICS_MATCH  = False)
            statictis_match_dict = {'statictis_match_ids':[(6,0,statictis_match_ids)]}
            update_dict.update(statictis_match_dict)
        return update_dict, score_odd_lst_strows
    
    