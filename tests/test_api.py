"""Unit test for API"""

import unittest

from mock import patch
from charmworldlib.api import API, MethodMismatch


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = API(server='example.tld')

    def test_earl(self):
        self.assertEqual('https://example.tld', self.a._earl())
        b = API(secure=False)
        self.assertEqual('http://manage.jujucharms.com', b._earl())

    def test_earl_port(self):
        a = API(port=8080)
        self.assertEqual('https://manage.jujucharms.com:8080', a._earl())
        a = API(port=8080, secure=False)
        self.assertEqual('http://manage.jujucharms.com:8080', a._earl())

    def test_build_url(self):
        self.assertEqual('https://example.tld/api/3/foo',
                         self.a._build_url('foo'))
        b = API(server='example.tld', version=2)
        self.assertEqual('https://example.tld/api/2/bar', b._build_url('bar'))

    @patch('requests.get')
    def test_fetch_request_get(self, mreq):
        endpoint = 't'
        self.a._fetch_request(endpoint, method='get')
        mreq.assert_called_with(self.a._build_url(endpoint), params={})

    @patch('requests.get')
    def test_fetch_request_get_params(self, mreq):
        endpoint = 'r/maties'
        params = {'foo': 'bar'}
        self.a._fetch_request(endpoint, method='get', params=params)
        mreq.assert_called_with(self.a._build_url(endpoint), params=params)

    def test_fetch_request_bad_method(self):
        self.assertRaises(MethodMismatch, self.a._fetch_request, 'bad',
                          method='bad')

    @patch('requests.post')
    def test_fetch_request_post(self, mreq):
        endpoint = 'posty'
        params = {'bar': 'baz'}
        self.a._fetch_request(endpoint, method='post', params=params)
        mreq.assert_called_with(self.a._build_url(endpoint), data=params)

    @patch('charmworldlib.api.API._fetch_request')
    def test_fetch_json(self, mfetch):
        req = mfetch.return_value
        req.status_code = 200
        req.json.return_value = 'JSON!'
        self.assertEqual('JSON!', self.a._fetch_json('r'))
        mfetch.assert_called_with('r', {}, 'get')

    @patch('charmworldlib.api.API._fetch_request')
    def test_fetch_json_failed(self, mfetch):
        req = mfetch.return_value
        req.status_code = 500
        self.assertRaises(Exception, self.a._fetch_json, 'bad')

    @patch('charmworldlib.api.API._fetch_json')
    def test_get(self, mfetch):
        self.a.get('end/of/the/world')
        mfetch.assert_called_with('end/of/the/world', {}, 'get')

    @patch('charmworldlib.api.API._fetch_json')
    def test_get_params(self, mfetch):
        self.a.get('end/of/the/world', {'isit'})
        mfetch.assert_called_with('end/of/the/world', {'isit'}, 'get')

    @patch('charmworldlib.api.API._fetch_json')
    def test_post(self, mfetch):
        self.a.post('end/of/the/world')
        mfetch.assert_called_with('end/of/the/world', {}, 'post')

    @patch('charmworldlib.api.API._fetch_json')
    def test_post_params(self, mfetch):
        self.a.post('end/of/the/world', {'isit'})
        mfetch.assert_called_with('end/of/the/world', {'isit'}, 'post')
