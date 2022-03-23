#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from xenoslib import *


class UAMTest(unittest.TestCase):
    def setUp(self):
        """run before each test"""
        print('*' * 79)

    def tearDown(self):
        """run after each test"""
        print('*' * 79)

    @classmethod
    def setUpClass(cls):
        """run before all tests"""
        print('=' * 79)

    @classmethod
    def tearDownClass(cls):
        """run after all tests"""
        print('=' * 79)

    def test_1_nesteddata(self):
        data = {'a': {'b': ['c', [0, {'d': 'e'}]]}}

        result = NestedData(data).find_key('d')
        self.assertEqual(result, 'e')

        result = NestedData(data).find_value('e')
        self.assertEqual(result, {'d': 'e'})

        result = NestedData(data).find_keyvalue('d', 'e')
        self.assertEqual(result, {'d': 'e'})


if __name__ == '__main__':
    unittest.main()  # run all unit tests
