
import models
from xwot.util import annotator
from xwot.util.serializer import Serializer
from xwot.util import local_ip
annotator = annotator()


serializer = Serializer(annotator)

entrypoint = models.EntryPoint()

url = "http://%s:%s" % (local_ip(), 3000)
output = serializer.serialize(entrypoint, content_type='text/html')

print(output)
m