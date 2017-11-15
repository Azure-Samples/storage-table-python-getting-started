#-------------------------------------------------------------------------
# Microsoft Developer & Platform Evangelism
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
#----------------------------------------------------------------------------------
# The example companies, organizations, products, domain names,
# e-mail addresses, logos, people, places, and events depicted
# herein are fictitious. No association with any real company,
# organization, product, domain name, email address, logo, person,
# places, or events is intended or should be inferred.
#--------------------------------------------------------------------------

#This sample can be run using either the Azure Storage Emulator (Windows) or by updating the config.py file with your Storage account name and key.

# To run the sample using the Storage Emulator:
# 1. Download and install the Azure Storage Emulator https://azure.microsoft.com/en-us/downloads/ 
# 2. Start the emulator (once only) by pressing the Start button or the Windows key and searching for it by typing "Azure Storage Emulator". Select it from the list of applications to start it.
# 3. Run the project. 

# To run the sample using the Storage Service
# 1. Open the config.py file and set IS_EMULATED to false.
# 2. Create a Storage Account through the Azure Portal and provide your STORAGE_ACCOUNT_NAME and STORAGE_ACCOUNT_KEY in the config.py file. See https://azure.microsoft.com/en-us/documentation/articles/storage-create-storage-account/ for more information.
# 3. Set breakpoints and run the project. 
#---------------------------------------------------------------------------

import config
import azure.common
from azure.storage import CloudStorageAccount
from table_basic_samples import TableBasicSamples
from table_advanced_samples import TableAdvancedSamples
from tablestorageaccount import TableStorageAccount

print('Azure Table Storage samples for Python')

# Create the storage account object and specify its credentials 
# to either point to the local Emulator or your Azure subscription
if config.IS_EMULATED:
    account = TableStorageAccount(is_emulated=True)
else:
    account_connection_string = config.STORAGE_CONNECTION_STRING
	# Split into key=value pairs removing empties, then split the pairs into a dict
    config = dict(s.split('=', 1) for s in account_connection_string.split(';') if s)

    # Authentication
    account_name = config.get('AccountName')
    account_key = config.get('AccountKey')
    # Basic URL Configuration
    endpoint_suffix = config.get('EndpointSuffix')
    if endpoint_suffix == None:
       table_endpoint  = config.get('TableEndpoint')
       table_prefix = '.table.'
       start_index = table_endpoint.find(table_prefix)
       end_index = table_endpoint.endswith(':') and len(table_endpoint) or table_endpoint.rfind(':')
       endpoint_suffix = table_endpoint[start_index+len(table_prefix):end_index]
    account = TableStorageAccount(account_name = account_name, connection_string = account_connection_string, endpoint_suffix=endpoint_suffix)
#Basic Table samples
print ('---------------------------------------------------------------')
print('Azure Storage Table samples')
table_basic_samples = TableBasicSamples()
table_basic_samples.run_all_samples(account)

#Advanced Table samples
print ('---------------------------------------------------------------')
print('Azure Storage Advanced Table samples')
table_advanced_samples = TableAdvancedSamples()
table_advanced_samples.run_all_samples(account)