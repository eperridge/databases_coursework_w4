"""
dbSeeding.py -
"""
import sqlite3

#Establish connection
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
for dest in destinations:
    cursor.execute("INSERT OR REPLACE INTO destination VALUES (?, ?, ?, ?)", dest)
conn.commit()

#terminal
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

#flight


conn.close()