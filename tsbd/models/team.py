# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Team(models.Model):
    _name='tsbd.team'
    name = fields.Char()
    bxh_ids = fields.One2many('tsbd.bxh','team_id')
    large_bxh_id = fields.Many2one('tsbd.bxh',compute='large_bxh_id_', store=True)
    trig = fields.Boolean()
    cate_id = fields.Many2one('tsbd.cate', related='large_bxh_id.cate_id', store=True)
    short = fields.Char()
    @api.multi
    def trig_button(self):
        self.write({'trig':True})
    @api.depends('bxh_ids','trig')
    def large_bxh_id_(self):
        for r in self:
#             if r.bxh_ids:
            bxh = self.env['tsbd.bxh'].search([('team_id','=', r.id), ('round','=', False), ('cate_id.no_match','>', 5)])
            if bxh:
#                 bxh_ids =  r.bxh_ids.sorted(key=lambda r: r.cate_id.no_match)
                r.large_bxh_id = bxh[0]
    def take_name(self):
        if self.large_bxh_id:
            return self.large_bxh_id.take_name(is_name_gon=True)
        else:
            return self.name
        
    @api.multi
    def name_get(self):
        rs = []
        for r in self:
#             else:
#                 stt = self.env['tsbd.bxh'].search([('team_id','=',r.id)])
#                 stt_bet = self.env['tsbd.betbxh'].search([('team_id','=',r.id)])
#                 stt = u'(%s)'%stt[0].stt if stt else ''
#                 stt_bet = u'[%s%%%s]'%(stt_bet[0].diem_phan_tram, stt_bet[0].stt) if stt_bet else ''
#                 name_show = u'%s%s%s'%(r.name,stt,stt_bet)
            rs.append((r.id, r.take_name()))
        return rs
    