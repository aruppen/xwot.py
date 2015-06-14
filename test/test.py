import json

from flask import Flask
from flask import Response
from flask import request
import models
from xwot.util.vocab import Hydra
from xwot.util.vocab import Owl
from xwot.util.hydra import flask_link
from xwot.util import local_ip
from xwot.util import serializer
from xwot.util import create_description
from xwot.util import pretty_json


from test_conf import annotator
serializer = serializer.Serializer(annotator)

# base config
ip = local_ip()
port = 3000
http_addr = "http://%s:%s/" % (ip, port)
iri = "%s%s" % (http_addr, 'vocab')
vocab_url = iri + '#'
link = flask_link(iri)

jsonld_description = create_description(xml_file="device.xwot", base=http_addr)
print(jsonld_description)


annotator.documentation({
    'entrypoint': http_addr,
    'title': 'My Api Doc',
    'description': 'Awesome xWoT Api documentation.',
    'id': iri,
    'vocab': vocab_url
})

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
@link
def entrypoint_get():
    data = {
      "@context": "/contexts/EntryPoint.jsonld",
      "@id": "/",
      "@type": "EntryPoint",
      "users": "/users/"
    }

    cts = request.accept_mimetypes
    ct = 'application/ld+json'

    if cts:
        ct,_ = cts[0]


    doc = serializer.serialize(entrypoint, content_type=ct)
    resp = Response(response=doc, status=200, content_type=ct)
    return resp


"""
User controller
"""

"""
    GET User collection
"""
@annotator.route('user_collection_retrieve', method='GET', description='Retrieves all User entities', returns=Hydra.Collection())
@app.route('/users', methods=['GET'])
@link
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
@link
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
@link
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
@link
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
@link
def delete_user(user_id):
    data = {}
    json_doc = pretty_json({})
    resp = Response(response=json_doc, status=200, mimetype='application/ld+json')
    return resp


json_doc, class_contexts_json_doc = annotator.build_vocab()
#annotator.write_files()

@app.route('/vocab')
@link
def vocab():
    if json_doc is not None:
        return Response(response=json_doc, status=200, content_type='application/ld+json')
    else:
        return Response(status=404)

@app.route('/contexts/<string:file>', methods=['GET'])
def contexts(file):
    if file in class_contexts_json_doc:
        doc = class_contexts_json_doc[file]
        return Response(response=doc, status=200, content_type='application/ld+json')
    else:
        return Response(status=404)

app.run(host='0.0.0.0', port=port)