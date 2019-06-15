# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from math import ceil

def goaldecorator(func):
    def awrapper(*arg,**karg):  
        self = arg[0]
        for r in self:
            if r.event =='goal' :
                func(r)
    return awrapper


class Event(models.Model):
    _name = 'tsbd.event'
    time = fields.Datetime(default=fields.Datetime.now)
    match_id = fields.Many2one('tsbd.match')
    event = fields.Selection([('reset_score','reset_score'),('goal1','goal1'),('goal2','goal2'),
                              ('corner1','corner1'),('corner2','corner2'),
                              ('goal','goal'),('h1_finish','H1 finish'),
                              ])
    score1 = fields.Integer()
    score2 = fields.Integer()
    current_time = fields.Integer()
    range_time = fields.Selection([('10','10'),('20','20'),('30','30'),('40','40'),('50','50'),('60','60'),('70','70'),('80','80'),('90','90')],compute = 'range_time_',store=True)
    
    @api.depends('current_time')
    @goaldecorator
    def range_time_(self):
        for r in self:
            if r.current_time <= 90:
                rs = ceil(r.current_time/10.0)
                rs = str(rs*10)
                r.range_time =rs
    adding_time = fields.Integer()
    des = fields.Text()
    str_score = fields.Char(compute='str_score_',store=True)
    @api.depends('score1','score2','event')
    def str_score_(self):
        for r in self:
            if r.event =='goal':
                r.str_score =u'%s-%s'%(r.score1, r.score2)
    
    
    
    @api.onchange('time')
    def _oc_time(self):
        current_time = fields.Datetime.from_string(self.time) - fields.Datetime.from_string(self.match_id.time)
        current_time = current_time.seconds/60
        if current_time > 47:
            current_time =current_time - 15
        self.current_time = current_time
    
    @api.onchange('current_time')
    def _oc_current_time(self):
        current_time = self.current_time
        current_time = current_time + 15 if current_time > 47 else current_time
        self.time = fields.Datetime.from_string(self.match_id.time)  +  timedelta(minutes=current_time)
        
    @api.onchange('event')
    def _oc_event(self):
        score1 = self._context.get('default_score1')
        score2 = self._context.get('default_score2')
        if score1 !=None and score2!=None:
            if self.event =='goal1':
                score1 = score1 +1
                score2 = score2
            elif self.event =='goal2':
                score1 = score1
                score2 = score2 + 1
            self.score1 = score1
            self.score2 = score2
            