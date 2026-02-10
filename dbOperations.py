"""
dbOperations.py - For Data Access
    Contains logic and SQL queries for the application. 
    It isolates the interactions with the database from the user's interactions with the interface (main.py).
    This file groups the code by purpose:
        > Lists of attributes & constants
        > Helper functions
        > Manage flights
        > Manage pilots
        > View reports & summaries
"""
import time
import sqlite3
import sys

conn = sqlite3.connect('flightManagement.db')
cursor = conn.cursor()

"""
_____________________________________________________________
=============• LISTS OF ATTRIBUTES & CONSTANTS •=============
-------------------------------------------------------------
"""

#Define allowed flightStatus values in a list
allowedFlightStatus = ['Scheduled', 'In-air', 'Landed', 'Cancelled']

flightAttributeList = [
    "flightID", "scheduledDepartureDateTime", "flightStatus", "captainID", "firstOfficerID", "arrivalDestinationID", 
    "departureDestinationID", "diversionDestinationID", "departureTerminalID", "arrivalTerminalID", "diversionTerminalID", 
    "scheduledArrivalDateTime", "actualArrivalDateTime", "actualDepartureDateTime"]

"""
______________________________________________
=============• HELPER FUNCTIONS •=============
----------------------------------------------
"""
"""
Formats SQL fetchall() results into a human readable table for the user.
It iterates through the results, prints headers and seperates headers and values with pipes.
"""
def printTableOfResults(results, selectedAttributes):
    if not results:
        print("\nNo results found.")
    else:
        header = " | ".join(selectedAttributes)
        print(f"\n{header}")
        print("-" * len(header))
        
        for row in results:
            print(" | ".join(str(item) for item in row))

"""
Creates and returns a connection and cursor for the SQLite database.
Called with: conn, cursor = getDBConnection()
"""            
def getDBConnection(): 
    try:
        conn = sqlite3.connect('flightManagement.db') 
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None
    
# """
#   ****FOR FUTURE ITERATION****
# User Selection: Leave This Session
#     Closes connection
# """
# def leaveSession(conn):
#     try:
#         if conn:
#             conn.commit()
#             conn.close()
#             print("\nDatabase connection has been closed.")
#             time.sleep(1)
#             print("\nThank you for using the Flight Management System! Goodbye!")
#             time.sleep(2)

#     except sqlite3.Error as e:
#         print("Error during closure: {e}")
#         time.sleep(2)
        
#     sys.exit()
   
"""
____________________________________________
=============• MANAGE FLIGHTS •=============
=================• (CRUD) •=================
--------------------------------------------
"""
"""
1.1. View All Flights
    Fulfils requirement for the airline staff to retrieve information.
    It dynamically constructs a SELECT query based on user-selected attributes and orders the results
    by a user-selected attribute, allowing them to choose whether to sort by ASC or DESC.
"""
def viewAllFlights(selectedAttributes, orderByString, orderDirection):
    conn, cursor = getDBConnection() 
    
    attributeString = ", ".join(selectedAttributes)
    
    
    sqlQuery = f"SELECT {attributeString} FROM flight ORDER BY {orderByString} {orderDirection}"
        
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        printTableOfResults(results, selectedAttributes)
        time.sleep(4)
    
    except sqlite3.Error as e:
        print(f"ERROR: {e}")
              

"""
1.2. Add a New Flight
    Fulfis requirement for airline staff to add information.
    Executes INSERT query to add a new flight record, using positional placeholders, ?. 
    The addFlightUserInput tuple must contain values in the correct order.
    Called by: addFlight(userInput)
"""
def addFlight(addFlightUserInput):
    flightAttributes = ", ".join(flightAttributeList)
    valuePlaceholders = ", ".join(["?"] * len(flightAttributeList))
   
    sqlQuery = f"INSERT INTO flight ({flightAttributes}) VALUES ({valuePlaceholders})"
    
    try:
        cursor.execute(sqlQuery, addFlightUserInput)
        conn.commit()
        print("\nOperation Successful. A new flight has been added to the database.")
    except sqlite3.IntegrityError as e:
        #Catch duplicate primary keys or foreign keys that don't exit
        print("Operation has failed.")
        time.sleep(2)  
        print("Check that")
        time.sleep(2)  
        print("(1) The flightID and Scheduled Time combination don't already exist.")
        print("(2) All IDs (except Flight ID) exist in other tables.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

        
"""
1.3. View Flights by Criteria
    Fulfils requirement for airline staff to retrieve information.
    Allow user to retrive flights based on status or destination. 
    Called by: getFlightsByCriteria()
"""
def viewFlightsByCriteria(criteria, value, selectedAttributes):
    conn, cursor = getDBConnection() 
    
    if "all" in selectedAttributes:
        attributeString = "*"
    else:
        attributeString = ", ".join(selectedAttributes)
    
    #dictionary to map criterias to specific SQL queries
    queries = {
        "flightStatus": f"SELECT {attributeString} FROM flight WHERE flightStatus = ?",
        "arrivalDestination": f"SELECT {attributeString} FROM flight WHERE arrivalDestinationID = ?",
        "unassigned": f"""SELECT {attributeString} FROM flight WHERE (captainID IS NULL OR firstOfficerID IS NULL) 
                     AND flightStatus = 'Scheduled'"""
    }
    
    sqlQuery = queries.get(criteria)
    
    try:
        cursor.execute(sqlQuery, value)
        results = cursor.fetchall()
        
        printTableOfResults(results, selectedAttributes)
                
    except sqlite3.Error as e:
        print(f"ERROR: {e}")
 
"""
1.4. Update Flight Schedule or Status
    Fulfils requirement for airline staff to update existing flight schedules.
    Asks the user to input the composite primary key of the record they'd like to update,
    then executes an UPDATE query on this record, using the changes selected by the user.
    - ask what would you like to update?
    - give option of all columns except flightID
    - show current table: flightID, scheduledDepartureDateTime and selected columns
    - ask user to which record (pk = flight ID + scheduledDepartureDateTime) they'd like to change
    - user enter new value
    - show updated table: flightID, scheduledDepartureDateTime and previously selected columns
""" 
def updateFlightRecord(flightID, scheduledDeparture, attributeToChange, newValue):
    conn, cursor = getDBConnection()
    
    sqlQuery = f"UPDATE flight SET {attributeToChange} = ? WHERE flightID = ? AND scheduledDepartureDateTime = ?"
    
    try:
        cursor.execute(sqlQuery, (newValue, flightID, scheduledDeparture))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"\nSuccess: {attributeToChange} updated to '{newValue}'.")
        else:
            print("\nError: No record found matching selected Flight ID and Departure Time.")
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")

#Display user selected columns. Filter for IDs
def viewSelectedFlightAttibutes(selectedAttributes, flightID=None, scheduledDeparture=None):
    conn, cursor = getDBConnection()
    
    displayCols = ["flightID", "scheduledDepartureDateTime"] + selectedAttributes
    attrString = ", ".join(displayCols)
    
    sqlQuery = f"SELECT {attrString} FROM flight"
    params = ()
    
    if flightID and scheduledDeparture:
        sqlQuery += " WHERE flightID = ? AND scheduledDepartureDateTime = ?"
        params = (flightID, scheduledDeparture)
        
    try:
        cursor.execute(sqlQuery, params)
        results = cursor.fetchall()
        printTableOfResults(results, displayCols)
        time.sleep(4)
        
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
        
"""
1.5. Delete a Flight Record
    Fulfils requirement for airline staff to delete a record.
    Pass in the composite primary key selected by the user to execute a DELETE FROM QUERY on a record in the flight table.
"""    
def deleteFlightRecord(flightID, scheduledDeparture):
    conn, cursor = getDBConnection()
    
    sqlQuery = "DELETE FROM flight WHERE flightID = ? AND scheduledDepartureDateTime = ?"
    
    try:
        cursor.execute(sqlQuery, (flightID, scheduledDeparture))
        conn.commit()
        if cursor.rowcount > 0: #no. of impacted flights > 0
            print(f"\nFlight {flightID} scheduled for {scheduledDeparture} has been deleted.")
        else:
            print("No record found matching those details - nothing has been deleted.")
    
    except sqlite3.Error as e:
        print(f"Error during deletion: {e}")

    
"""
___________________________________________
=============• MANAGE PILOTS •=============
=================• (CRUD) •================
-------------------------------------------
"""
"""
2.1. Add Pilot
    Fulfils requirement for airline staff to add a record.
    Executes INSERT query to add a new pilot record, using positional placeholders, ?. 
"""
def addPilot(pilotData):
    conn, cursor = getDBConnection()
    
    #pilotID is autogenerateed
    sqlQuery = """
        INSERT INTO pilot (pilotName, email, dob, isCaptainQualified, isFirstOfficerQualified) 
        VALUES (?, ?, ?, ?, ?)
    """
    
    try:
        cursor.execute(sqlQuery, pilotData)
        newPilotID = cursor.lastrowid
        conn.commit()
        
        print(f"\nNew pilot record has been added to the database.")
        time.sleep(2)
        #fetch the new record
        cursor.execute("SELECT * FROM pilot WHERE pilotID = ?", (newPilotID,))
        result = cursor.fetchall()
        
        #show new record with headers
        headers = ["pilotID", "pilotName", "email", "dob", "isCaptain", "isFO"]
        printTableOfResults(result, headers)
        time.sleep(4)
        
    except sqlite3.IntegrityError as e:
        print(f"\nERROR: Could not add pilot.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        
"""
2.2.1 View Pilot Schedules
    Fulfils requirement to retrive information about pilots. 
    Fetches table of pilots.
"""
def viewAllPilots():
    conn, cursor = getDBConnection()
    
    try:
        cursor.execute("SELECT * FROM pilot")
        results = cursor.fetchall()
        
        headers = ["ID", "Name", "Email", "DOB", "Captain", "First Officer"]
        print("\nAll Pilots:")
        time.sleep(2)
        printTableOfResults(results, headers)
   
    except sqlite3.Error as e:
        print(f"Database error: {e}")

"""
2.2.2 View Pilot Schedules
    Fulfuls requriements for airline staff to retrieve pilot and flight information.
    - Uses a UNION to fetch flights where a pilot is a Captain or First Officer.
    - Joins pilot with flight to show which flights pilots are assigned to and when.
    Lesson 3: Multiple Table Queries, Union and Intersection
"""
def viewPilotSchedules():
    conn, cursor = getDBConnection()
    
    #first join on p.pilotID = f.captainID, then take the union with the join p.pilotID = f.firstOfficerID
    sqlQuery = """
    SELECT
        p.pilotID,
        p.pilotName,
        f.flightID,
        f.scheduledDepartureDateTime,
        f.scheduledArrivalDateTime,
        f.departureDestinationID,
        f.arrivalDestinationID,
        'Captain' as Role
    FROM pilot p
    JOIN flight f ON p.pilotID = f.captainID
    
    UNION 
    
    SELECT
        p.pilotID,
        p.pilotName,
        f.flightID,
        f.scheduledDepartureDateTime,
        f.scheduledArrivalDateTime,
        f.departureDestinationID,
        f.arrivalDestinationID,
        'First Officer' as Role
    FROM pilot p
    JOIN flight f ON p.pilotID = f.firstOfficerID    
    
    ORDER BY pilotID ASC, flightID ASC, scheduledDepartureDateTime DESC;
    """
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        attributes = ["Pilot ID", "Name", "Flight", "Departure", "Arrival ", "Departing From", "Arriving To", "Role"]
        print("\nPilot Schedule:")
        printTableOfResults(results, attributes)
        
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")   
        
"""
2.2.3 View Pilot Schedules
    Fulfils requrement for airline staff to retrieve pilot and flight infroamtions.
    Retrieves a list of scheduled without a full crew assigned.
"""        
def viewUnassignedFlights():
    conn, cursor = getDBConnection()
    # Looking for NULLs in the pilot ID columns
    sqlQuery = """
        SELECT flightID, scheduledDepartureDateTime, scheduledArrivalDateTime, departureDestinationID, arrivalDestinationID,
        flightStatus
        FROM flight 
        WHERE (captainID IS NULL OR firstOfficerID IS NULL)
        AND flightStatus = 'Scheduled';
    """
    
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        attributes = ["Flight", "Departure", "Arrival ", "Departing From", "Arriving To", "Flight Status"]
        print("\nPilot Schedule:")
        printTableOfResults(results, attributes)
        
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")   

"""
2.2.4 View Pilot Schedules
    Fulfils requirement for staff to retrieve pilot and flight schedules.
    Allows the user to input a time period they need a pilot for. The query creates a list of pilots whose
    assignments overlap with the user selected time stamps and returns the list of pilots not in the list.
    A UNION is used to combine flight.captainID and flight.firstOfficerID into one pilotID column.
"""
def viewAvailablePilots(startTime, endTime):
    conn, cursor = getDBConnection()
    
    #Select pilots whose ID isn't in the flight table within the selected time period   (looking at scheduledDepartureDateTime and scheduledArrivalDateTime)
    sqlQuery = """
        SELECT pilotID, pilotName, email, isCaptainQualified, isFirstOfficerQualified
        FROM pilot
        WHERE pilotID NOT IN (
            SELECT captainID FROM flight 
            WHERE (scheduledDepartureDateTime < ? AND scheduledArrivalDateTime > ?)
            AND captainID IS NOT NULL
            UNION
            SELECT firstOfficerID FROM flight 
            WHERE (scheduledDepartureDateTime < ? AND scheduledArrivalDateTime > ?)
            AND firstOfficerID IS NOT NULL
        )
        """    
        
    try:
        # We pass the end and start times cross-wise to check for overlap
        params = (endTime, startTime, endTime, startTime)
        cursor.execute(sqlQuery, params)
        results = cursor.fetchall()
        
        headers = ["Pilot ID", "Name", "Email", "Captain", "First Officer"]
        
        print(f"\nAvailable Pilots: From {startTime} to {endTime}")
        printTableOfResults(results, headers)
        
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
    
"""
2.3. Assign pilot to flight
    Fulfils requirement for staff to update flight schedules.
    Updates a scheduled glight record with a pilotID in either the capitainID or firstOfficerID column.
"""
def assignPilotToFlight(flightID, departureTime, pilotID, role):
    conn, cursor = getDBConnection()
    
    sqlQuery = f"""UPDATE flight 
        SET {role} = ? 
        WHERE flightID = ? 
        AND scheduledDepartureDateTime = ?
        AND flightStatus = 'Scheduled'
    """
    
    try:
        cursor.execute(sqlQuery, (pilotID, flightID, departureTime))
        conn.commit()
        time.sleep(2)
        if cursor.rowcount > 0:
            print(f"\nPilot {pilotID} assigned as {role[:-2]} to flight {flightID} departure {departureTime}.")
        else:
            print("\nAssignment failed. Either flight does not exist or flight has already departed or has been cancelled.")
  
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")

"""
2.4. Update Pilot Details
    Fulfuls requirement for airline staff to modify information about pilots.
    Allows user to select the record they'd like to change. The program asks for the pilotName in 
    addition to the pilotID to ensure that the correct record is being selected - a pilotID is
    easier to get wrong than a pilotName. It then asks the user which attribute they'd like to 
    change. It notifies the user of the outcome of the action.
    
"""
def updatePilotDetails(pilotID, pilotName, attributeToChange, newValue):
    conn, cursor = getDBConnection()
    
    sqlQuery = f"UPDATE pilot SET {attributeToChange} = ? WHERE pilotID = ? AND pilotName = ?"
    
    try:
        cursor.execute(sqlQuery, (newValue, pilotID, pilotName))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"\nPilot {pilotID} has been updated. The value of {attributeToChange} is now {newValue}.")
        else:
            print("\nError: No match found for pilot ID and name combination.")
   
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
        
"""
______________________________________________________
=============• VIEW REPORTS & SUMMARIES •=============
------------------------------------------------------
"""        
"""
4.1.1. View Popularity Report
    Fulfils the requirement for staff to summarise information.
    Calculates flights each pilot has been assigned to, checking Captain ID and First Officer ID in the flight table,
    then joining to the pilot table to fetch names.
"""
def reportPilotFlightCount():
    conn, cursor = getDBConnection()
    # Subquery selects all pilotIDs from both roles, then the outer query joins to pilot to get the names for display.
    sqlQuery = """
        SELECT 
            p.pilotID, 
            p.pilotName, 
            COUNT(Flights.flightID) AS FlightCount
        FROM pilot p
        LEFT JOIN (
            SELECT captainID AS pilotID, flightID FROM flight
            UNION ALL
            SELECT firstOfficerID AS pilotID, flightID FROM flight
        ) AS Flights ON p.pilotID = Flights.pilotID
        GROUP BY p.pilotID, p.pilotName
        ORDER BY FlightCount DESC;
    """
    
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        headers = ["Pilot ID", "Pilot Name", "Count of Flights"]
        print("\nReport: Total Flights by Pilot")
        time.sleep(1)
        printTableOfResults(results, headers)
        time.sleep(4)
    except sqlite3.Error as e:
        print(f"Database error: {e}")        


"""
4.1.2  Report Pilot Workload by Month
    Fulfils the requirement for staff to summarise information.
    Gives a month-by-month view of pilot utilisation.
    Uses the strftime('%Y-%m', ...) SQL function to group flight data by month and year.
    A UNION ALL query is used to ensure that all pilots, as they may be a Captain or a 
    First Officers on a flight, are combined into 1 pilot column for the COUNT. The results
    are grouped by month and pilotName and ordered firstly by month, them count (i.e. Flights).
"""
def reportPilotWorkloadByMonth():
    sqlQuery = """
        SELECT strftime('%Y-%m', f.scheduledDepartureDateTime) as Month, p.pilotName, COUNT(*) as Flights
        FROM pilot p
        JOIN (
            SELECT captainID as pilotID, scheduledDepartureDateTime FROM flight
            UNION ALL
            SELECT firstOfficerID as pilotID, scheduledDepartureDateTime FROM flight
        ) f ON p.pilotID = f.pilotID
        GROUP BY Month, p.pilotName
        ORDER BY Month ASC, Flights DESC;
    """
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        headers = ["Month-Year", "Pilot Name", "Total Flights"]
        print("\nReport: Pilot Workload by Month")
        time.sleep(2)
        printTableOfResults(results, headers)
    
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")

"""
4.1.3. Busiest Terminal Overall
    Fulfils the requirement for staff to summarise information.
    Calculates how many times a terminal is used for departure, arrival or diversion.
    Logic:
    1. Performs 3 unions to consolidate all terminal columns in the flight table: departure, arrival and diversion.
    2. Pairs terminal IDs with their destination ID's to give context of where the terminal is, as they aren't 
    necessarily named uniquely, unilike destination ID's. 
    3. Filters out NULL values to remove unused terminals.
"""
def reportBusiestTerminal():
    conn, cursor = getDBConnection()
    
    sqlQuery = """
        SELECT Airport, Terminal, COUNT(*) as UsageCount
        FROM (
            SELECT arrivalDestinationID AS Airport, arrivalTerminalID AS Terminal FROM flight
            UNION ALL
            SELECT departureDestinationID AS Airport, departureTerminalID AS Terminal FROM flight
            UNION ALL
            SELECT diversionDestinationID AS Airport, diversionTerminalID AS Terminal FROM flight
        )
        WHERE Terminal IS NOT NULL AND Airport IS NOT NULL
        GROUP BY Airport, Terminal
        ORDER BY UsageCount DESC;
    """
    
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        # We display the Airport alongside the Terminal so the user knows which location it belongs to.
        headers = ["Airport ID", "Terminal", "Total Traffic Count"]
        time.sleep(2)
        print("\nReport: Busiest Terminals Overall")
        time.sleep(2)
        
        # This calls your standardised formatting helper.
        printTableOfResults(results, headers) 
        time.sleep(4)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

"""
4.2. View Flights Within Timeframe
    Fulfils the requirement for staff to summarise information.
    A dynamic report that allows the user to select a time period with params startDate and endDate to return a flitered list of flights
    occurring within this time period.
    The query executes a SELECT query using the BETWEEN operator on the scheduledDepartureDateTime.
    The user has the option to filter the query by pilot. This additional statement is added to the main query using +=.
"""

def reportByTimeframe(startDate, endDate, pilotID=None):
    conn, cursor = getDBConnection()
    
    # Base query for timeframe
    sqlQuery = "SELECT flightID, scheduledDepartureDateTime, flightStatus FROM flight WHERE scheduledDepartureDateTime BETWEEN ? AND ?"
    params = [startDate, endDate]

    # Ability to filter by pilot
    if pilotID:
        sqlQuery += " AND (captainID = ? OR firstOfficerID = ?)"
        params.extend([pilotID, pilotID])

    try:
        cursor.execute(sqlQuery, params)
        results = cursor.fetchall()
        printTableOfResults(results, ["Flight", "Departure", "Status"])
    
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
    
"""
4.3. Report: View Pilot Punctuality
    Fulfils the requirement for staff to summarise information.
    This report calculates on-time vs delayed status for both departures and arrivals, sumarised by pilot.
    Logic:
    1. Uses UNION ALL query to combine capitaID and firstOfficerID from the flight table as a single pilotID,
    as it is presented in the pilot table. This ensures that all pilot assignments to flights are counted.
    2. Uses conditional logic, CASE, to compared scheduled vs actual time stamps and takes the sum of 1/0.
    3. Groups by pilot ID.
"""
def reportPilotPunctuality():
    conn, cursor = getDBConnection()
    
    # Conditional aggregation to count on-time and delayed
    sqlQuery = """
        SELECT 
            p.pilotID,
            p.pilotName,
            SUM(CASE WHEN actualDepartureDateTime <= scheduledDepartureDateTime THEN 1 ELSE 0 END) as DepOnTime,
            SUM(CASE WHEN actualDepartureDateTime > scheduledDepartureDateTime THEN 1 ELSE 0 END) as DepDelayed,
            SUM(CASE WHEN f.actualArrivalDateTime <= f.scheduledArrivalDateTime THEN 1 ELSE 0 END) AS ArrOnTime,
            SUM(CASE WHEN f.actualArrivalDateTime > f.scheduledArrivalDateTime THEN 1 ELSE 0 END) AS ArrDelayed
        FROM pilot p
        JOIN (
            SELECT captainID AS pilotID, scheduledDepartureDateTime, actualDepartureDateTime,
            scheduledArrivalDateTime, actualArrivalDateTime FROM flight
            UNION ALL
            SELECT firstOfficerID AS pilotID, scheduledDepartureDateTime, actualDepartureDateTime,
            scheduledArrivalDateTime, actualArrivalDateTime FROM flight
        ) f ON p.pilotID = f.pilotID
        WHERE f.actualDepartureDateTime IS NOT NULL OR f.actualArrivalDateTime IS NOT NULL
        GROUP BY p.pilotID
        ORDER BY DepOnTime DESC;
        """
    
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        headers = ["Pilot ID", "Pilot Name", "On-Time Departures", "Delayed Departures", "On-Time Arrivals", "Delayed Arrivals"]
        print("\nReport: Pilot Punctuality")
        time.sleep(2)
        
        # Formatting the results for the airline manager
        printTableOfResults(results, headers)
        time.sleep(4)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

"""
4.4. Report: View Flight Punctuality
    Fulfils the requirement for staff to summarise information.
    This report uses fetches the calculated fields departureStatus and arrivalStatus for each flight
"""
def reportFlightPunctuality():
    conn, cursor = getDBConnection()
    
    # COALESCE to fill NULL results from the views with 'Pending'. 
    # In retrospect, the view currently is calculated so that flights are on time until proved otherwise
    sqlQuery = """
        SELECT 
            f.flightID, 
            f.scheduledDepartureDateTime, 
            COALESCE(dp.departureStatus, 'Pending') as departureStatus,
            COALESCE(ap.arrivalStatus, 'Pending') as arrivalStatus
        FROM flight f
        LEFT JOIN departurePerformance dp
            ON f.flightID = dp.flightID 
            AND f.scheduledDepartureDateTime = dp.scheduledDepartureDateTime
        LEFT JOIN arrivalPerformance ap 
            ON f.flightID = ap.flightID 
            AND f.scheduledArrivalDateTime = ap.scheduledArrivalDateTime
        ORDER BY f.scheduledDepartureDateTime DESC;
    """
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        
        headers = ["Flight ID", "Scheduled Departure", "Departure Status", "Arrival Status"]
        print("\nReport: Individual Flight Punctuality")
        time.sleep(2)
        
        printTableOfResults(results, headers)
        time.sleep(4)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        
