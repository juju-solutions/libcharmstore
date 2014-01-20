
import yaml
from . import api


class Bundles(api.API):
    _base_endpoint = 'bundle'

    def proof(self, deployer_contents):
        if not self.version >= 3:
            raise ValueError('Need to use charmworld API >= 3, selected: %s' %
                             self.version)
        if type(deployer_contents) is not dict:
            raise Exception('Invalid deployer_contents')

        return self.post('%s/proof' % self._base_endpoint,
                         {'deployer_file': yaml.dump(deployer_contents)})


class Bundle(object):
    def __init__(self):
        pass
