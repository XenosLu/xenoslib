@echo off
set current=%~dp0
cd /d %current%

python setup.py develop
