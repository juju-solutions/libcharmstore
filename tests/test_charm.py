"""Unit test for Charm"""

import unittest
import json

from mock import patch
from charmworldlib.charm import Charm, CharmNotFound


class CharmTests(unittest.TestCase):
    CHARM_JSON = """{
  "charm": {
    "categories": [
      "applications"
    ],
    "code_source": {
      "bugs_link": "https://bugs.launchpad.net/charms/+source/wordpress",
      "last_log": "README and Metadata audit updates.",
      "location": "lp:~charmers/charms/precise/wordpress/trunk",
      "revision": "72",
      "revisions": [
        {
          "authors": [
            {
              "email": "jorge@ubuntu.com",
              "name": "Jorge O. Castro"
            }
          ],
          "date": "2013-12-12T18:42:28Z",
          "message": "README and Metadata audit updates.",
          "revno": 72
        }
      ],
      "type": "bzr"
    },
    "date_created": "2012-04-16T18:29:14Z",
    "description": "This will install and setup WordPress optimized to",
    "distro_series": "precise",
    "downloads": 8059,
    "downloads_in_past_30_days": 1738,
    "files": [
      "hooks/website-relation-joined",
      "hooks/start",
      "hooks/config-changed",
      "hooks/db-relation-broken",
      "revision",
      "metadata.yaml",
      "hooks/loadbalancer-relation-departed",
      "hooks/stop",
      "hooks/loadbalancer-relation-joined",
      "hooks/loadbalancer-relation-broken",
      "hooks/db-relation-departed",
      "hooks/loadbalancer-relation-changed",
      "config.yaml",
      "hooks/restart",
      "icon.svg",
      "hooks/upgrade-charm",
      "README.md",
      "hooks/db-relation-changed",
      "hooks/install",
      "hooks/loadbalancer-rebuild"
    ],
    "id": "precise/fartpress-21",
    "is_approved": true,
    "is_subordinate": false,
    "maintainer": {
      "email": "marco@ceppi.net",
      "name": "Marco Ceppi"
    },
    "name": "wordpress",
    "options": {
      "debug": {
        "default": "no",
        "description": "Setting this option to yes will",
        "type": "string"
      },
      "engine": {
        "default": "nginx",
        "description": "Currently two web server engines are",
        "type": "string"
      }
    },
    "owner": "charmers",
    "rating_denominator": 0,
    "rating_numerator": 0,
    "relations": {
      "provides": {
        "website": {
          "interface": "http"
        }
      },
      "requires": {
        "db": {
          "interface": "mysql"
        }
      }
    },
    "revision": 93,
    "summary": "WordPress is a full featured web blogging tool,this charm",
    "tested_providers": {},
    "url": "cs:precise/wordpress-21"
  },
  "metadata": {
    "doctype": "charm"
  }
}"""

    RELATED_JSON = '''{
  "result": {
    "provides": {
      "memcache": [
        {
          "categories": [
            "applications"
          ],
          "code_source": {
            "last_log": "Add scale out usage.",
            "location": "lp:~charmers/charms/precise/memcached/trunk",
            "revision": "59",
            "type": "bzr"
          },
          "commits_in_past_30_days": 4,
          "downloads": 769,
          "downloads_in_past_30_days": 29,
          "has_icon": true,
          "id": "precise/memcached-11",
          "is_approved": true,
          "name": "memcached",
          "weight": 10.0
        }
      ],
      "mount": [
        {
          "categories": [
            "file-servers"
          ],
          "code_source": {
            "last_log": "Fix 404 link.",
            "location": "lp:~charmers/charms/precise/nfs/trunk",
            "revision": "15",
            "type": "bzr"
          },
          "commits_in_past_30_days": 0,
          "downloads": 244,
          "downloads_in_past_30_days": 12,
          "has_icon": false,
          "id": "precise/nfs-3",
          "is_approved": true,
          "name": "nfs",
          "weight": 10.0
        }
      ],
      "mysql": [
        {
          "categories": [
            "databases"
          ],
          "code_source": {
            "last_log": "[robert-ayres] Fix binlog-format config option",
            "location": "lp:~charmers/charms/precise/mysql/trunk",
            "revision": "110",
            "type": "bzr"
          },
          "commits_in_past_30_days": 1,
          "downloads": 14658,
          "downloads_in_past_30_days": 2223,
          "has_icon": true,
          "id": "precise/mysql-32",
          "is_approved": true,
          "name": "mysql",
          "weight": 10.0
        },
        {
          "categories": [],
          "code_source": {
            "last_log": "deep changes because new units share the same data",
            "location": "lp:~clint-fewbar/charms/precise/galera/trunk",
            "revision": "84",
            "type": "bzr"
          },
          "commits_in_past_30_days": 0,
          "downloads": 8,
          "downloads_in_past_30_days": 1,
          "has_icon": false,
          "id": "~clint-fewbar/precise/galera-0",
          "is_approved": false,
          "name": "galera",
          "weight": 1.0
        }
      ]
    },
    "requires": {
      "http": [
        {
          "categories": [
            "app-servers"
          ],
          "code_source": {
            "last_log": "[davidpbritton] config_changed hooks failed without",
            "location": "lp:~charmers/charms/precise/apache2/trunk",
            "revision": "50",
            "type": "bzr"
          },
          "commits_in_past_30_days": 2,
          "downloads": 665,
          "downloads_in_past_30_days": 55,
          "has_icon": true,
          "id": "precise/apache2-16",
          "is_approved": true,
          "name": "apache2",
          "weight": 10.0
        },
        {
          "categories": [
            "cache-proxy"
          ],
          "code_source": {
            "last_log": "README updates as part of charm audit.",
            "location": "lp:~charmers/charms/precise/haproxy/trunk",
            "revision": "74",
            "type": "bzr"
          },
          "commits_in_past_30_days": 3,
          "downloads": 1539,
          "downloads_in_past_30_days": 49,
          "has_icon": false,
          "id": "precise/haproxy-25",
          "is_approved": true,
          "name": "haproxy",
          "weight": 10.0
        }
      ]
    }
  }
}'''

    @classmethod
    def setUpClass(cls):
        cls.CHARM_OBJ = json.loads(cls.CHARM_JSON)
        cls.RELATED_OBJ = json.loads(cls.RELATED_JSON)

    def test_charm_parse(self):
        oc = self.CHARM_OBJ['charm']
        c = Charm(charm_data=self.CHARM_OBJ)
        self.assertEqual(oc['id'], c.id)
        self.assertEqual(oc['url'], c.url)
        self.assertEqual(oc['is_subordinate'], c.subordinate)
        self.assertEqual(oc['is_approved'], c.approved)
        self.assertEqual(oc['distro_series'], c.series)
        self.assertEqual(oc['code_source'], c.code_source)
        self.assertEqual(oc['code_source'], c.source)
        self.assertEqual(oc['relations']['provides'], c.provides)
        self.assertEqual(oc['relations']['requires'], c.requires)

    def test_charm_parse_fail(self):
        self.assertRaises(CharmNotFound, Charm, charm_data={'bad_data': {}})

    @patch('charmworldlib.charm.Charms')
    def test_charm_fetch(self, mcharms):
        charms_charm = mcharms.return_value
        charms_charm.charm.return_value = self.CHARM_OBJ
        c = Charm(charm_id='precise/wordpress-21')
        charms_charm.charm.assert_called_with('wordpress', series='precise',
                                              owner=None, revision=21,
                                              raw=True)
        self.assertEqual('precise/fartpress-21', c.id)

    @patch('charmworldlib.charm.Charms.get')
    def test_charm_fetch_fail(self, mget):
        msg = 'Request failed with: 500'
        mget.side_effect = Exception(msg)
        self.assertRaises(CharmNotFound, Charm, charm_id='precise/bad-charm')

    def test_charm_to_string(self):
        cjson = str(Charm(charm_data=self.CHARM_OBJ))
        self.assertEqual(self.CHARM_OBJ, json.loads(cjson))
        cjson = repr(Charm(charm_data=self.CHARM_OBJ))
        self.assertEqual(self.CHARM_OBJ, json.loads(cjson))

    @patch('charmworldlib.charm.api.API')
    def test_charm_file(self, mAPI):
        api = mAPI.return_value
        api._fetch_request.return_value.text = "I'm a hook"
        c = Charm(charm_data=self.CHARM_OBJ)
        self.assertEqual("I'm a hook", c.file('hooks/install'))

    def test_charm_file_404(self):
        c = Charm(charm_data=self.CHARM_OBJ)
        self.assertRaises(IOError, c.file, 'lolwut')

    @patch('charmworldlib.charm.Charms')
    @patch('charmworldlib.charm.api.API')
    def test_charm_related(self, mapi, mcharm):
        mget = mapi.return_value
        mget.get.return_value = self.RELATED_OBJ
        mcharm.return_value.charm.return_value = self.CHARM_OBJ
        c = Charm(charm_data=self.CHARM_OBJ)
        related = c.related()
        for relType, relations in self.RELATED_OBJ['result'].iteritems():
            self.assertEqual(len(self.RELATED_OBJ['result'][relType]),
                             len(related[relType]))
            for rel, charms in relations.iteritems():
                self.assertEqual(len(self.RELATED_OBJ['result'][relType][rel]),
                                 len(related[relType][rel]))

    def test_charm_fails(self):
        self.assertRaises(ValueError, Charm)
