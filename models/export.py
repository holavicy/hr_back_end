import json
import xlwt
import datetime
from time import time
from models.user import UserModel


class ExportModel(object):

    # 花名册
    @classmethod
    def export_hmc(cls, staff_no, name):
        total_num, df_records = UserModel.hua_ming_ce('', '', staff_no, name)
        result_list = json.loads(df_records)

        url = cls.write_excel_chart_hmc(result_list)
        return url

    @classmethod
    def write_excel_chart_hmc(cls, data):
        try:
            book = xlwt.Workbook()  # 新建一个Excel
            sheet = book.add_sheet('导出数据')  # 创建sheet
            title = ['工号', '姓名', '业务单元', '一级部门', '二级部门', '三级部门', '岗位', '籍贯', '民族', '性别',
                     '户口性质', '户口所在地', '政治面貌', '婚姻状况', '手机号码', '证件类型', '证件号码', '身份证有效期',
                     '身份证地址', '联系地址', '出生日期', '年龄', '入职集团日期', '入职母线日期', '职称等级', '职称名称',
                     '职称获取时间', '学历', '学校名称', '专业', '入校时间', '毕业时间', '集团工龄', '母线工龄',
                     '职务名称', '职务级别', '行政级别', '岗位序列', '员工状态', '是否有试用期', '试用期开始日期',
                     '试用期结束日期', '实际转正日期', '紧急联系人姓名', '紧急联系人电话']  # 写表头

            # 循环将表头写入到sheet页
            i = 0
            for header in title:
                sheet.write(0, i, header)
                i += 1

            # 写数据
            for index, item in enumerate(data):
                sheet.write(index + 1, 0, item['CODE'])
                sheet.write(index + 1, 1, item['NAME'])
                sheet.write(index + 1, 2, item['ORGNAME'])
                if len(item['dept_list']) >= 1:
                    sheet.write(index + 1, 3, item['dept_list'][0])
                else:
                    sheet.write(index + 1, 3, '')
                if len(item['dept_list']) >= 2:
                    sheet.write(index + 1, 4, item['dept_list'][1])
                else:
                    sheet.write(index + 1, 4, '')
                if len(item['dept_list']) >= 3:
                    sheet.write(index + 1, 5, item['dept_list'][2])
                else:
                    sheet.write(index + 1, 5, '')

                sheet.write(index + 1, 6, item['POSTNAME'])
                sheet.write(index + 1, 7, item['JIGUAN'])
                sheet.write(index + 1, 8, item['MINZU'])
                sheet.write(index + 1, 9, item['SEX'])

                sheet.write(index + 1, 10, item['HUKOUXINGZHI'])
                sheet.write(index + 1, 11, item['HUKOUSUOZAIDI'])
                sheet.write(index + 1, 12, item['ZHENGZHIMIANMAO'])
                sheet.write(index + 1, 13, item['HUNYINZHUANGKUANG'])
                sheet.write(index + 1, 14, item['MOBILE'])
                sheet.write(index + 1, 15, item['ZHENGJIANLEIXING'])
                sheet.write(index + 1, 16, item['ZHENGJIANHAO'])
                sheet.write(index + 1, 17, item['YOUXIAOQI'])
                sheet.write(index + 1, 18, item['CENSUSADDR'])
                sheet.write(index + 1, 19, item['GLBDEF1'])

                sheet.write(index + 1, 20, item['BIRTHDATE'])
                sheet.write(index + 1, 21, item['AGE'])
                sheet.write(index + 1, 22, item['JOINDATE'])
                sheet.write(index + 1, 23, item['MUXIANBEGINDATE'])
                sheet.write(index + 1, 24, item['ZCDENGJI'])
                sheet.write(index + 1, 25, item['ZCNAME'])
                sheet.write(index + 1, 26, item['CREATIONTIME'])
                sheet.write(index + 1, 27, item['XUELI'])
                sheet.write(index + 1, 28, item['SCHOOL'])
                sheet.write(index + 1, 29, item['MAJOR'])

                sheet.write(index + 1, 30, item['BEGINDATE'])
                sheet.write(index + 1, 31, item['ENDDATE'])
                sheet.write(index + 1, 32, item['JTAGE'])
                sheet.write(index + 1, 33, item['MXAGE'])
                sheet.write(index + 1, 34, item['ZWMC'])
                sheet.write(index + 1, 35, item['ZWJB'])
                sheet.write(index + 1, 36, item['ZHIJI'])
                sheet.write(index + 1, 37, item['POSTSERIESNAME'])
                sheet.write(index + 1, 38, item['JOBTYPENAME'])

                if item['IFPROP'] == 'Y':
                    sheet.write(index + 1, 39, '是')
                else:
                    sheet.write(index + 1, 39, '否')

                if item['JOBTYPENAME'] == '试用期员工':
                    sheet.write(index + 1, 40, item['PROBEGINDATE'])
                    sheet.write(index + 1, 41, item['PROBENDDATE'])
                else:
                    sheet.write(index + 1, 40, '')
                    sheet.write(index + 1, 41, '')

                sheet.write(index + 1, 42, item['ZZDATE'])
                sheet.write(index + 1, 43, item['LINKMAN'])
                sheet.write(index + 1, 44, item['LINKMANMOBILE'])

            now = datetime.datetime.now().strftime('%Y%m%d')
            timestamp = str(time())
            filename = 'files/export/huamingce_' + now + '_' + timestamp + ".xls"
            book.save(filename)

            return 'export/huamingce_' + now + '_' + timestamp + ".xls"
        except Exception as e:
            print(e)
