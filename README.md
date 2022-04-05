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

turn text with color if - windows then do nothing

`usage: color(value, color_name='blue')`

sample:
```
>>> import xenoslib
>>> xenoslib.color('blue')
'\x1b[1;34mblue\x1b[0m'
>>> print(xenoslib.color('blue'))
blue  # only turn blue in linux, in windows it will do nothing
```

to-do:

Finish the following docs...

- pause() - press any key to continue, support both windows and linux
- timeout(seconds) - wait seconds or press any key to continue, support both windows and linux
- del_to_recyclebin(filepath, on_fail_delete=False) - delete file to recyclebin if possible
- SingletonWithArgs  - inherit with class: allow one instance only.
- ArgMethodBase


### extend

    import xenoslib.extend

- YamlConfig


### dev

- RestartWhenModified()



