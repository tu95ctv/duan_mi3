# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_
from odoo.exceptions import UserError
def return_form_action(self):
    return {
                'type': 'ir.actions.act_window',
                'res_model': 'setaction.setaction',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
#                 'context':{'active_model':self.model, 'function_key': self.function_key},
                'views': [(False, 'form')],
                'target': 'new',
            }
def return_form_action_decorator(func):
    def wrapper(*args,**kargs):
        self = args[0]
#         default_loai_record = self._context
#         print ('**********default_loai_record,', default_loai_record)
#         print ('**********default_loai_record,', default_loai_record.get('default_loai_record'))
#         if default_loai_record.get('default_loai_record') != u'Công Việc':
#             raise UserError(u'Không phải công việc không sử dụng chức năng multi này')
        func(*args,**kargs)
        return return_form_action(self)
    return wrapper

class Setaction(models.TransientModel):
    _inherit = "setaction.setaction"
    @api.multi
    @return_form_action_decorator
    def multi_confirmed(self):
        active_ids = self._context.get('active_ids')
        self.choosed_object_qty = len(active_ids)
        if active_ids:
            affected_count = 0
            for r in self.env['cvi'].browse(active_ids):
                if r.state in ['draft'] and not r.cam_sua:
                    affected_count +=1
                    r.state = 'confirmed'
            self.affected_object_qty = affected_count
        else:
            raise UserError (u'Bạn chưa chọn dòng nào')
        return return_form_action(self)
        
    @api.multi
    @return_form_action_decorator
    def multi_approved(self):
        active_ids = self._context.get('active_ids')
        self.choosed_object_qty = len(active_ids)
        if active_ids:
            affected_count = 0
            for r in self.env['cvi'].browse(active_ids):
                if r.is_sep and r.state in ['confirmed']:
                    affected_count +=1
                    r.state = 'approved'
                else:
                    raise UserError (u'Bạn không phải là lãnh đạo của nhân viên tạo record này hoặc trạng thái chưa phải là confirm')
            self.affected_object_qty = affected_count
        else:
            raise UserError (u'Bạn chưa chọn dòng nào')
        return return_form_action(self)
    @api.multi
    @return_form_action_decorator
    def multi_draft(self):
        active_ids = self._context.get('active_ids')
        self.choosed_object_qty = len(active_ids)
        if active_ids:
            affected_count = 0
            for r in self.env['cvi'].browse(active_ids):
                state = r.state
                if (state in ['mark_delete','confirmed'] and  not r.cam_sua_do_diff_user) or (state =='approved' and r.is_sep) :
                    affected_count +=1
                    r.state = 'draft'
            self.affected_object_qty = affected_count
        else:
            raise UserError (u'Bạn chưa chọn dòng nào')
#         return return_form_action(self)
    @api.multi
    @return_form_action_decorator
    def multi_mark_delete(self):
        active_ids = self._context.get('active_ids')
        self.choosed_object_qty = len(active_ids)
        if active_ids:
            affected_count = 0
            for r in self.env['cvi'].browse(active_ids):
                state = r.state
                if state in ['draft'] and not r.cam_sua_do_diff_user:
                    affected_count +=1
                    r.state = 'mark_delete'
            self.affected_object_qty = affected_count
        else:
            raise UserError (u'Bạn chưa chọn dòng nào')
#         return return_form_action(self)
        
#     @api.multi
#     def multi_mark_delete(self):
#         active_ids = self._context.get('active_ids')
#         if active_ids:
#             cvis = self.env['cvi'].browse(active_ids)
#             cvis.write({'state':'mark_delete'})
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')
        
        