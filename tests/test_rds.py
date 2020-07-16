#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# using sys and os here ensures that we use the local RDS incase RDS has already been installed through pip
import sys, os
sys.path.insert(0, os.path.abspath(".."))

from rds import Server

server = Server("https://covid19.richdataservices.com/rds")

# testing metadata
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
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")

    count_results = dataproduct.count()
    assert count_results != None

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

def test_batch():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(limit=100000)
    
    assert len(results.records) == dataproduct.count()
    
# testing select
def test_select_simple():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select()
    
    first_record = ["2020-01-02", "39165", "2", "40", 1, 0, 0, None]
    last_record = ["2020-01-18", "39139", "2", "40", 1, 0, 0, None]
    _assert_results(results, 35124, 8, "date_stamp", "date_stamp_death", first_record, last_record)
    
def test_select_count():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(count=True)
    assert results.count == 34570

def test_select_cols():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(cols=['date_stamp', 'age_group', 'cnt_confirmed', 'cnt_death'])
    
    first_record = ["2020-01-02","40",1,0]
    last_record = ["2020-01-18", "40", 1, 0]
    _assert_results(results, 20, 4, "date_stamp", "cnt_death", first_record, last_record)

def test_select_where():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(where=["cnt_death>0 OR cnt_confirmed>1"])
    
    first_record = ["2020-01-13", "39159", "1", "70", 1, 0, 1, None]
    last_record = [ "2020-03-01", "39043", "2", "60", 2, 0, 0, None]
    _assert_results(results, 20, 8, "date_stamp", "date_stamp_death", first_record, last_record)

def test_select_orderby():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(orderby=["cnt_confirmed DESC"])
    
    first_record = ["2020-04-16", "39101", "1", "30", 408, 0, 0, None]
    last_record = ["2020-04-18", "39129", "1", "40", 44, 0, 0, None]
    _assert_results(results, 20, 8, "date_stamp", "date_stamp_death", first_record, last_record)

def test_select_groupby():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(cols=["date_stamp", "confirmed:sum(cnt_confirmed)"], groupby="date_stamp")

    first_record = ["2020-01-02", 3]
    last_record = ["2020-02-01", 8]
    _assert_results(results, 20, 2, "date_stamp", "confirmed", first_record, last_record)

def test_select_limit_low():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(limit=5)
    
    first_record = ["2020-01-02", "39043", "2", "80", 1, 0, 0, None]
    last_record = ["2020-01-05", "39151", "1", "40", 1, 0, 0, None]
    _assert_results(results, 5, 8, "date_stamp", "date_stamp_death", first_record, last_record)
    
def test_select_limit_high():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(limit=2000)
    
    first_record = ["2020-01-02", "39043", "2", "80", 1, 0, 0, None]
    last_record = ["2020-03-20", "39049", "2", "00", 1, 0, 1, None]
    _assert_results(results, 2000, 8, "date_stamp", "date_stamp_death", first_record, last_record)

def test_select_offset_low():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(offset=5)
    
    first_record = ["2020-01-07", "39109", "2", "70", 1, 0, 0, None]
    last_record = ["2020-01-26", "39091", "1", "50", 1, 0, 0, None]
    _assert_results(results, 20, 8, "date_stamp", "date_stamp_death", first_record, last_record)

def test_select_offset_high():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(offset=2000)
    
    first_record = ["2020-03-20", "39107", "1", "70", 1, 1, 1, "2020-04-03"]
    last_record = ["2020-03-21", "39061", "2", "60", 1, 0, 1, None]
    _assert_results(results, 20, 8, "date_stamp", "date_stamp_death", first_record, last_record)

def test_select_collimit_1():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(collimit=4)
    
    first_record = ["2020-01-02", "39043", "2", "80"]
    last_record = ["2020-01-18", "39139", "2", "40"]
    _assert_results(results, 20, 4, "date_stamp", "age_group", first_record, last_record)
    
def test_select_collimit_2():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(cols=["date_stamp", "age_group"], collimit=1)
    
    first_record = ["2020-01-02"]
    last_record = ["2020-01-18"]
    _assert_results(results, 20, 1, "date_stamp", "date_stamp", first_record, last_record)

def test_select_coloffset():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(coloffset=4)
    
    first_record = [1, 0, 0, None]
    last_record = [1, 0, 0, None]
    _assert_results(results, 20, 4, "cnt_confirmed", "date_stamp_death", first_record, last_record)

def test_select_inject():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(inject=True)
    
    first_record = ["2020-01-02", "Erie County, OH", "Female", "80 years or older", 1, 0, 0, None]
    last_record = ["2020-01-18", "Richland County, OH", "Female", "40 to 49 years", 1, 0, 0, None]
    _assert_results(results, 20, 8, "date_stamp", "date_stamp_death", first_record, last_record)

def test_select_metadata():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.select(metadata=False)
    
    assert results.metadata == None
    assert results.columns == None

def test_select_complex_1():
    dataproduct = _get_dataproduct("ca", "pums_cchs_2017")
    results = dataproduct.select(cols=["VERDATE", "GEO_PRV", "avg_weight:avg(HWTDGWTK)"], orderby=["VERDATE", "GEO_PRV"], groupby=["VERDATE", "GEO_PRV"], limit=40, offset=5)
    
    first_record = ["20190913", 35, 149.9011858792734]
    last_record = ["20190913", 62, 194.9764155844158]
    _assert_results(results, 8, 3, "VERDATE", "avg_weight", first_record, last_record)
    
    return results

def test_select_complex_2():
    dataproduct = _get_dataproduct("us", "jhu_county")
    results = dataproduct.select(cols=["date_stamp", "us_county_fips", "cnt_confirmed", "cnt_death", "cnt_recovered"], orderby=["date_stamp", "us_county_fips"], where=["us_county_fips!="], limit=3000, offset=1000)
    
    first_record = [ "2020-03-22", "21015", 0, 0, 0]
    last_record = ["2020-03-23", "19137", 0, 0, 0]
    _assert_results(results, 3000, 5, "date_stamp", "cnt_recovered", first_record, last_record)
    
    return results

def test_select_complex_3():
    dataproduct = _get_dataproduct("int", "google_mobility_country")
    results = dataproduct.select(cols=["date_stamp","parks_change:avg(parks_pct)"], where=["iso3166_1=NE"],orderby=["date_stamp desc"],groupby=["date_stamp","iso3166_1"], limit=7)
    
    first_record = ["2020-07-05", 4]
    last_record = ["2020-06-29", -9.5]
    _assert_results(results, 7, 2, "date_stamp", "parks_change", first_record, last_record)
    
    return results

def test_select_complex_4():
    dataproduct = _get_dataproduct("us", "jhu_county")
    print(dataproduct.count())
    results = dataproduct.select(cols=["date_stamp", "us_county_fips", "cnt_confirmed", "cnt_death", "cnt_recovered"], orderby=["date_stamp", "us_county_fips"], count=True)
    print(results.count)
    first_record = [ "2020-03-22", "21015", 0, 0, 0]
    last_record = ["2020-03-23", "19137", 0, 0, 0]
    _assert_results(results, 332973, 5, "date_stamp", "cnt_recovered", first_record, last_record)
    
    return results

# testing tabulate
def test_tabulate_simple():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate()
    
    first_record = [34123]
    last_record = [34123]
    _assert_results(results, 1, 1, "count", "count", first_record, last_record)
    
def test_tabulate_count():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(count=True)
    
    assert results.count == 1

def test_tabulate_dims():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(dims="date_stamp")
    
    first_record = ["2020-01-02", 3]
    last_record = ["2020-07-13", 6]
    _assert_results(results, 183, 2, "date_stamp", "count", first_record, last_record)

def test_tabulate_measure():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(measure=["sum(cnt_confirmed)"])
    
    first_record = [66853]
    last_record = [66853]
    _assert_results(results, 1, 1, "sumOfCnt_confirmed", "sumOfCnt_confirmed", first_record, last_record)

def test_tabulate_where():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(where=["cnt_confirmed>1"])
    
    first_record = [8963]
    last_record = [8963]
    _assert_results(results, 1, 1, "count", "count", first_record, last_record)

def test_tabulate_orderby():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(dims=["date_stamp"], orderby=["date_stamp desc"])
    
    first_record = ["2020-07-13", 6]
    last_record = ["2020-01-02", 3]
    _assert_results(results, 183, 2, "date_stamp", "count", first_record, last_record)

def test_tabulate_groupby():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(dims=["date_stamp"], measure=["confirmed:sum(cnt_confirmed)"], groupby="date_stamp")
    
    first_record = ["2020-01-02", 3]
    last_record = ["2020-07-13", 6]
    _assert_results(results, 183, 2, "date_stamp", "confirmed", first_record, last_record)

def test_tabulate_inject():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(dims=["us_county_fips"], inject=True)
    
    first_record = ["Mahoning County, OH", 1406]
    last_record = ["Vinton County, OH", 22]
    _assert_results(results, 88, 2, "us_county_fips", "count", first_record, last_record)

def test_tabulate_metadata():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(metadata=False)
    
    assert results.metadata == None
    assert results.columns == None

def test_tabulate_totals():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    results = dataproduct.tabulate(dims=["date_stamp"], totals=True)
    
    assert results.totals[0] == [None, 34123]

def test_tabulate_complex_1():
    dataproduct = _get_dataproduct("ca", "pums_cchs_2017")
    results = dataproduct.tabulate(dims=["GEO_PRV","DHHGMS"], measure=["count:count(*)"], where=["DHH_SEX=1"], orderby=["count desc"], inject=True)
    
    first_record = ["ONTARIO", "Married", 7280]
    last_record = ["NEWFOUNDLAND AND LABRADOR", "Not stated", 1]
    _assert_results(results, 64, 3, "GEO_PRV", "count", first_record, last_record)
    
    return results

def test_tabulate_complex_2():
    dataproduct = _get_dataproduct("us", "jhu_county")
    results = dataproduct.tabulate(dims=["date_stamp", "us_state_postal"], measure=["confirmed:sum(cnt_confirmed)"], orderby=["date_stamp", "us_state_postal"], where=["us_state_postal!= and date_stamp>=2020-04-01 and date_stamp<2020-04-08"], totals=True)
    
    first_record = ["2020-04-01", "AK", 132]
    last_record = ["2020-04-07", "WY", 216]
    _assert_results(results, 385, 3, "date_stamp", "confirmed", first_record, last_record, totals=True)
    assert results.totals[0] == [None, None, 2140308]
    assert results.totals[-1] == ["2020-04-07", None, 396071]
    
    return results

def test_tabulate_complex_3():
    dataproduct = _get_dataproduct("int", "google_mobility_country")
    results = dataproduct.tabulate(dims=["date_stamp", "iso3166_1"], measure=["average_work_change:avg(workplace_pct)"], orderby=["date_stamp", "average_work_change"], where="iso3166_1=US or iso3166_1=CA or iso3166_1=MX")
    
    first_record = ["2020-02-15", "CA", -1.4166666666666667]
    last_record = ["2020-07-05", "CA", -3.0833333333333335]
    _assert_results(results, 426, 3, "date_stamp", "average_work_change", first_record, last_record)
    
    return results
    
# testing invalid usage
def test_invalid_catalog():
    server.get_catalog("wrong")
    
def test_invalid_dataproduct():
    _get_dataproduct("us_oh", "wrong")
    
def test_invalid_column_name_cols():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    select_results = dataproduct.select(cols=["ate_stamp"])
    
    assert select_results.records == []
    assert select_results.columns == []
    assert select_results.metadata == []
    
def test_invalid_column_name_dims():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    dataproduct.tabulate(dims=["ate_stamp"])
    
def test_invalid_column_name_measure():
    dataproduct = _get_dataproduct("us_oh", "oh_doh_cases")
    dataproduct.tabulate(dims=["date_stamp"], measure=["sum:sum(ate_stamp)"])
    
def _get_dataproduct(catalog_id, dataproduct_id):
    catalog = server.get_catalog(catalog_id)
    return catalog.get_dataproduct(dataproduct_id)

def _assert_results(results, cnt_records, cnt_cols, first_var, last_var, first_record, last_record, totals=False):
    # record count
    assert len(results.records) == cnt_records
    # column count
    assert len(results.records[0]) == cnt_cols
    # variables' metadata count
    assert len(results.metadata) == cnt_cols
    # first variable metadata
    assert results.metadata[0]["id"] == first_var
    # last variable metadata
    assert results.metadata[-1]["id"] == last_var
    # one column for each metadata
    assert len(results.metadata) == len(results.columns)
    # first record matches
    assert results.records[0] == first_record
    # last record matches.
    assert results.records[-1] == last_record
    # no totals
    if totals == False:
        assert results.totals == None
    # first column matches
    try:
        assert results.columns[0] == results.metadata[0]["label"]
    except KeyError:
        assert results.columns[0] == results.metadata[0]["name"]
        
    # last column matches
    try:
        assert results.columns[-1] == results.metadata[-1]["label"]
    except KeyError:
        assert results.columns[-1] == results.metadata[-1]["name"]
