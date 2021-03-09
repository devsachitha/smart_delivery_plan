from flectra import fields, api, models, _
from datetime import date,datetime,timedelta
from flectra.addons import decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def write(self, vals):
        if vals.get('confirmation_date'):
            if vals['confirmation_date']:
                if self.order_line:
                    for record in self.order_line:
                        obj = self.env['sale.order.line'].search([('id', '=', record.id)])
                        obj.write({'order_date': datetime.now()})
        res = super(SaleOrder, self).write(vals)
        return res


class PendingDeliveryPlan(models.Model):

    _inherit = 'sale.order.line'

    qty_delivery_available = fields.Float(
        compute='_get_available_qty', string='To Deliver', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    order_date = fields.Date(string ='Order Date')

    @api.depends('qty_delivered')
    def _get_available_qty(self):
        """
        Compute the quantity to be delivered. .
        """
        for line in self:
            if line.product_uom_qty:
                line.qty_delivery_available = line.product_uom_qty - line.qty_delivered


