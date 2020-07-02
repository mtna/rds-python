#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# using sys and os here ensures that we use the local RDS incase RDS has already been installed through pip
import sys, os

sys.path.insert(0, os.path.abspath(".."))
from rds import Server
import pandas as pd

server = Server("https://covid19.richdataservices.com/rds")


def test_server():
    root_catalog = server.get_root_catalog()
    assert root_catalog != None and root_catalog != ""

    info = server.get_info()
    assert info != None and info != ""

    changelog = server.get_changelog()
    assert changelog != None and changelog != ""


def test_catalog():
    catalog = server.get_catalog("us_oh")

    metadata = catalog.get_metadata()
    assert metadata != None and metadata != ""


def test_dataproduct():
    catalog = server.get_catalog("us_oh")
    dataproduct = catalog.get_dataproduct("oh_doh_cases")

    count_results = dataproduct.count()
    assert count_results != None

    select_results = dataproduct.select()
    assert select_results != None

    tabulate_results = dataproduct.tabulate(dims="sex")
    assert tabulate_results != None

    variable = dataproduct.get_variable("sex")
    assert variable != None and variable != ""

    classification = dataproduct.get_classification("sex")
    assert classification != None and classification != ""

    code = dataproduct.get_code("sex")
    assert code != None and code != ""

    profile = dataproduct.profile("sex")
    assert profile != None and profile != ""

    metadata = dataproduct.get_metadata()
    assert metadata != None and metadata != ""


server = Server("https://covid19.richdataservices.com/rds")
catalog = server.get_catalog("us_tn")
dataProduct = catalog.get_dataproduct("us_tn_doh_county")
results = dataProduct.select(limit=10000)
print(dataProduct.count())
#Plug in the data and build our line plot
df = pd.DataFrame(results.records, columns = results.columns)
print(df)
