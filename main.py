import tornado

class Raijin(tornado.web.Application):
    pass


class SubmitJobHandler(tornado.web.RequestHandler):
    def post(self):
        print('hello world')


if __name__ == "__main__":
    app = Raijin([(r"/", SubmitJobHandler)])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
