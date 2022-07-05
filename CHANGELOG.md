# v0.2.18 (2022-7-1)
## Added
- `api_key` parameter to Server class, allows connecting to secure RDS host.

# v0.2.16 (2020-7-16)
## Changed
- limit defaults to `None` instead of 20

# v0.2.15 (2020-7-16)
Parameters modified and new ones added. Bugs fixed and tests created.
## Added
- `rds_format` parameter to select and tabulate queries, changes json output format
- `count` parameter to select and tabulate queries, returns row count
- `groupby` parameter to tabulate query
- returned RdsResults now has `count` and `totals` attributes
## Changed
- `include_metadata` parameter changed to `metadata`
- `limit` parameter default changed from 1000 to 20
- `measure` tabulate parameter default changed from count(*) to None
## Fixed
- query batching accounting for 10000 cell limit as opposed to row limit
## Removed
- batching queries in a tabulate query

# v0.2.14 (2020-7-08)
Modifying query parameters.
## Added
- `weights` parameter added to `select` and `tabulate` queries
## Fixed
- `inject_metadata` parameter changed to `include_metadata`

# v0.2.13 (2020-7-02)
Added additional Select parameter.
## Added
- Added `inject` parameter to inject labels into code values returned

# v0.2.12 (2020-6-30)
Bug fix.
## Fixed
- Fixed bug appending column names in results returned

# v0.2.11 (2020-6-30)
## Added
- Better error handling

# v0.2.0 (2020-6-30)
Created new classes to better encapsulate functions
## Added
- Server class for server information
- Catalog class for catalog information

# v0.1.2 (2020-5-21)
Bug fix, added more comprehensive tests.
## Fixed
- Default measure value in `tabulate()`

# v0.1.1 (2020-5-18)
Bug fix.
## Fixed
- Code metadata retrieval

# v0.1.0 (2020-5-15)
Initial commit.
## Added
- Select queries
- Tabulate queries
- Metadata retrieval
