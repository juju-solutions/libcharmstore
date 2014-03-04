"""Unit tests for utils."""

import unittest

from charmworldlib.utils import (
    check_constraints,
    parse_constraints,
)


class TestParseConstraints(unittest.TestCase):

    def test_valid_constraints(self):
        # Valid constraints are returned as they are.
        constraints = {
            'arch': 'i386',
            'cpu-cores': 4,
            'cpu-power': 2,
            'mem': 2000,
            'root-disk': '1G',
            'container': 'lxc',
        }
        self.assertEqual(constraints, parse_constraints(constraints))

    def test_valid_constraints_subset(self):
        # A subset of valid constraints is returned as it is.
        constraints = {'cpu-cores': '4', 'cpu-power': 2}
        self.assertEqual(constraints, parse_constraints(constraints))

    def test_invalid_constraints(self):
        # A ValueError is raised if unsupported constraints are found.
        with self.assertRaises(ValueError) as context_manager:
            parse_constraints({'arch': 'i386', 'not-valid': 'bang!'})
        self.assertEqual(
            'unsupported constraints: not-valid',
            str(context_manager.exception))

    def test_string_constraints_space_separated(self):
        # String constraints are converted to a dict.
        constraints = 'arch=i386 cpu-cores=4 cpu-power=2 mem=2000'
        expected = {
            'arch': 'i386',
            'cpu-cores': '4',
            'cpu-power': '2',
            'mem': '2000',
        }
        self.assertEqual(expected, parse_constraints(constraints))

    def test_string_constraints_comma_separated(self):
        # String constraints are converted to a dict.
        constraints = 'arch=i386,cpu-cores=4,cpu-power=2,mem=2000'
        expected = {
            'arch': 'i386',
            'cpu-cores': '4',
            'cpu-power': '2',
            'mem': '2000',
        }
        self.assertEqual(expected, parse_constraints(constraints))

    def test_string_constraints_mixed_separated(self):
        # String constraints are converted to a dict.
        constraints = 'arch=i386,  cpu-cores=4, cpu-power=2,mem=2000'
        expected = {
            'arch': 'i386',
            'cpu-cores': '4',
            'cpu-power': '2',
            'mem': '2000',
        }
        self.assertEqual(expected, parse_constraints(constraints))

    def test_unsupported_string_constraints(self):
        # A ValueError is raised if unsupported string constraints are found.
        with self.assertRaises(ValueError) as context_manager:
            parse_constraints('cpu-cores=4 invalid1=1 invalid2=2')
        self.assertEqual(
            'unsupported constraints: invalid1, invalid2',
            str(context_manager.exception))

    def test_invalid_string_constraints(self):
        # A ValueError is raised if an invalid string is passed.
        with self.assertRaises(ValueError) as context_manager:
            parse_constraints('arch=,cpu-cores=,')
        self.assertEqual(
            'invalid constraints: arch=,cpu-cores=,',
            str(context_manager.exception))

    def test_invalid_no_pairs(self):
        # A ValueError is raised if an invalid string is passed.
        with self.assertRaises(ValueError) as context_manager:
            parse_constraints('yo')
        self.assertEqual(
            'invalid constraints: yo',
            str(context_manager.exception))

    def test_not_key_value_pairs_constraints(self):
        # A ValueError is raised if a string doesn't have the same number of
        # tokens as '=' characters.
        with self.assertRaises(ValueError) as context_manager:
            parse_constraints('arch=1,cpu-cores')
        self.assertEqual(
            'invalid constraints: arch=1,cpu-cores',
            str(context_manager.exception))

    def test_empty_constraints_return_empty_dict(self):
        constraints = parse_constraints('')
        self.assertEqual({}, constraints)


class TestCheckConstraints(unittest.TestCase):

    def test_space_separated(self):
        constraints = 'cpu-cores=4 mem=2000 root-disk=1'
        result = check_constraints(constraints)
        self.assertTrue(result)

    def test_comma_separated(self):
        constraints = 'cpu-cores=4,mem=2000,root-disk=1'
        result = check_constraints(constraints)
        self.assertFalse(result)

    def test_invalid_separated(self):
        constraints = 'invalid=4,mem=2000,root-disk=1'
        result = check_constraints(constraints)
        self.assertFalse(result)
