import datetime
from db import DBConnection

class Meeting:
    def __init__(self, title, start_time, end_time, participants=None, room_id=None):
        self.id = None  # ID will be assigned when saved to DB
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.participants = participants if participants else []
        self.room_id = room_id

class User: 
    def __init__(self, name):
        self.id = None  # ID will be assigned when saved to DB
        self.name = name

class MeetingRoom:
    def __init__(self, name, capacity):
        self.id = None  # ID will be assigned when saved to DB
        self.name = name
        self.capacity = capacity

class CalendarSystem:
    def add_user(self, name):
        user = User(name)
        with DBConnection() as cursor:
            cursor.execute('INSERT INTO users (name) VALUES (%s) RETURNING id', (user.name,))
            user.id = cursor.fetchone()[0]
        return user.id

    def add_room(self, name, capacity):
        room = MeetingRoom(name, capacity)
        with DBConnection() as cursor:
            cursor.execute('INSERT INTO rooms (name, capacity) VALUES (%s, %s) RETURNING id', (room.name, room.capacity))
            room.id = cursor.fetchone()[0]
        return room.id

    def schedule_meeting(self, title, start_time, end_time, user_id, room_id=None, participants=None):
        participants = participants if participants else []
        new_meeting = Meeting(title, start_time, end_time, participants, room_id)

        # Check for user collision
        if not self._check_user_availability(user_id, start_time, end_time):
            return "Collision detected for user"

        # Check for room collision
        if room_id and not self._check_room_availability(room_id, start_time, end_time):
            return "Collision detected for room"

        # Check for participant availability
        for participant_id in participants:
            if not self._check_user_availability(participant_id, start_time, end_time):
                return f"Collision detected for participant with ID {participant_id}"

        # Schedule the meeting
        with DBConnection() as cursor:
            cursor.execute('''
                INSERT INTO meetings (title, start_time, end_time, room_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            ''', (new_meeting.title, new_meeting.start_time, new_meeting.end_time, new_meeting.room_id))
            new_meeting.id = cursor.fetchone()[0]

            cursor.execute('INSERT INTO participants (meeting_id, user_id) VALUES (%s, %s)', (new_meeting.id, user_id))
            for participant_id in participants:
                cursor.execute('INSERT INTO participants (meeting_id, user_id) VALUES (%s, %s)', (new_meeting.id, participant_id))

        return "Meeting scheduled successfully"

    def _check_user_availability(self, user_id, start_time, end_time):
        with DBConnection() as cursor:
            cursor.execute('''
                SELECT * FROM meetings m
                JOIN participants p ON m.id = p.meeting_id
                WHERE p.user_id = %s AND m.start_time < %s AND m.end_time > %s
            ''', (user_id, end_time, start_time))
            return cursor.fetchone() is None

    def _check_room_availability(self, room_id, start_time, end_time):
        with DBConnection() as cursor:
            cursor.execute('''
                SELECT * FROM meetings
                WHERE room_id = %s AND start_time < %s AND end_time > %s
            ''', (room_id, end_time, start_time))
            return cursor.fetchone() is None
