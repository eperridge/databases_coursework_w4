"""
dbSeeding.py - Data Population via Seeding
    This script seeds flightManagement.db with sample data
"""
import sqlite3
from dbOperations import flightAttributeList

#Establish connection to db
conn = sqlite3.connect('flightManagement.db')
cursor = conn.cursor()

#Add data to tables in order of reverse dependency (independent to dependent)

#destinations - create a list to be added using a loop
destinations = [
    ('LHR', 'London Heathrow', 'United Kingdom', 'London'),
    ('LGW', 'London Gatwick', 'United Kingdom', 'London'),
    ('BRS', 'Bristol Airport', 'United Kingdom', 'Bristol'),
    ('MAN', 'Manchester Airport', 'United Kingdom', 'Manchester'),
    ('EDI', 'Edinburgh Airport', 'United Kingdom', 'Edinburgh'),
    ('LCA', 'Larnaka International Airport', 'Cyprus', 'Larnaca'),
    ('INN', 'Innsbruck Airport', 'Austria', 'Innsbruck'),
    ('SIN', 'Singapore Changi', 'Singapore', 'Singapore'),
    ('LAX', 'Los Angeles International', 'USA', 'Los Angeles'),
    ('HKG', 'Hong Kong International', 'China', 'Hong Kong'),
    ('CDG', 'Paris Charles de Gaulle', 'France', 'Paris')
]

#Use loop in Python to go line by line to populate the tables record by record
#Use INSERT OR REPLACE to prevent key duplicate errors during re-runs
for dest in destinations:
    cursor.execute("INSERT OR REPLACE INTO destination VALUES (?, ?, ?, ?)", dest)
conn.commit()

#Seed terminal
terminals = [
    ('N', 'LGW', 'North Terminal'),
    ('S', 'LGW', 'South Terminal'),
    ('1', 'INN', 'Main Terminal'),
    ('T5', 'LHR', 'Terminal 5'),
    ('T3', 'LHR', 'Terminal 3'),
    ('T3', 'MAN', 'Terminal 3'),
    ('TERM', 'BRS', 'Main Terminal'),
    ('T3', 'SIN', 'Terminal 3'),
    ('T-B', 'LAX', 'Tom Bradley International'),
    ('T1', 'HKG', 'Terminal 1'),
    ('T1', 'EDI', 'Main Terminal'),
    ('T1', 'LCA', 'Main Terminal'),
    ('1', 'CDG', 'Terminal 1')
]
for term in terminals:
    cursor.execute("INSERT OR REPLACE INTO terminal VALUES (?, ?, ?)", term)
conn.commit()

#pilot
pilots = [
    ('Johnathon Truston', 'j.truston@airline.com', '1996-08-27', 1, 1),
    ('Amara Okoro', 'a.okoro@airline.com', '1988-11-04', 1, 1),
    ('Li Wei', 'l.wei@airline.com', '1962-03-15', 0, 1),
    ('Elena Rodriguez', 'e.rodriguez@airline.com', '1985-07-22', 1, 0),
    ('Mohammed Das', 'm.das@airline.com', '1990-09-30', 1, 1),
    ('Yuki Tanaka', 'y.tanaka@airline.com', '1994-01-12', 0, 1),
    ('Fatima Al-Sayed', 'f.alsayed@airline.com', '1982-05-18', 1, 1),
    ('Mateo Silva', 'm.silva@airline.com', '1979-12-03', 1, 0),
    ('Elena Andreou', 'e.andreou@airline.com', '1997-08-08', 0, 1),
    ('Olusola Adebayo', 'o.adebayo@airline.com', '1966-10-25', 1, 1)
]
for pilot in pilots:
    cursor.execute('''INSERT OR REPLACE INTO pilot 
                   (pilotName, email, dob, isCaptainQualified, isFirstOfficerQualified)
                   VALUES (?, ?, ?, ?, ?)
                   ''', pilot)
conn.commit()

#flight seeding
#(flightID, schDep, status, capt, FO, arrivDest, depDest, divertedDest, depTerminal, arrTerminal, divTerminal, scheduledArrival, actualArrival, actualDep)
flightAttributes = ", ".join(flightAttributeList)
valuePlaceholders = ", ".join(["?"] * len(flightAttributeList)) 
insertSQL = f"INSERT OR REPLACE INTO flight ({flightAttributes}) VALUES ({valuePlaceholders})"
flights = [
    # 1. Bristol to Innsbruck, 20.01
    ('EZY2101', '2026-01-20 06:15:00', 'Landed', 1, 2, 'INN', 'BRS', None, 'TERM', '1', None, '2026-01-20 09:15:00', '2026-01-20 09:10:00', '2026-01-20 06:20:00'),
    # 2. Innsbruck to London Heathrow, 20.01
    ('BA601', '2026-01-20 14:00:00', 'Landed', 1, 3, 'LHR', 'INN', None, '1', 'T5', None, '2026-01-20 16:05:00', '2026-01-20 16:15:00', None),
    # 3. Larnaca to Heathrow, 28.01
    ('BA663', '2026-01-28 14:45:00', 'Landed', 1, 2, 'LHR', 'LCA', None, '1', 'T5', None, '2026-01-28 17:45:00', '2026-01-28 17:50:00', '2026-01-28 14:50:00'),
    # 4. Edinburgh to Heathrow, diverted back to Edinburgh
    ('BA1435', '2025-12-02 14:00:00', 'Landed', 6, 7, 'LHR', 'EDI', 'EDI', 'T1', 'T5', 'T1', '2025-12-02 15:30:00', '2025-12-02 15:15:00', '2025-12-02 14:05:00'),
    # 5. INN to LGW, morning
    ('EZY8691', '2026-02-03 08:30:00', 'Landed', 1, 5, 'LGW', 'INN', None, '1', 'N', None, '2026-02-03 10:30:00', '2026-02-03 10:25:00', '2026-02-03 08:35:00'),
    # 6. LGW to BRS, late afternoon
    ('EZY442', '2026-02-03 17:00:00', 'In-air', 1, 6, 'BRS', 'LGW', None, 'S', 'TERM', None, '2026-02-03 18:00:00', None, '2026-02-03 17:05:00'),
    # 7. INN to BRS
    ('EZY2712', '2026-02-03 22:30:00', 'Scheduled', None, 7, 'INN', 'BRS', None, 'TERM', '1', None, '2026-02-04 01:30:00', None, None),
    # 8. CDG to LCA
    ('CY381', '2026-02-03 12:40:00', 'In-air', 1, 6, 'LCA', 'CDG', None, '1', '1', None, '2026-02-03 17:50:00', None, '2026-02-03 12:45:00'),
    # 9. CDG to LCA
    ('CY380', '2026-02-03 22:00:00', 'Scheduled', None, None, 'CDG', 'LCA', None, '1', '1', None, '2026-02-04 01:40:00', None, None),
    # 10. CDG to LCA, same flightID as #8
    ('CY381', '2026-02-19 08:00:00', 'Scheduled', None, None, 'LCA', 'CDG', None, '1', '1', None, '2026-02-05 13:10:00', None, None),
    # 11. LCA to LHR (Feb 6 Afternoon)
    ('BA663', '2026-02-06 14:45:00', 'Scheduled', 7, 6, 'LHR', 'LCA', None, '1', 'T5', None, '2026-02-06 17:45:00', None, None),
    # 12. INN to LHR, 26.02
    ('BA605', '2026-02-26 07:15:00', 'Scheduled', 1, None, 'INN', 'LHR', None, 'T5', '1', None, '2026-02-05 09:20:00', None, None)   
]
for flight in flights:
    cursor.execute(insertSQL, flight)
    # cursor.execute("""
    #     INSERT OR REPLACE INTO flight (
    #         flightID, scheduledDepartureDateTime, flightStatus, captainID, firstOfficerID, 
    #         arrivalDestinationID, departureDestinationID, diversionDestinationID, departureTerminalID, arrivalTerminalID, 
    #         diversionTerminalID, scheduledArrivalDateTime, actualArrivalDateTime, actualDepartureDateTime
    #     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    # """, flight) 
conn.commit()
print("Database seeding complete.")
conn.close()