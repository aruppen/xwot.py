# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from __future__ import absolute_import

from flask import Response
from datetime import timedelta
from flask import request, current_app
from functools import update_wrapper

__all__ = ['cors', 'make_response']


SERIALIZERS = {
    'application/json': lambda obj: obj.to_json(),
    'application/xml': lambda obj: obj.to_xml(),
    'text/plain': lambda obj: obj.to_html(),
    'application/ld+json': lambda obj: obj.to_jsonld()
}


def cors(origin='*', methods=None, headers=None, max_age=2520):
    # source: http://flask.pocoo.org/snippets/56/

    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    else:
        methods = 'GET, OPTIONS'

    if headers is not None:
        headers = ', '.join(headers)
    else:
        headers = 'x-prototype-version,x-requested-with'

    from flask import make_response

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = methods
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Headers'] = headers

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def make_response(obj, default='application/ld+json', status=200):
    cts = request.accept_mimetypes

    if cts:
        content_type, _ = cts[0]

        if content_type in SERIALIZERS:
            fun_serializer = SERIALIZERS[content_type]

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