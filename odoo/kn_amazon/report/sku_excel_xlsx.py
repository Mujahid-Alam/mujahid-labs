from odoo import models


class BoxExcelXlsx(models.AbstractModel):
    _name = 'report.kn_amazon.sku_excel_report_stn'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, box):
        row = 0
        col = 0
        for obj in box:
            
            sheet = workbook.add_worksheet('SKU')
            bold = workbook.add_format({'bold': True})

            sheet.write(row, col, ' Sku', bold)
            sheet.write(row, col+1, 'Asin', bold)
            sheet.write(row, col+2, 'STN Price', bold)
            sheet.write(row, col+3, 'Demanded Qty', bold)
            sheet.write(row, col+4, 'Confirmed  Qty', bold)
            sheet.write(row, col+5, 'Amazon Received  Qty', bold)

            sku =  obj.sku_line_ids.mapped('sku_id.sku_code')
            asin =  obj.sku_line_ids.mapped('sku_id.asin')
            stn_price =  obj.sku_line_ids.mapped('stn_price')
            demanded_quantity =  obj.sku_line_ids.mapped('demanded_quantity')
            confirmed_quantity =  obj.sku_line_ids.mapped('confirmed_quantity')
            amz_received_quantity =  obj.sku_line_ids.mapped('amz_received_quantity')
        
            for i, j, k, l, m, n in zip(sku, asin, stn_price, demanded_quantity, confirmed_quantity, amz_received_quantity):
                sheet.write(row+1, col, i)
                sheet.write(row+1, col+1, j)
                sheet.write(row+1, col+2, k)
                sheet.write(row+1, col+3, l)
                sheet.write(row+1, col+4, m)
                sheet.write(row+1, col+5, n)

                row += 1

            