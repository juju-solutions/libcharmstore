import os
import json

from theblues import charmstore
from theblues.utils import API_URL
from .error import CharmNotFound


DEFAULT_INCLUDES = [
    'bundle-metadata',
    'charm-actions',
    'charm-config',
    'charm-metadata',
    'extra-info',
    'tags',
    'promulgated',
    'id',
]

DEFAULT_TIMEOUT = 10
DEFAULT_CS_API_URL = API_URL


class CharmStore(object):
    def __init__(self, api=None):
        super(CharmStore, self).__init__()
        if not api:
            api = os.environ.get('CS_API_URL', DEFAULT_CS_API_URL)
        self.theblues = charmstore.CharmStore(url=api)

    def requires(self, interfaces=[], limit=None):
        return self.interfaces(requires=interfaces)

    def provides(self, interfaces=[], limit=None):
        return self.interfaces(provides=interfaces)

    def interfaces(self, requires=[], provides=[], limit=None):
        params = {}
        if type(requires) == str:
            requires = [requires]
        if type(provides) == str:
            provides = [provides]

        if type(requires) is not list or type(provides) is not list:
            raise Exception('requires/provides must be either a str or list')

        if requires:
            params['requires'] = '&requires='.join(requires)
        if provides:
            params['provides'] = '&provides='.join(provides)

        return self.search(params)

    def search(self, text=None, includes=None, doc_type=None, limit=None,
               autocomplete=False, promulgated_only=False, tags=None,
               sort=None, owner=None, series=None):

        if not includes:
            includes = DEFAULT_INCLUDES

        result = self.theblues.search(text, includes, doc_type, limit,
                                      autocomplete, promulgated_only, tags,
                                      sort, owner, series)

        return [Charm.from_data(charm.get('Meta')) for charm in result]

    def approved(self):
        return self.search(None, promulgated_only=True)


class Entity(object):
    @classmethod
    def from_data(cls, data):
        e = cls()
        e.load(data)

        return e

    def __init__(self, id=None, api=None, timeout=None):
        if not api:
            api = os.environ.get('CS_API_URL', DEFAULT_CS_API_URL)
        if not timeout:
            timeout = float(os.environ.get('CS_API_TIMEOUT', DEFAULT_TIMEOUT))
        self.id = None
        self.name = None
        self.owner = None
        self.series = None
        self.maintainer = None
        self.revision = None
        self._revisions = None
        self.url = None

        self.approved = False
        self.tags = None
        self.source = None

        self._files_fetched = False
        self.files = []

        self.stats = {}

        self.raw = {}
        self.theblues = charmstore.CharmStore(url=api, timeout=timeout)

        if id:
            self.load(
                self.theblues._meta(id.replace('cs:', ''),
                                    DEFAULT_INCLUDES).get('Meta')
            )

    def revisions(self):
        if self._revisions is None:
            self._revisions = self.theblues._meta(self.id, ['revision-info']) \
                or {}
        data = self._revisions.get('Revisions', [])
        return [self.__class__(e) for e in data]

    def file(self, path):
        if self._files_fetched is False:
            self.files = [
                f.get('Name') for f in
                    self.theblues._meta(self.id, ['manifest']) ]
            self._files_fetched = True
        if path not in self.files:
            raise IOError(
                0,
                'No such file in %s' % self.__class__.__name__.lower(),
                path)

        return self.theblues._get(self.theblues.file_url(self.id, path)).text

    def load(self, data):
        id = data.get('id', {})
        self.id = id.get('Id').replace('cs:', '')
        self.url = id.get('Id')
        self.name = id.get('Name')
        self.revision = id.get('Revision', 0)
        self.series = id.get('Series')

        self.tags = data.get('Tags', {}).get('Tags', [])

        extra_info = data.get('extra-info', {})
        self.source = extra_info.get('bzr-url')

        manifest = data.get('manifest', [])
        self.files = [f.get('Name') for f in manifest]

        self.approved = data.get('promulgated', {}).get('Promulgated', False)

        self.raw = data


class Charm(Entity):
    def __init__(self, id=None, api=None, timeout=None):
        self.summary = None
        self.description = None

        self.subordinate = False
        self.provides = {}
        self.requires = {}
        self.peers = {}

        self.actions = {}
        self.config = {}

        self.bundles = []
        self.terms = []

        super(Charm, self).__init__(id, api=api, timeout=timeout)

    def related(self):
        data = self.raw.get('charm-related')
        related = {}

        for relation, interfaces in data.items():
            related[relation.lower()] = {}
            for interface, charms in interfaces.items():
                related[relation][interface] = []
                for c in charms:
                    related[relation][interface].append(Charm(c.get['Id']))

        return related

    def load(self, charm_data):
        if 'charm-metadata' not in charm_data:
            raise CharmNotFound('Not a valid charm payload')

        super(Charm, self).load(charm_data)

        metadata = self.raw.get('charm-metadata')

        self.description = metadata.get('Description')
        self.summary = metadata.get('Summary')
        self.subordinate = metadata.get('Subordinate', False)
        self.terms = metadata.get('Terms', [])

        for rel, d in metadata.get('Provides', {}).items():
            self.provides[rel] = {k.lower(): v for k, v in d.items()}

        for rel, d in metadata.get('Requires', {}).items():
            self.requires[rel] = {k.lower(): v for k, v in d.items()}

        for rel, d in metadata.get('Peers', {}).items():
            self.peers[rel] = {k.lower(): v for k, v in d.items()}

        action_spec = self.raw.get('charm-actions', {}).get('ActionSpecs')
        if action_spec:
            self.actions = action_spec

        config_options = self.raw.get('charm-config', {}).get('Options')
        if config_options:
            self.config = config_options

    def __str__(self):
        return json.dumps(self.raw, indent=2)

    def __repr__(self):
        return '<Charm %s>' % self.id


class Bundle(Entity):
    def __init__(self, id=None, timeout=None):
        self.count = {'machines': 0, 'units': 0}
        self.relations = []
        self.services = None

        super(Charm, self).__init__(id, timeout)

    def load(self, charm_data):
        if 'charm-metadata' not in charm_data:
            raise CharmNotFound('Not a valid charm payload')

        super(Charm, self).load(charm_data)

        metadata = self.raw.get('bundle-metadata')

        self.relations = metadata.get('Relations', [])
        self.series = metadata.get('Series', 'bundle')
        self.services = metadata.get('Services', {})

        for rel, d in metadata.get('Provides', {}).items():
            self.provides[rel] = {k.lower(): v for k, v in d.items()}

        for rel, d in metadata.get('Requires', {}).items():
            self.requires[rel] = {k.lower(): v for k, v in d.items()}

        for rel, d in metadata.get('Peers', {}).items():
            self.peers[rel] = {k.lower(): v for k, v in d.items()}

        action_spec = self.raw.get('charm-actions', {}).get('ActionSpecs')
        if action_spec:
            self.actions = action_spec

        config_options = self.raw.get('charm-config', {}).get('Options')
        if config_options:
            self.config = config_options

    def __str__(self):
        return json.dumps(self.raw, indent=2)

    def __repr__(self):
        return '<Bundle %s>' % self.id
