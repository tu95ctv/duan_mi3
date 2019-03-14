# -*- coding: utf-8 -*-

from odoo import models, fields, api
class ErrorLog(models.Model):
    _name='tsbd.errorlog'
    match_id = fields.Many2one('tsbd.match')
    function = fields.Char()
    link = fields.Char()