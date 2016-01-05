# -*- coding: utf-8 -*-
import falcon
from jinja2 import FileSystemLoader, Environment



def getTemplate(name):
    templateLoader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=templateLoader)
    return env.get_template(name)

class StaticsLoader(object):
    def on_get(self, req, resp, name):
        filename = './static/' + name
        resp.stream = open(name=filename)
        content_type = name.split(".")[1]
        if content_type == "js":
            content_type = "text/javascript"
        elif content_type == "css":
            content_type = "text/css"
        resp.content_type = content_type
        resp.status = falcon.HTTP_200