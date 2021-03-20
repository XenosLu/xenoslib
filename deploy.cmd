@echo off
python setup.py check
python setup.py bdist_egg
python setup.py install
