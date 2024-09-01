import streamlit as st
import sqlite3
from datetime import datetime
from hashlib import sha256
import pandas as pd

# START CODE FOR BACKGROUND
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://assets.publishing.service.gov.uk/media/5a4f87d540f0b648c7222969/960-night-flight.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)
#END CODE FOR BACKGROUND


def get_db_connection():
    conn = sqlite3.connect('travel_booking.db')
    conn.row_factory = sqlite3.Row  
    return conn

def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()

def create_user(username, password, email, phone_no):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    cursor.execute("INSERT INTO Users (Username, Password, Email, PhoneNo, CDate, CTime) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, hashed_password, email, phone_no, current_date, current_time))
    conn.commit()
    conn.close()
    st.success("User created successfully!")

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user, user['UserId'] if user else None

def get_airports():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT DeptAirport AS Airport FROM Flights UNION SELECT DISTINCT ArrivalAirport AS Airport FROM Flights")
    airports = [row['Airport'] for row in cursor.fetchall()]

    conn.close()
    return airports


def search_flights(dept_airport, arrival_airport, dept_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Flights.FlightNo, FlightInfo.Airline, Flights.DeptDate, Flights.DeptTime,
               Flights.ArrivalDate, Flights.ArrivalTime, Flights.Price
        FROM Flights
        JOIN FlightInfo ON Flights.FlightID = FlightInfo.FlightID
        WHERE Flights.DeptAirport = ? AND Flights.ArrivalAirport = ? AND Flights.DeptDate = ?
    ''', (dept_airport, arrival_airport, dept_date))
    flights = cursor.fetchall()
    conn.close()
    return flights



def get_hotels_locations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Address FROM Hotels")
    locations = [row['Address'] for row in cursor.fetchall()]
    conn.close()
    return locations


def search_hotels(location, entry_date, exit_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT HotelInfo.HotelName, Hotels.Address, Hotels.Price, Hotels.Rating
        FROM Hotels
        JOIN HotelInfo ON Hotels.HotelID = HotelInfo.HotelID
        WHERE Hotels.Address = ? AND Hotels.EntryDate <= ? AND Hotels.ExitDate >= ?
    ''', (location, entry_date, exit_date))
    hotels = cursor.fetchall()
    conn.close()
    return hotels


def get_car_pickup_locations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT PickupLocation FROM Cars")
    locations = [row['PickupLocation'] for row in cursor.fetchall()]
    conn.close()
    return locations

def get_total_price(car_name, house_name, flight_name):
    conc = get_db_connection()
    cursor = conc.cursor()
    car_id = cursor.execute("SELECT CarID FROM CarsInfo WHERE CarType = ?", (car_name,)).fetchone()[0]
    house_id = cursor.execute("SELECT HotelID FROM HotelInfo WHERE HotelName = ?", (house_name,)).fetchone()[0]
    flight_id = cursor.execute("SELECT FlightID FROM FlightInfo WHERE Airline = ?", (flight_name,)).fetchone()[0]
    cursor.execute("SELECT Price FROM Cars WHERE CarID = ?", (car_id,))
    car_price = cursor.fetchone()[0]
    cursor.execute("SELECT Price FROM Hotels WHERE HotelID = ?", (house_id,))
    house_price = cursor.fetchone()[0]
    cursor.execute("SELECT Price FROM Flights WHERE FlightID = ?", (flight_id,))
    flight_price = cursor.fetchone()[0]

    total_price = car_price + house_price + flight_price
    return total_price


def search_cars(location, pickup_date, drop_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT PickupTime, RentalCompany, IsAvailable, Price, DropLocation, DropDate, DropTime FROM Cars
        WHERE PickupLocation = ? AND PickupDate = ? AND DropDate = ?
    ''', (location, pickup_date, drop_date))
    cars = cursor.fetchall()
    conn.close()
    return cars

st.title("Travel Booking System")

if 'user' not in st.session_state:

    st.header("Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    phone_no = st.text_input("Phone Number")

    if st.button("Create Account"):
        create_user(username, password, email, phone_no)

    st.header("Login")
    login_username = st.text_input("Login Username")
    login_password = st.text_input("Login Password", type="password")

    if st.button("Login"):
        user, user_id = login_user(login_username, login_password)
        if user:
            st.success(f"Logged in as {login_username}")
            st.session_state['user'] = user
            st.session_state['user_id'] = user_id
        else:
            st.error("Invalid username or password")
else:
    st.sidebar.title("Menu")
    menu_option = st.sidebar.selectbox("Choose an option", ["Search Flights", "Search Hotels", "Search Rental Cars", "Manage Bookings"])

    if menu_option == "Search Flights":
        st.header("Search for Flights")
        airports = get_airports()
        dept_airport = st.selectbox("Departure Airport", airports)
        arrival_airport = st.selectbox("Arrival Airport", airports)
        dept_date = st.date_input("Departure Date").strftime('%Y-%m-%d')
    
        if st.button("Search Flights"):
            flights = search_flights(dept_airport, arrival_airport, dept_date)
            if flights:
                    Flight_df = pd.DataFrame(flights, columns=['Flight Number','Airline Name', 'Dept Date', 'Dept Time', 'Arrival Date', 'Arrival Time', 'Price($)'])
                    st.dataframe(Flight_df, use_container_width=True)
            
            else:
                st.write("No flights found.")

    elif menu_option == "Search Hotels":
        st.header("Search for Hotels")
        locations = get_hotels_locations()
        location = st.selectbox("Hotel Location", locations)
        entry_date = st.date_input("Check-in Date").strftime('%Y-%m-%d')
        exit_date = st.date_input("Check-out Date").strftime('%Y-%m-%d')
        
        if st.button("Search Hotels"):
            hotels = search_hotels(location, entry_date, exit_date)
            if hotels:
                    Hotel_df = pd.DataFrame(hotels, columns=['HotelName','HotelAddress', 'Price($)', 'Rating'])
                    st.dataframe(Hotel_df, use_container_width=True)
            else:
                st.write("No hotels found.")

    
    elif menu_option == "Search Rental Cars":
        st.header("Search for Rental Cars")
        locations = get_car_pickup_locations()
        pickup_location = st.selectbox("Pickup Location", locations)
        pickup_date = st.date_input("Pickup Date").strftime('%Y-%m-%d')
        drop_date = st.date_input("Drop Date").strftime('%Y-%m-%d')
        
        if st.button("Search Cars"):
            cars = search_cars(pickup_location, pickup_date, drop_date)
            if cars:
                Car_df = pd.DataFrame(cars, columns=['PickupTime','RentalCompany', 'IsAvailable', 'Price($)', 'DropLocation', 'DropDate', 'DropTime'])
                st.dataframe(Car_df, use_container_width=True)
            
            else:
                st.write("No cars found.")


    elif menu_option == "Manage Bookings":
        st.header("Manage Bookings")
        
        if 'user' not in st.session_state:
            st.error("You need to be logged in to manage bookings.")
            st.stop()  
        
        user_id = st.session_state['user_id']
        
        submenu_option = st.sidebar.selectbox("Select an option", ["View Bookings", "Cancel Booking", "Modify Booking", "Add New Booking"])
        
        if submenu_option == "View Bookings":
            st.subheader("View Bookings")
            if user_id:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT BookingID, HotelInfo.HotelName, CarsInfo.CarType, TotalAmt
                    FROM Booking
                    JOIN HotelInfo ON Booking.HotelID = HotelInfo.HotelID
                    JOIN CarsInfo ON Booking.CarID = CarsInfo.CarID
                    WHERE UserID = ?
                ''', (user_id,))
                bookings = cursor.fetchall()
                conn.close()

                if bookings:
                    bookings_df = pd.DataFrame(bookings, columns=['BookingID','Hotel Name', 'Car Type', 'Spend Amount'])
                    st.dataframe(bookings_df, use_container_width=True)
                else:
                    st.write("No bookings found.")
            else:
                st.error("User ID not found in session.")

        elif submenu_option == "Cancel Booking":
            st.subheader("Cancel a Booking")
            booking_id_to_cancel = st.text_input("Enter Booking ID to Cancel")
            
            if st.button("Cancel Booking"):
                if booking_id_to_cancel:
                    if user_id:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM Booking WHERE BookingID = ? AND UserID = ?", (booking_id_to_cancel, user_id))
                        conn.commit()
                        conn.close()
                        st.success("Booking canceled successfully!")
                    else:
                        st.error("User ID not found in session.")
                else:
                    st.error("Please enter a Booking ID.")
        
        elif submenu_option == "Modify Booking":
            st.subheader("Modify a Booking")
            booking_id_to_modify = st.text_input("Enter Booking ID to Modify")
            
            if booking_id_to_modify:
                if user_id:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT FlightID, HotelID, CarID FROM Booking WHERE BookingID = ? AND UserID = ?
                    ''', (booking_id_to_modify, user_id))
                    booking = cursor.fetchone()
                    
                    if booking:
                        new_flight_name= st.selectbox("New Airline", [row[0] for row in [("Delta",), ("United",), ("Quantas",), ("Southwest",), ("American",)]])
                        new_hotel_name = st.selectbox("New Hotel", [row[0] for row in [("Grand Hotel",), ("Beach Resort",), ("Hilton Garden",), ("Marriott Inn",), ("Hyatt Hotel",)]])
                        new_car_name = st.selectbox("New Car Type", [row[0] for row in [('SUV',), ('Sedan',), ('Convertible',), ('Mini',), ('Truck',)]])
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        new_flight_id = cursor.execute("SELECT FlightID FROM FlightInfo WHERE Airline = ?", (new_flight_name,)).fetchone()[0]
                        new_hotel_id = cursor.execute("SELECT HotelID FROM HotelInfo WHERE HotelName = ?", (new_hotel_name,)).fetchone()[0]
                        new_car_id = cursor.execute("SELECT CarID FROM CarsInfo WHERE CarType = ?", (new_car_name,)).fetchone()[0]
                        total_amt = get_total_price(new_car_name, new_hotel_name, new_flight_name)
                        conn.close()
                        if st.button("Save Changes"):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute('''
                                UPDATE Booking
                                SET FlightID = ?, HotelID = ?, CarID = ?, TotalAmt = ?
                                WHERE BookingID = ? AND UserID = ?
                            ''', (new_flight_id, new_hotel_id, new_car_id, total_amt, booking_id_to_modify, user_id, ))
                            conn.commit()
                            conn.close()
                            st.success("Booking modified successfully!")
                    else:
                        st.error("Booking not found or you do not have permission to modify this booking.")
                else:
                    st.error("User ID not found in session.")
        
        elif submenu_option == "Add New Booking":
            conn = get_db_connection()
            cursor = conn.cursor()
            st.subheader("Add a New Booking")
            flight_name = st.selectbox("Select Flight", [row[0] for row in [("Delta",), ("United",), ("Quantas",), ("Southwest",), ("American",)]])
            hotel_name= st.selectbox("Select Hotel", [row[0] for row in [("Grand Hotel",), ("Beach Resort",), ("Hilton Garden",), ("Marriott Inn",), ("Hyatt Hotel",)]])
            car_name = st.selectbox("Select Car", [row[0] for row in [('SUV',), ('Sedan',), ('Convertible',), ('Mini',), ('Truck',)]])
            flight_id_to_book = cursor.execute("SELECT FlightID FROM FlightInfo WHERE Airline = ?", (flight_name,)).fetchone()[0]
            hotel_id_to_book = cursor.execute("SELECT HotelID FROM HotelInfo WHERE HotelName = ?", (hotel_name,)).fetchone()[0]
            car_id_to_book = cursor.execute("SELECT CarID FROM CarsInfo WHERE CarType = ?", (car_name,)).fetchone()[0]
            conn.close()

            if st.button("Add Booking"):
                if flight_id_to_book and hotel_id_to_book and car_id_to_book:
                    if user_id:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        total_amt = get_total_price(car_name, hotel_name, flight_name)
                        bookID = cursor.execute("SELECT BookingID FROM Booking ORDER BY BookingID DESC LIMIT 1").fetchone()[0]
                        bookID = bookID[:1] + str(int(bookID[1:]) + 1)
                        cursor.execute('''
                            INSERT INTO Booking (BookingID, UserID, FlightID, HotelID, CarID, BookingDate, TotalAmt)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (bookID ,user_id, flight_id_to_book, hotel_id_to_book, car_id_to_book, datetime.now().strftime('%Y-%m-%d'), total_amt))
                        conn.commit()
                        conn.close()
                        st.success("New booking added successfully!")
                    else:
                        st.error("User ID not found in session.")
                else:
                    st.error("Please select all the required details.")


