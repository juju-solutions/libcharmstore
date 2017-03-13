"""Unit test for Entity"""

import unittest

from mock import patch

import charmstore.lib
from util import CHARM, BUNDLE


class EntityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_entity_load(self):
        c = charmstore.lib.Entity.from_data(CHARM.get('Meta'))
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

    @patch.object(charmstore.lib, 'charmstore')
    def test_entity_default_cs_params(self, _charmstore):
        charmstore.lib.Entity.from_data(CHARM.get('Meta'))
        _charmstore.CharmStore.assert_called_once_with(
            timeout=10.0,
            url='https://api.jujucharms.com/charmstore/v5')

    @patch.dict(charmstore.lib.os.environ, {
        'CS_API_URL': 'alturl',
        'CS_API_TIMEOUT': '200'})
    @patch.object(charmstore.lib, 'charmstore')
    def test_entity_env(self, _charmstore):
        charmstore.lib.Entity.from_data(CHARM.get('Meta'))
        _charmstore.CharmStore.assert_called_once_with(
            timeout=200.0,
            url='alturl')
