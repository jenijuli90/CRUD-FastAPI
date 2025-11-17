#!/bin/bash
# Install Microsoft ODBC Driver 17 for SQL Server on Ubuntu

# Add Microsoft repository key
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Add Microsoft SQL Server Ubuntu repository
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Update package lists
apt-get update

# Install ODBC driver and unixODBC development files
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev