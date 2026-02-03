"""
main.py - Command-Line Interface (CLI)
-------------------------------------
This file serves as the entry point, the CLI, for the Flight Management System. The user 
interacts with this file: it handles input and orchestrates calls to functions in other 
files (namely dbOperations.py) which are necessary to carry out queries on the data, 
such as making changes to the database and getting information from the database.

Press play to run the script or type 'python main.py' into the terminal to start the 
application.
"""

import sqlite3

print("Hello World")