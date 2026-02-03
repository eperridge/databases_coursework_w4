"""
dbSetup.py - 

Contains queries necessary to create schemas, set-up tables and views. It drops existing 
the schemas at the beginning of each run for a clean slate. This is because...
"""

import sqlite3

#Establish connection
conn = sqlite3.connect('flightManagement.db')
cursor = conn.cursor()

#Drop tables in order of dependency (dependent to independent)
cursor.execute('DROP TABLE IF EXISTS flight')
cursor.execute('DROP TABLE IF EXISTS terminal')
cursor.execute('DROP TABLE IF EXISTS pilot')
cursor.execute('DROP TABLE IF EXISTS destination')

print('Drop tables script complete.')

#Create tables, in order of reverse dependency (independent to dependent)
createDestinationTable = '''
                       CREATE TABLE destination (
                            destinationID CHAR(3) NOT NULL PRIMARY KEY,
                            destinationName VARCHAR(60) NOT NULL,
                            country VARCHAR(60) NOT NULL,
                            city VARCHAR(60) NOT NULL
                       )
                       '''
cursor.execute(createDestinationTable)

createTerminalTable = '''
                    CREATE TABLE terminal (
                        terminalID VARCHAR NOT NULL,
                        destinationID CHAR NOT NULL,
                        terminalName VARCHAR,
                        PRIMARY KEY (terminalID, destinationID),
                        FOREIGN KEY (destinationID) REFERENCES destination(destinationID)
                    );
                    '''
cursor.execute(createTerminalTable)


createPilotTable = '''
                    CREATE TABLE pilot (
                        pilotID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        pilotName VARCHAR,
                        email VARCHAR,
                        dob DATE,
                        isCapitainQualified BOOLEAN,
                        isFirstOfficerQualified BOOLEAN
                    );
                    '''
cursor.execute(createPilotTable)

createFlightTable = '''
                    CREATE TABLE flight (
                        flightID VARCHAR NOT NULL,
                        scheduled DATETIME NOT NULL,
                        flightStatus VARCHAR,
                        captainID INTEGER,
                        firstOfficer INTEGER,
                        arrivalDestinationID CHAR NOT NULL,
                        departureDestinationID CHAR NOT NULL,
                        diversionDestinationID CHAR,
                        departureTerminalID CHAR NOT NULL,
                        arrivalTerminalID CHAR,
                        scheduledArrivalDateTime DATETIME NOT NULL,
                        actualArrivalDateTime DATETIME,
                        PRIMARY KEY (flightID, scheduled),
                        FOREIGN KEY (captainID) REFERENCES pilot(pilotID),
                        FOREIGN KEY (firstOfficer) REFERENCES pilot(pilotID),
                        FOREIGN KEY (arrivalDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (departureDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (diversionDestinationID) REFERENCES destination(destinationID),
                        FOREIGN KEY (departureTerminalID) REFERENCES terminal(terminalID),
                        FOREIGN KEY (arrivalTerminalID) REFERENCES terminal(terminalID)
                    );
                    '''
cursor.execute(createFlightTable)

print('Table creation script complete.')