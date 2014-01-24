"""Unit test for Charms"""

import unittest

from mock import patch
from charmworldlib.charm import Charms


class CharmsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = Charms()

    @patch('charmworldlib.charm.Charm')
    @patch('charmworldlib.charm.Charms.get')
    def test_charms_search(self, mget, mCharm):
        cdata = {'charm': {'id': 'oneiric/charm-0'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual([mCharm.from_charmdata()], self.c.search())
        mget.assert_called_with('search', {})
        mCharm.from_charmdata.assert_called_with(cdata)

    @patch('charmworldlib.charm.Charms.get')
    def test_charms_search_string(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.c.search('blurb', 2))
        mget.assert_called_with('search', {'text': 'blurb', 'limit': 2})

    @patch('charmworldlib.charm.Charms.get')
    def test_charms_search_params(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.c.search({'approved': True}, 1))
        mget.assert_called_with('search', {'approved': True, 'limit': 1})

    @patch('charmworldlib.charm.Charms.get')
    def test_charms_search_no_results(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.c.search('no-match'))
        mget.assert_called_with('search', {'text': 'no-match'})

    @patch('charmworldlib.charm.Charm')
    @patch('charmworldlib.charm.Charms.get')
    def test_charms_search_versions(self, mget, mCharm):
        self.c.version = 2
        cdata = {'charm': {'id': 'oneiric/charm-0'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual([mCharm.from_charmdata()], self.c.search())
        mget.assert_called_with('charms', {})
        mCharm.from_charmdata.assert_called_with(cdata)

    @patch('charmworldlib.charm.Charms.get')
    def test_charms_approved(self, mget):
        mget.return_value = {'result': None}
        self.assertEqual([], self.c.approved())
        mget.assert_called_with('search', {'type': 'approved'})

    @patch('charmworldlib.charm.Charm.from_charmdata')
    @patch('charmworldlib.charm.Charms.get')
    def test_charms_charm(self, mget, mCharm):
        cdata = {'charm': {'id': 'oneiric/charm-0'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual(mCharm(), self.c.charm('charm', series='oneiric',
                                                revision=0))
        mget.assert_called_with('charm/oneiric/charm-0')
        mCharm.assert_called_with(cdata)

    @patch('charmworldlib.charm.Charm.from_charmdata')
    @patch('charmworldlib.charm.Charms.get')
    def test_charms_charm_full(self, mget, mCharm):
        cdata = {'charm': {'id': '~me/oneiric/charm-0'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual(mCharm(), self.c.charm('charm', series='oneiric',
                                                revision=0, owner='~me'))
        mget.assert_called_with('charm/~me/oneiric/charm-0')
        mCharm.assert_called_with(cdata)

    @patch('charmworldlib.charm.Charms.get')
    def test_charms_charm_404(self, mget):
        mget.return_value = {'none': None}
        self.assertEqual(None, self.c.charm('charm', series='oneiric',
                                            revision=0, owner='~me'))
        mget.assert_called_with('charm/~me/oneiric/charm-0')

    @patch('charmworldlib.charm.Charm.from_charmdata')
    @patch('charmworldlib.charm.Charms.get')
    def test_charms_charm_full_owner(self, mget, mCharm):
        cdata = {'charm': {'id': '~me/oneiric/charm-0'}}
        mget.return_value = {'result': [cdata]}
        self.assertEqual(mCharm(), self.c.charm('charm', series='oneiric',
                                                revision=0, owner='me'))
        mget.assert_called_with('charm/~me/oneiric/charm-0')
        mCharm.assert_called_with(cdata)

    @patch('charmworldlib.charm.Charms.search')
    def test_charms_interfaces(self, msearch):
        self.c.interfaces(['baz', 'buzz'], ['bar', 'foo'])
        msearch.assert_called_with({'requires': 'baz,buzz',
                                    'provides': 'bar,foo'})

    @patch('charmworldlib.charm.Charms.search')
    def test_charms_interfaces_str(self, msearch):
        self.c.interfaces('foo', 'bar')
        msearch.assert_called_with({'requires': 'foo',
                                    'provides': 'bar'})

    @patch('charmworldlib.charm.Charms.search')
    def test_charms_interfaces_bad(self, msearch):
        self.assertRaises(Exception, self.c.interfaces, IOError, {})

    @patch('charmworldlib.charm.Charms.interfaces')
    def test_charms_provides(self, minterface):
        self.c.provides(['baz', 'buzz'])
        minterface.assert_called_with(provides=['baz', 'buzz'])

    @patch('charmworldlib.charm.Charms.interfaces')
    def test_charms_requires(self, minterface):
        self.c.requires(['baz', 'buzz'])
        minterface.assert_called_with(requires=['baz', 'buzz'])
