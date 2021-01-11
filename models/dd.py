import pymssql
import requests
import urllib.parse
import hashlib
import time
import pandas as pd
from common.tool import TaskErr, get_now


class DDModel(object):

    url = "https://oapi.dingtalk.com"
    appKey = 'ding27e0amfvxsepglcw'
    appSecret = '_obcQq8T_M-fCU75ARkVKxJufamykziYsJuAf5b4gi-d3xINxcqfT8srD0ZWWFPe'
    agent_id = '1051673121'
    CorpId = 'dingcd0f5a2514db343b35c2f4657eb6378f'

    conn_ss = pymssql.connect(host='192.168.40.229:1433', port=3306, user='serverapp', password='wetown2020',
                              database='DingDB')

    '''
    获取access_token
    params: appKey, appSecret
    '''
    @classmethod
    def get_access_token(cls):
        response = requests.get(
            url=cls.url + "/gettoken",
            params=dict(appkey=cls.appKey, appsecret=cls.appSecret)
        )
        access_token = response.json()["access_token"]
        return access_token

    '''
    获取用户基本信息
    params: code, access_token
    '''
    @classmethod
    def get_user_info(cls, code, access_token):
        response = requests.get(
            url=cls.url + "/user/getuserinfo",
            params=dict(access_token=access_token, code=code)
        )
        response = response.json()
        if response.get('errcode') != 0:
            raise TaskErr(1, response)
        return response

    '''
    获取用户详细信息
    :param: access_token, userid
    '''
    @classmethod
    def get_user_detail(cls, access_token, user_id):
        response = requests.get(
            url=cls.url + "/user/get",
            params=dict(access_token=access_token, userid=user_id)
        )

        response = response.json()
        return response
