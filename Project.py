import pandas as pd
import numpy as np
from datetime import datetime

# Define flight details using pandas DataFrame
flights_data = pd.DataFrame({
    'FlightNumber': [101, 102, 103, 104, 105],
    'Departure': ['2024-06-01 08:00', '2024-06-01 12:00', '2024-06-01 16:00', '2024-06-02 10:00', '2024-06-02 14:00'],
    'Destination': ['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Miami, FL', 'Dallas, TX'],
    'AvailableSeatsEconomy': [150, 200, 180, 120, 160],
    'AvailableSeatsFirstClass': [30, 40, 35, 25, 30],
    'TicketPriceEconomy': [200, 300, 250, 180, 220],
    'TicketPriceFirstClass': [500, 700, 600, 450, 550]
})

# Define airport locations
airport_locations = {
    'New York, NY': 'JFK International Airport (JFK)',
    'Los Angeles, CA': 'Los Angeles International Airport (LAX)',
    'Chicago, IL': 'O Hare International Airport (ORD)',
    'Miami, FL': 'Miami International Airport (MIA)',
    'Dallas, TX': 'Dallas/Fort Worth International Airport (DFW)'
}

def get_nearest_airport(departure_location):
    nearest_airport = ""
    min_distance = float('inf')
    for location, airport in airport_locations.items():
        distance = abs(hash(location) - hash(departure_location))  # Calculate distance (hash difference for simplicity)
        if distance < min_distance:
            min_distance = distance
            nearest_airport = airport
    return nearest_airport

def get_available_departure_times(date):
    # Assuming a simplified availability based on the flight schedule
    available_times = flights_data.loc[flights_data['Departure'].str.startswith(date), 'Departure'].tolist()
    return available_times

def book_flight(name, flight_number, num_tickets, flight_class):
    # Check if the flight exists
    if flight_number in flights_data['FlightNumber'].values:
        # Determine the class
        if flight_class.lower() == 'economy':
            class_key = 'AvailableSeatsEconomy'
            available_seats_key = 'AvailableSeatsEconomy'
            ticket_price_key = 'TicketPriceEconomy'
        elif flight_class.lower() == 'first class':
            class_key = 'AvailableSeatsFirstClass'
            available_seats_key = 'AvailableSeatsFirstClass'
            ticket_price_key = 'TicketPriceFirstClass'
        else:
            return "Invalid flight class. Please choose either Economy or First Class."

        # Check seat availability
        idx = flights_data[flights_data['FlightNumber'] == flight_number].index[0]
        available_seats = flights_data.loc[idx, available_seats_key]
        if num_tickets <= available_seats:
            # Update available seats
            flights_data.loc[idx, available_seats_key] -= num_tickets
            # Calculate total cost
            ticket_price = flights_data.loc[idx, ticket_price_key]
            total_cost = num_tickets * ticket_price
            return f"Dear {name}, your {flight_class} booking for Flight {flight_number} is confirmed. Total cost: ${total_cost}"
        else:
            return "Not enough seats available."
    else:
        return "Flight not found."

# Example usage with user interaction
print("Welcome to Flight Booking System!")
name = input("Please enter your name: ")

print("Available Departure Locations:")
print(list(airport_locations.keys()))
departure_location = input("Enter your departure location: ")

print("Nearest Airport:")
nearest_airport = get_nearest_airport(departure_location)
print(nearest_airport)

date = input("Enter your preferred departure date (YYYY-MM-DD): ")
available_departure_times = get_available_departure_times(date)
print("Available Departure Times:")
print(available_departure_times)

print("Available Flights:")
print(flights_data[['FlightNumber', 'Destination']])

flight_num = int(input("Enter the Flight Number you want to book: "))
num_tickets = int(input("Enter the number of tickets: "))
flight_class = input("Enter the class you want to book (Economy or First Class): ")

booking_result = book_flight(name, flight_num, num_tickets, flight_class)
print(booking_result)
