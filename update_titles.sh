#!/bin/bash

export DJANGO_SETTINGS_MODULE="settings"

python update_titles.py

date >> .updated
