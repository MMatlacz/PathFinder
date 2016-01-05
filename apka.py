# -*- coding: utf-8 -*-
from wsgiref import simple_server

import falcon

import Dijkstra
import db_handler
import webpage
from Statics import StaticsLoader

app_url = '/matlaczm/MapaApi'
app = application = falcon.API()

app.add_route('/', webpage.Main())
app.add_route('/map/{start}/{finish}', Dijkstra.Dijkstra())
app.add_route('/modify/{start}/{finish}', db_handler.Modify())
app.add_route('/modify/{start}/{finish}/{distance}', db_handler.Modify())
app.add_route('/static/{name}', StaticsLoader())
app.add_route('/cities', db_handler.Search())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 9999, app)
    httpd.serve_forever()