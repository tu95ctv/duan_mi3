
# -*- coding: utf-8 -*-
import sys
from unidecode import unidecode
import re
from odoo import fields
import pytz
VERSION_INFO   = sys.version_info[0]
if VERSION_INFO ==2:
    unicode =  unicode
else:
    unicode  =  str
def pn_replace(pn):
    if pn:
        pn_replace =  re.sub('[- _ \s \\\ \/ |.]','',pn)
        return pn_replace
    else:
        pn_replace = pn
    return pn_replace


def viet_tat(string):
    string = string.strip()
    ns = re.sub('\s{2,}', ' ', string)
    ns = re.sub('[^\w ]','', ns,flags = re.UNICODE)
    slit_name = ns.split(' ')
    slit_name = filter(lambda w : True if w else False, slit_name)
    one_char_slit_name = map(lambda w: w[0],slit_name)
    rs = ''.join(one_char_slit_name).upper()
    return rs
def name_khong_dau_compute(self_):
    for r  in self_:
        if r.name:
            name = r.name
            if name:
                try:
                    name_khong_dau = unidecode(name)
                except:
                    raise ValueError(name)
                r.name_khong_dau = name_khong_dau
                r.name_viet_tat = viet_tat(name_khong_dau)
                
def name_compute(r,adict=None,join_char = u' - ',junc_char=u':'):
    names = []
    for fname,attr_dict in adict:
#         not_use_val = attr_dict.get('attr_dict')
        val = getattr(r,fname)
        func = attr_dict.get('func',None)
        karg = attr_dict.get('karg',{})
        
        if func:
            val = func(val,**karg)
        else:
            if hasattr(val, 'name'):
                val = val.name
        if  val ==False or (not val and  fname=='id' ):# Cho có trường hợp New ID
            if attr_dict.get('skip_if_False',True):
                continue
            if  fname=='id' :
                val ='New'
            else:
                val ='_'
        if attr_dict.get('pr',None):
            a_junc_char = attr_dict.get('junc_char',junc_char)
            item =  attr_dict['pr'] + a_junc_char + ' ' + unicode(val)
        else:
            item = unicode (val)
        names.append(item)
    if names:
        name = join_char.join(names)
    else:
        name = False
    return name


def convert_odoo_datetime_to_vn_str(odoo_datetime, format='%d/%m/%Y %H:%M' ):
    if odoo_datetime:
        utc_datetime_inputs = fields.Datetime.from_string(odoo_datetime)
        vn_time = convert_utc_to_gmt_7(utc_datetime_inputs)
        vn_time_str = vn_time.strftime(format)
        return vn_time_str
    else:
        return False
    
def convert_utc_to_gmt_7(utc_datetime_inputs):
    local = pytz.timezone('Etc/GMT-7')
    utc_tz =pytz.utc
    gio_bat_dau_utc_native = utc_datetime_inputs#fields.Datetime.from_string(self.gio_bat_dau)
    gio_bat_dau_utc = utc_tz.localize(gio_bat_dau_utc_native, is_dst=None)
    gio_bat_dau_vn = gio_bat_dau_utc.astimezone (local)
    return gio_bat_dau_vn
