#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:13:22 2020

@author: seanlucas
"""

import urllib
import sys
import json


def get_response(api_call):
    if sys.version_info > (3, 0):
        return urllib.request.urlopen(api_call)
    else:
        return urllib.urlopen(api_call)


def check_valid(api_call, message, is_json=False):
    try:
        response = get_response(api_call)
        if is_json:
            return json.load(response)
    except Exception:
        print(message)
        sys.exit
