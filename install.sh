#!/bin/bash

pip install -U pywin32
pip install -U pyinstaller
pip install -Ur requirements.txt

pyinstaller --clean --name gerritqueue --upx-dir /path/to/upx -F run.py
