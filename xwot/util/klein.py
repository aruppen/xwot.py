# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       13.07.2015

"""

SERIALIZERS = {
    'application/json': lambda obj: obj.to_json(),
    'application/xml': lambda obj: obj.to_xml(),
    'text/plain': lambda obj: obj.to_html(),
    'application/ld+json': lambda obj: obj.to_jsonld()
}


def make_response(obj, request, default='application/ld+json', status=200):
    content_type = request.getHeader('Accept')

    if content_type in SERIALIZERS:
        fun_serializer = SERIALIZERS[content_type]
        doc = fun_serializer(obj)
        request.setHeader('Content-Type', content_type)
        request.setResponseCode(status)
        return doc
    else:
        fun_serializer = SERIALIZERS[default]
        doc = fun_serializer(obj)
        request.setHeader('Content-Type', default)
        request.setResponseCode(status)
        return doc


