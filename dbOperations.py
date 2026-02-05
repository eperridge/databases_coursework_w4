"""
dbOperations.py - 
"""
import time
import sqlite3

conn = sqlite3.connect('flightManagement.db')
cursor = conn.cursor()

#Define allowed flightStatus values in a list
allowedFlightStatus = ['Scheduled', 'In-air', 'Landed', 'Cancelled']

flightAttributeList = [
    "flightID", "scheduledDepartureDateTime", "flightStatus", "captainID", "firstOfficerID", "arrivalDestinationID", 
    "departureDestinationID", "diversionDestinationID", "departureTerminalID", "arrivalTerminalID", "diversionTerminalID", 
    "scheduledArrivalDateTime", "actualArrivalDateTime", "actualDepartureDateTime"]

"""
2. Add a New Flight
Executes INSERT query to add a new flight record. The addFlightUserInput tuple must contain values in the correct order.
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
    finally:
        conn.close()
        
"""
3. View Flights by Criteria
Allow user to input criteria: 
    departureStatus, destination, flightStatus, scheduledDepartureDateTime,
    flightStatus AND scheduledDepartureDateTime
"""
def viewFlightsByCriteria(criteria, value, selectedAttributes):
    conn = sqlite3.connect('flightManagement.db')
    cursor = conn.cursor()    
    
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
        
        if not results:
            print("No matches found for selected criteria.")
        else:
            header = " | ".join(selectedAttributes)
            print(f"\n{header}")
            print("-" * len(header))
            for row in results:
                print(" | ".join(str(item) for item in row))
                
    except sqlite3.Error as e:
        print(f"ERROR: {e}")
    finally:
        conn.close()