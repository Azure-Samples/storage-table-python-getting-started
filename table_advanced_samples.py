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
import config
import datetime
import time
from random_data import RandomData
from tablestorageaccount import TableStorageAccount
from azure.storage import CloudStorageAccount, AccessPolicy
from azure.storage.table import TableService, Entity, TablePermissions
from azure.storage.models import CorsRule, Logging, Metrics, RetentionPolicy, ResourceTypes, AccountPermissions

#
# Azure Table Service Sample - Demonstrate how to perform common tasks using the Microsoft Azure Table Service
# including creating a table, CRUD operations and different querying techniques.
#
# Documentation References:
#  - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
#  - Getting Started with Tables - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-table-storage/
#  - Table Service Concepts - http://msdn.microsoft.com/en-us/library/dd179463.aspx
#  - Table Service REST API - http://msdn.microsoft.com/en-us/library/dd179423.aspx
#  - Table Service Python API - http://azure.github.io/azure-storage-python/ref/azure.storage.table.html
#  - Storage Emulator - http://azure.microsoft.com/en-us/documentation/articles/storage-use-emulator/
#
class TableAdvancedSamples():

    def __init__(self):
        self.random_data = RandomData()

    # Runs all samples for Azure Storage Table service.
    def run_all_samples(self, account):
        table_service = account.create_table_service()
        print('Azure Storage Advanced Table samples - Starting.')
        
        print('\n\n* List tables *\n')
        self.list_tables(table_service)
        
        if not account.is_azure_cosmosdb_table():
           print('\n\n* Set service properties *\n')
           self.set_service_properties(table_service)
        
           print('\n\n* Set Cors rules *\n')
           self.set_cors_rules(table_service)
        
           print('\n\n* ACL operations *\n')
           self.table_acl_operations(table_service)
        
        if (config.IS_EMULATED):
            print('\n\n* Shared Access Signature is not supported in emulator *\n')
        else:
            print('\n\n* SAS operations *\n')
            self.table_operations_with_sas(account)

        print('\nAzure Storage Advanced Table samples - Completed.\n')

    # Manage tables including creating, listing and deleting
    def list_tables(self, table_service):
        table_prefix = 'table' + self.random_data.get_random_name(6)

        try:        
            # Create tables
            for i in range(5):
                table_name = table_prefix + str(i)
                print('1. Create a table with name - ' + table_name)
                table_service.create_table(table_name)
            
            # List all the tables 
            print('2. List tables')
            tables = table_service.list_tables()
            for table in tables:
                print('\Table Name: ' + table.name)

        finally:
            # Delete the tables
            print("3. Delete Tables")
            for i in range(5):
                table_name = table_prefix + str(i)
                if(table_service.exists(table_name)):
                    table_service.delete_table(table_name)
            
        print("List tables sample completed")
    
    # Manage properties of the Table service, including logging and metrics settings, and the default service version.
    def set_service_properties(self, table_service):
        print('1. Get Table service properties')
        props = table_service.get_table_service_properties()

        retention = RetentionPolicy(enabled=True, days=5)
        logging = Logging(delete=True, read=False, write=True, retention_policy=retention)
        hour_metrics = Metrics(enabled=True, include_apis=True, retention_policy=retention)
        minute_metrics = Metrics(enabled=False)

        try:
            print('2. Ovewrite Table service properties')
            table_service.set_table_service_properties(logging=logging, hour_metrics=hour_metrics, minute_metrics=minute_metrics)

        finally:
            print('3. Revert Table service properties back to the original ones')
            table_service.set_table_service_properties(logging=props.logging, hour_metrics=props.hour_metrics, minute_metrics=props.minute_metrics)

        print('4. Set Table service properties completed')
    
    # Manage CORS rules on the table service
    def set_cors_rules(self, table_service):
        cors_rule = CorsRule(
            allowed_origins=['*'], 
            allowed_methods=['POST', 'GET'],
            allowed_headers=['*'],
            exposed_headers=['*'],
            max_age_in_seconds=3600)
        
        print('1. Get Cors Rules')
        original_cors_rules = table_service.get_table_service_properties().cors

        try:        
            print('2. Overwrite Cors Rules')
            table_service.set_table_service_properties(cors=[cors_rule])

        finally:
            #reverting cors rules back to the original ones
            print('3. Revert Cors Rules back the original ones')
            table_service.set_table_service_properties(cors=original_cors_rules)
        
        print("CORS sample completed")

    # Manage table access policy
    def table_acl_operations(self, table_service):
        table_name = 'acltable' + self.random_data.get_random_name(6)

        try:        
            print('1. Create a table with name - ' + table_name)
            table_service.create_table(table_name)
                
            print('2. Set access policy for table')
            access_policy = AccessPolicy(permission=TablePermissions.QUERY,
                                        expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1))
            identifiers = {'id': access_policy}
            table_service.set_table_acl(table_name, identifiers)

            print('3. Wait 30 seconds for acl to propagate')
            time.sleep(30)

            print('4. Get access policy from table')
            acl = table_service.get_table_acl(table_name)

            print('5. Clear access policy in table')
            table_service.set_table_acl(table_name)

        finally:
            print('5. Delete table')
            if(table_service.exists(table_name)):
                table_service.delete_table(table_name)
            
        print("Table ACL operations sample completed")
    
    # Manage shared access signature on a table
    def table_operations_with_sas(self, account):
        table_name = 'sastable' + self.random_data.get_random_name(6)
        
        try:
            # Create a Table Service object
            table_service = account.create_table_service()
            
            print('1. Create table with name - ' + table_name)
            table_service.create_table(table_name)
            
            # Create a Shared Access Signature for the table
            print('2. Get sas for table')
            
            table_sas = table_service.generate_table_shared_access_signature(
                table_name, 
                TablePermissions.QUERY + TablePermissions.ADD + TablePermissions.UPDATE + TablePermissions.DELETE, 
                datetime.datetime.utcnow() + datetime.timedelta(hours=1))

            shared_account = TableStorageAccount(account_name=account.account_name, sas_token=table_sas, endpoint_suffix=account.endpoint_suffix)
            shared_table_service = shared_account.create_table_service()

            # Create a sample entity to insert into the table
            customer = {'PartitionKey': 'Harp', 'RowKey': '1', 'email' : 'harp@contoso.com', 'phone' : '555-555-5555'}

            # Insert the entity into the table
            print('3. Insert new entity into table with sas - ' + table_name)
            shared_table_service.insert_entity(table_name, customer)
            
            # Demonstrate how to query the entity
            print('4. Read the inserted entity with sas.')
            entity = shared_table_service.get_entity(table_name, 'Harp', '1')
            
            print(entity['email'])
            print(entity['phone'])

            # Demonstrate how to update the entity by changing the phone number
            print('5. Update an existing entity by changing the phone number with sas')
            customer = {'PartitionKey': 'Harp', 'RowKey': '1', 'email' : 'harp@contoso.com', 'phone' : '425-123-1234'}
            shared_table_service.update_entity(table_name, customer)

            # Demonstrate how to delete an entity
            print('6. Delete the entity with sas')
            shared_table_service.delete_entity(table_name, 'Harp', '1')

        finally:
            print('7. Delete table')
            if(table_service.exists(table_name)):
                table_service.delete_table(table_name)
            
        print("Table operations with sas completed")