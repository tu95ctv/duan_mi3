# -*- coding: utf-8 -*-

# from odoo.tests import Form
from odoo.tests import common
# from odoo.addons.test_mail.tests.common import mail_new_test_user

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class TestHrResign(common.TransactionCase):

    def setUp(self):
        super(TestHrResign, self).setUp()
        print ('setUp test***************8')
        

#         self.employee_admin = self.env.ref('hr.employee_admin')
#         self.user_admin = self.env.ref('base.user_admin')
# 
#         self.department = self.env.ref('hr.dep_rd')
#         self.department.write({'manager_id': self.employee_admin.id})
# 
#         self.job = self.env.ref('hr.job_cto')
# 
# #         self.res_users_1 = mail_new_test_user(self.env, login='hro1', groups='base.group_user,xb_hr_resign.group_hr_resign_manager,hr_contract.group_hr_contract_manager', name='HR Officer 1', email='hro1@example.com')
#         Employee = self.env['hr.employee'].sudo(self.res_users_1)
#         employee_form = Form(Employee)
#         employee_form.name = 'Raoul Grosbedon'
#         employee_form.work_email = 'raoul@example.com'
#         employee_form.work_location = 'HCM City'
#         employee_form.department_id = self.department
#         employee_form.job_id = self.job
#         self.employee = employee_form.save()
# 
#         self.Resign = self.env['hr.resign']
#         self.ResignType = self.env['hr.resign.type']
#         self.Activity = self.env['mail.activity']

    def test_resign_change_status(self):
        print ('test****************8')
#         resignation = self.ResignType.create({
#             'name': 'Resignation',
#             'category': 'resignation'
#         })
#         vals = {
#             'name': 'reclassify: Change Position',
#             'employee_id': self.employee.id,
#             'type_id': resignation.id,
#         }
#         resign = self.Resign.create(vals)
#         resign.company_id.write({
#             'resign_user_id': self.res_users_1.id,
#             'resign_manager_id': self.user_admin.id,
#         })
#         self.assertEquals(resign.state, 'draft')
# 
#         resign.onchange_employee_id()
#         self.assertEquals(resign.manager_id, self.employee_admin)
# 
#         resign.action_submit()
#         self.assertEquals(resign.state, 'submitted')
#         activities_submitted = self.Activity.search([('res_model_id', '=', self.env['ir.model']._get(resign._name).id), ('res_id', '=', resign.id)])
#         self.assertEquals(len(activities_submitted.ids), 1)
# 
#         resign.action_validate()
#         self.assertEquals(resign.state, 'validate')
