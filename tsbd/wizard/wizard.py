# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'tsbd.wizard'
    name  = fields.Char()
    res_model = fields.Char(default = lambda self: self._context.get('active_model'))
    log = fields.Text()
    
    @api.multi
    def save_avatar_player(self):
        players = self.env['tsbd.player'].search([('image_link', '!=', False)])
        for r in players:
            r.saved_image_view = r.image_view
    @api.multi
    def xoa_bxh_not_cated(self):
        not_cate_bxh = self.env['tsbd.bxh'].search([('cate_id','=',False)])
        not_cate_bxh.unlink()
        self.log = u'Đã xóa %s bxh'%(len(not_cate_bxh))
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'tsbd.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'context':{'active_model':self.res_model},
                'views': [(False, 'form')],
                'target': 'new',
            }
        
    @api.multi
    def trig(self):
        if self.res_model =='tsbd.match':
            domain = [('state','=',u'Kết thúc')]
        else:
            domain = []
        not_cate_bxh = self.env[self.res_model].search(domain)
        not_cate_bxh.write({'trig':True})
        self.log = u'Đã trig %s Predict'%(len(not_cate_bxh))
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'tsbd.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'context':{'active_model':self.res_model},
                'views': [(False, 'form')],
                'target': 'new',
            }
    
    def return_this(self):
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'tsbd.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'context':{'active_model':self.res_model},
                'views': [(False, 'form')],
                'target': 'new',
            }
        
    @api.multi
    def xoa_bxh(self):
        cates = self.env['tsbd.cate'].search([('large_cate','=', True)])
        for c in cates:
            c.clear_bxh()
        self.log = u'Đã Clear BXH'
        return self.return_this()
        
    
    
    @api.multi
    def gen_bxh(self):
        cates = self.env['tsbd.cate'].search([('large_cate','=', True)])
        for c in cates:
            c.bxh()
        for c in cates:
            c.with_context(for_bet=True).bxh()
        self.log = u'Đã Gen BXH'
        return self.return_this()
    
    
        

    