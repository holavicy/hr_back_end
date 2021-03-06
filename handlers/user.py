import json
from tornado.escape import json_encode
from handlers.base import BaseHandler
from models.user import UserModel


class UserInfoHandler(BaseHandler):

    def get(self):
        code = self.get_argument('code')

        response = {
            'code': 0,
            'data': '',
            'errorMsg': ''
        }

        df_records = UserModel.get_user_info(code)
        data = {
            'list': json.loads(df_records)
        }
        response['data'] = data
        self.write(json_encode(response))


class OrgList(BaseHandler):
    def get(self):

        response = {
            'code': 0,
            'data': '',
            'errorMsg': ''
        }

        df_records = UserModel.get_org_list()
        data = {
            'list': json.loads(df_records)
        }
        response['data'] = data
        self.write(json_encode(response))


class GroupsList(BaseHandler):
    def get(self):

        response = {
            'code': 0,
            'data': '',
            'errorMsg': ''
        }

        df_records = UserModel.get_groups_list()
        data = {
            'list': json.loads(df_records)
        }
        response['data'] = data
        self.write(json_encode(response))


class UserListHandler(BaseHandler):

    def get(self):
        page = self.get_argument('page')
        page_size = self.get_argument('pageSize')
        staff_no = self.get_argument('staffNo')
        name = self.get_argument('name')
        get_status = self.get_argument('getStatus')
        get_year = self.get_argument('getYear')
        response = {
            'code': 0,
            'data': '',
            'errorMsg': ''
        }

        total_num, df_records = UserModel.get_user_list(page, page_size, staff_no, name, get_status, get_year)
        if isinstance(total_num, int):
            total_num = total_num
        else:
            total_num = total_num.tolist()
        data = {
            'count': total_num,
            'list': json.loads(df_records)
        }
        response['data'] = data
        self.write(json_encode(response))


class HuaMingCeHandler(BaseHandler):

    def get(self):
        page = self.get_argument('page')
        page_size = self.get_argument('pageSize')
        staff_no = self.get_argument('staffNo')
        name = self.get_argument('name')
        group_value = self.get_argument('groupValue')
        response = {
            'code': 0,
            'data': '',
            'errorMsg': ''
        }

        total_num, df_records = UserModel.hua_ming_ce(page, page_size, staff_no, name, group_value)
        if isinstance(total_num, int):
            total_num = total_num
        else:
            total_num = total_num.tolist()
        data = {
            'count': total_num,
            'list': json.loads(df_records)
        }
        response['data'] = data
        self.write(json_encode(response))
