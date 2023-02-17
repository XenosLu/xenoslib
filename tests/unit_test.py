#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

import xenoslib
import xenoslib.dev
import xenoslib.onedrive
from xenoslib.extend import YamlConfig
from xenoslib import NestedData


class UnitTest(unittest.TestCase):
    def setUp(self):
        """run before each test"""
        print("*" * 79)

    def tearDown(self):
        """run after each test"""
        print("*" * 79)

    @classmethod
    def setUpClass(cls):
        """run before all tests"""
        print("=" * 79)

    @classmethod
    def tearDownClass(cls):
        """run after all tests"""
        print("=" * 79)

    def test_Singleton(self):
        class TestSingleton(xenoslib.Singleton):
            pass

        obj_a = TestSingleton()
        obj_b = TestSingleton()
        self.assertEqual(id(obj_a), id(obj_b))

    def test_SingletonWithArgs(self):
        class TestSingletonWithArgs(xenoslib.SingletonWithArgs):
            pass

        obj_a = TestSingletonWithArgs("a")
        obj_b = TestSingletonWithArgs("b")
        obj_c = TestSingletonWithArgs("a")
        self.assertNotEqual(id(obj_a), id(obj_b))
        self.assertEqual(id(obj_a), id(obj_c))

    def test_monkey_patch(self):
        self.assertNotEqual(xenoslib.__version__, "injected version")
        xenoslib.monkey_patch("xenoslib", "__version__", "injected version")
        self.assertEqual(xenoslib.about.__version__, "injected version")
        self.assertEqual(xenoslib.__version__, "injected version")

    def test_yamlconfig(self):
        config = YamlConfig()
        config2 = YamlConfig()
        config3 = YamlConfig("new.yml")
        data = {"a": {"b": ["c", [0, {"d": "e"}, {"a": "b"}]]}}
        config["data"] = data
        self.assertEqual(
            str(config), "data:\n  a:\n    b:\n    - c\n    - - 0\n      - d: e\n      - a: b\n"
        )
        self.assertEqual(config2.data, data)
        self.assertEqual(id(config), id(config2))
        self.assertNotEqual(id(config), id(config3))


class TestNestedData(unittest.TestCase):
    def setUp(self):
        self.data = {"a": 1, "b": {"c": 2, "d": [3, 4, {"e": 5}]}, "f": (6, 7, {"g": 8})}

    def test_find_keys(self):
        nd = NestedData(self.data)
        result = list(nd.find_keys("c"))
        self.assertEqual(result, [({"c": 2, "d": [3, 4, {"e": 5}]}, "['b']['c']")])

    def test_find_values(self):
        nd = NestedData(self.data)
        result = list(nd.find_values(5))
        self.assertEqual(result, [({"e": 5}, "['b']['d'][2]['e']")])

    def test_find_keyvalues(self):
        nd = NestedData(self.data)
        result = list(nd.find_keyvalues("c", 2))
        self.assertEqual(result, [({"c": 2, "d": [3, 4, {"e": 5}]}, "['b']['c']")])

    def test_find_any_keyvalues(self):
        nd = NestedData(self.data)
        result = list(nd.find_any_keyvalues("c"))
        self.assertEqual(result, [({"c": 2, "d": [3, 4, {"e": 5}]}, "['b']['c']")])
        result = list(nd.find_any_keyvalues("g"))
        self.assertEqual(result, [({"g": 8}, "['f'][2]['g']")])

    def test_find_any(self):
        nd = NestedData(self.data)
        result = nd.find_any(5)
        self.assertEqual(result, {"e": 5})

    def test_find_key(self):
        nd = NestedData(self.data)
        result = nd.find_key("c")
        self.assertEqual(result, 2)

    def test_find_value(self):
        nd = NestedData(self.data)
        result = nd.find_value(5)
        self.assertEqual(result, {"e": 5})

    def test_find_keyvalue(self):
        nd = NestedData(self.data)
        result = nd.find_keyvalue("c", 2)
        self.assertEqual(result, {"c": 2, "d": [3, 4, {"e": 5}]})


if __name__ == "__main__":
    unittest.main()  # run all unit tests
