# RDS Python
## WARNING: THIS PROJECT IS IN EARLY DEVELOPMENT STAGE. CONTENT OR CODE SHOULD ONLY BE USED FOR TESTING OR EVALUATION PURPOSES.
[![Build Status](https://travis-ci.com/mtna/rds-python.svg?branch=master)](https://travis-ci.org/mtna/rds-python) 
[![Coverage Status](https://coveralls.io/repos/github/mtna/rds-python/badge.svg?branch=master&service=github)](https://coveralls.io/github/mtna/rds-python?branch=master)
[![PyPI version](https://badge.fury.io/py/mtna-rds.svg)](https://badge.fury.io/py/mtna-rds)
![Python Version](https://img.shields.io/badge/python-2.7|3.6|3.7|3.8-blue)  
[![License](https://img.shields.io/badge/license-apache_2.0-green)](https://www.apache.org/licenses/LICENSE-2.0)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://pypi.org/project/black/)
  
This python module utilizes MTNA's Rich Data Services API to quickly and efficiently access data sets and metadata stored in our repository. Through RDS, you can easily perform complex queries and tabulations on the data you are interested in while also getting back any relevant metadata.

RDS greatly simplifies the long process finding the data to begin with, cleaning and transforming the data, and converting the data into a dataframe. All of this is done in a single step using our queries. This lets you focus on the analyzing and visualizing of the data instead of managing it.  

## References
[RDS API Documentation](https://covid19.richdataservices.com/rds/swagger/) | [Examples](https://github.com/mtna/rds-python-examples) | [Contributing](CONTRIBUTING.md) | [Developer Documentation](DEVELOPER.md) | [Changelog](CHANGELOG.md)
|---|---|---|---|---|

**Contents:**  
- [Announcements](#announcements)  
- [Installation](#installation)  
- [Usage](#usage)  
- [About](#about)  
- [Software](#software)  
- [License](#license)  
    
## Announcements
### Version v0.1.2 released
This version of **RDS** Python allows you to take advantage of our powerful database framework through its select queries, tabulation queries, and metadata retrieval. All features for our query system are available through this python API.  
{release date}

## Installation
### Using pip
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rds python
```bash
pip install mtna-rds
```

## Usage
Through the **RDS** API, you care able to query for records of data as well as perform a tabulation. Both a simple query and a tabulation contain options for grouping, ordering and filtering of the data, as well as specifying if metadata is wanted or not.

The data returned by a query/tabulation will be contained within an `RdsResults` object. This object has three properties: one is the records of data that can be used to build out a dataframe for a graph or chart, one is the column names for each column of data in the records, and the last is a collection of metadata in JSON format that provides information that can be used for better analyzation of your data.

### Select Query
Imagine that you would like to get some demographic data in the United State. You look through our **Catalog** and see that we have the data you are interested in. The first thing you would need to do to access this data is to establish a link to the demographic dataset that we host in our repository. To do this, you simply create a `DataProduct` with the **ID** of the dataproduct that contains the demographic information and the **ID** of the catalog that contains the dataproduct.
```python
from rds import DataProduct

dataproduct = DataProduct("catalog_id", "dataproduct_id")
```

Once the `DataProduct` is created, you can perform your query and get back the results (which contains records in a dataframe). If you wanted to know how many people were born between the years 1900 and 1950 for each year, you could perform the following query.
```python
results = dataproduct.select(cols=["year_of_birth", "amount_born:count(*)"], where=["year_of_birth>1900"], orderby=["year_of_birth"], groupby=["year_of_birth"], limit=50)
```

This query tells **RDS** that we want the year of birth for each records as well as the number of records with that year of birth (where we are renaming the column to "amount_born"). We then filter for everyone born after 1900. We also make sure the data is in the correct order and then group the data by year of birth so that we only have a single record returned per year. Setting the limit to 50 ensures we only get date from years 1900 to 1950 (assuming there are no missing years of data).

After obtaining the data, you can pull out the records and columns and place directly into a dataframe for use in a graph or chart. Below we demonstrate by building out a simple line plot of people born per year, utilizing the pandas package.
```python
import pandas as pd

dataframe = pd.DataFrame(results.records, columns=results.columns)

sns.lineplot(data=dataframe, x=dataframe.columns[0], y=dataframe.columns[1])
plt.show()
```

### Tabulation Query
A tabulation query is used almost identically to a select query, except it uses different parameters as a tabulation is more useful for checking the relationships between columns of data

If you wanted to know the amount of male/females for each race in the census, you would perform the below tabulation query.
```python
results = dataproduct.select(dims=["sex", "race"], measure=["count(*)"], orderby=["race"], inject=True)
```

You can think of the parameter `dims` as the dimension of a tabulation table, and the parameter `measure` as the value that you want in each cell of the table. One thing you may notice that is new is the `inject` parameter. This signifies that we want to replace any "coded" values with their more readable labels. Sex can be an example of a "coded" value as many times the data is coded as "1" to refer to male and a "2" to refer to female. Since "1" and "2" would not be very descriptive in a chart, **RDS** gives you the ability to replace them with what the codes actually mean.

### Metadata
Metadata can be directly asked for on any of our resources. This includes catalogs, dataproduct, variables, classifications, and codes. The metadata contains extensive information on what the resource is and what it is used for.

## About
This project is developed and maintained by [MTNA](https://www.mtna.us/).

More detailed documentation about what the current version of RDS can do can be found [here](https://documenter.getpostman.com/view/2220438/SzS4QmXD?version=latest#intro.)

If you are interested in using the RDS framework directly, you can visit our site [here](https://www2.richdataservices.com/).

## Software
Compatible with Python 2.7 and Python 3.6 and higher.

If using python 3, it is recommended that you utilize [pandas](https://pandas.pydata.org/) dataframes when working with any records returned from an RDS query.

The are no dependencies required to run RDS Python.

## License
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
