"""Unit test for API"""

import unittest

from mock import patch
from charmworldlib.bundle import (
    Bundle,
    Bundles,
)


class BundlesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = Bundles()

    @patch('charmworldlib.bundle.api.API.post')
    def test_bundles_proof(self, mpost):
        mpost.return_value = {'deploy'}
        self.b.proof({'deployment': {}})
        mpost.assert_called_with('bundle/proof', {'deployer_file':
                                                  'deployment: {}\n'})

    def test_bundles_proof_ver(self):
        b = Bundles(version=2)
        self.assertRaises(ValueError, b.proof, 'garbage')

    def test_bundles_proof_invalid(self):
        self.assertRaises(Exception, self.b.proof, 'garbage')


class BundleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = Bundle()

    def test_bundle(self):
        pass
