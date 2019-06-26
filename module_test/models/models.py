# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ModuleTest(models.Model):
    _name = 'module_test.test'
    is_raise_when_not_equal = fields.Boolean()
    log = fields.Text()
    @api.multi
    def test(self):
        CVI_obj = self.env['cvi']
        cvi_fields = CVI_obj._fields
        rs = CVI_obj.default_get([])
        self.log = '%s'%rs
    

