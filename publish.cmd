@echo off
REM python setup.py sdist
set current=%~dp0
cd /d %current%

python setup.py develop
python tests\unit_test.py || goto :END

rd /s /q dist
python -m build
twine upload dist/*

:END
pause
REM python setup.py sdist upload -r pypi
