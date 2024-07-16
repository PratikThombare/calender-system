import sys
from calendar_system import CalendarSystem
import utils
from db import create_tables
import datetime

def get_datetime(prompt):
    while True:
        try:
            date_str = input(prompt)
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid format. Please enter in 'YYYY-MM-DD HH:MM' format.")

def main():
    # Create tables if they do not exist
    create_tables()
    
    # Initialize the calendar system
    calendar_system = CalendarSystem()

    while True:
        print("\nCalendar System")
        print("1. Add User")
        print("2. Add Room")
        print("3. Schedule Meeting")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter user name: ")
            user_id = calendar_system.add_user(name)
            print(f"User added with ID: {user_id}")

        elif choice == "2":
            name = input("Enter room name: ")
            capacity = int(input("Enter room capacity: "))
            room_id = calendar_system.add_room(name, capacity)
            print(f"Room added with ID: {room_id}")

        elif choice == "3":
            title = input("Enter meeting title: ")
            start_time = get_datetime("Enter start time (YYYY-MM-DD HH:MM): ")
            end_time = get_datetime("Enter end time (YYYY-MM-DD HH:MM): ")
            user_id = int(input("Enter user ID: "))
            room_id = input("Enter room ID (optional, press Enter to skip): ")
            room_id = int(room_id) if room_id else None
            participants = input("Enter participant IDs (comma-separated, optional): ")
            participants = [int(pid) for pid in participants.split(",")] if participants else []

            result = calendar_system.schedule_meeting(title, start_time, end_time, user_id, room_id, participants)
            print(result)

        elif choice == "4":
            print("Exiting...")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
