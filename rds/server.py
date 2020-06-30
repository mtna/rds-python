#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains server properties and hosts catalogs and dataproducts
"""

import json

from .catalog import Catalog
from .utility import get_response


class Server:
    """
    Holds information to connect to a server hosting Rich Data Services (RDS).
    
    Parameters
    ----------
    domain : str, required
        The RDS server domain name
    protocol: str, optional
        The network protocol, defaults to https
    path: str, optional
        The RDS path, defaults to /rds
    port: str, optional
        The port, defaults to None
    """

    def __init__(self, domain, protocol="https", path="/rds", port=None):
        api = domain
        if "http" not in domain:
            api = protocol + "://" + api
        port = "" if port == None else (":" + port)
        if port not in domain:
            api += port
        if path not in domain:
            api += path

        self.api = api

    def get_catalog(self, catalog_id):
        """
        Gets a catalog.
        
        Parameters
        ----------
        catalog_id : string
            ID of the catalog you want.
    
        Returns
        -------
        Catalog
            An object that contains data products and catalog properties.
        """
        return Catalog(self.api, catalog_id)

    def get_root_catalog(self):
        """
        Gets the root catalog that holds a list of all catalogs and data products along with their descriptive metadata. This provides the user an entry point into an application.

        Returns
        -------
        JSON
            The root catalog.
        """
        return json.load(get_response(self.api + "/api/catalog"))

    def get_changelog(self):
        """
        Gets the changelog that describes all additions/removals/fixes listed on the date they were made.

        Returns
        -------
        JSON
            The changelog.

        """
        return json.load(get_response(self.api + "/api/server/info"))

    def get_info(self):
        """
        Gets information about the server.

        Returns
        -------
        JSON
            Server information.

        """
        return json.load(get_response(self.api + "/api/server/changelog"))
