# databases_coursework_w4
Project overview:
    This Python & SQL based command-line interface (CLI) application is desgined for airline staff to view and manage flights, pilots and destinations. In addition, it allows them to view reports. THis is done using a SQLite relational database.

Features:
    Full CRUD Operations
    - Create, read, update and delete data and records
    Tables & Views
    - Tables for destinations, terminals, flights and pilots
    - Views for departurePerformance and arrivalPerformance with calculated fields for On Time or Delayed.
        (Note that a flight is On Time until it's proven to be Delayed!)
    Pilot Assignment
    - Check pilot schedules and assign them to flights in specific roles (Captain or First Officer)
    Reporting On
    - Flights 
    - Destinations
    - Pilots
    - Time periods
    Data Integrity
    - Use of contrains: Primary Keys, Foreign Keys and CHECK constraints

How users can get started with the project:
    (1) Initiaise the database, python dbSetup.py
    (2) Data seeding,           python dbSeeding.py
    (3) Lauch the application,  python main.py

Database Schema:
    As mentioned above, there are 4 main entities.
    (1) Destination     - Stores airport information.                         PK: destinationID
    (2) Terminal        - Stores terminal airport information.                PK: terminalID, destinationID
                        - Each is linked to a destination.
    (3) Pilot           - Stores pilot information.                           PK: pilotID
    (4) Flight          - Stores flight information.                          PK: flightID, scheduledDepartureDateTime
                        - Central table connecting desinations and pilots.
