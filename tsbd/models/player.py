# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
try:
    import urllib.request as urllib2_or_urllib_request
except:
    import urllib2 as urllib2_or_urllib_request
class Player(models.Model):
    _name='tsbd.player'
    name = fields.Char()
#     birthday = fields.One2many('tsbd.bxh','team_id')
    
    current_team_id = fields.Many2one('tsbd.team')
    da_chinh_hay_du_bi = fields.Selection([('da_chinh', 'da_chinh'), ('du_bi', 'du_bi')])
    number = fields.Integer()
    birthday = fields.Date()
    image_link = fields.Char()
    image_view = fields.Binary(compute='thumb_view_')
    saved_image_view = fields.Binary(attachment=True)
    team_id = fields.Many2one('tsbd.team')
    @api.depends('image_link')
    def thumb_view_(self):
        for r in self:
            if r.image_link:
                photo = base64.encodestring(urllib2_or_urllib_request.urlopen(r.image_link).read())
                r.image_view = photo 
    da_chinh_number = fields.Integer()
    du_bi_number = fields.Integer()
class PlayerLine(models.Model):
    _name = 'tsbd.playerline'
    player_id = fields.Many2one('tsbd.player')
    team_id = fields.Many2one('tsbd.team')
    match_id = fields.Many2one('tsbd.match')
    da_chinh_hay_du_bi = fields.Selection([('da_chinh', 'da_chinh'), ('du_bi', 'du_bi')])
    home_or_away = fields.Selection([('home', 'home'), ('away', 'away')])
