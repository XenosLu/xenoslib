#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

import xenoslib
import xenoslib.dev
import xenoslib.onedrive
from xenoslib.extend import YamlConfig


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

    def test_1_NestedData(self):
        data = {"a": {"b": ["c", [0, {"d": "e"}, {"a": "b"}]], "e": []}}
        nesteddata = xenoslib.NestedData(data)

        result = nesteddata.find_key("d")
        self.assertEqual(result, "e")
        result = nesteddata.path
        self.assertEqual(result, "['a']['b'][1][1]['d']")

        result = nesteddata.find_value("e")
        self.assertEqual(result, {"d": "e"})
        result = nesteddata.path
        self.assertEqual(result, "['a']['b'][1][1]['d']")

        result = nesteddata.find_keyvalue("d", "e")
        self.assertEqual(result, {"d": "e"})
        result = nesteddata.path
        self.assertEqual(result, "['a']['b'][1][1]['d']")

        results = nesteddata.find_any_keyvalues("e")
        results = list(results)
        result = nesteddata.find_values("e")
        self.assertEqual(results[0], list(result)[0])
        result = nesteddata.find_keys("e")
        self.assertEqual(results[1], list(result)[0])

    def test_2_Singleton(self):
        class TestSingleton(xenoslib.Singleton):
            pass

        obj_a = TestSingleton()
        obj_b = TestSingleton()
        self.assertEqual(id(obj_a), id(obj_b))

    def test_3_SingletonWithArgs(self):
        class TestSingletonWithArgs(xenoslib.SingletonWithArgs):
            pass

        obj_a = TestSingletonWithArgs("a")
        obj_b = TestSingletonWithArgs("b")
        obj_c = TestSingletonWithArgs("a")
        self.assertNotEqual(id(obj_a), id(obj_b))
        self.assertEqual(id(obj_a), id(obj_c))

    def test_4_monkey_patch(self):
        self.assertNotEqual(xenoslib.__version__, "injected version")
        xenoslib.monkey_patch("xenoslib", "__version__", "injected version")
        self.assertEqual(xenoslib.about.__version__, "injected version")
        self.assertEqual(xenoslib.__version__, "injected version")

    def test_5_yamlconfig(self):
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


if __name__ == "__main__":
    unittest.main()  # run all unit tests
