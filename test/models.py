from xwot.util.vocab import Xsd
from xwot.util.vocab import Hydra
from xwot.util.vocab import SchemaOrg
from test_conf import annotator

from xwot.util.hydra import Collection


class User(object):

    __COLLECTION__ = None

    def __init__(self, name, email, password, id):
        self._name = name
        self._email = email
        self._password = password
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    @classmethod
    def user(cls, id):
        if cls.__COLLECTION__ is not None and len(cls.__COLLECTION__.members) > id:
            return cls.__COLLECTION__.get(id)
        else:
            return None

    @classmethod
    def users(cls):
        return cls.__COLLECTION__


alex = User(name='Alexander Rueedlinger', email='a.rueedlinger@gmail.com', password=None, id=0)
peter = User(name='Peter Muller', email='peter.muller@gmail.com', password=None, id=1)
bill = User(name='Bill Gates', email='bill@microsoft.com', password=None, id=2)
User.__COLLECTION__ = Collection(members=[alex, peter, bill])



# annotate User class
user = annotator.klass(User)
user.describe(title='User', description='A User represents a person registered in the system.',
              operations=['user_retrieve', 'user_replace', 'user_delete'], id_prefix='/users/', embed=True, id='id',
              iri=SchemaOrg.Person())
user.expose('name', description="The user's full name.", iri=SchemaOrg.name(), required=True, range=Xsd.string())
user.expose('email', description="The user's email address", range=Xsd.string(), iri=SchemaOrg.email(), required=True)
user.expose('password', description="The user's password.", range=Xsd.string(), required=True, writeonly=True)


class EntryPoint(object):

    def __init__(self):
        self._users = '/users'

    @property
    def users(self):
        return self._users

    @property
    def name(self):
        return 'a name'


# annotate EntryPoint class
entrypoint = annotator.klass(EntryPoint)
#entrypoint.add_context('http://xwot.lexruee.ch/contexts/xwot.jsonld')
entrypoint.describe(title='Entrypoint', description='The main entry point or homepage of the API.',
                    operations=['entry_point'])
entrypoint.expose('users', description='The collection of all users (for debugging purposes)',
                  range=Hydra.Collection(),
                  operations=["user_create", "user_collection_retrieve"],
                  type=Hydra.Link())
entrypoint.expose('name', description="The entrypoint's name", range=Xsd.string(), iri=SchemaOrg.name())
