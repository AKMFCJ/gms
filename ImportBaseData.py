# -*- coding:utf-8 -*-
__author__ = 'changjie.fan'

"""
导入基础数据库
"""

# -*- coding:utf-8 -*-
__author__ = 'changjie.fan'

"""Excel文件读写操作"""
import os
import sys
from datetime import datetime

import pyexcel as pe
import pyexcel.ext.xlsx
import pyexcel.ext.xls
import xlwt
import xlrd

from DBOption import DBOption


def db_connect():

    db_url = {'host': '118.192.160.233', 'db_name': 'wmt', 'username': 'root', 'password': 'gms'}
    db_option = DBOption(db_url, 'mysql')
    db_option.db_connect()
    return db_option


class ExcelOptions:
    def __init__(self, file_path):
        self.file_path = file_path

    def import_wording(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        records = pe.get_records(file_name=self.file_path)
        result = []

        db_option = db_connect()
        # 已存在的语言
        language_sql = 'SELECT id, abbreviation FROM wmt_language'
        exists_language = [(tmp[0], tmp[1]) for tmp in db_option.fetch_all(language_sql)]
        exists_wording = []
        for record in records:
            if record['Relative Path'].strip() and record['Relative Path'].strip().endswith('.xml'):
                relative_path = record['Relative Path'].replace('\\', '/')
                if relative_path.find('/frameworks/') > 0:
                    path = relative_path.split('/frameworks/')[1]
                elif relative_path.find('/packages/') > 0:
                    path = relative_path.split('/packages/')[1]

                abs_path = os.path.join(path, record['name'])

                # 不添加重复字串
                if abs_path in exists_wording:
                    continue
                name = record['name']
                description = record['Description']
                sub_description = record['Sub-Description']
                whole_string = record['Whole String']
                size = len(whole_string)

                # 新增字符串
                insert_wording = 'INSERT INTO wording(abs_path, path, name, description, sub_description, ' \
                                 'whole_string, size) VALUES (%s,%s,%s,%s,%s,%s,%s)'

                db_option.insert_all(insert_wording, [(abs_path, path, name, description, sub_description,
                                                       whole_string, size)])
                # 新增客户字串
                wording_sql = 'SELECT id FROM wording WHERE abs_path="%s"' % abs_path
                wording_id = db_option.fetch_one(wording_sql)[0]
                insert_customer_wording = 'INSERT INTO customer_wording(wording_id, customer_id, status) ' \
                                          'VALUES(%s, %s, 1)' % (wording_id, 2)
                db_option.insert_one(insert_customer_wording)

                customer_wording_sql = 'SELECT id FROM customer_wording WHERE wording_id=%s AND customer_id=2' % wording_id
                customer_wording_id = db_option.fetch_one(customer_wording_sql)[0]

                # 添加各语言的值
                for language_id, language in exists_language:
                    translated_value = record.get(language, '').strip()
                    if translated_value:
                        insert_customer_wording_value = \
                            'INSERT INTO customer_wording_language_value (customer_wording_id, translated_value, ' \
                            'size, translated_time, language_id) VALUES (%s, %s, %s, %s, %s)'
                        db_option.insert_all(insert_customer_wording_value, [(customer_wording_id, translated_value,
                                                                              len(translated_value), now, language_id)])
                exists_wording.append(abs_path)


def import_language(excel_path):

    db_option = db_connect()
    # 已存在的语言
    language_sql = 'SELECT abbreviation FROM wmt_language'
    exists_language = [tmp[0] for tmp in db_option.fetch_all(language_sql)]

    # 读取Excel中语言
    wb = xlrd.open_workbook(excel_path)
    sheet = wb.sheet_by_index(0)
    ncols = sheet.ncols
    language_data = []
    for col in range(5, ncols):
        if sheet.cell(0, col).value != '' and sheet.cell(1, col).value not in exists_language:
            exists = False
            for language in language_data:
                if language[1] == sheet.cell(1, col).value:
                    exists = True
            if not exists:
                language_data.append((sheet.cell(0, col).value, sheet.cell(1, col).value))

    # 新增语言
    if language_data:
        insert_sql = 'INSERT INTO wmt_language (name, abbreviation) VALUES(%s, %s)'
        db_option.insert_all(insert_sql, language_data)
    db_option.close()

if __name__ == '__main__':
    # import_language(sys.argv[1])
    excel_option = ExcelOptions(sys.argv[1])
    excel_option.import_wording()

