
from . import api

_base_endpoint = 'charms'


class Charms(api.API):
    def requires(self, interfaces=[]):
        return self.interfaces(requires=interfaces)

    def provides(self, interfaces=[]):
        return self.interfaces(provides=interfaces)

    def interfaces(self, requires=[], provides=[]):
        if type(requires) == str:
            requires = [requires]
        if type(provides) == str:
            provides = [provides]

        if not type(requires) == list or not type(provides) == list:
            raise Exception('requires/provides must be either a str or list')

        return self.search({'requires': ','.join(requires),
                            'provides': ','.join(provides)})

    def approved(self):
        return self.search({'type': 'approved'})

    def search(self, criteria={}):
        return self.get(_base_endpoint, criteria)
