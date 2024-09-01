import sqlite3

# Connect to (or create) the SQLite database
conn = sqlite3.connect('travel_booking.db')
cursor = conn.cursor()

# SQL queries to create tables
tables = [
    '''CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Email TEXT NOT NULL,
        PhoneNo TEXT,
        CDate TEXT NOT NULL,
        CTime TEXT NOT NULL
    )''',
    '''CREATE TABLE IF NOT EXISTS FlightInfo (
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
        Airline TEXT NOT NULL
    )''',
    '''CREATE TABLE IF NOT EXISTS Flights (
        FlightID INTEGER,
        FlightNo TEXT NOT NULL,
        DeptAirport TEXT NOT NULL,
        ArrivalAirport TEXT NOT NULL,
        DeptDate TEXT NOT NULL,
        DeptTime TEXT NOT NULL,
        ArrivalDate TEXT NOT NULL,
        ArrivalTime TEXT NOT NULL,
        Price DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (FlightID) REFERENCES FlightInfo(FlightID)
    )''',
    '''CREATE TABLE IF NOT EXISTS HotelInfo (
        HotelID INTEGER PRIMARY KEY AUTOINCREMENT,
        HotelName TEXT NOT NULL
    )''',
    '''CREATE TABLE IF NOT EXISTS Hotels (
        HotelID INTEGER,
        Address TEXT NOT NULL,
        Price DECIMAL(10, 2) NOT NULL,
        Rating DECIMAL(1, 1) NOT NULL,
        EntryDate TEXT NOT NULL,
        EntryTime TEXT NOT NULL,
        ExitDate TEXT NOT NULL,
        ExitTime TEXT NOT NULL,
        FOREIGN KEY (HotelID) REFERENCES HotelInfo(HotelID)
    )''',
    '''CREATE TABLE IF NOT EXISTS CarsInfo (
        CarID INTEGER PRIMARY KEY AUTOINCREMENT,
        CarType TEXT NOT NULL
    )''',
    '''CREATE TABLE IF NOT EXISTS Cars (
        CarID INTEGER,
        RentalCompany TEXT NOT NULL,
        IsAvailable TEXT NOT NULL DEFAULT 'Yes',
        PickupLocation TEXT NOT NULL,
        DropLocation TEXT NOT NULL,
        Price DECIMAL(10, 2) NOT NULL,
        PickupDate TEXT NOT NULL,
        PickupTime TEXT NOT NULL,
        DropDate TEXT NOT NULL,
        DropTime TEXT NOT NULL,
        FOREIGN KEY (CarID) REFERENCES CarsInfo(CarID)
    )''',
    '''CREATE TABLE IF NOT EXISTS Booking (
        BookingID TEXT PRIMARY KEY,
        UserID INTEGER NOT NULL,
        FlightID INTEGER,
        HotelID INTEGER,
        CarID INTEGER,
        BookingDate TEXT NOT NULL,
        TotalAmt DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (FlightID) REFERENCES Flights(FlightID),
        FOREIGN KEY (HotelID) REFERENCES Hotels(HotelID),
        FOREIGN KEY (CarID) REFERENCES Cars(CarID)
    )''',
    '''CREATE TABLE IF NOT EXISTS Payment (
        PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        BookingID TEXT NOT NULL,
        Amount DECIMAL(10, 2) NOT NULL,
        PaymentMethod TEXT NOT NULL,
        TransactionDate TEXT NOT NULL,
        TransactionTime TEXT NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
    )''',
    '''CREATE TABLE IF NOT EXISTS Notifications (
        NotificationID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        BookingID TEXT NOT NULL,
        Type TEXT NOT NULL,
        Message TEXT NOT NULL,
        SentDate TEXT NOT NULL,
        NotificationType TEXT NOT NULL CHECK (NotificationType IN ('SMS', 'Email')),
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
    )'''
]

# Create tables
for table in tables:
    cursor.execute(table)

# Insert initial data into tables
data = {
    "Users": {
        "columns": ["Username", "Password", "Email", "PhoneNo", "CDate", "CTime"],
        "values": [
            ("john_doe", "password123", "john@yahoo.com", '111-222-3333', "2024-08-01", "08:00:00"),
            ("jane_smith", "password456", "jane@hotmail.com", '222-333-4444', "2024-08-02", "09:00:00"),
            ("bob_johnson", "password789", "bob@yahoo.com", '333-444-5555', "2024-08-15", "21:00:00"),
            ("alice_william", "password1011", "alice@rediff.com", '444-555-6666', "2024-09-04", "11:00:00"),
            ("michael_brown", "password1213", "michael@gmail.com", '555-666-7777', "2024-09-05", "12:00:00")
        ]
    },
    "FlightInfo": {
        "columns": ["Airline"],
        "values": [("Delta",), ("United",), ("Quantas",), ("Southwest",), ("American",)]
    },
    "Flights": {
        "columns": ["FlightID", "FlightNo", "DeptAirport", "ArrivalAirport", "DeptDate", "DeptTime", "ArrivalDate", "ArrivalTime", "Price"],
        "values": [
            (1, "DL123", "JFK", "LAX", "2024-08-01", "10:00:00", "2024-08-01", "13:00:00", 299.99),
            (2, "UA456", "ORD", "SFO", "2024-08-02", "14:00:00", "2024-08-02", "17:00:00", 399.99),
            (3, "QU789", "DFW", "CHI", "2024-08-15", "09:00:00", "2024-08-15", "11:00:00", 499.99),
            (4, "SW101", "SEA", "LAX", "2024-09-04", "12:00:00", "2024-09-04", "16:00:00", 599.99),
            (5, "AM112", "TEX", "ATL", "2024-09-05", "13:00:00", "2024-09-05", "14:00:00", 699.99)
        ]
    },
    "HotelInfo": {
        "columns": ["HotelName"],
        "values": [("Grand Hotel",), ("Beach Resort",), ("Hilton Garden",), ("Marriott Inn",), ("Hyatt Hotel",)]
    },
    "Hotels": {
        "columns": ["HotelID", "Address", "Price", "Rating", "EntryDate", "EntryTime", "ExitDate", "ExitTime"],
        "values": [
            (1, "New York", 199.99, 4.5, '2024-08-01', '15:00:00', '2024-09-07', '11:00:00'),
            (2, "Miami", 299.99, 4.8, '2024-08-02', '18:00:00', '2024-09-06', '12:00:00'),
            (3, "Chicago", 349.99, 4.3, '2024-08-03', '14:00:00', '2024-09-08', '10:00:00'),
            (4, "Las Vegas", 499.99, 4.7, '2024-09-04', '17:00:00', '2024-09-09', '11:00:00'),
            (5, "Atlanta", 274.99, 4.2, '2024-09-05', '16:00:00', '2024-09-10', '12:00:00')
        ]
    },
    "CarsInfo": {
        "columns": ["CarType"],
        "values": [('SUV',), ('Sedan',), ('Convertible',), ('Mini',), ('Truck',)]
    },
    "Cars": {
        "columns": ["CarID", "RentalCompany", "IsAvailable", "PickupLocation", "DropLocation", "Price", "PickupDate", "PickupTime", "DropDate", "DropTime"],
        "values": [
            (1, 'Avis', 'Yes', '101 Airport Rd', '202 City Center', 60.00, '2024-09-01', '09:00:00', '2024-09-07', '17:00:00'),
            (2, 'Hertz', 'Yes', '202 Downtown Blvd', '303 Park Ave', 55.00, '2024-09-02', '10:00:00', '2024-09-08', '18:00:00'),
            (3, 'Rentaz', 'No', '303 High St', '404 Lakeview Dr', 75.00, '2024-09-03', '11:00:00', '2024-09-09', '19:00:00'),
            (4, 'Pablo Carz', 'No', '404 Main St', '505 Mountain Rd', 85.00, '2024-09-04', '12:00:00', '2024-09-10', '20:00:00'),
            (5, 'Zipcar', 'Yes', '505 West Dr', '606 Riverbank Ln', 50.00, '2024-09-05', '13:00:00', '2024-09-11', '21:00:00')
        ]
    },
    "Booking": {
        "columns": ["BookingID", "UserID", "FlightID", "HotelID", "CarID", "BookingDate", "TotalAmt"],
        "values": [
            ("B123", 1, 1, 1, 1, '2024-09-01', 560.00),
            ("B456", 2, 2, 2, 2, '2024-09-02', 755.00),
            ("B789", 3, 3, 3, 3, '2024-09-03', 924.99),
            ("B101", 4, 4, 4, 4, '2024-09-04', 1184.99),
            ("B112", 5, 5, 5, 5, '2024-09-05', 1055.00)
        ]
    },
    "Payment": {
        "columns": ["UserID", "BookingID", "Amount", "PaymentMethod", "TransactionDate", "TransactionTime"],
        "values": [
            (1, 'B123', 560.00, 'Credit Card', '2024-09-01', '09:10:00'),
            (2, 'B456', 755.00, 'Debit Card', '2024-09-02', '10:20:00'),
            (3, 'B789', 924.99, 'PayPal', '2024-09-03', '11:30:00'),
            (4, 'B101', 1184.99, 'Net Banking', '2024-09-04', '12:40:00'),
            (5, 'B112', 1055.00, 'Credit Card', '2024-09-05', '13:50:00')
        ]
    },
    "Notifications": {
        "columns": ["UserID", "BookingID", "Type", "Message", "SentDate", "NotificationType"],
        "values": [
            (1, 'B123', 'Booking', 'Your booking is confirmed.', '2024-09-01', 'Email'),
            (2, 'B456', 'Payment', 'Your payment was successful.', '2024-09-02', 'SMS'),
            (3, 'B789', 'Flight', 'Your flight is scheduled.', '2024-09-03', 'Email'),
            (4, 'B101', 'Hotel', 'Your hotel reservation is confirmed.', '2024-09-04', 'SMS'),
            (5, 'B112', 'Car', 'Your car rental is ready.', '2024-09-05', 'Email')
        ]
    }
}

# Insert data into tables
for table_name, content in data.items():
    columns = ', '.join(content["columns"])
    placeholders = ', '.join('?' * len(content["columns"]))
    for value in content["values"]:
        cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', value)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created, and data inserted successfully.")
