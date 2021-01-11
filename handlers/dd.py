from tornado.escape import json_encode
from models.dd import DDModel
from handlers.base import BaseHandler


class UserHandler(BaseHandler):
    url = "https://oapi.dingtalk.com"
    appkey = 'ding27e0amfvxsepglcw'
    appsecret = '_obcQq8T_M-fCU75ARkVKxJufamykziYsJuAf5b4gi-d3xINxcqfT8srD0ZWWFPe'

    def get(self):
        code = self.get_argument('code')
        access_token = DDModel.get_access_token()
        user_info = DDModel.get_user_info(code, access_token)
        user_id = user_info['userid']
        user_detail = DDModel.get_user_detail(access_token, user_id)
        self.write(json_encode(user_detail))
