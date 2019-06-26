# -*- coding: utf-8 -*-
from odoo.tests import common
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from odoo.tests import Form
from odoo.tests import common
# from odoo.addons.base.tests.test_mail.tests.common import mail_new_test_user



class TestDai(common.TransactionCase):
    def setUp(self):
        super(TestDai, self).setUp()
        
#         self.department = self.env.ref('hr.dep_rd')
#         self.department.write({'manager_id': self.employee_admin.id})
#         self.job = self.env.ref('hr.job_cto')
#         self.res_users_1 = mail_new_test_user(self.env, login='hro1', groups='base.group_user,dai_tgg.group_cvi_user', name='HR Officer 1', email='hro1@example.com')
#         Employee = self.env['hr.employee'].sudo(self.res_users_1)
#         employee_form = Form(Employee)
#         employee_form.name = 'Raoul Grosbedon'
#         employee_form.work_email = 'raoul@example.com'
#         employee_form.work_location = 'HCM City'
#         employee_form.department_id = self.department
#         employee_form.job_id = self.job
#         self.employee = employee_form.save()
        
#         print ('*********888employee', self.employee.name, self.res_users_1.name, self.res_users_1.login)
#         print ('*********888employee', self.res_users_1.name, self.res_users_1.login)
#         print ('setUp test dai TGG*******************')
#         tvcv = self.env['tvcv'].search([('diem','!=',0)],limit=1)
#         print ('tvcv.name',tvcv.name)
#         new_cvi = self.env['cvi'].create({'tvcv_id':tvcv.id})
#         print ('new_cvi.diemld*********',new_cvi.diemld)
    def test_dai_tgg_1(self):
        print ('test*** DAITGGGGGGGGGGGGGGGGG')
        tvcv = self.env['tvcv'].search([('diem','!=',0)],limit=1)
        print ('tvcv.name',tvcv.name)
        new_cvi = self.env['cvi'].create({'tvcv_id':tvcv.id, 'cd_children_ids':[(0,0,{'user_id':4})]})
        print ('new_cvi.diemld*********',new_cvi.diemld)
        print ('cd_childrend_ids*********',new_cvi.cd_children_ids)
        self.assertEquals(new_cvi.diemld, new_cvi.cd_children_ids[0].diemld)
        self.assertEquals(new_cvi.diemld, tvcv.diem/2)


