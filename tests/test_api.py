"""Unit test for API"""

import unittest

from mock import patch
from charmworldlib.api import API, MethodMismatch


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = API(server='example.tld')

    @patch('requests.get')
    def test_fetch_request_get(self, mreq):
        endpoint = 't'
        self.a.fetch_request(endpoint, method='get')
        mreq.assert_called_with(self.a._build_url(endpoint), params={})

    @patch('requests.get')
    def test_fetch_request_get_params(self, mreq):
        endpoint = 'r/maties'
        params = {'foo': 'bar'}
        self.a.fetch_request(endpoint, method='get', params=params)
        mreq.assert_called_with(self.a._build_url(endpoint), params=params)

    def test_fetch_request_bad_method(self):
        self.assertRaises(MethodMismatch, self.a.fetch_request, 'bad',
                          method='bad')

    @patch('requests.post')
    def test_fetch_request_post(self, mreq):
        endpoint = 'posty'
        params = {'bar': 'baz'}
        self.a.port = 8080
        self.a.fetch_request(endpoint, method='post', params=params)
        mreq.assert_called_with(self.a._build_url(endpoint), data=params)
        self.a.port = None

    @patch('charmworldlib.api.API.fetch_request')
    def test_fetch_json(self, mfetch):
        req = mfetch.return_value
        req.status_code = 200
        req.json.return_value = 'JSON!'
        self.assertEqual('JSON!', self.a.fetch_json('r'))
        mfetch.assert_called_with('r', {}, 'get')

    @patch('charmworldlib.api.API.fetch_request')
    def test_fetch_json_failed(self, mfetch):
        req = mfetch.return_value
        req.status_code = 500
        self.a.port = 8080
        self.assertRaises(Exception, self.a.fetch_json, 'bad')
        self.a.port = None

    @patch('charmworldlib.api.API.fetch_request')
    def test_fetch_json_failed_port(self, mfetch):
        req = mfetch.return_value
        req.status_code = 500
        self.assertRaises(Exception, self.a.fetch_json, 'bad')

    @patch('charmworldlib.api.API.fetch_json')
    def test_get(self, mfetch):
        self.a.get('end/of/the/world')
        mfetch.assert_called_with('end/of/the/world', {}, 'get')

    @patch('charmworldlib.api.API.fetch_json')
    def test_get_params(self, mfetch):
        self.a.get('end/of/the/world', {'isit'})
        mfetch.assert_called_with('end/of/the/world', {'isit'}, 'get')

    @patch('charmworldlib.api.API.fetch_json')
    def test_post(self, mfetch):
        self.a.post('end/of/the/world')
        mfetch.assert_called_with('end/of/the/world', {}, 'post')

    @patch('charmworldlib.api.API.fetch_json')
    def test_post_params(self, mfetch):
        self.a.post('end/of/the/world', {'isit'})
        mfetch.assert_called_with('end/of/the/world', {'isit'}, 'post')
