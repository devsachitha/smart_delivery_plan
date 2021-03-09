from flectra import fields, api, models, _
from datetime import date, datetime, timedelta
from flectra.addons import decimal_precision as dp


class NextDayDeliveryPlan(models.Model):
    _name = 'next.day.delivery.plan'

    delivery_date = fields.Date(string='Delivery Plan Date', required=True)
    delivery_lines = fields.One2many(comodel_name='next.day.delivery.lines', inverse_name='delivery_plan_id')

    @api.model
    def default_get(self, fields):
        result = super(NextDayDeliveryPlan, self).default_get(fields)
        if self.env.context.get('from_delivery'):
            result['delivery_date'] = date.today()
            active_ids = self.env.context.get('active_ids')
            if active_ids:
                delivery_lines = []
                for active_id in active_ids:
                    delivery_line_obj = self.env['sale.order.line'].search([('id', '=', active_id)])
                    value = (0, 0, {'order_id': delivery_line_obj.order_id.id,
                                    'order_date': datetime.strptime(delivery_line_obj.order_date, "%Y-%m-%d").date(),
                                    'order_partner_id': delivery_line_obj.order_partner_id.id,
                                    'product_id': delivery_line_obj.product_id.id,
                                    'product_uom_qty': delivery_line_obj.product_uom_qty,
                                    'qty_delivered': delivery_line_obj.qty_delivered,
                                    'qty_delivery_available': delivery_line_obj.qty_delivery_available,
                                    'product_uom': delivery_line_obj.product_uom.id,
                                    })

                    delivery_lines.append(value)
                result['delivery_lines'] = delivery_lines
        return result


class NextDayDeliveryLines(models.Model):
    _name = 'next.day.delivery.lines'

    priority_number = fields.Integer(string="Priority Number")
    delivery_plan_id = fields.Many2one(comodel_name='next.day.delivery.plan', string='Delivery Plan', required=True,
                                       ondelete='cascade', index=True,
                                       copy=False)

    order_date = fields.Date(string='Order Date', readonly=True)
    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True,
                               copy=False, readonly=True)

    order_partner_id = fields.Many2one(related='order_id.partner_id', store=True, string='Customer', readonly=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Product', domain=[('sale_ok', '=', True)],
                                 change_default=True, ondelete='restrict', required=True, readonly=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True,
                                   default=1.0, readonly=True)
    qty_delivered = fields.Float(string='Delivered', copy=False, digits=dp.get_precision('Product Unit of Measure'),
                                 default=0.0, readonly=True)
    qty_delivery_available = fields.Float(string='To Deliver', readonly=True, store=True,
        digits=dp.get_precision('Product Unit of Measure'))
    plan_to_deliver = fields.Integer(string='Plan to Deliver')
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)

    @api.model
    def create(self, values):
        values['qty_delivery_available'] = values['product_uom_qty'] - values['qty_delivered']
        res = super(NextDayDeliveryLines, self).create(values)
        return res
