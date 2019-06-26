# -*- coding: utf-8 -*-
from odoo.tests import common
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
class TestTonKho(common.TransactionCase):
    def setUp(self):
        super(TestTonKho, self).setUp()
        pass
#         print ('setUp test***************8')
#         tvcv = self.env['tvcv'].search([('diem','!=',0)],limit=1)
#         print ('tvcv.name',tvcv.name)
#         new_cvi = self.env['cvi'].create({'tvcv_id':tvcv.id})
#         print ('new_cvi.diemld*********',new_cvi.diemld)
    def test_resign_change_status(self):
        pass
#         print ('test*** test_resign_change_status*************8')
#         tvcv = self.env['tvcv'].search([('diem','!=',0)],limit=1)
#         print ('tvcv.name',tvcv.name)
#         new_cvi = self.env['cvi'].create({'tvcv_id':tvcv.id})
#         print ('new_cvi.diemld*********',new_cvi.diemld)
#         

