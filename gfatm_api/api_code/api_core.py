'''
    Author: Kyle Simpson
    Description: PCore methods for running the API and handling requests
'''

# Module imports
import flask
from flask import request, jsonify
import sqlite3
from gfatm_api.api_code.db.db_utils import create_connection, insert_into_table


# Initialize application
app = flask.Flask(__name__)
app.config['DEBUG'] = True

# Set db string
db = "program_docs"


# Set the homepage for the website
@app.route('/', methods=['GET'])
def home():
    return '''<h1>GFATM Test API</h1><p>A prototype API pulling GFATM data</p>'''


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


@app.errorhandler(403)
def update_failed(e):
    return "<h1>403</h1><p>The resource could not be updated</p>", 403


# Setup queries for api requests
@app.route('/api/v1/resources/program_docs', methods=['GET'])
def api_filter():
    # Hold onto the request arguments
    query_params = request.args

    # Define all possible filters
    filters = {
        'id' : None, 'programDocumentId' : None, 'documentTypeId' : None,
        'documentTypeDescription' : None, 'documentTypeCode' : None,
        'documentTypeSortOrder' : None, 'geographicAreaId' : None,
        'geographicAreaCode_ISO3' : None, 'geographicAreaName' : None,
        'organizationId' : None, 'organizationName' : None, 'componentId' : None,
        'componentName' : None, 'grantAgreementId' : None, 'grantAgreementNumber' : None,
        'implementationPeriodId' : None, 'implementationPeriodName' : None,
        'processName' : None, 'processYear' : None, 'processWindow' : None,
        'fileName' : None, 'fileIndex' : None, 'fileExtension' : None, 'fileSize' : None,
        'fileLanguage' : None, 'fileModifiedDateTime' : None, 'fileCreatedDateTime' : None,
        'fileURL' : None
    }

    # Parse the parameters
    for filter in filters.keys():
        filters[filter] = query_params.get(filter)

    # Init base query ther we'll format with further args
    query = 'SELECT * FROM program_documents WHERE'
    to_filter = []

    # Add to the query and to_filter if any variables exist
    for filter in filters.keys():
        if filters[filter]:
            query += ' {}=? AND'.format(filter)
            to_filter.append(filters[filter])

    # If no filters supplied, throw error
    if all(filter is None for filter in filters.values()):
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


@app.route('/api/v1/resources/program_docs/update', methods=['GET', 'POST'])
def update_form():
    if request.method== 'POST':
        prog_docs_insert(request.form)
        return '<h1>New Document Added</h1>'

    form = '<form method="POST">'
    inputs = [['Program Document ID', 'programDocumentId'], ['Document Type ID', 'documentTypeId'],
                ['Document Type Description', 'documentTypeDescription'], ['Document Type Code', 'documentTypeCode'],
                ['Document Type Sort Order', 'documentTypeSortOrder'], ['Geographic Area ID', 'geographicAreaId'],
                ['Geographic Area Code - ISO3', 'geographicAreaCode_ISO3'], ['Geographic Area Name', 'geographicAreaName'],
                ['Organization ID', 'organizationId'], ['Organization Name', 'organizationName'],
                ['Component ID', 'componentId'], ['Component Name', 'componentName'], ['Grant Agreement Id', 'grantAgreementId'],
                ['Grant Agreement Number', 'grantAgreementNumber'], ['Implementation Period ID', 'implementationPeriodId'],
                ['Implementation Period Name', 'implementationPeriodName'], ['Process Name', 'processName'],
                ['Process Year', 'processYear'], ['Process Window', 'processWindow'], ['File Name', 'fileName'],
                ['File Index', 'fileIndex'], ['File Extension', 'fileExtension'], ['File Size', 'fileSize'],
                ['File Language', 'fileLanguage'], ['File Modified Date Time', 'fileModifiedDateTime'],
                ['File Created Date Time', 'fileCreatedDateTime'], ['File URL', 'fileURL']]

    for input in inputs:
        form += '{}: <input type="text" name="{}"><br>'.format(input[0], input[1])

    form += '<input type="submit" value="submit"></form>'

    return form


# Define method to create new data
def prog_docs_insert(request):
    # Hold onto the request arguments
    query_params = request

    # Define all possible filters
    filters = {
        'programDocumentId' : None, 'documentTypeId' : None,
        'documentTypeDescription' : None, 'documentTypeCode' : None,
        'documentTypeSortOrder' : None, 'geographicAreaId' : None,
        'geographicAreaCode_ISO3' : None, 'geographicAreaName' : None,
        'organizationId' : None, 'organizationName' : None, 'componentId' : None,
        'componentName' : None, 'grantAgreementId' : None, 'grantAgreementNumber' : None,
        'implementationPeriodId' : None, 'implementationPeriodName' : None,
        'processName' : None, 'processYear' : None, 'processWindow' : None,
        'fileName' : None, 'fileIndex' : None, 'fileExtension' : None, 'fileSize' : None,
        'fileLanguage' : None, 'fileModifiedDateTime' : None, 'fileCreatedDateTime' : None,
        'fileURL' : None
    }

    # Init base query ther we'll format with further args
    query = ("INSERT INTO program_documents (programDocumentId, documentTypeId, documentTypeDescription, documentTypeCode, ",
                "documentTypeSortOrder, geographicAreaId, geographicAreaCode_ISO3, geographicAreaName, organizationId, organizationName, ",
                "componentId, componentName, grantAgreementId, grantAgreementNumber, implementationPeriodId, implementationPeriodName, ",
                "processName, processYear, processWindow, fileName, fileIndex, fileExtension, fileSize, fileLanguage, fileModifiedDateTime, ",
                "fileCreatedDateTime, fileURL) VALUES (")
    query = ''.join(query)

    # Parse the parameters
    for filter in filters.keys():
        filters[filter] = query_params.get(filter)
    to_filter = []

    # Add to the query and to_filter if any variables exist
    for filter in filters.keys():
        if filters[filter]:
            query += '?, '
            to_filter.append('{}'.format(filters[filter]))
        else:
            query += '"NULL", '

    # If no filters supplied, throw error
    if all(filter is None for filter in filters.values()):
        return update_failed(403)

    # Remove any trailing space and add a semicolon
    query = query[:-2] + ');'

    # Initialize the db connection
    conn = create_connection(db)
    c = conn.cursor()

    # Execute the query and add the filters
    c.execute(query, to_filter)
    conn.commit()

    # Close the connection
    c.close()
    conn.close()


# Run the application
app.run()