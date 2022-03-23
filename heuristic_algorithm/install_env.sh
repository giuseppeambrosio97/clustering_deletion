#!/bin/bash
python -m pip install --upgrade pip
pip install virtualenv
python -m venv venv
source venv/bin/activate
pip install -e .