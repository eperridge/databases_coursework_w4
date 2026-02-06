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
import sys
import time
from dbOperations import (flightAttributeList, viewAllFlights, addFlight, viewFlightsByCriteria, leaveSession, updateFlightRecord, viewSelectedFlightAttibutes, allowedFlightStatus, deleteFlightRecord, viewUnassignedFlights,
addPilot, viewPilotSchedules, updatePilotDetails, viewAvailablePilots, assignPilotToFlight, viewAllPilots,
 reportPilotFlightCount, reportPilotWorkloadByMonth, reportByTimeframe, reportBusiestTerminal, reportPunctualityPerformance)   
#import sqlite3

# =================• ENTRY POINT & ROLE SELECTION •=================

def main():
    print("\nHello, welcome to the flight management system.")
    time.sleep(2)
    print("\nPlease enter select your role number:")
    time.sleep(1.5)
    print("1. Cat Walking Over Keyboard")
    print("2. Flight Attendant")
    print("3. Airlines Manager")
    time.sleep(1.5)
    
    userRole = input("\nEnter role number: ").strip() # strip() to remove leading and trailing spaces
    time.sleep(1.5)
    
    if userRole == "1":
        catRole()
    elif userRole == "2":
        flightAttendantActions() #view/read only
    elif userRole == "3":
        airlinesManagerActions() #full CRUD permissions
    else:
        print("Invalid role. Restarting.")
        time.sleep(3)
        main()
        
# =================• 2. SUB-MENUS (ORCHESTRATION) •=================
#================•ROLE MENUS•================
def catRole():
    print("\nSorry, you don't have access to the data.")
    time.sleep(1.5)
    

#The Flight Attended is only able to view (SELECT) data.
def flightAttendantActions():
    print("\nHello, Flight Attendant")    
    time.sleep(2)
    print("\nSorry, your profile hasn't been set up yet.")
    time.sleep(1.5)
    handleUserReset()
    # print("\nWhat would you like to do? Please select an action from the menu:")
    # time.sleep(2)
    # print("View Flights by Criteria")

#The Airlines Manager is able to perform all CRUD operations.
def airlinesManagerActions():
    while True:
        print("\nHello, Airlines Manager")    
        time.sleep(2)  
        print("\nWhat would you like to do? Please review the below actions:")
        time.sleep(2)
        print("1. Manage Flights")
        print("2. Manage Pilots")
        print("3. Manage Destinations")
        print("4. View Reports & Summaries")
        
        time.sleep(2)
        userChoice = input("\nEnter your selection's number: ").strip()   
        
        if userChoice == "1":
            getManageFlightsMenu()
            # getAllFlights()
        if userChoice == "2":
            getManagePilotsMenu()
        if userChoice == "3":
            print("Destination Management - Coming Soon")
            pass
        if userChoice == "4":
            getReportsMenu()
        else:
            print("\nInvalid selection, please enter a number from the options.")    
        time.sleep(1)  


"""
____________________________________________
=============• MANAGE FLIGHTS •=============
--------------------------------------------
"""
def getManageFlightsMenu():
    while True:
        time.sleep(2)
        print("\n======FLIGHT MANAGEMENT======")
        print("1. View All Flights")
        print("2. Add a New Flight")
        print("3. View Flights by Criteria (Status, Destination, Date)")
        print("4. Update Flight Details")
        print("5. Delete a Flight Record")
        print("6. Return to Main Menu")
        
        time.sleep(2)
        userChoice = input("\nEnter the number of your choice: ").strip()
        
        if userChoice == '1':
            getAllFlights()
        elif userChoice == '2':
            userInput = getUserInput("flight", flightAttributeList)
            addFlight(userInput)
        elif userChoice == '3':
            getFlightsByCriteria()
        elif userChoice == '4':
            getUpdateFlightRecord()     
        elif userChoice == '5':
            getDeleteFlightRecord()
        elif userChoice == '6':
            main() 
        else:
            print("\nInvalid selection. Please try again by entering a number from the menu.")
        
"""
1.1.
"""
def getAllFlights():
    print("\nAction: View all flights")
    print(f"\nAvailable columns: {', '.join(flightAttributeList)}")
    colInput = input("Enter columns (comma-separated) or 'all': ").strip().lower()
    
    selectedAttributes = flightAttributeList if colInput == 'all' else [a.strip() for a in colInput.split(",")]
    
    print(f"\nSort by which column? ({', '.join(flightAttributeList)})")
    orderCol = input("Enter column(s) (comma-separated): ").strip()
    
    direction = input("Order by ASC or DESC? ").strip().upper()
    if direction not in ["ASC", "DESC"]: direction = "ASC"
    
    viewAllFlights(selectedAttributes, orderCol, direction)
    
"""
1.2. Not needed, addFlight() from dbOperations.py is used directly
"""
"""
1.3.
"""
def getFlightsByCriteria():
    print("\nAction: View flights by criteria")
    time.sleep(1)
    print("\nDo you want to view flight by...")
    time.sleep(2)
    print("1. By Flight Status")
    print("2. Arrival Destination")
    time.sleep(2)
    
    userChoice = input("Enter the number of your selection: ").strip()
    
    print("\nWhich information would you like to see? Provide a comma seperated list.")
    time.sleep(1)
    print(f"The available columns are: {', '.join(flightAttributeList)}")
    time.sleep(2)
    attributeInput = input("Enter columns (or 'all'): ").strip().lower()
    
    selectedAttributes = [a.strip() for a in attributeInput.split(",")]
    
    if userChoice == "1":
        search = getUserInput("flight", ["flightStatus"])
        #pass tuple to function in dbOperations
        viewFlightsByCriteria("flightStatus", search, selectedAttributes)
        
    elif userChoice == "2":
        search = getUserInput("flight", ["arrivalDestinationID"])
        viewFlightsByCriteria("arrivalDestination", search, selectedAttributes)
"""
1.4. 
"""
def getUpdateFlightRecord():
    print("\nAction: Update Flight Information")
    # Exclude PK from update options 
    updatableValues = [attr for attr in flightAttributeList if attr not in ["flightID", "scheduledDepartureDateTime"]]
    
    print(f"\nAvailable fields to update: \n{', '.join(updatableValues)}")
    valueToChange = input("\nWhich value would you like to change? ").strip()
    time.sleep(2)
    
    if valueToChange not in updatableValues:
        print("Invalid column selection.")
        return
    time.sleep(1)

    # 2. Show current table with context
    print("\nCurrent Records")
    time.sleep(1)
    viewSelectedFlightAttibutes([valueToChange])
    
    # 3. Identify the record (composite PK)
    print("\nPlease use the table above to identify the record to change")
    time.sleep(2)
    targetFlightID = input("Enter Flight ID: ").strip().upper()
    time.sleep(1)
    targetDepartureTime = input("Enter Current Scheduled Departure (YYYY-MM-DD HH:MM:SS): ").strip()
    
    # 4. Get new value
    newValue = input(f"Enter the new value for {valueToChange}: ").strip()
    
    #handle capitlisation of flightStatus
    if valueToChange == 'flightStatus':
        print(f"\nERROR: {newValue} is an invalid status.")
        time.sleep(0.5) 
        print(f"\nflightStatus must be one of: {', '.join(allowedFlightStatus)}")
        print("Please wait while I try to correct this.")
        time.sleep(5)       
        newValue = newValue.strip().capitalize()
        
        while newValue not in allowedFlightStatus:
            time.sleep(1)
            print(f"\nERROR: {newValue} is an invalid status.")
            time.sleep(1)
            print(f"flightStatus must be one of: {', '.join(allowedFlightStatus)}")
            newValue = input(f"Please enter a valid status: ").strip().capitalize()
    time.sleep(2)
    
    # 5. Perform update 
    updateFlightRecord(targetFlightID, targetDepartureTime, valueToChange, newValue)
    
    # 6. Show updated table for verification [cite: 51, 64]
    print("\nYour Record:")
    time.sleep(2)
    viewSelectedFlightAttibutes([valueToChange], targetFlightID, targetDepartureTime)
 
"""
1.5. Delete a Flight Record
"""    
def getDeleteFlightRecord():
    print("\nAction: Delete a flight record")  
    time.sleep(2) 
    
    print("\nFlights in database:")
    time.sleep(1)
    viewSelectedFlightAttibutes([]) #fetch PK's and pass in 0 extra attributes
    
    #identify record to be created using PK
    print("\nWhich record would you like to delete?")  
    time.sleep(1)
    targetFlightID = input("Enter Flight ID: ").strip()
    time.sleep(1)
    targetDepartureTime = input("Enter Scheduled Departure (YYYY-MM-DD HH:MM:SS): ").strip()
    time.sleep(2)
    
    userConfirm = input(f"\nAre you sure you want to delete {targetFlightID} at {targetDepartureTime}? (Y/N): ").strip().upper()
    time.sleep(2)
    
    if userConfirm == 'Y':
        deleteFlightRecord(targetFlightID, targetDepartureTime)
    else:
        print("\nDeletion cancelled. Returning to menu.")
        
"""
____________________________________________
=============• MANAGE PILOTS •=============
--------------------------------------------
"""
def getManagePilotsMenu():
    while True:
        print("\n======PILOT MANAGEMENT======")
        print("1. Add New Pilot")
        print("2. View Pilot Schedules")
        print("3. Assign Pilot to Flight")
        print("4. Update Pilot Details")
        print("5. Delete Pilot")
        print("6. Return to Main Menu")
        
        userChoice = input("\nEnter the number of your choice: ").strip()
        
        if userChoice == '1':
            getAddPilot()
        elif userChoice == '2':
            getPilotSchedule()
        elif userChoice == '3':
            getAssignPilot()
        elif userChoice == '4':
            getUpdatePilotDetails()       
        elif userChoice == '5':
            print("Delete Pilot - Functionality Coming Soon!")
        elif userChoice == '6':
            main() 
        else:
            print("\nInvalid selection. Please try again by entering a number from the menu.")

"""
2.1. Add pilot
"""
def getAddPilot():
    print("\nAction: Add A New Pilot")
    
    #omit pilot ID
    pilotAttributeList = [
        "pilotName", "email", "dob", "isCaptainQualified", "isFirstOfficerQualified"
    ]
    
    userInput = getUserInput("pilot", pilotAttributeList)
    
    #call db operation
    addPilot(userInput)
    
    
"""
2.2. View Pilot Schedules
"""
def getPilotSchedule():
    time.sleep(1)
    print("\nLoading pilot schedules...")
    time.sleep(2)
    viewPilotSchedules()
    time.sleep(3)
    
    inSubMenu = True
    while inSubMenu:
        print("\nNext, would you like to:")
        time.sleep(1)
        print("1. See flights without full crew?")
        print("2. See available pilots for a time period?")
        print("3. Assign a pilot to a flight?")
        print("4. Return to Main Menu?")
        time.sleep(1)
    
        userChoice = input("\nEnter your choice (1-4): ").strip()
        
        if userChoice == '1':
            viewUnassignedFlights()
            time.sleep(3)
        
        elif userChoice == '2':
            print("\nChecking pilot availability...")
            startTime = input("Planned Departure (YYYY-MM-DD HH:MM:SS): ").strip()
            endTime = input("Planned Arrival (YYYY-MM-DD HH:MM:SS): ").strip()
            viewAvailablePilots(startTime, endTime)
            time.sleep(4)
            
        elif userChoice == '3':
            getAssignPilot() 
            
        elif userChoice == '4':
            inSubMenu = False 
            
        else:
            print("Invalid choice. Please enter 1-4.")        

"""
2.3. Assign Pilot to Flight
"""

def getAssignPilot():
    print("\nAction: Assign Pilot To Flight")
    time.sleep(2)
    
    #1. Show scheduled flights without full crew
    print("\nAvailable 'Scheduled' flights needing crew:")
    time.sleep(2)
    viewUnassignedFlights()
    time.sleep(3)
    
    #2. Collect ID's for flight and pilot
    print("\nWhich flight would you like to assign a pilot to?")
    time.sleep(1)
    flightID = input("\nEnter Flight ID: ").strip().upper()
    time.sleep(1)
    depTime = input("Enter Scheduled Departure (YYYY-MM-DD HH:MM:SS): ").strip()
    time.sleep(1)
    print("\nWould you like to available pilots? (Y/N) ")
    userInput = input().strip().upper()
    time.sleep(2)
    
    if userInput == "Y":
        print("For which time period?")
        time.sleep(2)
        startTime = input("Planned Departure (YYYY-MM-DD HH:MM:SS): ").strip()
        time.sleep(2)
        endTime = input("Planned Arrival (YYYY-MM-DD HH:MM:SS): ").strip()
        time.sleep(2)
        
        viewAvailablePilots(startTime, endTime)
        time.sleep(4)
    else: pass
    
    print("\nWhich pilot would you like to assign a the flight?")
    time.sleep(1)
    pilotID = input("Enter Pilot ID: ").strip()
    
    #3. Choose role
    print("\nWhat would you like to assign them as? Enter 1 for Captain or 2 for First Officer")
    time.sleep(1)
    roleChoice = input("Selection: ").strip()
    role = "captainID" if roleChoice == "1" else "firstOfficerID"
    
    assignPilotToFlight(flightID, depTime, pilotID, role)
    
"""
2.4. Update Pilot Details
"""
def getUpdatePilotDetails():
    print("\nAction: Update Pilot Details")
    time.sleep(2)
    
    viewAllPilots()
    time.sleep(2)
    targetID = input("\nEnter Pilot ID to update: ").strip()
    time.sleep(1)
    targetName = input("Enter Pilot Name (to confirm): ").strip()
    
    updatingPilot = True
    while updatingPilot:
        print("\nWhich value would you like to change?")
        time.sleep(2)
        print("1. Name\n2. Email\n3. DOB\n4. Captain Status (0/1)\n5. First Officer Status (0/1)")
        time.sleep(2)
    
        userChoice = input("Enter Choice (1-6): ").strip()
        
        fieldMapping = {
            "1": "pilotName",
            "2": "email",
            "3": "dob",
            "4": "isCaptainQualified",
            "5": "isFirstOfficerQualified"
        }
    
        if userChoice in fieldMapping:
            attributeToChange = fieldMapping[userChoice]
            newValue = input(f"Enter the new value for {attributeToChange}: ").strip()
            
        updatePilotDetails(targetID, targetName, attributeToChange, newValue)
        
        anotherChange = input("\nWould you like to change another attribute for this pilot? (Y/N): ").strip().upper()
        if anotherChange != 'Y':
                updatingPilot = False
        
        elif userChoice == "6":
            updatingPilot = False
        else:
            print("Invalid selection. Please choose 1-6.")


"""
______________________________________________________
=============• VIEW REPORTS & SUMMARIES •=============
------------------------------------------------------
"""
def getReportsMenu():
    while True:
        print("\n======REPORTS & SUMMARIES======")
        time.sleep(2)
        print("\nWould you like to...")
        time.sleep(2)
        print("1. View Popularity")
        print("2. View Flights Within Timeframe")
        print("3. View Punctuality Performance")
        print("4. Return to Main Menu")
        time.sleep(2)
        
        userChoice = input("\nEnter the number of your choice (1-4): ").strip()
        
        if userChoice == '1':
            getPopularityReport()
        elif userChoice == '2':
            startDate = input("Enter Start Date (YYYY-MM-DD): ")
            endDate = input("Enter End Date (YYYY-MM-DD): ")
            reportByTimeframe(startDate + " 00:00:00", endDate + " 23:59:59")
        elif userChoice == '3':
            reportPunctualityPerformance()
        elif userChoice == '4':
            main() 
        else:
            print("\nInvalid selection. Please try again by entering a number from the menu.")

"""
4.1 Report Counter
"""
def getPopularityReport():
    print("\nAction: View Popularity Report")
    time.sleep(2)
    print("1. Flights by Pilot")
    print("2. Pilot Workload by Month")
    print("3. Busiest Terminal Overall")
    print("4. Return to Reports & Summaries Main Menu")
    
    time.sleep(2)
    userChoice = input("\nSelect an option (1-6): ")
    time.sleep(2)
    
    if userChoice == '1':
        reportPilotFlightCount()
    elif userChoice == '2':
        reportPilotWorkloadByMonth() # Uses UNION ALL grouped by month
    elif userChoice == '3':
        reportBusiestTerminal() # Uses UNION ALL for Departure + Arrival terminals 
    elif userChoice == '4':
            getReportsMenu() 
    else:
        print("Invalid choice. Returning to reports menu.")
    

# """
# Option 5: Get flights without full crew
# """
# def getFlightsWithoutCrew():
#     print("\nSearching for Scheduled Flights without a Pilot assigned...")

#     selectedAttributes = [
#         "flightID", "scheduledDepartureDateTime", "flightStatus", "captainID", "firstOfficerID", "arrivalDestinationID", "departureDestinationID"
#         ]
#     viewFlightsByCriteria("unassigned", (), selectedAttributes) #() because no ? placeholder
            

#================•UTILITY DATA & INPUT HANDLING================
def handleUserReset():
    print("\nEnter 'Exit' to leave the session, enter 'Return' to start again.")
    userInput = input("Enter: ").strip().lower() #lower so that it isn't case sensitive
    time.sleep(2)
    if userInput == 'exit':
        sys.exit()
    else:
        main()
        
"""
Dictionary for field guidance
"""
attributeGuidance = {
    "destination": {
        "destinationID": "(PK. 3 character airport name abbreviation)",
        "destinationName": "(Airport name)"
    },
    "terminal": {
        "terminalID": "(PK. Terminal name abbreviation)",
        "terminalName": "(Optional. Full terminal name)"
    },
    "pilot": {
        "pilotID": "PK. Autogenerated by system", #auto
        "pilotName": "",
        "email": "",#enfoce "@domain"
        "dob": "(YYYY-MM-DD)",
        "isCaptainQualified": "(0 for No, 1 for Yes)",
        "isFirstOfficerQualified": "(0 for No, 1 for Yes)"
    },
    "flight": {
        "flightID": "(Flight Number, Part 1 of PK)",
        "scheduledDepartureDateTime": "(YYYY-MM-DD HH:MM:SS, Part 2 of PK)",
        "flightStatus": "(Allowable values: Scheduled, In-air, Landed, Cancelled)",
        "captainID": "(Optional. Must exist in pilot table)",
        "firstOfficerID": "(Optional. Must exist in pilot table)",
        "arrivalDestinationID": "(3 letter airport code. Must exist in destination table)",
        "departureDestinationID": "(3 letter airport code. Must exist in destination table)",
        "diversionDestinationID": "(Optional. 3 letter airport code. Must exist in destination table)",
        "departureTerminalID": "(Must exist in terminal table)",
        "arrivalTerminalID": "(Optional. Must exist in terminal table)",
        "diversionTerminalID": "(Optional. Must exist in terminal table)",
        "scheduledArrivalDateTime": "(YYYY-MM-DD HH:MM:SS)",
        "actualArrivalDateTime": "(Optional. YYYY-MM-DD HH:MM:SS)",
        "actualDepartureDateTime": "(Optional. YYYY-MM-DD HH:MM:SS)",
    }
}

"""
Reusable function to get user input for any table
"""
def getUserInput(tableName, attributeList):
    print(f"Entering details for {tableName} table...")
    collectedData = []
    
    inputGuidance = attributeGuidance.get(tableName, {})
    
    for attribute in attributeList:
        #pilotID is an autoincrement ID. Don't want user input for this
        if attribute == "pilotID":
            print(f"{attribute}: No entry needed. Auto-generated")
            continue #skip input call for this attribute
        guidance = inputGuidance.get(attribute, "")
        val = input(f"Enter {attribute} {guidance}: ").strip()
        
        #Capitalise flightID
        if attribute in [
            "flightID", "arrivalDestinationID", "departureDestinationID", "diversionDestinationID"
            ]:
            val = val.upper()
        
        #Check for missing mandatory field. If error, ask user to re-enter value
        if val == "" and ("PK" in guidance or "Optional" not in guidance):
            while val == "":
                print(f"ERROR: {attribute} is required.")
                val = input(f"Enter {attribute} {guidance}: ").strip()
            
        collectedData.append(val if val != "" else None)
        
    return tuple(collectedData)

if __name__ == "__main__":
    main()
