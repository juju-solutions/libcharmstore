"""Unit test for Entity"""

import unittest

from mock import patch

from charmstore.lib import Entity
from util import CHARM, BUNDLE


class EntityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_entity_load(self):
        c = Entity.from_data(CHARM.get('Meta'))
        self.assertEqual(c.id, 'trusty/benchmark-gui-0')
        self.assertEqual(c.url, 'cs:trusty/benchmark-gui-0')
        self.assertEqual(c.series, 'trusty')
        self.assertEqual(c.owner, None)
        self.assertEqual(c.name, 'benchmark-gui')
        self.assertEqual(c.revision, 0)

        self.assertEqual(c.approved, True)
        self.assertEqual(c.source, None)

        files = ['revision', 'README.md', 'config.yaml', 'metadata.yaml']
        self.assertEqual(c.files, files)

        self.assertEqual(c.stats, {})

        self.assertEqual(c.raw, CHARM.get('Meta'))
