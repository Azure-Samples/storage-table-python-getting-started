---
services: storage
platforms: python
author: dineshmurthy
---

# Azure Storage: Getting Started with Azure Storage in Python
This demo demonstrates how to perform common tasks using Azure Table storage 
and Azure Cosmos DB Table API including creating a table, CRUD operations, 
batch operations and different querying techniques. 

If you don't have a Microsoft Azure subscription you can get a FREE trial 
account [here](http://go.microsoft.com/fwlink/?LinkId=330212)

##Minimum Requirements & Install Instructions
Python 2.7, 3.3, or 3.4.
To install Python, please go to https://www.python.org/downloads/

Please run 'pip install -r requirements.txt' to set up the Python environment.

## Running this sample

### Azure Cosmos DB Table API

1. Go to your Azure Cosmos DB Table API instance in the Azure Portal and select 
"Connection String" in the menu, select the Read-write Keys tab and copy the value 
in the "CONNECTION STRING" field.
2. Open config.py and set IS\_EMULATED to False and set STORAGE\_CONNECTION\_STRING to the
connection string value from the previous step.
3. Run 'python start.py'

#### More Information
-[Introduction to Azure Cosmos DB Table API](https://docs.microsoft.com/en-us/azure/cosmos-db/table-introduction)

### Azure Table Storage

This sample can be run using either the Azure Storage Emulator or with your 
Azure Storage account by updating the config.properties file with your 
connection string.

To run the sample using the Storage Emulator (Only available on Microsoft 
Windows OS):

1. Download and install the Azure Storage Emulator https://azure.microsoft.com/en-us/downloads/ 
2. Start the Azure Storage Emulator by pressing the Start button or the Windows 
key and searching for it by typing "Azure Storage Emulator". Select it from the 
list of applications to start it.
3. Open the config.py file and set IS\_EMULATED to true.
4. Run 'python start.py' 

To run the sample using the Storage Service:

1. Go to your Azure Storage account in the Azure Portal and under "SETTINGS" 
click on "Access keys". Copy either key1 or key2's "CONNECTION STRING".
2. Open config.py and set IS\_EMULATED to False and set STORAGE\_CONNECTION\_STRING to the
connection string value from the previous step.
3. Run 'python start.py'

#### More information
  - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/  
  - Getting Started with Tables - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-table-storage/
  - Table Service Concepts - http://msdn.microsoft.com/en-us/library/dd179463.aspx
  - Table Service REST API - http://msdn.microsoft.com/en-us/library/dd179423.aspx
  - Storage Emulator - http://azure.microsoft.com/en-us/documentation/articles/storage-use-emulator/