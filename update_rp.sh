#!/bin/bash

export DJANGO_SETTINGS_MODULE="settings"

~/.virtualenvs/rp/bin/python update_rp.py

date >> .updated
