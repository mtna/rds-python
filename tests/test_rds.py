#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rds import DataProduct

def test_select():
    DataProduct("http://dev.richdataservices.com", 'covid19', 'us_oh_doh')

def test_tabulate():
    DataProduct("http://dev.richdataservices.com", 'covid19', 'us_oh_doh')

def test_metadata():
    DataProduct("http://dev.richdataservices.com", 'covid19', 'us_oh_doh')
    
test_select()
test_tabulate()
test_metadata()
