@echo off
REM python setup.py sdist
set current=%~dp0
cd /d %current%

flake8 . --count --max-complexity=10 --max-line-length=127 --statistics || goto :END
python tests\unit_test.py || goto :END

rd /s /q dist
python -m build
twine upload dist/*

:END
pause
REM python setup.py sdist upload -r pypi
