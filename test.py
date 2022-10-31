import logging
import gspread
from gspread import Spreadsheet
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive']

def get_creds(scope = scope, path = 'E:\st-web\Assets\credentials_sheet.json'):
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    return gspread.authorize(creds)

def open_google_spreadsheet(spreadsheet_id: str) -> Spreadsheet:
    """Open sheet using gspread.
    :param spreadsheet_id: Grab spreadsheet id from URL to open. Like *1jMU5gNxEymrJd-gezJFPv3dQCvjwJs7QcaB-YyN_BD4*.
    """
    client = get_creds(scope = ['https://spreadsheets.google.com/feeds'])
    return client.open_by_key(spreadsheet_id)

"""
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
'__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
'__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_add_dimension_group',
'_auto_resize', '_delete_dimension_group', '_finder', '_get_sheet_property', '_hide_dimension', '_list_cells', '_properties',
'_set_hidden_flag', '_unhide_dimension', 'acell', 'add_cols', 'add_dimension_group_columns', 'add_dimension_group_rows',
'add_protected_range', 'add_rows', 'append_row', 'append_rows', 'batch_clear', 'batch_format', 'batch_get', 'batch_update',
'cell', 'clear', 'clear_basic_filter', 'clear_note', 'client', 'col_count', 'col_values', 'columns_auto_resize', 'copy_to',
'define_named_range', 'delete_columns', 'delete_dimension', 'delete_dimension_group_columns', 'delete_dimension_group_rows',
'delete_named_range', 'delete_protected_range', 'delete_row', 'delete_rows', 'duplicate', 'export', 'find', 'findall', 'format',
'freeze', 'frozen_col_count', 'frozen_row_count', 'get', 'get_all_cells', 'get_all_records', 'get_all_values', 'get_note',
'get_values', 'hide', 'hide_columns', 'hide_rows', 'id', 'index', 'insert_cols', 'insert_note', 'insert_row', 'insert_rows',
'list_dimension_group_columns', 'list_dimension_group_rows', 'merge_cells', 'range', 'resize', 'row_count', 'row_values',
'rows_auto_resize', 'set_basic_filter', 'show', 'sort', 'spreadsheet', 'tab_color', 'title', 'unhide_columns', 'unhide_rows',
'unmerge_cells', 'update', 'update_acell', 'update_cell', 'update_cells', 'update_index', 'update_note', 'update_tab_color',
'update_title', 'updated', 'url']
"""
spreadsheet = open_google_spreadsheet('1rS51rM-NWMHfaC5JRqf5QZPr4epCXqlmWkD3hnpCJCQ')
sheets = spreadsheet.worksheets()

import pandas as pd
import numpy as np

sheet1 = sheets[0]
name = sheet1.col_values(1)[2:]
price = sheet1.col_values(2)[2:]
remain = sheet1.col_values(6)[2:]

df = pd.DataFrame(np.array([price, remain]).T, index = name)
df = df.drop(index = '')
df.columns = ['Giá tiền', 'Thừa/Thiếu']
print(df.head(50))
print(df.shape)

# row = sheet.row_values(3)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column
# cell = sheet.cell(1,2).value  # Get the value of a specific cell

# insertRow = ["hello", 5, "red", "blue"]
# sheet.add_rows(insertRow, 4)  # Insert the list as a row at index 4

# sheet.update_cell(2,2, "CHANGED")  # Update one cell

# numRows = sheet.row_count  # Get the number of rows in the sheet


