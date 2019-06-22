# -*- coding: utf-8 -*-
from odoo.tests import common
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
class TestTonKho(common.TransactionCase):
    def setUp(self):
        super(TestTonKho, self).setUp()
        print ('setUp test***************8')
    def test_resign_change_status(self):
        print ('test*** test_resign_change_status*************8')

