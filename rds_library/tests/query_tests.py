#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:41:16 2020

@author: seanlucas
"""

#%%
import sys
sys.path.append('..')
from rds_library.rds_library import DataProduct

dp = DataProduct('covid19', 'us_oh_doh')
results = dp.select(cols=['date_stamp', 'deaths:sum(cnt_death)'], orderby=['date_stamp'], groupby=['date_stamp'], where=['date_stamp>=2020-03-01'], limit=14)
print(results.records)
print(results.columns)
print(results.metadata)
#%%
import sys
sys.path.append('..')
from rds_library.rds_library import DataProduct

dp = DataProduct('covid19', 'us_oh_doh')
results = dp.tabulate(dims=['date_stamp'], measure=['deaths:sum(cnt_death)'], orderby=['date_stamp'], where=['date_stamp>=2020-03-01'])
print(results.records)
#%%
import json
import sys
sys.path.append('..')
from rds_library.rds_library import DataProduct

dp = DataProduct('covid19', 'us_oh_doh')
print(json.dumps(dp.catalog(), indent=1))
#%%
import sys
sys.path.append('..')
from rds_library.rds_library import DataProduct

dp = DataProduct('covid19', 'us_oh_doh')
results = dp.select(cols=['dat_stamp', 'deaths:sum(cntdeath)'], orderby=['date_stamp'], groupby=['date_stamp'], where=['date_stamp>=2020-03-01'], limit=14)
print(results.records)
