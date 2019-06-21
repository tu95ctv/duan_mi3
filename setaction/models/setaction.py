# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_


class Setaction(models.TransientModel):
    _name = "setaction.setaction"
#     @api.multi
#     def multi_approved(self):
#         active_ids = self._context.get('active_ids')
#         if active_ids:
#             cac_linh_ids = self.env.user.cac_linh_ids
#             for r in self.env['cvi'].browse(active_ids):
#                 if r.is_sep:#or r.is_admin or (cac_linh_ids and (r.create_uid == r.env.user or r.user_id == r.env.user)):
#                     r.state = 'approved'
#                 else:
#                     raise UserError (u'Bạn không phải là lãnh đạo của nhân viên tạo record này')
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')