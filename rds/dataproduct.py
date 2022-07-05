#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retrieves data and metadata from RDS.
"""

# Built-in/Generic Imports
import sys
import json
import math

from .utility import get_response, check_valid


#TODO pass api key to util methods
class DataProduct:
    """
    Holds information to connect to a data product and allows methods for querying it.
    
    Parameters
    ----------
    api : str, required
        The url hosting an RDS server
    catalog_id : str, required
        ID of the catalog, required
    dataproduct_id : str, optional
        ID of the data product. Default is None
    """

    def __init__(self, api, api_key, catalog_id, dataproduct_id):
        metadata = check_valid(
            api + "/api/catalog/" + catalog_id + "/" + dataproduct_id,
            api_key, "Invalid dataproduct ID",
            is_json=True,
        )
        self.api = api
        self.api_key = api_key
        self.catalog_id = catalog_id
        self.dataproduct_id = dataproduct_id
        self.name = metadata["name"]
        self.description = metadata["description"]
        self.last_update = metadata["lastUpdate"]
        self.uri = metadata["uri"]

    def count(self):
        """
        Gets the count of records

        Returns
        -------
        int
            The record count.

        """
        api_call = self._get_url("query") + "/count"
        response = get_response(api_call, self.api_key)
        return json.load(response)

    def select(
        self,
        cols=None,
        where=None,
        orderby=None,
        groupby=None,
        collimit=None,
        coloffset=0,
        weights=None,
        metadata=True,
        inject=False,
        count=False,
        limit=None,
        offset=0,
        rds_format=None,
    ):
        """
        Queries the data product for a set of records.

        Parameters
        ----------
        cols : list of str, required
            the columns of the records to be returned. The default is None which queries for all columns.
        where : list of str, optional
            filtering by comparative and conjunctive operators. The default is None.
        orderby : list of str, optional
            orders the records by a one or more columns. The default is None.
        groupby : list of str, optional
            groups the records by one or more columns. The default is None.
        collimit : int, optional
            limit of the columns in the data frame. The default is 1000.
        coloffset : int, optional
            offset of the columns in the data frame. The default is 0.
        weights : list of str, optional
            columns to be weighed. The default is None.
        metadata : bool, optional
            flag for if metadata should be used/returned with the data frame. Setting this to false will also cause no column names to return in the results. The default is True.
        inject : bool, optional
            flag for if the code labels should be used over the code values. The default is False.
        count : bool, optional
            flag for returning the record count in the info. The default is False.
        limit : int, optional
            limit for the records in the data frame. The default is 1000.
        offset : int, optional
            offset for the records in the data frame. The default is 0.
        rds_format : string, optional
            the format of the json object returned. The default is mtna_simple.

        Returns
        -------
        results : object
            A wrapper object for the dataframe and metadata.

        """
        api_call = self._get_url("query") + "/select?"
        params = {}
        params.update(self._get_param(cols, "cols"))
        params.update(self._get_param(where, "where"))
        params.update(self._get_param(orderby, "orderby"))
        params.update(self._get_param(groupby, "groupby"))
        params.update(self._get_param(collimit, "collimit"))
        params.update(self._get_param(coloffset, "coloffset"))
        params.update(self._get_param(weights, "weights"))
        params.update(self._get_param(rds_format, "format"))
        params.update(self._get_param(str(metadata).lower(), "metadata"))
        params.update(self._get_param(str(inject).lower(), "inject"))
        params.update(self._get_param(str(count).lower(), "count"))

        max_records = limit
        col_count = self._get_column_count(cols, collimit)
        if limit == None or limit * col_count > 10000:
            limit = math.floor(10000 / col_count)

        results = self._batch(api_call, params, max_records, limit, offset)

        metadata_json = None
        if metadata:
            metadata_json = _get_metadata(results)

        count_value = None
        if count:
            count_value = results[0]["info"]["rowCount"]

        return _get_rds_results(results, metadata_json, count_value)

    def tabulate(
        self,
        dims=None,
        measure=None,
        where=None,
        orderby=None,
        groupby=None,
        weights=None,
        totals=False,
        metadata=True,
        inject=False,
        count=False,
        rds_format=None,
    ):
        """
        Queries the data product for a set of tabulated records.

        Parameters
        ----------
        dims : list of str, required
            dimensions of the tabulation, represents the rows and table of table. Default is None.
        measure : list of str, optional
            value the tabulation is calculating from the measures, represents the values in the
            cells of a table. The default is count(*).
        where : list of str, optional
            filtering by comparative and conjunctive operators. The default is None.
        orderby : list of str, optional
            orders the records by one or more columns. The default is None.
        groupby : list of str, optional
            groups the records by one or more columns. The default is None.
        weights : list of str, optional
            columns to be weighed. The default is None.
        totals : bool, optional
            flag for if the totals should be returned with the data frame. The default is False.
        metadata : bool, optional
            flag for if metadata should be used/returned with the data frame. The default is True.
        inject : bool, optional
            flag for if the code labels should be used over the code values. The default is False.
        count : bool, optional
            flag for returning the record count in the info. The default is False.
        rds_format : string, optional
            the format of the json object returned. The default is mtna_simple.

        Returns
        -------
        results : object
            A wrapper object for the dataframe and metadata.
        """
        api_call = self._get_url("query") + "/tabulate?"
        params = {}
        params.update(self._get_param(dims, "dims"))
        params.update(self._get_param(measure, "measure"))
        params.update(self._get_param(where, "where"))
        params.update(self._get_param(orderby, "orderby"))
        params.update(self._get_param(groupby, "groupby"))
        params.update(self._get_param(weights, "weights"))
        params.update(self._get_param(rds_format, "format"))
        params.update(self._get_param(str(metadata).lower(), "metadata"))
        params.update(self._get_param(str(inject).lower(), "inject"))
        params.update(self._get_param(str(totals).lower(), "totals"))
        params.update(self._get_param(str(count).lower(), "count"))

        results = [_query(api_call, self.api_key, params)]

        metadata_json = None
        if metadata:
            metadata_json = _get_metadata(results)

        count_value = None
        if count:
            count_value = results[0]["info"]["rowCount"]

        return _get_rds_results(results, metadata_json, count_value)

    def get_variable(self, variable=None):
        """
        Gets the metadata for one or more variables in JSON format.

        Parameters
        ----------
        variable : list of str, optional
            A list of variable names you want the metadata of. The default is None which
            will return metadata for all variables.

        Returns
        -------
        metadata : JSON
            Detailed information surrounding the variable(s).

        """
        api_call = self._get_url("catalog")
        if variable is None:
            api_call += "/variables"
        else:
            api_call += "/variable/" + variable

        response = get_response(api_call, self.api_key)
        return json.load(response)

    def get_classification(self, classification=None):
        """
        Gets the metadata for one or more classifications in JSON format.

        Parameters
        ----------
        classification : list of str, optional
            A list of classification names you want the metadata of. The default is None which
            will return metadata for all classifications.

        Returns
        -------
        metadata : JSON
            Detailed information surrounding the classification(s).

        """
        api_call = self._get_url("catalog")
        if classification is None:
            api_call += "/classifications"
        else:
            api_call += "/classification/" + classification

        response = get_response(api_call, self.api_key)
        return json.load(response)

    def get_code(self, classification, limit=20):
        """
        Gets the metadata for codes in JSON format.

        Parameters
        ----------
        classification : str
            The name of the classification you want the codes' metadata of.
        limit : int, optional
            The amount of codes you want returned. The default is 20.

        Returns
        -------
        metadata : JSON
            Detailed information surrounding the code(s).

        """
        api_call = (
            self._get_url("catalog") + "/classification/" + classification + "/codes?"
        )
        params = {}
        params.update(self._get_param(limit, "limit"))

        return _query(api_call, self.api_key, params)

    def profile(self, variable):
        """
        Gets a profile on a variable that contains statistical information.

        Parameters
        ----------
        variable : str
            The name of the variable you want the profile of.

        Returns
        -------
        profile : JSON
            Detailed information surrounding a profile on a variable.

        """
        api_call = self._get_url("catalog") + "/variables/profile?cols=" + variable

        response = get_response(api_call, self.api_key)
        return json.load(response)

    def get_metadata(self):
        """
        Gets the metadata for the dataproduct in JSON format.

        Returns
        -------
        metadata : JSON
            Detailed information surrounding the dataproduct.

        """
        api_call = self._get_url("catalog")

        response = get_response(api_call, self.api_key)
        return json.load(response)

    def _get_column_count(self, cols, collimit):
        col_count = None
        if cols == None:
            col_count_api_call = self._get_url("query") + "/select?"
            col_count_params = {}
            col_count_params.update(self._get_param(1, "limit"))

            col_count_results = _query(col_count_api_call, self.api_key, col_count_params)
            col_count = len(col_count_results["records"][0])
        else:
            col_count = len(cols)
            
        if collimit == None:
            return col_count
        else:
            return col_count if col_count < collimit else collimit

    def _get_url(self, endpoint):
        if self.catalog_id is None:
            raise ValueError("Catalog ID must be specified")

        if self.dataproduct_id is None:
            raise ValueError("Data Product ID must be specified")

        return (
            self.api
            + "/api/"
            + endpoint
            + "/"
            + self.catalog_id
            + "/"
            + self.dataproduct_id
        )

    def _get_param(self, param_values, param_name):
        if param_values is not None:
            param = ""
            if type(param_values) is list:
                value_delim = ""
                for param_value in param_values:
                    param += value_delim + str(param_value)
                    value_delim = ","
            else:
                param = str(param_values)

            return {param_name: param}
        else:
            return {}

    def _batch(self, api_call, params, max_records, limit, offset=0):
        results = []

        first_pass = True
        more_rows = True
        while (first_pass or more_rows) and (max_records == None or max_records > 0):
            first_pass = False
            api_call_copy = api_call
            params.update(self._get_param(offset, "offset"))

            if max_records == None:
                params.update(self._get_param(limit, "limit"))
                offset += limit
            else:
                if max_records > limit:
                    params.update(self._get_param(limit, "limit"))
                    offset += limit
                    max_records -= limit
                else:
                    params.update(self._get_param(max_records, "limit"))
                    max_records = 0

            result = _query(api_call_copy, self.api_key, params)
            results.append(result)

            more_rows = result["info"]["moreRows"]

        return results


class RdsResults:
    """A wrapper object that binds the records, the column names, and metadata on the columns together."""

    def __init__(self, records, columns, metadata, totals=None, count=None):
        self.records = records
        self.columns = columns
        self.metadata = metadata
        self.totals = totals
        self.count = count


def _get_metadata(results):
    metadata = {}
    for result in results:
        for variable in result["variables"]:
            var_name = ""
            try:
                var_name = variable["label"]
            except KeyError:
                var_name = variable["name"]

            metadata[var_name] = variable

    return metadata


def _query(api_call, api_key, params):
    if sys.version_info > (3, 0):
        import urllib.parse

        api_call += urllib.parse.urlencode(params)
    else:
        import urllib

        api_call += urllib.urlencode(params)

    response = get_response(api_call, api_key)
    return json.load(response)


def _get_rds_results(results, metadata_json, count):
    col_names = None
    metadata = None
    if metadata_json is not None:
        col_names = []
        for var_name in metadata_json.keys():
            col_names.append(var_name)
        metadata = list(metadata_json.values())

    records = []
    totals = None
    for result in results:
        for record in result["records"]:
            records.append(record)
        if result["totals"] != None and result["totals"] != []:
            if totals == None:
                totals = []
            for total in result["totals"]:
                totals.append(total)

    return RdsResults(records, col_names, metadata, totals, count)
