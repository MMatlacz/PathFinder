# -*- coding: utf-8 -*-
from wsgiref import simple_server

import falcon

import db_handler
import path_computing_logic
from Statics import StaticsLoader

app_url = '/matlaczm/MapaApi'
app = application = falcon.API()

app.add_route('/path/{start}/{finish}', path_computing_logic.Path())
app.add_route('/path/{start}/{finish}/{distance}', path_computing_logic.Path())
app.add_route('/static/{name}', StaticsLoader())
app.add_route('/cities', db_handler.Search())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 9999, app)
    httpd.serve_forever()
