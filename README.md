# calender-system
This project implements a calendar system that allows users to schedule meetings, detect collisions, and manage participants and meeting rooms. 

## Project Structure

- 'calendar_system.py': Core functionality of the calendar system.
- 'db.py': Database connection and setup.
- 'main.py': Entry point for running the calendar system.

- 
## Example Usage

1. Add User
    - Enter user name: 'Anand'
    - Output: 'User added with ID: 1'

2. Add Room
    - Enter room name: 'Dev Room'
    - Enter room capacity: '5'
    - Output: 'Room added with ID: 2'

3. Schedule Meeting
    - Enter meeting title: 'Development'
    - Enter start time (YYYY-MM-DD HH:MM): '2024-07-15 09:00'
    - Enter end time (YYYY-MM-DD HH:MM): '2024-07-15 10:00'
    - Enter user ID: '1'
    - Enter room ID (optional, press Enter to skip): '2'
    - Enter participant IDs (comma-separated, optional): '2,3'
    - Output: 'Meeting scheduled successfully'
