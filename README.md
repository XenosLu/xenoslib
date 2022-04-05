#
## Introduce
[![Python CI](https://github.com/XenosLu/xenoslib/actions/workflows/main.yml/badge.svg)](https://github.com/XenosLu/xenoslib/actions/workflows/main.yml)

This project include some common codes.

## Requirements
- Python >= 3.6

## Installation
### Install from pypi

    pip3 install xenoslib

### Install directly from github

    pip3 install git+https://github.com/XenosLu/xenoslib.git

## Use

### base features

```
>>> from xenoslib import sleep
>>> sleep(5)
ETA 5/4  s
```

```
import xenoslib
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
```


```
class TestSingleton(xenoslib.Singleton):
    pass

obj_a = TestSingleton()
obj_b = TestSingleton()
self.assertEqual(id(obj_a), id(obj_b))
```
```
class TestSingletonWithArgs(xenoslib.SingletonWithArgs):
    pass

obj_a = TestSingletonWithArgs('a')
obj_b = TestSingletonWithArgs('b')
obj_c = TestSingletonWithArgs('a')
self.assertNotEqual(id(obj_a), id(obj_b))
self.assertEqual(id(obj_a), id(obj_c))
```

```
self.assertNotEqual(xenoslib.__version__, 'injected version')
xenoslib.monkey_patch('xenoslib', '__version__', 'injected version')
self.assertEqual(xenoslib.version.__version__, 'injected version')
self.assertEqual(xenoslib.__version__, 'injected version')
```


### extend

```
from xenoslib.extend import YamlConfig
config = YamlConfig()
config2 = YamlConfig()
data = {'a': {'b': ['c', [0, {'d': 'e'}, {'a': 'b'}]]}}
config['data'] = data
self.assertEqual(config2.data, data)
self.assertEqual(id(config), id(config2))
```

### dev

- RestartWhenModified()

to-do:

Finish the following docs...
NestedData
- pause() - press any key to continue, support both windows and linux
- timeout(seconds) - wait seconds or press any key to continue, support both windows and linux
- del_to_recyclebin(filepath, on_fail_delete=False) - delete file to recyclebin if possible


