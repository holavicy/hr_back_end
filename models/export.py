import json
import xlwt
from time import time
from models.user import UserModel


class ExportModel(object):

    # 花名册
    @classmethod
    def export_hmc(cls):
        total_num, df_records = UserModel.hua_ming_ce('', '')
        result_list = json.loads(df_records)

        url = cls.write_excel_chart_hmc(result_list)
        return url

    @classmethod
    def write_excel_chart_hmc(cls, data):
        try:
            book = xlwt.Workbook()  # 新建一个Excel
            sheet = book.add_sheet('导出数据')  # 创建sheet
            title = ['序号', '工号', '姓名',  '公司', '主职部门', '职等', '职级', '岗位', '岗位序列', '出生日期', '联系方式', '转正日期', '任职类型']  # 写表头

            # 循环将表头写入到sheet页
            i = 0
            for header in title:
                sheet.write(0, i, header)
                i += 1

            # 写数据
            for index, item in enumerate(data):
                sheet.write(index + 1, 0, index + 1)
                sheet.write(index + 1, 1, item['CODE'])
                sheet.write(index + 1, 2, item['NAME'])
                sheet.write(index + 1, 3, item['ORGNAME'])
                sheet.write(index + 1, 4, ','.join(item['dept_list']))
                sheet.write(index + 1, 5, item['ZHIDENG'])
                sheet.write(index + 1, 6, item['ZHIJI'])
                sheet.write(index + 1, 7, item['POSTNAME'])
                sheet.write(index + 1, 8, item['POSTSERIESNAME'])
                sheet.write(index + 1, 9, item['BIRTHDATE'])
                sheet.write(index + 1, 10, item['MOBILE'])
                sheet.write(index + 1, 11, item['ZZDATE'])
                sheet.write(index + 1, 12, item['JOBTYPENAME'])

            timestamp = str(time())
            filename = 'files/export/huamingce_ ' + timestamp + ".xls"
            book.save(filename)
            return 'export/huamingce_' + timestamp + ".xls"
        except Exception as e:
            print(e)
