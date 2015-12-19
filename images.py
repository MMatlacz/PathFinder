import os
import uuid

import falcon
import msgpack

ALLOWED_IMAGE_TYPES = (
    'image/gif',
    'image/jpeg',
    'image/png',
)

def validate_image_type(req, resp, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'image type not allowed. must be png, jpeg or gif'
        raise falcon.HTTPBadRequest('Bad request', msg)

def _media_type_to_exit(media_type):
    #strip off the 'image/' prefix
    return media_type[6: ]

def _ext_to_media_type(ext):
    return 'image/' + ext

def generate_id():
    return str(uuid.uuid4())

class Collection(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path


    def on_get(self, req, resp):
        resp.data = msgpack.packb('{"message": "Hello World"}')
        resp.content_type = 'application/msgpack'
        resp.status = falcon.HTTP_200

    @falcon.before(validate_image_type)
    def on_post(self, req, resp):
        image_id = generate_id()
        ext = _media_type_to_exit(req.content_type)
        filename = image_id + '.' + ext

        image_path = os.path.join(self.storage_path, filename)

        with open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(4096)
                if not chunk:
                    break
                else:
                    image_file.write(chunk)

        resp.status = falcon.HTTP_201
        resp.location = '/images/' + image_id

class Item(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_get(self, req, resp, name):
        ext = os.path.splitext(name)[1][1:]
        resp.content_type = _ext_to_media_type(ext)

        image_path = os.path.join(self.storage_path, name)
        resp.stream = open(image_path, 'rb')
        resp.stream_len = os.path.getsize(image_path)



