from Patrick import *
lst_of_users: list[User] = []



user1 = User("Patrick", [Event({'start date': '2024-05-20', 'start time': '12:00', 'end date': '2024-05-20', 'end time': '15:00', 'Original time zone': '-04:00', 'description': 'Hello world'})])
user2 = User("Gavin", [Event({'start date': '2024-05-20', 'start time': '16:45', 'end date': '2024-05-20', 'end time': '17:45', 'Original time zone': '-04:00', 'description': 'Hello world'})])

print(time_overlap([user1, user2], "2024-05-20"))
