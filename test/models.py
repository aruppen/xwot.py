from xwot.util.vocab import Xsd
from xwot.util.vocab import Hydra
from xwot.util.vocab import Xwot

from xwot.model import Collection
from xwot.model import CollectionMember
from xwot.util.vocab import SchemaOrg
from xwot.model import Resource
from xwot.util.annotator import Annotator

annotate = Annotator()


@annotate.resource(description='A User represents a person registered in the system.',
                   routes=['user_retrieve', 'user_replace', 'user_delete'], iri=Xwot.Resource())
class User(CollectionMember):
    __expose__ = ['id', 'email', 'name', 'password']
    __self_link__ = ''

    def __init__(self, name, email, password, id):
        super(User, self).__init__()
        self._name = name
        self._email = email
        self._password = password
        self._id = id

    @property
    @annotate.property(description="The user's email address", iri=SchemaOrg.email(), required=True)
    def email(self):
        return self._email

    @property
    def id(self):
        return self._id

    @property
    @annotate.property(description="The user's full name.", iri=SchemaOrg.name(), required=True)
    def name(self):
        return self._name

    @property
    @annotate.property(description="The user's password.", required=True, writeonly=True, range=Xsd.string(),
                       iri=SchemaOrg.accessCode())
    def password(self):
        return self._password


@annotate.resource(description='A collection of users', routes=['user_collection_retrieve', 'user_create'], iri=Hydra.Collection())
class UserCollection(Collection):

    def __init__(self, users):
        super(UserCollection, self).__init__()
        self._users = users

    @property
    def members(self):
        return self._users

    def user(self, id):
        return self._users[id]


alex = User(name='Alexander Rueedlinger', email='a.rueedlinger@gmail.com', password=None, id=0)
peter = User(name='Peter Muller', email='peter.muller@gmail.com', password=None, id=1)
bill = User(name='Bill Gates', email='bill@microsoft.com', password=None, id=2)
user_collection = UserCollection(users=[alex, peter, bill])


@annotate.resource(description='The main entry point or homepage of the API.', routes=['entry_point'], iri=Xwot.Resource())
class EntryPoint(Resource):
    __expose__ = ['users', 'name']

    def __init__(self):
        super(EntryPoint, self).__init__()
        self.add_link('users')

    @property
    @annotate.property(description='The collection of all users (for debugging purposes)',
                       routes=["user_create", "user_collection_retrieve"], iri=SchemaOrg.url())
    def users(self):
        return '/users'

    @property
    @annotate.property(description="The entrypoint's name", iri=SchemaOrg.name())
    def name(self):
        return 'a name'
