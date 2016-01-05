import falcon

from Statics import getTemplate


class Main(object):
    def on_get(self, req, resp):
        resp.body = getTemplate('main.html').render()
        resp.content_type = 'text/html'
        resp.status = falcon.HTTP_200