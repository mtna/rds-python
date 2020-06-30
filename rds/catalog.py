#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains data products and catalog properties
"""
import json

from .dataproduct import DataProduct
from .utility import get_response, check_valid


class Catalog:
    """
    Holds information to connect to a catalog and allows access to its data products.
    
    Parameters
    ----------
    api : str, required
        The url hosting an RDS server.
    catalog_id : str, required
        ID of the catalog, required
    """

    def __init__(self, api, catalog_id):
        metadata = check_valid(
            api + "/api/catalog/" + catalog_id, "Invalid catalog ID", is_json=True
        )
        self.api = api
        self.catalog_id = catalog_id
        self.name = metadata["name"]
        self.description = metadata["description"]
        self.uri = metadata["uri"]
        # itll look itself up to make sure the ID exists and itll fill its description and name

    def get_dataproduct(self, dataproduct_id):
        """
        Gets a dataproduct.
        
        Parameters
        ----------
        dataproduct_id : string
            ID of the dataproduct you want.
    
        Returns
        -------
        DataProduct
            An object that can retrieve data and metadata from RDS.
        """
        return DataProduct(self.api, self.catalog_id, dataproduct_id)

    def get_metadata(self):
        """
        Gets the metadata for the catalog in JSON format.

        Returns
        -------
        metadata : JSON
            Detailed information surrounding the catalog.
        """
        api_call = self.api + "/api/catalog/" + self.catalog_id

        response = get_response(api_call)
        return json.load(response)
