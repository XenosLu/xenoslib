#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

import xenoslib
from xenoslib.extend import YamlConfig


class UnitTest(unittest.TestCase):
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

    def test_1_NestedData(self):
        data = {'a': {'b': ['c', [0, {'d': 'e'}, {'a': 'b'}]]}}
        nesteddata = xenoslib.NestedData(data)

        result = nesteddata.find_key('d')
        self.assertEqual(result, 'e')
        result = nesteddata.path
        self.assertEqual(result, "['a']['b'][1][1]['d']")

        result = nesteddata.find_value('e')
        self.assertEqual(result, {'d': 'e'})
        result = nesteddata.path
        self.assertEqual(result, "['a']['b'][1][1]['d']")

        result = nesteddata.find_keyvalue('d', 'e')
        self.assertEqual(result, {'d': 'e'})
        result = nesteddata.path
        self.assertEqual(result, "['a']['b'][1][1]['d']")

    def test_2_Singleton(self):
        class TestSingleton(xenoslib.Singleton):
            pass

        obj_a = TestSingleton()
        obj_b = TestSingleton()
        self.assertEqual(id(obj_a), id(obj_b))

    def test_3_SingletonWithArgs(self):
        class TestSingletonWithArgs(xenoslib.SingletonWithArgs):
            pass

        obj_a = TestSingletonWithArgs('a')
        obj_b = TestSingletonWithArgs('b')
        obj_c = TestSingletonWithArgs('a')
        self.assertNotEqual(id(obj_a), id(obj_b))
        self.assertEqual(id(obj_a), id(obj_c))

    def test_4_yamlconfig(self):
        config = YamlConfig()
        config2 = YamlConfig()
        data = {'a': {'b': ['c', [0, {'d': 'e'}, {'a': 'b'}]]}}
        config['data'] = data
        self.assertEqual(config2.data, data)
        self.assertEqual(id(config), id(config2))


if __name__ == '__main__':
    unittest.main()  # run all unit tests
