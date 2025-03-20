# carDataProject

Install PIP Packages:
pip install pyodbc
pip install numpy

Create DB and table using TableDeclaration.txt

Using car.dev api as data source with a free API key
https://www.auto.dev/docs

Using Python to invoke endpoints which returns 20 rows per call. Loop through all pages and write the values to a SQL tables
Endpoints used:
'auto.dev/api/listings' - getListings.py
'auto.dev/api/vin'

The api is not unique on the ID for each car listing so there can be duplicates rows (about 16%) with the same ID.

This will give us the source data we need.
Pull this data into Power BI
Sanitize removing any troublesome rows or data issues
