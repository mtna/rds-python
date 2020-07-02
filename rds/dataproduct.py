#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retrieves data and metadata from RDS.
"""

# Built-in/Generic Imports
import sys
import urllib
import json

from .utility import get_response, check_valid


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

    def __init__(self, api, catalog_id, dataproduct_id):
        metadata = check_valid(
            api + "/api/catalog/" + catalog_id + "/" + dataproduct_id,
            "Invalid dataproduct ID",
            is_json=True,
        )
        self.api = api
        self.catalog_id = catalog_id
        self.dataproduct_id = dataproduct_id
        self.name = metadata["name"]
        self.description = metadata["description"]
        self.last_update = metadata["lastUpdate"]
        self.uri = metadata["uri"]
        self.param_delim = ""
        # itll look itself up to make sure the ID exists and itll fill its description and name

    def count(self):
        """
        Gets the count of records

        Returns
        -------
        int
            The record count.

        """
        api_call = self._get_url("query") + "/count"
        response = get_response(api_call)
        return json.load(response)

    def select(
        self,
        cols=None,
        where=None,
        orderby=None,
        groupby=None,
        collimit=1000,
        coloffset=0,
        inject_metadata=True,
        inject=False,
        totals=False,
        limit=1000,
        offset=0,
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
        inject_metadata : bool, optional
            flag for if metadata should be used/returned with the data frame. The default is True.
        inject : bool, optional
            flag for if the code labels should be used over the code values. The default is False.
        totals : bool, optional
            flag for if the totals should be returned with the data frame. The default is False.
        limit : int, optional
            limit for the records in the data frame. The default is 1000.
        offset : int, optional
            offset for the records in the data frame. The default is 0.

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
        params.update(self._get_param([str(inject_metadata).lower()], "metadata"))
        params.update(self._get_param([str(inject).lower()], "inject"))
        params.update(self._get_param(totals, "totals"))

        results = self._batch(api_call, params, limit, offset)
        self.param_delim = ""

        metadata = None
        if inject_metadata:
            metadata = _get_metadata(results)

        return _get_rds_results(results, metadata, cols)

    def tabulate(
        self,
        dims=None,
        measure=["count(*)"],
        where=None,
        orderby=None,
        totals=False,
        inject_metadata=True,
        inject=False,
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
        totals : bool, optional
            flag for if the totals should be returned with the data frame. The default is False.
        inject_metadata : bool, optional
            flag for if metadata should be used/returned with the data frame. The default is True.
        inject : bool, optional
            flag for if the code labels should be used over the code values. The default is False.

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
        params.update(self._get_param([str(inject_metadata).lower()], "metadata"))
        params.update(self._get_param([str(inject).lower()], "inject"))
        params.update(self._get_param([str(totals).lower()], "totals"))

        results = self._batch(api_call, params)
        self.param_delim = ""

        metadata = None
        if inject_metadata:
            metadata = _get_metadata(results)

        return _get_rds_results(results, metadata, dims + measure)

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

        response = get_response(api_call)
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

        response = get_response(api_call)
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

        # must use different methods depending on python version 3.X vs 2.X
        if sys.version_info > (3, 0):
            api_call += urllib.parse.urlencode(params)
        else:
            api_call += urllib.urlencode(params)

        response = get_response(api_call)
        return json.load(response)

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

        response = get_response(api_call)
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

        response = get_response(api_call)
        return json.load(response)

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

    def _batch(self, api_call, params, limit=10000, offset=0):
        results = []

        first_pass = True
        more_rows = True
        while (first_pass or more_rows) and limit > 0:
            first_pass = False
            api_call_copy = api_call
            params.update(self._get_param(offset, "offset"))

            if limit > 500:
                params.update(self._get_param(500, "limit"))
                offset += 500
                limit -= 500
            else:
                params.update(self._get_param(limit, "limit"))
                limit = 0

            # must use different methods depending on python version 3.X vs 2.X
            if sys.version_info > (3, 0):
                api_call_copy += urllib.parse.urlencode(params)
            else:
                api_call_copy += urllib.urlencode(params)

            response = get_response(api_call_copy)
            result = json.load(response)
            results.append(result)

            more_rows = result["info"]["moreRows"]

        return results


class RdsResults:
    """A wrapper object that binds the records, the column names, and metadata on the columns together."""

    def __init__(self, records, columns, metadata):
        self.records = records
        self.columns = columns
        self.metadata = metadata


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


def _get_rds_results(results, metadata, columns):
    col_names = []
    if metadata is not None:
        for var_name in metadata.keys():
            col_names.append(var_name)
    else:
        for column in columns:
            col_names.append(column)

    records = []
    for result in results:
        for record in result["records"]:
            records.append(record)

    return RdsResults(records, col_names, list(metadata.values()))
