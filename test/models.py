from xwot.util.vocab import Xsd
from xwot.util.vocab import Hydra
from xwot.util.vocab import SchemaOrg
from test_conf import annotator


class User(object):

    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = password

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password


# annotate User class
user = annotator.klass(User)
user.describe(title='User', description='A User represents a person registered in the system.', iri=SchemaOrg.Person(),
              operations=['user_retrieve', 'user_replace', 'user_delete'])
user.expose('name', description="The user's full name.", iri=SchemaOrg.name(), required=True, range=Xsd.string())
user.expose('email', description="The user's email address", range=Xsd.string(), iri=SchemaOrg.email(), required=True)
user.expose('password', description="The user's password.", range=Xsd.string(), required=True, writeonly=True)


class Issue(object):

    def __init__(self, title, description, is_open):
        self._title = title
        self._description = description
        self._is_open = is_open

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def is_open(self):
        return self._is_open


# annotate Issue class
issue = annotator.klass(Issue)
issue.describe(title='A issue', description='An Issue tracked by the system.',
               operations=['issue_retrieve', 'issue_replace', 'issue_delete'])
issue.expose('title', description="The issue's title.", required=True, range=Xsd.string())
issue.expose('description', description='A description of the issue', range=Xsd.string(), required=True)
issue.expose('is_open', description='Is the issue open?\nUse for 1 yes, 0 for no when modifying this value.',
             range=Xsd.boolean(),
             required=True)


class EntryPoint(object):

    def __init__(self):
        self._issues = '/issues'
        self._users = '/users'

    @property
    def issues(self):
        return self._issues

    @property
    def users(self):
        return self._users

    @property
    def name(self):
        return 'a name'


# annotate EntryPoint class
entrypoint = annotator.klass(EntryPoint)
entrypoint.describe(title='Entrypoint', description='The main entry point or homepage of the API.',
                    operations=['entry_point'])
entrypoint.expose('users', description='The collection of all users (for debugging purposes)',
                  range=Hydra.Collection(),
                  operations=["user_create", "user_collection_retrieve"],
                  type=Hydra.Link())
entrypoint.expose('issues', description='The collection of all issues',
                  range=Hydra.Collection(),
                  operations=["issue_create", "issue_collection_retrieve"],
                  type=Hydra.Link())
entrypoint.expose('name', description="The entrypoint's name", range=Xsd.string(), iri=SchemaOrg.name())
