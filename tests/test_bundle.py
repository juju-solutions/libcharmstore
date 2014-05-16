"""Unit test for Bundle"""

import json
from mock import patch
import unittest

from charmworldlib.bundle import Bundle, BundleNotFound

BUNDLE_DATA = json.loads(r'''
{
  "basket_name": "mediawiki",
  "basket_revision": 6,
  "branch_deleted": false,
  "branch_spec": "~charmers/charms/bundles/mediawiki/bundle",
  "changes": [
    {
      "authors": [
        "Jorge O. Castro <jorge@ubuntu.com>"
      ],
      "committer": "Jorge O. Castro <jorge@ubuntu.com>",
      "created": 1383229159.809,
      "message": "Initial commit\n",
      "revno": 1
    }
  ],
  "charm_metadata": {
    "mediawiki": {
      "annotations": {
        "gui-x": 609,
        "gui-y": -15
      },
      "categories": [
        "applications"
      ],
      "code_source": {
        "bugs_link": "https://bugs.launchpad.net/charms/+source/mediawiki",
        "last_log": "merging lp:~dave-cheney/charms/precise/mediawiki/trunk as per https://code.launchpad.net/~dave-cheney/charms/precise/mediawiki/trunk/+merge/182803",
        "location": "lp:~charmers/charms/precise/mediawiki/trunk",
        "revision": "72",
        "revisions": [
          {
            "authors": [
              {
                "email": "clint@ubuntu.com",
                "name": "Clint Byrum"
              }
            ],
            "date": "2012-06-28T00:02:47Z",
            "message": "removing old broken munin bits",
            "revno": 63
          }
        ],
        "type": "bzr"
      },
      "date_created": "2012-04-16T18:29:51Z",
      "description": "MediaWiki is a wiki engine (a program for creating a collaboratively\nedited website). It is designed to handle heavy websites containing\nlibrary-like document collections, and supports user uploads of\nimages/sounds, multilingual content, TOC autogeneration, ISBN links,\netc.\n",
      "distro_series": "precise",
      "downloads": 3928,
      "downloads_in_past_30_days": 484,
      "files": [
        "hooks/slave-relation-departed",
        "hooks/combine-dbservers",
        "hooks/cache-relation-changed",
        "hooks/website-relation-joined",
        "revision",
        "icon.svg",
        "hooks/upgrade-charm",
        "hooks/stop",
        "README.md",
        "hooks/db-relation-changed",
        "hooks/db-relation-departed",
        "hooks/install",
        "metadata.yaml",
        "hooks/config-changed",
        "hooks/slave-relation-changed",
        "config.yaml",
        "hooks/slave-relation-broken"
      ],
      "id": "precise/mediawiki-10",
      "is_approved": true,
      "is_subordinate": false,
      "maintainer": {
        "email": "clint@ubuntu.com",
        "name": "Clint Byrum"
      },
      "maintainers": [
        {
          "email": "clint@ubuntu.com",
          "name": "Clint Byrum"
        }
      ],
      "name": "mediawiki",
      "options": {
        "admins": {
          "description": "Admin users to create, user:pass",
          "type": "string"
        },
        "debug": {
          "default": false,
          "description": "turn on debugging features of mediawiki",
          "type": "boolean"
        },
        "logo": {
          "description": "URL to fetch logo from",
          "type": "string"
        },
        "name": {
          "default": "Please set name of wiki",
          "description": "The name, or Title of the Wiki",
          "type": "string"
        },
        "skin": {
          "default": "vector",
          "description": "skin for the Wiki",
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
          "cache": {
            "interface": "memcache"
          },
          "db": {
            "interface": "mysql"
          },
          "slave": {
            "interface": "mysql"
          }
        }
      },
      "revision": 90,
      "summary": "Website engine for collaborative work",
      "tested_providers": {
        "ec2": "SUCCESS",
        "openstack": "SUCCESS"
      },
      "url": "cs:precise/mediawiki-10"
    },
    "mysql": {
      "annotations": {
        "gui-x": 610,
        "gui-y": 255
      },
      "categories": [
        "databases"
      ],
      "code_source": {
        "bugs_link": "https://bugs.launchpad.net/charms/+source/mysql",
        "last_log": "Updated README",
        "location": "lp:~charmers/charms/precise/mysql/trunk",
        "revision": "105",
        "revisions": [
          {
            "authors": [
              {
                "email": "marco@ceppi.net",
                "name": "Marco Ceppi"
              }
            ],
            "date": "2013-04-25T18:19:45Z",
            "message": "Added icon.svg",
            "revno": 96
          }
        ],
        "type": "bzr"
      },
      "date_created": "2012-04-16T18:30:00Z",
      "description": "MySQL is a fast, stable and true multi-user, multi-threaded SQL database\nserver. SQL (Structured Query Language) is the most popular database query\nlanguage in the world. The main goals of MySQL are speed, robustness and\nease of use.\n",
      "distro_series": "precise",
      "downloads": 21895,
      "downloads_in_past_30_days": 2006,
      "files": [
        "hooks/munin-relation-joined",
        "hooks/monitors.common.bash",
        "hooks/db-relation-joined",
        "hooks/shared-db-relation-changed",
        "hooks/master-relation-departed",
        "hooks/monitors-relation-departed",
        "hooks/master-relation-broken",
        "hooks/lib/cluster_utils.py",
        "hooks/shared_db_relations.py",
        "hooks/slave-relation-broken",
        "hooks/lib/utils.py",
        "hooks/ha-relation-changed",
        "hooks/munin-relation-changed",
        "hooks/common.py",
        "hooks/start",
        "hooks/config-changed",
        "hooks/db-relation-broken",
        "hooks/slave-relation-changed",
        "hooks/shared-db-relation-joined",
        "hooks/ha_relations.py",
        "hooks/cluster-relation-changed",
        "hooks/slave-relation-departed",
        "hooks/lib/ceph_utils.py",
        "hooks/ceph-relation-changed",
        "metadata.yaml",
        "hooks/ha-relation-joined",
        "hooks/stop",
        "hooks/db-admin-relation-joined",
        "config.yaml",
        "hooks/monitors-relation-joined",
        "icon.svg",
        "hooks/upgrade-charm",
        "README.md",
        "hooks/ceph-relation-joined",
        "hooks/master-relation-changed",
        "hooks/lib/__init__.py",
        "hooks/slave-relation-joined",
        "hooks/install",
        "hooks/local-monitors-relation-joined",
        "revision",
        "hooks/monitors-relation-broken"
      ],
      "id": "precise/mysql-28",
      "is_approved": true,
      "is_subordinate": false,
      "maintainer": {
        "email": "marco@ceppi.net",
        "name": "Marco Ceppi"
      },
      "maintainers": [
        {
          "email": "marco@ceppi.net",
          "name": "Marco Ceppi"
        }
      ],
      "name": "mysql",
      "options": {
        "binlog-format": {
          "default": "MIXED",
          "description": "If binlogging is enabled, this is the format that will be used. Ignored when tuning-level == fast.",
          "type": "string"
        },
        "block-size": {
          "default": 5,
          "description": "Default block storage size to create when setting up MySQL block storage.\nThis value should be specified in GB (e.g. 100 not 100GB).\n",
          "type": "int"
        },
        "dataset-size": {
          "default": "80%",
          "description": "How much data do you want to keep in memory in the DB. This will be used to tune settings in the database server appropriately. Any more specific settings will override these defaults though. This currently sets innodb_buffer_pool_size or key_cache_size depending on the setting in preferred-storage-engine. If query-cache-type is set to 'ON' or 'DEMAND' 20% of this is given to query-cache-size. Suffix this value with 'K','M','G', or 'T' to get the relevant kilo/mega/etc. bytes. If suffixed with %, one will get that percentage of RAM devoted to dataset and (if enabled) query cache.",
          "type": "string"
        },
        "flavor": {
          "default": "distro",
          "description": "Possible values are 'distro' or 'percona'",
          "type": "string"
        },
        "ha-bindiface": {
          "default": "eth0",
          "description": "Default network interface on which HA cluster will bind to communication\nwith the other members of the HA Cluster.\n",
          "type": "string"
        },
        "ha-mcastport": {
          "default": 5411,
          "description": "Default multicast port number that will be used to communicate between\nHA Cluster nodes.\n",
          "type": "int"
        },
        "max-connections": {
          "default": -1,
          "description": "Maximum connections to allow. -1 means use the server's compiled in default.",
          "type": "int"
        },
        "preferred-storage-engine": {
          "default": "InnoDB",
          "description": "Tune the server for usage of this storage engine. Other possible value is MyISAM. Comma separated will cause settings to split resources evenly among given engines.",
          "type": "string"
        },
        "query-cache-size": {
          "default": -1,
          "description": "Override the computed version from dataset-size. Still works if query-cache-type is \"OFF\" since sessions can override the cache type setting on their own.",
          "type": "int"
        },
        "query-cache-type": {
          "default": "OFF",
          "description": "Query cache is usually a good idea, but can hurt concurrency. Valid values are \"OFF\", \"ON\", or \"DEMAND\". http://dev.mysql.com/doc/refman/5.1/en/server-system-variables.html#sysvar_query_cache_type",
          "type": "string"
        },
        "rbd-name": {
          "default": "mysql1",
          "description": "The name that will be used to create the Ceph's RBD image with. If the\nimage name exists in Ceph, it will be re-used and the data will be\noverwritten.\n",
          "type": "string"
        },
        "tuning-level": {
          "default": "safest",
          "description": "Valid values are 'safest', 'fast', and 'unsafe'. If set to safest, all settings are tuned to have maximum safety at the cost of performance. Fast will turn off most controls, but may lose data on crashes. unsafe will turn off all protections.",
          "type": "string"
        },
        "vip": {
          "description": "Virtual IP to use to front mysql in ha configuration",
          "type": "string"
        },
        "vip_cidr": {
          "default": 24,
          "description": "Netmask that will be used for the Virtual IP",
          "type": "int"
        },
        "vip_iface": {
          "default": "eth0",
          "description": "Network Interface where to place the Virtual IP",
          "type": "string"
        }
      },
      "owner": "charmers",
      "rating_denominator": 0,
      "rating_numerator": 0,
      "relations": {
        "provides": {
          "db": {
            "interface": "mysql"
          },
          "db-admin": {
            "interface": "mysql-root"
          },
          "local-monitors": {
            "interface": "local-monitors",
            "scope": "container"
          },
          "master": {
            "interface": "mysql-oneway-replication"
          },
          "monitors": {
            "interface": "monitors"
          },
          "munin": {
            "interface": "munin-node"
          },
          "shared-db": {
            "interface": "mysql-shared"
          }
        },
        "requires": {
          "ceph": {
            "interface": "ceph-client"
          },
          "ha": {
            "interface": "hacluster",
            "scope": "container"
          },
          "slave": {
            "interface": "mysql-oneway-replication"
          }
        }
      },
      "revision": 309,
      "summary": "MySQL is a fast, stable and true multi-user, multi-threaded SQL database",
      "tested_providers": {},
      "url": "cs:precise/mysql-28"
    }
  },
  "data": {
    "relations": [
      [
        "mediawiki:db",
        "mysql:db"
      ]
    ],
    "series": "precise",
    "services": {
      "mediawiki": {
        "annotations": {
          "gui-x": 609,
          "gui-y": -15
        },
        "charm": "cs:precise/mediawiki-10",
        "num_units": 1,
        "options": {
          "debug": false,
          "name": "Please set name of wiki",
          "skin": "vector"
        }
      },
      "mysql": {
        "annotations": {
          "gui-x": 610,
          "gui-y": 255
        },
        "charm": "cs:precise/mysql-28",
        "num_units": 1,
        "options": {
          "binlog-format": "MIXED",
          "block-size": 5,
          "dataset-size": "80%",
          "flavor": "distro",
          "ha-bindiface": "eth0",
          "ha-mcastport": 5411,
          "max-connections": -1,
          "preferred-storage-engine": "InnoDB",
          "query-cache-size": -1,
          "query-cache-type": "OFF",
          "rbd-name": "mysql1",
          "tuning-level": "safest",
          "vip_cidr": 24,
          "vip_iface": "eth0"
        }
      }
    }
  },
  "deployer_file_url": "http://manage.jujucharms.com/bundle/%7Echarmers/mediawiki/6/single/json",
  "description": "",
  "downloads": 58,
  "downloads_in_past_30_days": 4,
  "files": [
    "README.md",
    "bundles.yaml"
  ],
  "first_change": {
    "authors": [
      "Jorge O. Castro <jorge@ubuntu.com>"
    ],
    "committer": "Jorge O. Castro <jorge@ubuntu.com>",
    "created": 1383229159.809,
    "message": "Initial commit\n",
    "revno": 1
  },
  "id": "~charmers/mediawiki/6/single",
  "last_change": {
    "authors": [
      "Jorge O. Castro <jorge@ubuntu.com>"
    ],
    "committer": "Jorge O. Castro <jorge@ubuntu.com>",
    "created": 1394724884.008,
    "message": "Combine single and scalable bundles into one.\n",
    "revno": 6
  },
  "name": "single",
  "owner": "charmers",
  "permanent_url": "bundle:~charmers/mediawiki/6/single",
  "promulgated": true,
  "title": ""
}''')


class BundleTest(unittest.TestCase):
    def test_from_bundledata(self):
        b = Bundle.from_bundledata(BUNDLE_DATA)
        self.assertIsInstance(b, Bundle)
        self.assertEqual(b._raw, BUNDLE_DATA)

    @patch('charmworldlib.bundle.api.API.get')
    def test_init(self, get):
        get.return_value = BUNDLE_DATA
        self.assertEqual(
            Bundle('~me/mediawiki/0/single')._raw,
            Bundle.from_bundledata(BUNDLE_DATA)._raw)

    def test_getattr(self):
        b = Bundle.from_bundledata(BUNDLE_DATA)
        for k, v in b._raw.items():
            self.assertEqual(v, getattr(b, k))

    @patch('charmworldlib.bundle.api.API.get')
    def test_bundle_fetch_fail(self, mget):
        msg = 'Request failed with: 500'
        mget.side_effect = Exception(msg)
        self.assertRaises(BundleNotFound, Bundle, bundle_id='mediawiki/single')

    def test_parse(self):
        from charmworldlib.charm import Charm
        b = Bundle.from_bundledata(BUNDLE_DATA)
        self.assertEqual(len(b.charms), 2)
        self.assertTrue('mediawiki' in b.charms)
        self.assertTrue('mysql' in b.charms)
        for charm in b.charms.values():
            self.assertIsInstance(charm, Charm)

    def test_parse_id(self):
        b = Bundle()

        self.assertEqual(
            b._parse_id('~me/mediawiki/0/single'),
            ('~me', 'mediawiki', 0, 'single'))
        self.assertEqual(
            b._parse_id('~me/mediawiki/single'),
            ('~me', 'mediawiki', None, 'single'))
        self.assertEqual(
            b._parse_id('mediawiki/0/single'),
            (None, 'mediawiki', 0, 'single'))
        self.assertEqual(
            b._parse_id('mediawiki/single'),
            (None, 'mediawiki', None, 'single'))
        self.assertRaises(ValueError, b._parse_id, 'mediawiki')

    def test_str(self):
        b = Bundle.from_bundledata(BUNDLE_DATA)
        self.assertEqual(str(b), json.dumps(BUNDLE_DATA, indent=2))

    def test_repr(self):
        b = Bundle.from_bundledata(BUNDLE_DATA)
        self.assertEqual(repr(b), '<Bundle ~charmers/mediawiki/6/single>')
