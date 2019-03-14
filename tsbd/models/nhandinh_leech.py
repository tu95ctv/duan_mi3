# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.tsbd.models.tool import  request_html
from bs4 import BeautifulSoup
import re
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.addons.tsbd.models.tool import   get_or_create_object_sosanh


def int_a_minute(str_minute):
    if str_minute:
        return int(str_minute)
    else:
        return 0
def get_team1_team2_name(team_vs_team):
    team_vs_team = team_vs_team.replace(',','')
    two_team = team_vs_team.split('vs')
    team1= two_team[0].strip()
    team2= two_team[1].strip()
    return (team1,team2)

def parse_title_bongdanet(str):
#     str= u'Nhận định Guingamp vs Nantes, 21h ngày 3/3 (VĐQG Pháp)'
#     str = u'Phân tích tỷ lệ Porto vs AS Roma, 3h ngày 7/3'
    print ('str***',str)
    rs_search = re.search('Nhận định(.*?)(\d+)h(\d*)\s+ngày\s+(\d+)/(\d+)',str, re.I)
    if rs_search:
        type_du_doan = u'nhận định'
    if not rs_search:
        rs_search = re.search('Nhận định(.*?)(\d+)h(\d*), (\d+)/(\d+)',str, re.I)
        type_du_doan = u'nhận định'
    if  not rs_search:
        rs_search = re.search('Phân tích tỷ lệ(.*?)(\d+)h(\d*) ngày (\d+)/(\d+)',str, re.I)
        type_du_doan = u'phân tích tỉ lệ'
    print ('***rs_search',rs_search)
    if not rs_search:
        return None
    rs =  (rs_search.group(2), rs_search.group(3),rs_search.group(4),rs_search.group(5))
    rs = list(map(lambda i:int_a_minute(i), rs))
    adt = datetime(year=datetime.now().year, month= rs[3], day= rs[2], hour= rs[0], minute = rs[1]) - timedelta(hours=7)
    team1_2 = get_team1_team2_name(rs_search.group(1))
    return team1_2, adt

def du_doan_ti_so(str):
#         rs = re.search('[(?:Dự đoán tỷ số)|(?:Dự đoán kết quả)].*?[:|\s]*(\d+)[-|\s](\d+)', str, re.I)
#         rs = re.search('[(?:Dự đoán tỷ số)|(?:Dự đoán kết quả)].*?(\d+)[-|\s](\d+)', str, re.I)
        rs = re.search('Dự đoán tỷ số.*?(\d+)[-|\s](\d+)', str, re.I)
        if not rs:
            rs = re.search('Dự đoán kết quả.*?(\d+)[-|\s](\d+)', str, re.I)     
        if not rs:
            rs = re.search('Dự đoán.*?(\d+)[-|\s](\d+)', str, re.I)     
        if rs:
            return  rs.group(1), rs.group(2)
    
class FETCHERROR(Exception):
    pass
def lay_du_doan_ngay_gio(gio,ngay):
#     gio = '03h20'
#     ngay = u'26/2'
    if len(ngay) < 8:
        ngays = ngay.split('/')
        if len(ngays[1]) == 1:
            ngay = ngays[0] + '/0' + ngays[1] 
        ngay = ngay + '/2019'
        ngay_gio = ngay + ' ' + gio
        dt = datetime.strptime(ngay_gio,'%d/%m/%Y %Hh%M')
    return dt


class NHANDINHLEECH(models.Model):
    _name='tsbd.ndl'
    name = fields.Char(compute='name_',store=True)
    @api.depends('all_nhan_dinh_link')
    def name_(self):
        for r in self:
            r.name = r.all_nhan_dinh_link
    link = fields.Char()
    log = fields.Text()
    all_nhan_dinh_link = fields.Char()
    ndline_ids = fields.One2many('tsbd.ndlline', 'nd_id')
    link_select = fields.Selection ([('link1', 'link1'), ('link2', 'link2')], default = 'link1')
    take_topic_from_link = fields.Selection([('from_link','from_link'), ('from_disk','from_disk')], default='from_link')
    range_select = fields.Boolean(default = True)
    range1 =  fields.Integer(default=1)
    range2 = fields.Integer(default =1,string="range 2( lấy luôn)")
    def map_predict_id (self):
        for r in self.ndline_ids:
            if 'bongdanet' in r.link:
                name_site ='bdnet'
            elif 'aegoal' in r.link:
                name_site ='aegoal'
            else:
                name_site = 'bdp.com'
            if r.match_id and r.state =='tu_dong':
                site_id = get_or_create_object_sosanh(self, 'tsbd.site', {'name': name_site}).id
                predict_id = get_or_create_object_sosanh(self, 'tsbd.predict', {'link':r.link, 'match_id':r.match_id.id}, 
                                                          {'site_id':site_id,'predict_score1':r.score1,'predict_score2':r.score2, 'state':r.state})
                r.predict_id = predict_id
    def map_match_id (self):
        for r in self.ndline_ids:
            team1 = r.team1
            team2 = r.team2
#             match_id = self.env['tsbd.match'].search([('date','=',r.ngay),'|',('team1.name','ilike',team1),('team2.name','ilike',team2)])
#             team1s = team1.split(' ')
            match_id = self.env['tsbd.match'].search([('date','=',r.ngay),'|','|','|',('team1.name','ilike',team1),('team1.short','ilike',team1),('team2.name','ilike',team2),('team2.short','ilike',team2)])
            if match_id:
                r.match_id = match_id[0]
    def du_doan(self,soup):
        ct = soup.select('div#postContent')
        ct =  ct[0].get_text()
        rs = re.search('DỰ ĐOÁN:\s*?(\d)\s*?-\s*?(\d)', ct,re.I)
        if not rs:
            rs = re.search('DỰ DOÁN:\s*?(\d)\s*?-\s*?(\d)', ct,re.I)
        if not rs:
            raise FETCHERROR('ti so eror')
        ti_so =  (int(rs.group(1)),int(rs.group(2)))
        
        return ti_so
#     def du_doan_ti_so(self,str):
#         str = u'Dự đoán tỷ số: 0-0'
#         rs = re.search('Dự đoán tỷ số[:|\s]*\d[-|\s]\d', st, re.I)
    @api.multi
    def leech_button(self):
        link = self.link if self.link_select == 'link1' else self.all_nhan_dinh_link
        rs  = request_html(link)
        file = open('/media/sf_C_DRIVE/D4/dl/testfile_%s.html'%self.link_select,'w') 
        file.write(rs) 
        file.close() 
        self.log =rs
    @api.multi
    def parse_button(self, all_nhan_dinh_link= None):
        all_nhan_dinh_link = 'http://bongdaplus.vn/nhan-dinh-bong-da/trang-1.html'
        range_page = self.gen_range(all_nhan_dinh_link= all_nhan_dinh_link)
        for link in range_page:
            if link ==None:
                pass
            else:
                html =  request_html(link)
            soup = BeautifulSoup(html, 'html.parser')
            a_s = soup.select('a')
            hrefs = []
            for a in a_s:
                try:
                    hrefs.append(a['href'])
                except:
                    pass
            hrefs =  list(filter ( lambda a: 'nhan-dinh-bong-da-' in a, hrefs))
            for h in hrefs:
                link = 'http://bongdaplus.vn/' + h
                rs  = request_html(link)
                soup = BeautifulSoup(rs, 'html.parser')
                self.nhan_dinh_a_match_bondaplus(link=link)
                
        self.map_match_id()
        self.map_predict_id()
        
    @api.multi
    def nhan_dinh_chung(self,link = None):
        self.parse_button()
        self.nhan_dinh_bongdanet()
        self.nhan_dinh_aegoal()
            
        
        
    @api.multi
    def nhan_dinh_a_match_bondaplus(self,*arg,**karg):
        link = karg.get('link')
        if not link:
            print ('Not link***********')
            file = open('/media/sf_C_DRIVE/D4/dl/testfile_link1.html','r') 
            html = file.read()
            soup = BeautifulSoup(html, 'html.parser')
        else:
            print ('Co link************')
            rs  = request_html(link)
            soup = BeautifulSoup(rs, 'html.parser')
        s = soup.select('h1.tit')
        str = s[0].get_text()
        print ('title **', str)
        rs = re.search(r'Nhận định bóng đá (.+?) vs (.+?),', str)
        if not rs:
            rs = re.search(r'Nhận định bóng đá (.+?) và (.+?),', str)
        if not rs:
            rs  = re.search(r'Nhận định bóng đá.*?: (.+?) vs (.+?)$', str)
        if not rs:
            rs  = re.search(r'Nhận định bóng đá.*?: (.+?) và (.+?)$', str)
        team1= rs.group(1).strip()
        team2= rs.group(2).strip()
       
        
        rs_search = re.search('(\d+)h(\d*).*?ngày\s+(\d+)/(\d+)', str)
#         gio= rs.group(1).strip()
#         rs_ngay = re.search('ngày\s+(\d+)/(\d+)', str)
#         ngay= rs.group(1).strip()
        
        rs =  (rs_search.group(1), rs_search.group(2),rs_search.group(3),rs_search.group(4))
        rs = list(map(lambda i:int_a_minute(i), rs))
        dt = datetime(year=datetime.now().year, month= rs[3], day= rs[2], hour= rs[0], minute = rs[1]) - timedelta(hours=7)
#         dt = lay_du_doan_ngay_gio(gio,ngay)
        dt = dt - timedelta(hours = 7)
        ngay =dt.date()
        dt = fields.Datetime.to_string(dt)
        
        
        update_dict = {'ngay':ngay,'ngay_gio':dt,'nd_id':self.id}
        try:
            score1,score2 = self.du_doan(soup)
            update_dict.update({ 'score1':score1,'score2':score2, 'state':'tu_dong'})
        except FETCHERROR:
            update_dict.update({ 'state':'can_read_du_doan'})
        ndlline = get_or_create_object_sosanh(self,'tsbd.ndlline', {'link':link,'team1':team1,'team2':team2}, update_dict)   

    @api.multi
    def nhan_dinh_a_match_bongdanet(self,*arg,**karg):
        link = karg.get('link')
        atuple = karg.get('atuple')
        link =  atuple[0]
        team_1_2_date = atuple[2]
        team1_2 = team_1_2_date[0]
        dt = team_1_2_date[1]
        ngay = dt.date()
        dt = fields.Datetime.to_string(dt)
        if not link:
            print ('Not link***********')
            file = open('/media/sf_C_DRIVE/D4/dl/testfile_link1.html','r') 
            html = file.read()
            soup = BeautifulSoup(html, 'html.parser')
        else:
            print ('Co link************')
            rs  = request_html(link)
            soup = BeautifulSoup(rs, 'html.parser')
            
        rs = soup.select('div#detail-content-news')[0].get_text()
        ti_so = du_doan_ti_so(rs)
        update_dict = {'nd_id':self.id}
        if ti_so:
            update_dict_more = { 'score1':ti_so[0],'score2':ti_so[1], 'state':'tu_dong'}
        else:
            update_dict_more = {'state':'can_read_du_doan'}
        update_dict.update(update_dict_more)
        ndlline = get_or_create_object_sosanh(self,'tsbd.ndlline', {'link':link, 'ngay':ngay,'ngay_gio':dt,'team1':team1_2[0],'team2':team1_2[1]}, update_dict)   
        return ti_so

        
        
    @api.multi
    def xoa_line(self):
        self.ndline_ids = [(5,0,0)]
   
    
    @api.multi
    def nhan_dinh_bongdanet(self, all_nhan_dinh_link= None ):
        
        all_nhan_dinh_link = 'http://bongdanet.vn/nhan-dinh/p2'
        range_page = list(self.gen_range( patern = 'http://bongdanet.vn/nhan-dinh/p\d+',
                                          replacement = 'http://bongdanet.vn/nhan-dinh/p%s',
                                          all_nhan_dinh_link= all_nhan_dinh_link
                                          ))
        for link in range_page:
            html =  request_html(link)
            soup = BeautifulSoup(html, 'html.parser')
            a_s = soup.select('div.news-item div.detail-news-item a')
            hrefs = []
            for a in a_s:
                try:
                    hrefs.append(['http://bongdanet.vn'+a['href'],a.get_text()])
                except:
                    pass
            hrefs =  list(filter ( lambda a: 'nhan-dinh' in a[0] or 'phan-tich' in a[0], hrefs))
            for atuple in hrefs:
                rs = parse_title_bongdanet(atuple[1])
                atuple.append(rs)
                
                
            for  c, at in enumerate(hrefs):
                if at[2] != None:
                    ti_so = self.nhan_dinh_a_match_bongdanet(link=at[0],atuple= at)
        self.map_match_id()
        self.map_predict_id()
                    
    @api.multi
    def nhan_dinh_a_match_aegoal(self,*arg,**karg):
        link = karg.get('link')
        
        if not link:
            print ('Not link***********')
            file = open('/media/sf_C_DRIVE/D4/dl/testfile_link1.html','r') 
            html = file.read()
            soup = BeautifulSoup(html, 'html.parser')
        else:
            atuple = karg.get('atuple')
            link =  atuple[0]
            team_1_2_date = atuple[2]
            team1_2 = team_1_2_date[0]
            dt = team_1_2_date[1]
            ngay = dt.date()
            dt = fields.Datetime.to_string(dt)
            print ('Co link************')
            rs  = request_html(link)
            soup = BeautifulSoup(rs, 'html.parser')
            
        rs = soup.select('div.box-text-detail')[0].get_text()
        ti_so = du_doan_ti_so(rs)
        
#         raise UserError(ti_so)
        update_dict = {'nd_id':self.id}
        if ti_so:
            update_dict_more = { 'score1':ti_so[0],'score2':ti_so[1], 'state':'tu_dong'}
        else:
            update_dict_more = {'state':'can_read_du_doan'}
        update_dict.update(update_dict_more)
        ndlline = get_or_create_object_sosanh(self,'tsbd.ndlline', {'link':link, 'ngay':ngay,'ngay_gio':dt,'team1':team1_2[0],'team2':team1_2[1]}, update_dict)   
        return ti_so
    
    
    @api.multi
    def nhan_dinh_aegoal(self, all_nhan_dinh_link= None ):
#         all_nhan_dinh_link = 'http://bongdaplus.vn/nhan-dinh-bong-da/trang-1.html'
        all_nhan_dinh_link = 'https://aegoal.net/nhan-dinh-bong-da.html?trang=1'
        range_page = self.gen_range(patern = 'trang-\d+',replacement = 'trang-%s', all_nhan_dinh_link= all_nhan_dinh_link)

        for link in range_page:
            html =  request_html(link)
            soup = BeautifulSoup(html, 'html.parser')
            rs = soup.select('div.list-item-new a')
            hrefs = []
            for a in rs:
                hrefs.append([a['href'],a.get_text()])
                
            hrefs =  list(filter ( lambda a: 'nhan-dinh' in a[0] or 'phan-tich' in a[0], hrefs))
            for atuple in hrefs:
                rs = parse_title_bongdanet(atuple[1])
                atuple.append(rs)
            for  c, at in enumerate(hrefs):
                    if at[2] != None:
                        ti_so = self.nhan_dinh_a_match_aegoal(link=at[0],atuple= at)

        self.map_match_id()
        self.map_predict_id()
        

                    

        
        
        
    
    def gen_range(self , patern = 'trang-\d+',replacement = 'trang-%s', take_topic_from_link=None, all_nhan_dinh_link = None):
        if take_topic_from_link or self.take_topic_from_link == 'from_disk':
            file = open('/media/sf_C_DRIVE/D4/dl/testfile_link2.html','r') 
            html = file.read()
            return html
            range_page = [None]
        else:
            all_nhan_dinh_link = all_nhan_dinh_link or self.all_nhan_dinh_link
            if self.range_select == True:
                int_ranges = range(self.range1, self.range2 +1)
                range_page = map(lambda i: re.sub(patern,replacement%i, all_nhan_dinh_link),int_ranges)
            else:
                range_page = [all_nhan_dinh_link]
        return range_page
        
    
        
class NHANDINHLEECHLINE(models.Model):
    _name='tsbd.ndlline'
    team1 = fields.Char()
    team2 = fields.Char()
    score1 = fields.Integer()
    score2 = fields.Integer()
    ngay_gio = fields.Datetime()
    ngay = fields.Date()
    nd_id = fields.Many2one('tsbd.ndl')
    match_id = fields.Many2one('tsbd.match')
    predict_id = fields.Many2one('tsbd.predict')
    link = fields.Char()
    state =  fields.Selection([('nhap_tay',u'Nhập tay'),('tu_dong','Tự động'),('can_read_du_doan','Không đọc được dự đoán')],default = 'nhap_tay')
    manual_updated_score= fields.Boolean()
    