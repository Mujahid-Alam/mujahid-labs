from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
import pandas as pd
from odoo.tools.mimetypes import guess_mimetype
import base64

import datetime
import time
from pytz import timezone

_logger = logging.getLogger(__name__)


class Import(models.TransientModel):
    _inherit = 'base_import.import'

    def parse_preview(self, options, count=10):
        if self.res_model == 'hr.attendance':
            dict_of_file_type = {
                'text/csv': 'csv',
                'application/vnd.ms-excel': 'xls',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
            }
            mimetype = guess_mimetype(self.file or b'')
            file_extension = dict_of_file_type.get(mimetype)
            if file_extension not in ['csv', 'xls', 'xlsx']:
                raise ValidationError('File type not supported')
            else:
                if file_extension == 'csv':
                    df = pd.read_csv(self.file, dtype=str)
                else:
                    df = pd.read_excel(self.file, dtype=str)
                cols = df.columns
                should_process = True
                if len(cols) == 3:
                    for col in cols:
                        if col not in ['date_time', 'emp_batch_num', 'in_out']:
                            should_process = False
                else:
                    should_process = False
                if should_process:
                    def _check_col_in_out(df):
                        list_of_values = df['in_out'].unique().tolist()
                        for value in list_of_values:
                            if value.lower() not in ['in', 'out']:
                                raise ValidationError(
                                    'Invalid value for in_out column: %s' % value)

                    def _check_row_is_valid(df):
                        list_of_employee_ids = df['employee_id'].unique(
                        ).tolist()
                        for employee_id in list_of_employee_ids:
                            df_for_employee_id = df[df['employee_id'] == employee_id].reset_index(
                                drop=True)
                            att_count = df_for_employee_id.shape[0]
                            if att_count <= 2:
                                att_count_in_db = self.env['hr.attendance'].search_count(
                                    [('employee_id', '=', employee_id), ('check_out', '=', False)])
                                if att_count_in_db > 1:
                                    raise ValidationError(
                                        'More than one active attendance(s) already exists for employee: %s' % employee_id)
                                if att_count == 2 or (att_count == 1 and df_for_employee_id['in_out'][0].lower() == 'in'):
                                    # check if all other attendance entries have both check_in and check_out values
                                    if att_count_in_db > 0:
                                        raise ValidationError(
                                            'Active attendance already exists for employee: %s' % employee_id)
                                elif att_count == 1:
                                    if att_count_in_db == 0:
                                        raise ValidationError(
                                            'No active attendance exists for employee: %s' % employee_id)
                            else:
                                raise ValidationError(
                                    'Attendance count cannot be more than 2 for import via badge ids. Error in: %s' % employee_id)

                    def add_employee_ids(row):
                        emp = self.env['hr.employee'].search(
                            [('barcode', '=', row['emp_batch_num'])])
                        if emp:
                            row['employee_id'] = emp.name
                            return row
                        else:
                            raise ValidationError(
                                'Employee not found with batch number: %s' % row['emp_batch_num'])
                    df = df.apply(add_employee_ids, axis=1)
                    df['date_time'] = pd.to_datetime(df['date_time'])
                    _check_col_in_out(df)
                    _check_row_is_valid(df)
                    list_of_dict = []
                    list_of_employee_ids = df['employee_id'].unique().tolist()
                    for employee_id in list_of_employee_ids:
                        df_for_employee_id = df[df['employee_id'] == employee_id].reset_index(
                            drop=True)
                        att_count = df_for_employee_id.shape[0]
                        dict_to_append = {}
                        if att_count == 2:
                            dict_to_append['id'] = ''
                            dict_to_append['check_in'] = df_for_employee_id[df_for_employee_id['in_out'].str.lower() == 'in'].reset_index(drop=True)[
                                'date_time'][0]
                            dict_to_append['check_out'] = df_for_employee_id[df_for_employee_id['in_out'].str.lower() == 'out'].reset_index(drop=True)[
                                'date_time'][0]
                        elif att_count == 1:
                            if df_for_employee_id['in_out'][0].lower() == 'in':
                                dict_to_append['id'] = ''
                                dict_to_append['check_in'] = df_for_employee_id['date_time'][0]
                                dict_to_append['check_out'] = ''
                            else:
                                att_id = self.env['hr.attendance'].search(
                                    [('employee_id', '=', employee_id), ('check_out', '=', False)]).ensure_one()
                                dict_to_append['id'] = att_id.export_data(
                                    ['id']).get('datas')[0][0]
                                dict_to_append['check_in'] = att_id.check_in.astimezone(
                                    timezone(self.env.context.get('tz'))).strftime('%Y-%m-%d %H:%M:%S')
                                dict_to_append['check_out'] = df_for_employee_id['date_time'][0]
                        dict_to_append['employee_id'] = employee_id
                        list_of_dict.append(dict_to_append)
                    df = pd.DataFrame(list_of_dict)
                    file_path = '/var/tmp/' + self.file_name
                    if file_extension == 'csv':
                        df.to_csv(file_path, index=False)
                    else:
                        df.to_excel(file_path, index=False)
                    self.file = open(file_path, "rb").read()
                    # if file_extension == 'csv':
                    #     df = pd.read_csv(self.file, dtype=str)
                    # else:
                    #     df = pd.read_excel(self.file, dtype=str)
                    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                    #     _logger.info(df)
        res = super(Import, self).parse_preview(options, count)
        return res
