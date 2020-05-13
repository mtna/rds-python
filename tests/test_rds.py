#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from rds_library.rds_library import DataProduct

def test_select():
    dp = DataProduct('covid19', 'us_oh_doh')
    dp.select(cols=['date_stamp', 'deaths:sum(cnt_death)'], orderby=['date_stamp'], groupby=['date_stamp'], where=['date_stamp>=2020-03-01'], limit=14)

def test_tabulate():
    dp = DataProduct('covid19', 'us_oh_doh')
    dp.tabulate(dims=['date_stamp'], measure=['deaths:sum(cnt_death)'], orderby=['date_stamp'], where=['date_stamp>=2020-03-01'])

def test_metadata():
    dp = DataProduct('covid19', 'us_oh_doh')
    dp.catalog()
