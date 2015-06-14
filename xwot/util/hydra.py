#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from functools import wraps
from flask import make_response


def add_response_header(headers):
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


def flask_link(vocab_url):
    link_header = '<' + vocab_url + '>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
    def link(f):
        @wraps(f)
        @add_response_header({'Link': link_header})
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return link