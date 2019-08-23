# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_round, float_is_zero

class StockMove(models.Model):
    _inherit = ['stock.move']
    ghi_chu = fields.Char()
    
#     def _quantity_done_set(self):
#         quantity_done = self[0].quantity_done  # any call to create will invalidate `move.quantity_done`
#         for move in self:
#             move_lines = move._get_move_lines()
#             if not move_lines:
#                 if quantity_done:
#                     # do not impact reservation here
#                     vals = dict(move._prepare_move_line_vals(), qty_done=quantity_done, ghi_chu='duoc tao tu _quantity_done_setƯ')
#                     move_line = self.env['stock.move.line'].create(vals)
#                     move.write({'move_line_ids': [(4, move_line.id)]})
#             elif len(move_lines) == 1:
#                 move_lines[0].qty_done = quantity_done
#             else:
#                 raise UserError("Cannot set the done quantity from this stock move, work directly with the move lines.")

#     def _action_cancel(self):
#         print( '**** _action_cancel: self 3',self)
#         rs = super(StockMove, self)._action_cancel()
#         return rs
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if 'search_move_line_in_write' in self._context:# de lam gì?
            return False
        return super(StockMove,self).search(args, offset, limit, order, count=count)
# 
#     def _action_confirm(self, merge=True, merge_into=False):
#         """ Confirms stock move or put it in waiting if it's linked to another move.
#         :param: merge: According to this boolean, a newly confirmed move will be merged
#         in another move of the same picking sharing its characteristics.
#         """
#         move_create_proc = self.env['stock.move']
#         move_to_confirm = self.env['stock.move']
#         move_waiting = self.env['stock.move']
# 
#         to_assign = {}
#         for move in self:
#             # if the move is preceeded, then it's waiting (if preceeding move is done, then action_assign has been called already and its state is already available)
#             if move.move_orig_ids:
#                 move_waiting |= move
#             else:
#                 if move.procure_method == 'make_to_order':
#                     move_create_proc |= move
#                 else:
#                     move_to_confirm |= move
#             if not move.picking_id and move.picking_type_id:
#                 key = (move.group_id.id, move.location_id.id, move.location_dest_id.id)
#                 if key not in to_assign:
#                     to_assign[key] = self.env['stock.move']
#                 to_assign[key] |= move
# 
#         # create procurements for make to order moves
#         for move in move_create_proc:
#             values = move._prepare_procurement_values()
#             origin = (move.group_id and move.group_id.name or (move.rule_id and move.rule_id.name or move.origin or move.picking_id.name or "/"))
#             self.env['procurement.group'].run(move.product_id, move.product_uom_qty, move.product_uom, move.location_id, move.rule_id and move.rule_id.name or "/", origin,
#                                               values)
# 
#         move_to_confirm.write({'state': 'confirmed'})
#         (move_waiting | move_create_proc).write({'state': 'waiting'})
# 
#         # assign picking in batch for all confirmed move that share the same details
#         for moves in to_assign.values():
#             moves._assign_picking()
#         self._push_apply()
# #         if merge:
# #             return self._merge_moves()
#         return self
#     
#     def _create_extra_move(self):
#         """ If the quantity done on a move exceeds its quantity todo, this method will create an
#         extra move attached to a (potentially split) move line. If the previous condition is not
#         met, it'll return an empty recordset.
#             
#         The rationale for the creation of an extra move is the application of a potential push
#         rule that will handle the extra quantities.
#         """
#         extra_move = self
#         rounding = self.product_uom.rounding
#         # moves created after the picking is assigned do not have `product_uom_qty`, but we shouldn't create extra moves for them
# #         raise UserError(u'self.quantity_done, self.product_uom_qty %s-%s'%(self.quantity_done, self.product_uom_qty))
#         if float_compare(self.quantity_done, self.product_uom_qty, precision_rounding=rounding) > 0:
# #             raise UserError(u'self.quantity_done, self.product_uom_qty %s-%s'%(self.quantity_done, self.product_uom_qty))
#             # create the extra moves
#             extra_move_quantity = float_round(
#                 self.quantity_done - self.product_uom_qty,
#                 precision_rounding=rounding,
#                 rounding_method='HALF-UP')
#             extra_move_vals = self._prepare_extra_move_vals(extra_move_quantity)
#             extra_move = self.copy(default=extra_move_vals)
#             if extra_move.picking_id:
#                 extra_move = extra_move._action_confirm(merge_into=self)
#             else:
#                 extra_move = extra_move._action_confirm()
#     
#             # link it to some move lines. We don't need to do it for move since they should be merged.
#             if self.exists() and not self.picking_id:
#                 for move_line in self.move_line_ids.filtered(lambda ml: ml.qty_done):
#                     if float_compare(move_line.qty_done, extra_move_quantity, precision_rounding=rounding) <= 0:
#                         # move this move line to our extra move
#                         move_line.move_id = extra_move.id
#                         extra_move_quantity -= move_line.qty_done
#                     else:
#                         # split this move line and assign the new part to our extra move
#                         quantity_split = float_round(
#                             move_line.qty_done - extra_move_quantity,
#                             precision_rounding=self.product_uom.rounding,
#                             rounding_method='UP')
#                         move_line.qty_done = quantity_split
#                         move_line.copy(default={'move_id': extra_move.id, 'qty_done': extra_move_quantity, 'product_uom_qty': 0})
#                         extra_move_quantity -= extra_move_quantity
#                     if extra_move_quantity == 0.0:
#                         break
#         return extra_move
    
#     def _action_confirm(self, merge=True, merge_into=False):
#         print ('***_action_confirm self2', self)
# #         pass
#         rs = super(StockMove, self)._action_confirm(merge=merge, merge_into=merge_into)
# #         raise UserError('kakak hehehe')
#         return rs
            
   
#     def _create_extra_move(self):
#         extra_move = super(StockMove, self)._create_extra_move()
#         print ('************extra_move', extra_move)
# #         raise ValueError('extra_move %s'%extra_move)
#         return extra_move
    
   
    
    
    
    
    
    

    
    
#     def _action_done(self):
#         print ('***_action_done')
#         return super(StockMove, self.with_context(stt=self.stt))._action_done()
    
#     def choose_ghi_chu(self):
#         if  len(self.move_line_ids)==1:
#             
#         notempty_ghi_chu_in_ml_ids = set(self.move_line_ids.filtered(lambda r: r.ghi_chu).mapped('ghi_chu'))
#         if not notempty_ghi_chu_in_ml_ids:
#             merge = True
#             ghi_chu = self.ghi_chu
#         else:
#             merge = False
#             ghi_chu = ml.ghi_chu or self.ghi_chu
#             if len(notempty_ghi_chu_in_ml_ids) ==1:
#                 merge = True
                
    
#     def ghi_chu_theo_move_line_ids_(self):
#         rs= True if self.move_line_ids.filtered(lambda r:bool(r.ghi_chu)) else False
# #         print (self.product_id.name,rs, self.move_line_ids.mapped('ghi_chu'))
#         return rs
#     def colspan_(self,has_serial_number):
#         print ('has_serial_number***',has_serial_number)
#         has_serial_number = 3 if has_serial_number else 1 # co tinh trang
#         ghi_chu_move_lines_ids = self.ghi_chu_theo_move_line_ids_()
#         ghi_chu_move_lines_ids = 1 if ghi_chu_move_lines_ids else 0
#         val = ghi_chu_move_lines_ids + has_serial_number
#         print (self.product_id.name,'val********',val,has_serial_number,ghi_chu_move_lines_ids)
#         return val
        
#     def action_show_details(self):
#         """ Returns an action that will open a form view (in a popup) allowing to work on all the
#         move lines of a particular move. This form view is used when "show operations" is not
#         checked on the picking type.
#         """
#         self.ensure_one()
# 
#         # If "show suggestions" is not checked on the picking type, we have to filter out the
#         # reserved move lines. We do this by displaying `move_line_nosuggest_ids`. We use
#         # different views to display one field or another so that the webclient doesn't have to
#         # fetch both.
#         if self.picking_id.picking_type_id.show_reserved:
#             view = self.env.ref('stock.view_stock_move_operations')
#         else:
#             view = self.env.ref('stock.view_stock_move_nosuggest_operations')
#         show_lots_m2o=self.has_tracking != 'none' and (self.picking_type_id.use_existing_lots or self.state == 'done' or self.origin_returned_move_id.id),  # able to create lots, whatever the value of ` use_create_lots`.
#         print ("self.has_tracking != 'none' ",self.has_tracking != 'none' )
#         print ("self.picking_type_id.use_existing_lots",self.picking_type_id.use_existing_lots)
#         print ("self.origin_returned_move_id.id",self.origin_returned_move_id.id)
#         print ('show_lots_m2o',show_lots_m2o)
#         return {
#             'name': _('Detailed Operations'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'stock.move',
#             'views': [(view.id, 'form')],
#             'view_id': view.id,
#             'target': 'new',
#             'res_id': self.id,
#             'context': dict(
#                 self.env.context,
#                 show_lots_m2o=self.has_tracking != 'none' and (self.picking_type_id.use_existing_lots or self.state == 'done' or self.origin_returned_move_id.id),  # able to create lots, whatever the value of ` use_create_lots`.
#                 show_lots_text=self.has_tracking != 'none' and self.picking_type_id.use_create_lots and not self.picking_type_id.use_existing_lots and self.state != 'done' and not self.origin_returned_move_id.id,
#                 show_source_location=self.location_id.child_ids,
#                 show_destination_location=self.location_dest_id.child_ids,
#                 show_package=not self.location_id.usage == 'supplier',
#                 show_reserved_quantity=self.state != 'done'
#             ),
#         }
        
        
    
#     def _action_cancel(self):
#         if any(move.state == 'done' for move in self):
#             raise UserError(_('You cannot cancel a stock move that has been set to \'Done\'.'))
#         for move in self:
#             if move.state == 'cancel':
#                 continue
# #             move._do_unreserve()
#             siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
#             if move.propagate:
#                 # only cancel the next move if all my siblings are also cancelled
#                 if all(state == 'cancel' for state in siblings_states):
#                     move.move_dest_ids._action_cancel()
#             else:
#                 if all(state in ('done', 'cancel') for state in siblings_states):
#                     move.move_dest_ids.write({'procure_method': 'make_to_stock'})
#                     move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
#         self.write({'state': 'cancel', 'move_orig_ids': [(5, 0, 0)]})
#         return True
        
        

#     def _unreserve_initial_demand(self, new_move):
#         print ('***_unreserve_initial_demand ')
# #         super(StockMove, self)._unreserve_initial_demand(new_move)
#         pass

#     def _create_extra_move(self):
#         extra_move = super(StockMove, self)._create_extra_move()
#         print ('************extra_move', extra_move)
#         return extra_move
    @api.multi
    def _action_done(self):
#         print ('********kakakak111111')
#         print('***self 1',self)
#         moves_todo = super(StockMove, self)._action_done()
#         return moves_todo
        
        self.filtered(lambda move: move.state == 'draft')._action_confirm()  # MRP allows scrapping draft moves
        moves = self.exists().filtered(lambda x: x.state not in ('done', 'cancel'))
        moves_todo = self.env['stock.move']#moves#

        # Cancel moves where necessary ; we should do it before creating the extra moves because
        # this operation could trigger a merge of moves.
        for move in moves:
            if move.quantity_done <= 0:
                if float_compare(move.product_uom_qty, 0.0, precision_rounding=move.product_uom.rounding) == 0:
                    move._action_cancel()

        # Create extra moves where necessary
        for move in moves:
            if move.state == 'cancel' or move.quantity_done <= 0:
                continue
            # extra move will not be merged in mrp
            if not move.picking_id:
                moves_todo |= move
            moves_todo |= move._create_extra_move()
        print ('****************moves_todo 1',moves, moves_todo)
        # Split moves where necessary and move quants
        for move in moves_todo:
            print ('****************moves_todo 2',moves, moves_todo)
            # To know whether we need to create a backorder or not, round to the general product's
            # decimal precision and not the product's UOM.
            rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            if float_compare(move.quantity_done, move.product_uom_qty, precision_digits=rounding) < 0:
                # Need to do some kind of conversion here
                qty_split = move.product_uom._compute_quantity(move.product_uom_qty - move.quantity_done, move.product_id.uom_id, rounding_method='HALF-UP')
                new_move = move._split(qty_split)
                for move_line in move.move_line_ids:
                    if move_line.product_qty and move_line.qty_done:
                        # FIXME: there will be an issue if the move was partially available
                        # By decreasing `product_qty`, we free the reservation.
                        # FIXME: if qty_done > product_qty, this could raise if nothing is in stock
                        try:
                            move_line.write({'product_uom_qty': move_line.qty_done})
                        except UserError:
                            pass
                move._unreserve_initial_demand(new_move)
            move.move_line_ids._action_done()
        # Check the consistency of the result packages; there should be an unique location across
        # the contained quants.
        for result_package in moves_todo\
                .mapped('move_line_ids.result_package_id')\
                .filtered(lambda p: p.quant_ids and len(p.quant_ids) > 1):
            if len(result_package.quant_ids.mapped('location_id')) > 1:
                raise UserError(_('You should not put the contents of a package in different locations.'))
        picking = moves_todo and moves_todo[0].picking_id or False
        moves_todo.write({'state': 'done', 'date': fields.Datetime.now()})
        moves_todo.mapped('move_dest_ids')._action_assign()

        # We don't want to create back order for scrap moves
        # Replace by a kwarg in master
        if self.env.context.get('is_scrap'):
            return moves_todo

        if picking:
            picking._create_backorder()

        return moves_todo
    

#     

#     
