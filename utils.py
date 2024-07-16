import datetime

def get_datetime(prompt):
    while True:
        try:
            date_str = input(prompt)
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid format. Please enter in 'YYYY-MM-DD HH:MM' format.")
