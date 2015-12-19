import falcon
from jinja2 import FileSystemLoader, Environment



def getTemplate(name):
    templateLoader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=templateLoader)
    return env.get_template(name)

class CssLoader(object):
    def on_get(self, req, resp, name):
        print(name)
        filename = './static/' + name
        resp.stream = open(name=filename)
        resp.content_type = 'text/css'
        resp.status = falcon.HTTP_200