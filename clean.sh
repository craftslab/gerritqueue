#!/bin/bash

chmod 644 .gitignore
chmod 644 LICENSE MANIFEST.in README.md requirements.txt setup.cfg
chmod 644 setup.py run.py

find gerritqueue tests -name "*.json" -exec chmod 644 {} \;
find gerritqueue tests -name "*.py" -exec chmod 644 {} \;
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "*.sh" -exec chmod 755 {} \;
find . -name "__pycache__" -exec rm -rf {} \;
