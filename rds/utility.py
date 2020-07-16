#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:13:22 2020

@author: seanlucas
"""

import sys
import json


def get_response(api_call, message=""):
    if sys.version_info > (3, 0):
        import urllib.request

        try:
            return urllib.request.urlopen(api_call)
        except urllib.error.HTTPError as e:
            print(e)
            print(message)
            sys.exit()
    else:
        import urllib

        try:
            return urllib.urlopen(api_call)
        except urllib.HTTPError as e:
            print(e)
            print(message)
            sys.exit()


def check_valid(api_call, message, is_json=False):
    try:
        response = get_response(api_call, message=message)
        if is_json:
            return json.load(response)
    except Exception as e:
        print(e)
        print(message)
        sys.exit()
