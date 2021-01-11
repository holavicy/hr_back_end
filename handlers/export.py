from tornado.escape import json_encode
from handlers.base import BaseHandler
from models.export import ExportModel


class ExportGoodsHandler(BaseHandler):

    def get(self):
        response = {
            'code': 0,
            'data': '',
            'errorMsg': ''
        }

        goods_name = self.get_argument('goodsName')
        goods_status = self.get_argument('goodsStatus')

        url = ExportModel.export_goods(goods_name, goods_status)
        data = {
            'url': url
        }
        response['data'] = data
        self.write(json_encode(response))


class ExportHMCHandler(BaseHandler):

    def get(self):

        response = {
            'code': 0,
            'data': '',
            'errorMsg': ''
        }

        staff_no = self.get_argument('staffNo')
        name = self.get_argument('name')
        get_year = self.get_argument('getYear')

        url = ExportModel.export_hmc()
        data = {
            'url': url
        }
        response['data'] = data
        self.write(json_encode(response))