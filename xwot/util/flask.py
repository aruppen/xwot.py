# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from __future__ import absolute_import
from functools import wraps

from flask import request
from flask import Response


def _add_response_header(headers):
    from flask import make_response

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp

        return decorated_function

    return decorator


def hydra_link(apidoc_url):
    link_header = '<' + apidoc_url + '>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'

    def wrapped_link(f):
        @wraps(f)
        @_add_response_header({'Link': link_header})
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return wrapped_link


def mount_apidoc(app, builder):
    doc = builder.documentation
    link = hydra_link(doc.apidoc_url)
    jsonld_doc = builder.build()

    @link
    def vocab():
        if jsonld_doc is not None:
            return Response(response=jsonld_doc, status=200, content_type='application/ld+json')
        else:
            return Response(status=404)

    app.add_url_rule('/vocab', 'vocab', vocab)



SERIALIZERS = {
    'application/json': lambda obj: obj.to_json(),
    'application/xml': lambda obj: obj.to_xml(),
    'text/plain': lambda obj: obj.to_html(),
    'application/ld+json': lambda obj: obj.to_jsonld()
}


def make_response(obj, default='application/ld+json', status=200):
    cts = request.accept_mimetypes
    path = request.path

    if cts:
        content_type, _ = cts[0]

        if content_type in SERIALIZERS:
            fun_serializer = SERIALIZERS[content_type]
            if path:
                obj.resource_path = path
            doc = fun_serializer(obj)
            return Response(response=doc, status=status, content_type=content_type)
        else:
            fun_serializer = SERIALIZERS[default]
            doc = fun_serializer(obj)
            return Response(response=doc, status=status, content_type=default)
    else:
        fun_serializer = SERIALIZERS[default]
        doc = fun_serializer(obj)
        return Response(response=doc, status=status, content_type=default)

