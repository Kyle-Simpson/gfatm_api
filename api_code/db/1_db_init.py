'''
    Author: Kyle Simpson
    Description: Initialize SQL database
'''

import sys
from db_utils import create_connection


# Create a connection to the user-specified database
if __name__ == '__main__':
    # Intake the database name
    db_name = str(sys.argv[1])
    # Create a connection to the db
    create_connection(db_name)
