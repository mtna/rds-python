#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:13:22 2020

@author: seanlucas
"""

import sys
import json


#TODO add api key header
def get_response(api_call, api_key, message=""):
    if sys.version_info > (3, 0):
        import urllib.request

        try:
            request = urllib.request.Request(api_call)
            if (api_key is not None):
                request.add_header('X-API-KEY', api_key)
            response = urllib.request.urlopen(request)
            
            if (response.getcode() != 200):
                raise Exception("Error making call [" + api_call + "], response code [" + response.getcode() + "].")
            
            return response
        except urllib.error.HTTPError as e:
            print(e)
            print(message)
            sys.exit()
    else:
        import urllib

        try:
            request = urllib.Request(api_call)
            if (api_key is not None):
                request.add_header('X-API-KEY', api_key)
            response = urllib.urlopen(api_call)
            
            if (response.getcode() != 200):
                raise Exception("Error making call [" + api_call + "], response code [" + response.getcode() + "].")
            
            return response
        except urllib.HTTPError as e:
            print(e)
            print(message)
            sys.exit()


def check_valid(api_call, api_key, message, is_json=False):
    try:
        response = get_response(api_call, api_key, message=message)
        if is_json:
            return json.load(response)
    except Exception as e:
        print(e)
        print(message)
        sys.exit()
