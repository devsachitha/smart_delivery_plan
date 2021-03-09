from flectra import fields, api, models, _


class NextDayDeliveryReportXls(models.AbstractModel):
    _name = 'report.smart_delivery_plan.report_next_day_delivery_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        title_format = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        table_header_style = workbook.add_format({'font_size': 11, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Nexy Day Delivery Plan')
               
        # Column headers
        sheet.merge_range('A4:A4', 'Pr.Num', table_header_style)
        sheet.merge_range('B4:B4', 'Or.Date', table_header_style)
        sheet.merge_range('C4:D4', 'Order Number', table_header_style)
        sheet.merge_range('E4:F4', 'Product', table_header_style)
        sheet.merge_range('G4:I4', 'Customer', table_header_style)
        sheet.merge_range('J4:J4', 'Or.QTY', table_header_style)
        sheet.merge_range('K4:K4', 'Del.QTY', table_header_style)
        sheet.merge_range('L4:L4', 'To Delivered', table_header_style)
        sheet.merge_range('M4:M4', 'Planing to Deliver', table_header_style)

        for line in lines:
            # Title of the report
            sheet.merge_range('A2:G3', 'Delivery Plan For ' + ' '+ line.delivery_date, title_format)
            
            if line.delivery_lines:
                row_number = 5
                for delivery_line in line.delivery_lines:
                    sheet.merge_range(row_number, row_number, 0, 0, delivery_line.priority_number, table_header_style)
                    sheet.merge_range(row_number, row_number, 1, 1, delivery_line.order_date, table_header_style)
                    sheet.merge_range(row_number, row_number, 2, 3, delivery_line.order_id.name, table_header_style)
                    sheet.merge_range(row_number, row_number, 4, 5, delivery_line.product_id.name, table_header_style)
                    sheet.merge_range(row_number, row_number, 6, 8, delivery_line.order_partner_id.name, table_header_style)
                    sheet.merge_range(row_number, row_number, 9, 9, delivery_line.product_uom_qty, table_header_style)
                    sheet.merge_range(row_number, row_number, 10, 10, delivery_line.qty_delivered, table_header_style)
                    sheet.merge_range(row_number, row_number, 11, 11, delivery_line.qty_delivery_available, table_header_style)
                    sheet.merge_range(row_number, row_number, 12, 12, delivery_line.plan_to_deliver, table_header_style)

                    row_number += 1
        
        
