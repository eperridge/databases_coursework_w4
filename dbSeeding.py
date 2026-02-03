"""
dbSeeding.py -
"""
import sqlite3

#Establish connection
conn = sqlite3.connect('flightManagement.db')
cursor = conn.cursor()

#Add data to tables in order of reverse dependency (independent to dependent)

#destination
destinations = [
    ('LHR', 'London Heathrow', 'United Kingdom', 'London'),
    ('LGW', 'London Gatwick', 'United Kingdom', 'London'),
    ('BRS', 'Bristol Airport', 'United Kingdom', 'Bristol'),
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
    cursor.execute("INSERT INTO destination VALUES (?, ?, ?, ?)", dest)
conn.commit()
#terminal


#pilot


#flight


conn.close()