'''
    Author: Kyle Simpson
    Description: Populate the provided database with the 
                 VProgramDocuments txt file in ./gfatm_api/db_data/
'''

import json
import sys
import os
import pandas as pd
from db_utils import create_connection, create_table, insert_into_table


wd = os.getcwd()
if 'gfatm_api' not in wd.lower():
    wd += '/gfatm_api'
prog_docs_location = '{}/db_data/raw_program_docs.json'.format(wd)


def load_prog_docs():
    data = []
    with open(prog_docs_location) as f:
        data = json.load(f)['value']
        data = pd.DataFrame.from_dict(data)

    return(data)



def create_base_table(conn):
    '''
        Description: Define the SQL to create the program_documents table, and call the
                     create_table() function to execute the command
    '''
    prog_docs_sql = """ CREATE TABLE IF NOT EXISTS program_documents (
                          id integer PRIMARY KEY AUTOINCREMENT,
                          programDocumentID text,
                          documentTypeId text,
                          documentTypeDescription text,
                          documentTypeCode text,
                          documentTypeSortOrder text,
                          geographicAreaId text,
                          geographicAreaCode_ISO3 text,
                          geographicAreaName text,
                          organizationId text,
                          organizationName text,
                          componentId text,
                          componentName text,
                          grantAgreementId text,
                          grantAgreementNumber text,
                          implementationPeriodId text,
                          implementationPeriodName text,
                          processName text,
                          processYear text,
                          processWindow text,
                          fileName text,
                          fileIndex text,
                          fileExtension text,
                          fileSize text,
                          fileLanguage text,
                          fileModifiedDateTime text,
                          fileCreatedDateTime text,
                          fileURL text
                      ); """
    
    if conn is not None:
        create_table(conn, prog_docs_sql)



def insert_all(conn, prog_docs):
    '''
        Description: Loop through prog_docs and call the insert_into_table function
    '''

    print('  Filling the program_documents table - thank you for your patience')

    # Loop through each row of prog_docs
    for index, doc in prog_docs.iterrows():
        # Generate the SQL to insert into program_documents table
        insert_sql = ("INSERT INTO program_documents (programDocumentId, documentTypeId, documentTypeDescription, documentTypeCode, ",
                      "documentTypeSortOrder, geographicAreaId, geographicAreaCode_ISO3, geographicAreaName, organizationId, organizationName, ",
                      "componentId, componentName, grantAgreementId, grantAgreementNumber, implementationPeriodId, implementationPeriodName, ",
                      "processName, processYear, processWindow, fileName, fileIndex, fileExtension, fileSize, fileLanguage, fileModifiedDateTime, ",
                      "fileCreatedDateTime, fileURL) ",
                      "VALUES (",
                      '"{}", '.format(str(doc['programDocumentId'])),
                      '"{}", '.format(str(doc['documentTypeId'])),
                      '"{}", '.format(str(doc['documentTypeDescription'])),
                      '"{}", '.format(str(doc['documentTypeCode'])),
                      '"{}", '.format(str(doc['documentTypeSortOrder'])),
                      '"{}", '.format(str(doc['geographicAreaId'])),
                      '"{}", '.format(str(doc['geographicAreaCode_ISO3'])),
                      '"{}", '.format(str(doc['geographicAreaName'])),
                      '"{}", '.format(str(doc['organizationId'])),
                      '"{}", '.format(str(doc['organizationName'])),
                      '"{}", '.format(str(doc['componentId'])),
                      '"{}", '.format(str(doc['componentName'])),
                      '"{}", '.format(str(doc['grantAgreementId'])),
                      '"{}", '.format(str(doc['grantAgreementNumber'])),
                      '"{}", '.format(str(doc['implementationPeriodId'])),
                      '"{}", '.format(str(doc['implementationPeriodName'])),
                      '"{}", '.format(str(doc['processName'])),
                      '"{}", '.format(str(doc['processYear'])),
                      '"{}", '.format(str(doc['processWindow'])),
                      '"{}", '.format(str(doc['fileName'])),
                      '"{}", '.format(str(doc['fileIndex'])),
                      '"{}", '.format(str(doc['fileExtension'])),
                      '"{}", '.format(str(doc['fileSize'])),
                      '"{}", '.format(str(doc['fileLanguage'])),
                      '"{}", '.format(str(doc['fileModifiedDateTime'])),
                      '"{}", '.format(str(doc['fileCreatedDateTime'])),
                      '"{}"'.format(str(doc['fileURL'])),
                      ");")
        
        # Call the insert_into_table function
        if conn is not None:
            insert_into_table(conn, ''.join(insert_sql))
        
    print('  Table created successfully')



if __name__ == "__main__":
    print(' ')
    print(' ')

    # Connect to the provided database
    print('  Connecting to db')
    db_name = str(sys.argv[1])
    conn = create_connection(db_name)

    # Load the VProgramDocuments json file
    prog_docs = load_prog_docs()

    # Create base table
    print('  Creating program_documents table')
    create_base_table(conn)
    
    # Insert all the observations into the db
    insert_all(conn, prog_docs)

    print('  Database is ready for use')
    print(' ')
    print(' ')