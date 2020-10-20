'''
    Author: Kyle Simpson
    Description: PCore methods for running the API and handling requests
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



# Run the application
app.run()