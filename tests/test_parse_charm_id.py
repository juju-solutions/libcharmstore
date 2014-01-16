"""Unit test for Charm ID"""

import unittest

from charmworldlib.charm import parse_charm_id


class CharmIDTests(unittest.TestCase):
    def test_parse_charm_id(self):
        charm = (None, 'precise', 'test', None)
        self.assertEqual(charm, parse_charm_id('test'))
        self.assertEqual(charm, parse_charm_id('cs:test'))
        self.assertEqual(charm, parse_charm_id('precise/test'))
        self.assertEqual(charm, parse_charm_id('cs:precise/test'))

        charm = (None, 'precise', 'test', 1)
        self.assertEqual(charm, parse_charm_id('test-1'))
        self.assertEqual(charm, parse_charm_id('cs:test-1'))
        self.assertEqual(charm, parse_charm_id('precise/test-1'))
        self.assertEqual(charm, parse_charm_id('cs:precise/test-1'))

        charm = ('~charmers', 'precise', 'test', None)
        self.assertEqual(charm, parse_charm_id('~charmers/test'))
        self.assertEqual(charm, parse_charm_id('cs:~charmers/test'))
        self.assertEqual(charm, parse_charm_id('~charmers/precise/test'))
        self.assertEqual(charm, parse_charm_id('cs:~charmers/precise/test'))

        charm = ('~charmers', 'precise', 'test', 0)
        self.assertEqual(charm, parse_charm_id('~charmers/test-0'))
        self.assertEqual(charm, parse_charm_id('cs:~charmers/test-0'))

        charm = ('~charmers', 'oneiric', 'test', 0)
        self.assertEqual(charm, parse_charm_id('~charmers/oneiric/test-0'))
        self.assertEqual(charm, parse_charm_id('cs:~charmers/oneiric/test-0'))
