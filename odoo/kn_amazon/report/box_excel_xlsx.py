from odoo import models
from itertools import zip_longest

class BoxExcelXlsx(models.AbstractModel):
    _name = 'report.kn_amazon.box_excel_report_stn'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, box):
        row = 0
        col = 0
        for obj in box:
            sheet = workbook.add_worksheet('BoxesQ')
            bold = workbook.add_format({'bold': True})

            sheet.write(row, col, 'Package', bold)
            sheet.write(row, col+1, 'Location', bold)
            sheet.write(row, col+2, 'Box Number', bold)
            sheet.write(row, col+3, 'Weight(kg)', bold)
            sheet.write(row, col+4, 'Length(cm)', bold)
            sheet.write(row, col+5, 'Width (cm)', bold)
            sheet.write(row, col+6, 'Height (cm)', bold)
            sheet.write(row, col+7, 'Confirmed Qty', bold)

            package =  obj.box_ids.mapped('package_id.name')
            location =  obj.box_ids.mapped('package_id.location_id.name')
            box_num =  obj.box_ids.mapped('box_num')
            weight =  obj.box_ids.mapped('weight')
            length =  obj.box_ids.mapped('length')
            width =  obj.box_ids.mapped('width')
            height =  obj.box_ids.mapped('height')
            conf_qty =  obj.box_ids.mapped('confirmed_qty')
            
            for i,j,k,l,m,n,o,p in zip_longest(package,location,box_num,weight,length,width,height,conf_qty):
                sheet.write(row+1, col, i)
                sheet.write(row+1, col+1, j)
                sheet.write(row+1, col+2, k)
                sheet.write(row+1, col+3, l)
                sheet.write(row+1, col+4, m)
                sheet.write(row+1, col+5, n)
                sheet.write(row+1, col+6, o)
                sheet.write(row+1, col+7, p)
                row += 1

            