#!/bin/bash

export DJANGO_SETTINGS_MODULE="settings"

python update_rp.py

date >> .updated
