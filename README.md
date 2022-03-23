# Introduce
> Some commonly useful functions

## Requirements
- Python >= 3.5

## Download and Installation
### Install from pypi:

    pip3 install xenoslib

### Install directly from github:

    pip3 install git+https://github.com/XenosLu/xenoslib.git

# Feature lists:

- color(value, color_name='blue') - turn text with color if - windows then do nothing
- pause() - press any key to continue, support both windows and linux
- timeout(seconds) - wait seconds or press any key to continue, support both windows and linux

- del_to_recyclebin(filepath, on_fail_delete=False) - delete file to recyclebin if possible

- SingletonWithArgs  - inherit with class: allow one instance only.
- ArgMethodBase
- RestartSelfIfUpdated
- YamlConfig