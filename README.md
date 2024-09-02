# Travel Booking System

## Table of Contents
- [Description](#Description)
- [ER Diagram](#ER-Diagram)
- [Features](#Features)
- [Tech Stack](#Tech-Stack)
- [Running Instructions](#Running-Instructions)

## Description
This project is a comprehensive travel booking system built using Python and Streamlit. The database is created and managed by using SQLite which integrates SQL in Python. The application allows users to search and book flights, hotels, and rental cars. It is designed to provide a seamless and user-friendly experience for managing travel plans.

## ER Diagram
![Travel_ER](https://github.com/user-attachments/assets/ba8d122e-ed8a-4cdd-a289-21291712c541)


## Features

- **User Authentication**: Users can create accounts and log in to access personalized features.
- **Search Flights**: Users can search for flights based on departure and arrival airports and specific dates.
- **Search Hotels**: Users can search for hotels in various locations with specified check-in and check-out dates.
- **Search Rental Cars**: Users can search for available rental cars based on pickup location, pickup date, and drop-off date.
- **Manage Bookings**: Logged-in users can view, modify, and cancel their bookings directly through the application.


## Tech Stack
- **SQLite**: Database system used to store user data, flights, hotels, and car information.
- **Streamlit**: Web framework used to create the interactive user interface.
- **Pandas**: Library used for data manipulation and displaying results in table format.

## Running Instructions

### Pre-requisites

Ensure that you have the following installed on your machine:
- Python3
- SQLite
- Streamlit
- Pandas

### Setup
- Clone the repository:
    ```bash
    git clone https://github.com/Anushka-1603/TravelBookingSystem.git
    ```
- Navigate to the project directory:
    ```bash
    cd TravelBookingSystem
    ```
- Run the application:
    ```bash
    streamlit run server.py
    ```
