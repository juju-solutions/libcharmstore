import collections
import re
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


# Define a sequence of allowed constraints to be used in the process of
# preparing the bundle object. See the _prepare_constraints function below.
ALLOWED_CONSTRAINTS = (
    'arch',
    'container',
    'cpu-cores',
    'cpu-power',
    'mem',
    'root-disk',
    # XXX: BradCrittenden 2014-02-12:
    # tags are supported by MaaS only so they are not currently implemented.
    # It is unclear whether the GUI should support them or not so they are
    # being left out for now.
    # Also, tags are a comma-separated, which would clash with the currently
    # broken constraint parsing in the GUI.
    # 'tags',
)


CONSTRAINTS_REGEX = re.compile('([\w-]+=\w+)[,\s]*?')


def validate_constraints(original_constraints):
    """Parse the constraints and validate them.

    constraints is a space-separated string of key=value pairs or a dict.
    Returns a dict of validated constraints.
    Raises ValueError if one or more constraints is invalid.
    """

    constraints = original_constraints
    if not isinstance(constraints, collections.Mapping):
        pairs = CONSTRAINTS_REGEX.findall(constraints)
        constraints = dict(i.split('=') for i in pairs)
    if len(constraints) == 0 or not all(constraints.values()):
        raise ValueError('invalid constraints: {}'.format(
            original_constraints))
    unsupported = set(constraints).difference(ALLOWED_CONSTRAINTS)
    if unsupported:
        msg = 'unsupported constraints: {}'.format(
            ', '.join(sorted(unsupported)))
        raise ValueError(msg)
    return constraints
