@echo off
set current=%~dp0
cd /d %current%
pip uninstall -y xenoslib
python setup.py develop
