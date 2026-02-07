"""
dbSetup.py - Database Initialisation
    This script creates the relational schema for the Flight Management System.
    It contains queries necessary to create schemas, set-up tables and views and it defines primary and foreign keys. 
    It drops existing the schemas at the beginning of each run for a clean slate. 
"""

import sqlite3
from dbOperations import allowedFlightStatus

#Establish connection to database file
conn = sqlite3.connect('flightManagement.db')
cursor = conn.cursor()

#Drop existing tables in order of dependency (dependent to independent) to avoid foreign key dependencies
cursor.execute('DROP TABLE IF EXISTS flight')
cursor.execute('DROP TABLE IF EXISTS terminal')
cursor.execute('DROP TABLE IF EXISTS pilot')
cursor.execute('DROP TABLE IF EXISTS destination')

print('Drop tables script complete.')


#Drop existing views
cursor.execute('DROP VIEW IF EXISTS departurePerformance')
cursor.execute('DROP VIEW IF EXISTS arrivalPerformance')

print('Drop views script complete.')

#Create tables, in order of reverse dependency (independent to dependent). 
#Independent tables have no foreign keys and are created first.

#Table for storing airports, i.e. destinations
createDestinationTable = '''
                       CREATE TABLE destination (
                            destinationID CHAR(3) NOT NULL PRIMARY KEY,
                            destinationName VARCHAR(60) NOT NULL,
                            country VARCHAR(60) NOT NULL,
                            city VARCHAR(60) NOT NULL
                       )
                       '''

#Table for storing airport terminals, linked to destinations
createTerminalTable = '''
                    CREATE TABLE terminal (
                        terminalID VARCHAR NOT NULL,
                        destinationID CHAR NOT NULL,
                        terminalName VARCHAR,
                        PRIMARY KEY (terminalID, destinationID),
                        FOREIGN KEY (destinationID) REFERENCES destination(destinationID)
                    );
                    '''

#Table for storing pilots and their details
createPilotTable = '''
                    CREATE TABLE pilot (
                        pilotID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        pilotName VARCHAR NOT NULL,
                        email VARCHAR NOT NULL,
                        dob DATE NOT NULL,
                        isCaptainQualified BOOLEAN NOT NULL,
                        isFirstOfficerQualified BOOLEAN NOT NULL
                    );
                    '''

#Check constraint for flightStatus, which is an attribute in the flight table
flightStatusConstraint = ", ".join([f"'{s}'" for s in allowedFlightStatus])

#Flight table for storing flight details
#Has many foreign keys and uses the contraint above
createFlightTable = f'''
                    CREATE TABLE flight (
                        flightID VARCHAR NOT NULL,
                        scheduledDepartureDateTime DATETIME NOT NULL,
                        flightStatus VARCHAR CHECK (flightStatus IN ({flightStatusConstraint})),
                        captainID INTEGER,
                        firstOfficerID INTEGER,
                        arrivalDestinationID CHAR NOT NULL,
                        departureDestinationID CHAR NOT NULL,
                        diversionDestinationID CHAR,
                        departureTerminalID CHAR NOT NULL,
                        arrivalTerminalID CHAR,
                        diversionTerminalID CHAR,
                        scheduledArrivalDateTime DATETIME NOT NULL,
                        actualArrivalDateTime DATETIME,
                        actualDepartureDateTime DATETIME,
                        PRIMARY KEY (flightID, scheduledDepartureDateTime),
                        FOREIGN KEY (captainID) REFERENCES pilot(pilotID),
                        FOREIGN KEY (firstOfficerID) REFERENCES pilot(pilotID),
                        FOREIGN KEY (arrivalDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (departureDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (diversionDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (departureTerminalID) REFERENCES terminal(terminalID),
                        FOREIGN KEY (arrivalTerminalID) REFERENCES terminal(terminalID)
                        FOREIGN KEY (diversionTerminalID) REFERENCES terminal(terminalID)
                    );
                    '''

print('Table creation script complete.')

#Create view for calculated field departureStatus
    #This view calculates the field departureStatus, giving it a value of Delayed or On Time without altering the flight table
    #source: https://www.sqlite.org/lang_expr.html
createDeparturePerformanceView = '''
                                CREATE VIEW departurePerformance AS
                                    SELECT
                                        flightID, scheduledDepartureDateTime, actualDepartureDateTime,
                                        CASE
                                            WHEN actualDepartureDateTime IS NULL THEN 'On Time'
                                            WHEN actualDepartureDateTime > scheduledDepartureDateTime THEN 'Delayed'
                                            ELSE 'On Time'
                                        END AS departureStatus
                                    FROM flight;
                            '''
                            
#Create view for calculated field arrivalStatus
createArrivalPerformanceView = '''
                                CREATE VIEW arrivalPerformance AS
                                    SELECT
                                        flightID, scheduledArrivalDateTime, actualArrivalDateTime,
                                        CASE
                                            WHEN actualArrivalDateTime IS NULL THEN 'On Time'
                                            WHEN actualArrivalDateTime > scheduledArrivalDateTime THEN 'Delayed'
                                            ELSE 'On Time'
                                        END AS arrivalStatus
                                    FROM flight;
                            '''

# Execute table and view creation within a try-except block to handle errors
    #Taken from exceptions lesson from in Database APIs using python
try:
    cursor.execute(createDestinationTable)
    conn.commit()
    cursor.execute(createTerminalTable)
    conn.commit()
    cursor.execute(createPilotTable)
    conn.commit()
    cursor.execute(createFlightTable)
    conn.commit()
    cursor.execute(createDeparturePerformanceView)
    conn.commit()
    cursor.execute(createArrivalPerformanceView)
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f'Error during table creation: {e}')
    raise e
finally:
    conn.close()

print('View creation script complete.')