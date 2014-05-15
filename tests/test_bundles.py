"""Unit test for Bundles"""

import unittest

from mock import patch
from charmworldlib.bundle import Bundles


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

    @patch('charmworldlib.bundle.Bundle')
    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_search(self, mget, mBundle):
        cdata = {'bundle': {'id': 'oneiric/bundle-0'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual([mBundle.from_bundledata()], self.b.search())
        mget.assert_called_with('search', {'text': 'bundle'})
        mBundle.from_bundledata.assert_called_with(cdata)

    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_search_string(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.b.search('blurb', 2))
        mget.assert_called_with('search', {'text': 'bundle:blurb', 'limit': 2})

    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_search_params(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.b.search({'approved': True}, 1))
        mget.assert_called_with(
            'search', {'approved': True, 'limit': 1, 'text': 'bundle'})

    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_search_no_results(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.b.search('no-match'))
        mget.assert_called_with('search', {'text': 'bundle:no-match'})

    @patch('charmworldlib.bundle.Bundle')
    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_search_versions(self, mget, mBundle):
        self.b.version = 2
        cdata = {'bundle': {'id': 'mediawiki/0/single'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual([mBundle.from_bundledata()], self.b.search())
        mget.assert_called_with('search', {'text': 'bundle'})
        mBundle.from_bundledata.assert_called_with(cdata)

    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_approved(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.b.approved())
        mget.assert_called_with(
            'search', {'type': 'approved', 'text': 'bundle'})

    @patch('charmworldlib.bundle.Bundle.from_bundledata')
    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_bundle(self, mget, mBundle):
        cdata = {'bundle': {'id': 'mediawiki/0/single'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual(mBundle(), self.b.bundle('mediawiki', 'single',
                                                  revision=0))
        mget.assert_called_with('bundle/mediawiki/0/single')
        mBundle.assert_called_with(cdata)

    @patch('charmworldlib.bundle.Bundle.from_bundledata')
    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_bundle_full(self, mget, mBundle):
        cdata = {'bundle': {'id': '~me/mediawiki/0/single'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual(mBundle(), self.b.bundle('mediawiki', 'single',
                                                  revision=0, owner='~me'))
        mget.assert_called_with('bundle/~me/mediawiki/0/single')
        mBundle.assert_called_with(cdata)

    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_bundle_404(self, mget):
        mget.return_value = {'none': None}
        self.assertEqual(None, self.b.bundle('mediawiki', 'single',
                                             revision=0, owner='~me'))
        mget.assert_called_with('bundle/~me/mediawiki/0/single')

    @patch('charmworldlib.bundle.Bundle.from_bundledata')
    @patch('charmworldlib.bundle.Bundles.get')
    def test_bundles_bundle_full_owner(self, mget, mBundle):
        cdata = {'bundle': {'id': '~me/mediawiki/0/single'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual(mBundle(), self.b.bundle('mediawiki', 'single',
                                                  revision=0, owner='me'))
        mget.assert_called_with('bundle/~me/mediawiki/0/single')
        mBundle.assert_called_with(cdata)
