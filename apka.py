# -*- coding: utf-8 -*-
from wsgiref import simple_server

import falcon

import db_handler
import path_computing_logic

#app_url needs to be changed if using uwsgi
app_url = ''
app = application = falcon.API()

app.add_route(app_url + '/path/{start}/{finish}', path_computing_logic.Path())
app.add_route(app_url + '/path/{start}/{finish}/{distance}', path_computing_logic.Path())
app.add_route(app_url + '/cities', db_handler.Search())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 9999, app)
    httpd.serve_forever()
