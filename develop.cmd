@echo off
set current=%~dp0
cd /d %current%
pip install pywin32
pip uninstall -y xenoslib
python setup.py develop
