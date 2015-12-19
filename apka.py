import falcon

import Dijkstra
from Statics import CssLoader

api = application = falcon.API()


api.add_route('/map/{start}/{end}', Dijkstra.Dijkstra())
api.add_route('/static/{name}', CssLoader())
