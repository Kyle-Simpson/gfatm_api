'''
    Author: Kyle Simpson
    Description: Practice building an API in Python
'''

# Module imports
import flask
from flask import request, jsonify
import sqlite3
from db.db_utils import create_connection


# Initialize application
app = flask.Flask(__name__)
app.config['DEBUG'] = True

# Set db string
db = "program_docs"


# Set the homepage for the website
@app.route('/', methods=['GET'])
def home():
    return ''' <h1>GFATM Test API</h1><p>A prototype API pulling GFATM data</p>'''


# Define method to pull all books from api homepage
@app.route('/api/v1/resources/program_docs/all', methods=['GET'])
def api_all():
    # Connect to the database
    conn = create_connection(db)
    # Create variable containing the cursor (what goes and pulls our data)
    curr = conn.cursor()

    # Pull all books
    all_books = curr.execute("SELECT * FROM program_documents;").fetchall()

    # Close the connection
    curr.close()
    conn.close()

    # Return a json-version of the SQL statement
    return jsonify(all_books)


# Define method to return 404 page error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found</p>", 404


# Setup queries for api requests
@app.route('/api/v1/resources/program_docs', methods=['GET'])
def api_filter():
    # Hold onto the request arguments
    query_params = request.args

    # Parse the parameters - could enforce data types here too, but a bit unnecessary
    # since it'll always be coming from the URL and not a user input
    id = query_params.get('id')
    programDocumentId = query_params.get('programDocumentId')
    documentTypeId = query_params.get('documentTypeId')
    documentTypeDescription = query_params.get('documentTypeDescription')
    documentTypeCode = query_params.get('documentTypeCode')
    documentTypeSortOrder = query_params.get('documentTypeSortOrder')
    geographicAreaId = query_params.get('geographicAreaId')
    geographicAreaCode_ISO3 = query_params.get('geographicAreaCode_ISO3')
    geographicAreaName = query_params.get('geographicAreaName')
    organizationId = query_params.get('organizationId')
    organizationName = query_params.get('organizationName')
    componentId = query_params.get('componentId')
    componentName = query_params.get('componentName')
    grantAgreementId = query_params.get('grantAgreementId')
    grantAgreementNumber = query_params.get('grantAgreementNumber')
    implementationPeriodId = query_params.get('implementationPeriodId')
    implementationPeriodName = query_params.get('implementationPeriodName')
    processName = query_params.get('processName')
    processYear = query_params.get('processYear')
    processWindow = query_params.get('processWindow')
    fileName = query_params.get('fileName')
    fileIndex = query_params.get('fileIndex')
    fileExtension = query_params.get('fileExtension')
    fileSize = query_params.get('fileSize')
    fileLanguage = query_params.get('fileLanguage')
    fileModifiedDateTime = query_params.get('fileModifiedDateTime')
    fileCreatedDateTime = query_params.get('fileCreatedDateTime')
    fileURL = query_params.get('fileURL')

    # Init base query ther we'll format with further args
    query = 'SELECT * FROM program_documents WHERE'
    to_filter = []

    # Add to the query and to_filter if any variables exist
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if programDocumentId:
        query += ' programDocumentId=? AND'
        to_filter.append(programDocumentId)
    if documentTypeId:
        query += ' documentTypeId=? AND'
        to_filter.append(documentTypeId)
    if documentTypeDescription:
        query += ' documentTypeDescription=? AND'
        to_filter.append(documentTypeDescription)
    if documentTypeCode:
        query += ' documentTypeCode=? AND'
        to_filter.append(documentTypeCode)
    if documentTypeSortOrder:
        query += ' documentTypeSortOrder=? AND'
        to_filter.append(documentTypeSortOrder)
    if geographicAreaId:
        query += ' geographicAreaId=? AND'
        to_filter.append(geographicAreaId)
    if geographicAreaCode_ISO3:
        query += ' geographicAreaCode_ISO3=? AND'
        to_filter.append(geographicAreaCode_ISO3)
    if geographicAreaName:
        query += ' geographicAreaName=? AND'
        to_filter.append(geographicAreaName)
    if organizationId:
        query += ' organizationId=? AND'
        to_filter.append(organizationId)
    if organizationName:
        query += ' organizationName=? AND'
        to_filter.append(organizationName)
    if componentId:
        query += ' componentId=? AND'
        to_filter.append(componentId)
    if componentName:
        query += ' componentName=? AND'
        to_filter.append(componentName)
    if grantAgreementId:
        query += ' grantAgreementId=? AND'
        to_filter.append(grantAgreementId)
    if grantAgreementNumber:
        query += ' grantAgreementNumber=? AND'
        to_filter.append(grantAgreementNumber)
    if implementationPeriodId:
        query += ' implementationPeriodId=? AND'
        to_filter.append(implementationPeriodId)
    if implementationPeriodName:
        query += ' implementationPeriodName=? AND'
        to_filter.append(implementationPeriodName)
    if processName:
        query += ' processName=? AND'
        to_filter.append(processName)
    if processYear:
        query += ' processYear=? AND'
        to_filter.append(processYear)
    if processWindow:
        query += ' processWindow=? AND'
        to_filter.append(processWindow)
    if fileName:
        query += ' fileName=? AND'
        to_filter.append(fileName)
    if fileIndex:
        query += ' fileIndex=? AND'
        to_filter.append(fileIndex)
    if fileExtension:
        query += ' fileExtension=? AND'
        to_filter.append(fileExtension)
    if fileSize:
        query += ' fileSize=? AND'
        to_filter.append(fileSize)
    if fileLanguage:
        query += ' fileLanguage=? AND'
        to_filter.append(fileLanguage)
    if fileModifiedDateTime:
        query += ' fileModifiedDateTime=? AND'
        to_filter.append(fileModifiedDateTime)
    if fileCreatedDateTime:
        query += ' fileCreatedDateTime=? AND'
        to_filter.append(fileCreatedDateTime)
    if fileURL:
        query += ' fileURL=? AND'
        to_filter.append(fileURL)
    if not (id or programDocumentId or documentTypeId or documentTypeDescription or documentTypeCode or documentTypeSortOrder or \
        geographicAreaId or geographicAreaCode_ISO3 or geographicAreaName or organizationId or organizationName or componentId or \
            componentName or grantAgreementId or grantAgreementNumber or implementationPeriodId or implementationPeriodName or processName or \
                processYear or processWindow or fileName or fileIndex or fileExtension or fileSize or fileLanguage or fileModifiedDateTime or \
                    fileCreatedDateTime or fileURL):
        return page_not_found(404)

    # Remove any trailing `AND` and add a semicolon
    query = query[:-4] + ';'

    # Initialize the db connection
    conn = create_connection(db)
    curr = conn.cursor()

    # Execute the query and add the filters
    results = curr.execute(query, to_filter).fetchall()

    # Close the connection
    curr.close()
    conn.close()

    return jsonify(results)



# Run the application
app.run()