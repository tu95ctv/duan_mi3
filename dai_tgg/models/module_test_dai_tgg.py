# -*- cding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_
from odoo.exceptions import UserError


class TestError(Exception):
    type = None
    pass
class ModuleTest(models.Model):
    _inherit = "module_test.test"
    def assertEquals(self,*args):
        print (u'So sánh %s'%str(args))
        if len(args) < 2:
            raise UserError('%s tham số đưa vào ít hơn 2 tham số'%str(args))
        equal = True
        for i in args[1:]:
            if i !=args[0]:
                equal = False
        print (u'Equal:%s--%s'%(equal, str(args)))
        if not equal and self.is_raise_when_not_equal:
            raise TestError(u'TestError, Equal:%s--%s'%(equal, str(args)))
            
    @api.multi
    def test_dai_tgg(self):
        try:
            self = self.with_context(default_loai_record = u'Công Việc')
            print ('test*** DAITGGGGGGGGGGGGGGGGG')
            last_user = self.env['res.users'].search([],limit=1,order='id desc')
            tvcv = self.with_context(default_loai_record = u'Công Việc').env['tvcv'].search([('diem','!=',0)],limit=1)
            new_cvi = self.with_context(default_loai_record = u'Công Việc').env['cvi'].create({'tvcv_id':tvcv.id, 'loai_record':u'Công Việc', 'cd_children_ids':[(0,0,{'loai_record':u'Công Việc', 'user_id':last_user.id})]})
            print ('tvcv.name',tvcv.name,'diem', tvcv.diem)
            print ('new_cvi*********',new_cvi.name, new_cvi.diemld,'slncl',new_cvi.slncl)
            print ('cd_childrend_ids*********',new_cvi.cd_children_ids)
            cvi_con = new_cvi.cd_children_ids[0]
            print ('cvi_con*********',cvi_con.name, cvi_con.diemld,'slncl',cvi_con.slncl)
            self.assertEquals(new_cvi.diemld, new_cvi.cd_children_ids[0].diemld)
            self.assertEquals(new_cvi.diemld, tvcv.diem/3)
            raise UserError (u'Bạn chưa chọn dòng nào')
        except TestError as e:
            raise UserError(str(e))
