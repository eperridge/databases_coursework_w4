"""
dbSetup.py - 

Contains queries necessary to create schemas, set-up tables and views. It drops existing 
the schemas at the beginning of each run for a clean slate. This is because...
"""

import sqlite3
from dbOperations import allowedFlightStatus

#Establish connection
conn = sqlite3.connect('flightManagement.db')
cursor = conn.cursor()

#Drop tables in order of dependency (dependent to independent)
cursor.execute('DROP TABLE IF EXISTS flight')
cursor.execute('DROP TABLE IF EXISTS terminal')
cursor.execute('DROP TABLE IF EXISTS pilot')
cursor.execute('DROP TABLE IF EXISTS destination')

print('Drop tables script complete.')


#Drop views
cursor.execute('DROP VIEW IF EXISTS departureStatus')
cursor.execute('DROP VIEW IF EXISTS arrivalStatus')

print('Drop views script complete.')

#Create tables, in order of reverse dependency (independent to dependent)
createDestinationTable = '''
                       CREATE TABLE destination (
                            destinationID CHAR(3) NOT NULL PRIMARY KEY,
                            destinationName VARCHAR(60) NOT NULL,
                            country VARCHAR(60) NOT NULL,
                            city VARCHAR(60) NOT NULL
                       )
                       '''

createTerminalTable = '''
                    CREATE TABLE terminal (
                        terminalID VARCHAR NOT NULL,
                        destinationID CHAR NOT NULL,
                        terminalName VARCHAR,
                        PRIMARY KEY (terminalID, destinationID),
                        FOREIGN KEY (destinationID) REFERENCES destination(destinationID)
                    );
                    '''


createPilotTable = '''
                    CREATE TABLE pilot (
                        pilotID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        pilotName VARCHAR,
                        email VARCHAR,
                        dob DATE,
                        isCaptainQualified BOOLEAN,
                        isFirstOfficerQualified BOOLEAN
                    );
                    '''

flightStatusConstraint = ", ".join([f"'{s}'" for s in allowedFlightStatus])

createFlightTable = f'''
                    CREATE TABLE flight (
                        flightID VARCHAR NOT NULL,
                        scheduledDepartureDateTime DATETIME NOT NULL,
                        flightStatus VARCHAR CHECK (flightStatus IN ({flightStatusConstraint})),
                        captainID INTEGER,
                        firstOfficer INTEGER,
                        arrivalDestinationID CHAR NOT NULL,
                        departureDestinationID CHAR NOT NULL,
                        diversionDestinationID CHAR,
                        departureTerminalID CHAR NOT NULL,
                        arrivalTerminalID CHAR,
                        scheduledArrivalDateTime DATETIME NOT NULL,
                        actualArrivalDateTime DATETIME,
                        actualDepartureDateTime DATETIME,
                        PRIMARY KEY (flightID, scheduledDepartureDateTime),
                        FOREIGN KEY (captainID) REFERENCES pilot(pilotID),
                        FOREIGN KEY (firstOfficer) REFERENCES pilot(pilotID),
                        FOREIGN KEY (arrivalDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (departureDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (diversionDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (departureTerminalID) REFERENCES terminal(terminalID),
                        FOREIGN KEY (arrivalTerminalID) REFERENCES terminal(terminalID)
                    );
                    '''

print('Table creation script complete.')

#Create view for calculated field departureStatus
 #source: https://www.sqlite.org/lang_expr.html
createDepartureStatusView = '''
                                CREATE VIEW departureStatus AS
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
createArrivalStatusView = '''
                                CREATE VIEW arrivalStatus AS
                                    SELECT
                                        flightID, scheduledArrivalDateTime, actualArrivalDateTime,
                                        CASE
                                            WHEN actualArrivalDateTime IS NULL THEN 'On Time'
                                            WHEN actualArrivalDateTime > scheduledArrivalDateTime THEN 'Delayed'
                                            ELSE 'On Time'
                                        END AS arrivalStatus
                                    FROM flight;
                            '''

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
    cursor.execute(createDepartureStatusView)
    conn.commit()
    cursor.execute(createArrivalStatusView)
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f'Error during table creation: {e}')
    raise e
finally:
    conn.close()

print('View creation script complete.')