import json
import os
from flask import Flask
from flask import Response
from flask import request
import models
from xwot.util.vocab import Hydra
from xwot.util.vocab import Owl
from xwot.util.flask import hydra_link
from xwot.util import local_ip
from xwot.util import serializer
from xwot.util import create_description
from xwot.util import pretty_json
from xwot.util import dir_path

from xwot.util.flask import mount_vocab
from xwot.util.flask import Serializer as FlaskSerializer

from test_conf import annotator
serializer = serializer.Serializer(annotator)
flask_serializer = FlaskSerializer(annotator)

# base config
ip = local_ip()
port = 3000
http_addr = "http://%s:%s/" % (ip, port)
vocab_url = "%s%s#" % (http_addr, 'vocab')
hydra_link = hydra_link(vocab_url)


jsonld_description = create_description(xwot_file=os.path.join(dir_path(__file__), "device.xwot"), base=http_addr)


annotator.documentation(entrypoint=http_addr, title='My Api Doc', description='Awesome xWoT Api documentation.',
                        vocab_url=vocab_url)

app = Flask(__name__, static_path='')



entrypoint = models.EntryPoint()

"""
Entrypoint controller
"""

"""
    GET EntryPoint
"""
@annotator.route('entry_point', method='GET', description='The APIs main entry point.', returns=models.EntryPoint)
@app.route('/', methods=['GET'])
@hydra_link
def entrypoint_get():
    data = {
      "@context": "/contexts/EntryPoint.jsonld",
      "@id": "/",
      "@type": "EntryPoint",
      "users": "/users/"
    }

    # cts = request.accept_mimetypes
    # ct = 'application/ld+json'
    #
    # if cts:
    #     ct,_ = cts[0]

    return flask_serializer.serialize(entrypoint)
    #resp = Response(response=doc, status=200, content_type=ct)
    #return resp


"""
User controller
"""

"""
    GET User collection
"""
@annotator.route('user_collection_retrieve', method='GET', description='Retrieves all User entities', returns=Hydra.Collection())
@app.route('/users', methods=['GET'])
@hydra_link
def get_user_collection():
    json_doc = pretty_json({})
    resp = Response(response=json_doc, status=200, mimetype='application/ld+json')
    return resp


"""
    POST User
"""
@annotator.route('user_create', method='POST', description='Creates a new User entity', returns=models.User,
                 expects=models.User, status_codes=[{"code": 201, "description": "If the User entity was created successfully."}])
@app.route('/users', methods=['POST'])
@hydra_link
def post_user(user_id):
    json_doc = pretty_json({})
    resp = Response(response=json_doc, status=200, mimetype='application/ld+json')
    return resp

"""
    PUT User
"""
@annotator.route('user_replace', method='PUT', description='Replaces a new User entity', returns=models.User,
                 expects=models.User, status_codes=[{"code": 201, "description": "If the User entity was created successfully."}])
@app.route('/users', methods=['PUT'])
@hydra_link
def put_user(user_id):
    json_doc = pretty_json({})
    resp = Response(response=json_doc, status=200, mimetype='application/ld+json')
    return resp


"""
    GET User
"""
@annotator.route('user_retrieve', method='GET', description='Retrieves a User entity', returns=models.User,
                 status_codes=[{"code": 404, "description": "If the User entity wasn't found."}])
@app.route('/users/<int:user_id>', methods=['GET'])
@hydra_link
def get_user(user_id):
    json_doc = pretty_json({})
    resp = Response(response=json_doc, status=200, mimetype='application/ld+json')
    return resp


"""
    DELETE user
"""
@annotator.route('user_delete', method='DELETE', description='Deletes a User entity', returns=Owl.Nothing(),
                 status_codes=[{"code": 404, "description": "If the User entity wasn't found."}])
@app.route('/users/<int:user_id>', methods=['DELETE'])
@hydra_link
def delete_user(user_id):
    data = {}
    json_doc = pretty_json({})
    resp = Response(response=json_doc, status=200, mimetype='application/ld+json')
    return resp


#annotator.write_files()
#
# @app.route('/vocab')
# @link
# def vocab():
#     if json_doc is not None:
#         return Response(response=json_doc, status=200, content_type='application/ld+json')
#     else:
#         return Response(status=404)
#
# @app.route('/contexts/<string:file>', methods=['GET'])
# def contexts(file):
#     if file in class_contexts_json_doc:
#         doc = class_contexts_json_doc[file]
#         return Response(response=doc, status=200, content_type='application/ld+json')
#     else:
#         return Response(status=404)
from xwot.util.hydra import VocabBuilder
builder = VocabBuilder(annotator)
mount_vocab(app, builder)
app.run(host='0.0.0.0', port=port)