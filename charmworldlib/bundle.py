
from . import api

_base_endpoint = 'bundle'


class Bundle(api.API):
    def proof(self, deployer_contents):
        if not self.version >= 3:
            raise Exception('Need to use CharmWorld API >= 3')
        if not typeof(deployer_contents) == 'object':
            raise Exception('Invalid deployer_contents')

        return self.post('%s/proof' % _base_endpoint,
                         {'deployer_file': deployer_contents})
