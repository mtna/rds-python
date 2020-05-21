#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# using sys and os here ensures that we use the local RDS incase RDS has already been installed through pip
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from rds import DataProduct


def test_select():
    DataProduct('https://covid19.richdataservices.com', 'us_oh', 'oh_doh')
#    results = dp.select(cols=['sex', 'sum(cnt_death)'], where='sex=male', orderby=['sum(cnt_death)'], groupby=['sex'])
#    assert results.records is not None
#    assert results.columns is not None
#    assert results.metadata is not None

#def test_tabulate():
#    dp = DataProduct('https://covid19.richdataservices.com', 'us_oh', 'oh_doh')
#    results = dp.tabulate(dims=['sex'], measure=['deaths:sum(cnt_death)'])
#    assert results.records is not None
#    assert results.columns is not None
#    assert results.metadata is not None

#def test_metadata_catalog():
#    dp = DataProduct('https://covid19.richdataservices.com', 'us_oh', 'oh_doh')
#    metadata = dp.catalog()
#    assert len(metadata) > 0

#def test_metadata_variables():
#    dp = DataProduct('https://covid19.richdataservices.com', 'us_oh', 'oh_doh')
#    metadata = dp.variable()
#    assert len(metadata) > 0
    
#def test_metadata_profile():
#    dp = DataProduct('https://covid19.richdataservices.com', 'us_oh', 'oh_doh')
#    metadata = dp.profile('sex')
#    assert len(metadata) > 0
    
#def test_metadata_classification():
#    dp = DataProduct('https://covid19.richdataservices.com', 'us_oh', 'oh_doh')
#    metadata = dp.classification('sex')
#    assert len(metadata) > 0
    
#def test_metadata_code():
#    dp = DataProduct('https://covid19.richdataservices.com', 'us_oh', 'oh_doh')
#    metadata = dp.code('sex')
#    assert len(metadata) > 0
