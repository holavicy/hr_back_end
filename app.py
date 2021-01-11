import tornado.web
import tornado.httpserver
import tornado.ioloop
import logging
import time
from handlers import user as user_handlers
from handlers import export as export_handlers

HANDLERS = [
    (r"/api/huaMingCe", user_handlers.HuaMingCeHandler),
    # 报表相关
    (r"/api/exportHuaMingCe", export_handlers.ExportHMCHandler),
]
logging.basicConfig(filename=f"./log/web.{time.strftime('%Y_%m_%d')}.txt",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run():
    app = tornado.web.Application(
        HANDLERS
    )
    http_server = tornado.httpserver.HTTPServer(app)
    port = 8083
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()
