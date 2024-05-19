def _time_overlap_for_2_people(lst1: list[list[str]], lst2: list[list[str]],
                               duration: int = 0) -> list[list[str]]:
    """takes in two lists representing schedules of free times and outputs
    the compatible times between the two where they can have a meeting with
    minimum duration <duration> which is in minutes. If duration == 0 or not
    specified then it outputs all the overlapping free times for the two.

    Precondition: lists are sorted in increasing time
    >>> _time_overlap_for_2_people([["9:00", "9:24"], ["13:00", "14:00"]], [["13:29", "15:00"]], 60)
    []
    >>> _time_overlap_for_2_people([["10:00", "11:30"], ["12:30", "14:10"]], [["11:00", "12:00"], ["13:30", "15:00"]], 35)
    [['13:30', '14:10']]

    >>> _time_overlap_for_2_people([["9:00", "10:30"]], [["11:00", "12:00"]], 0)  # No overlap
    []

    >>> _time_overlap_for_2_people([["9:00", "12:00"]], [["10:00", "11:00"]], 50)  # Complete overlap
    [['10:00', '11:00']]

    >>> _time_overlap_for_2_people([], [["10:00", "11:00"]], 5) # Empty list
    []

    >>> _time_overlap_for_2_people([["09:00", "11:00"]], [["9:30", "10:30"], ["11:15", "12:30"]], 70) # Multiple overlapping intervals
    []
    >>> _time_overlap_for_2_people([["11:30", "12:30"], ["15:00", "16:00"], ["17:00", "18:30"]], [["10:30", "12:00"], ["13:00", "16:00"], ["18:00", "20:00"]], 30)
    [['11:30', '12:00'], ['15:00', '16:00'], ['18:00', '18:30']]
    """
    first, second, overlap = [], [], []
    # convert the times to decimals to compare them. (in the form of: the number
    # of hours after midnight) Ex: 13:30 -> 13.5 & 09:45 -> 9.75 & 13.5 > 9.75
    for lst in lst1:  # lst represents a time block
        first.append((int(lst[0][:lst[0].find(":")]) + int(
            lst[0][lst[0].find(":") + 1:]) / 60
                      , int(lst[1][:lst[1].find(":")]) + int(
            lst[1][lst[1].find(":") + 1:]) / 60))
    for lst in lst2:
        second.append((int(lst[0][:lst[0].find(":")]) + int(
            lst[0][lst[0].find(":") + 1:]) / 60
                       , int(lst[1][:lst[1].find(":")]) + int(
            lst[1][lst[1].find(":") + 1:]) / 60))

    # for each time-interval in the first list, find ALL overlapping intervals
    # from the other list and add them to <overlap> if that overlapping time is
    # greater than or equal to the min duration.
    for interval in first:
        for other in second:
            start = max(other[0], interval[0])
            end = min(other[1], interval[1])
            if end > start and (end - start) * 60 >= duration:
                overlap.append((start, end))

            # if the first interval ends before the second then it's impossible
            # for it to overlap with any other intervals in the second list
            if other[1] >= interval[1]:
                break

    return [  # format the lists of time-intervals in <overlap> to military time
        [f"0{int(i[0] // 1)}:"[-3:] +
         f"0{int(round(60 * (i[0] - i[0] // 1), 0))}"[-2:]
            ,
         f"0{int(i[1] // 1)}:"[-3:] +
         f"0{int(round(60 * (i[1] - i[1] // 1), 0))}"[-2:]
         ] for i in overlap]  # and then returns it


def time_overlap_for_n_people(lst: list[list[list[str]]], duration: int = 0) \
        -> list[list[str]]:
    """takes in a list of lists representing schedules of free times and outputs
    the compatible times between all the people where they can have a meeting
    with minimum duration <duration> which is in minutes. If duration == 0 or
    not specified then it outputs all the overlapping free times for the two.

    Precondition: lists are sorted in increasing time
    >>> time_overlap_for_n_people([[["9:00", "9:24"], ["13:00", "14:00"]], [["13:29", "15:00"]], [["13:29", "15:00"]]], 60)
    []
    >>> time_overlap_for_n_people([[["10:00", "11:30"], ["12:30", "14:10"]], [["11:00", "12:00"], ["13:30", "15:00"]]], 35)
    [['13:30', '14:10']]

    >>> time_overlap_for_n_people([[["9:00", "10:30"]], [["11:00", "12:00"]]], 0)  # No overlap
    []

    >>> time_overlap_for_n_people([[["9:00", "12:00"]], [["10:00", "11:00"]]], 50)  # Complete overlap
    [['10:00', '11:00']]

    >>> time_overlap_for_n_people([[], [["10:00", "11:00"]]], 5) # Empty list
    []

    >>> time_overlap_for_n_people([[["09:00", "11:00"]], [["9:30", "10:30"], ["11:15", "12:30"]]], 70) # Multiple overlapping intervals
    []
    >>> time_overlap_for_n_people([[["11:30", "12:30"], ["15:00", "16:00"], ["17:00", "18:30"]], [["10:30", "12:00"], ["13:00", "16:00"], ["18:00", "20:00"]]], 30)
    [['11:30', '12:00'], ['15:00', '16:00'], ['18:00', '18:30']]

    Precondition: lists are sorted in increasing time and len(lst) >= 2
    """
    overlap = lst[0]
    for i in range(1, len(lst)):
        overlap = _time_overlap_for_2_people(overlap, lst[i], duration)
    return overlap


"""                     "data base" format
dict = {"user_1_id": {'name': str, 'email': str, 'token': dict}
        "user_2_id": {'name': str, 'email': str, 'token': dict}
        ...
        ...
        "user_n_id": {'name': str, 'email': str, 'token': dict}
        }
"""


class Event:
    def __init__(self, dictionary: dict):
        # sample input: {'start date': '2024-05-21', 'start time': '12:00', 'end date': '2024-05-21', 'end time': '13:00', 'Original time zone': '-04:00', 'description': 'Hello world'}
        self.description = dictionary['description']
        self.start_date = dictionary['start date']
        self.start_time = dictionary['start time']
        self.end_date = dictionary['end date']
        self.end_time = dictionary['end time']
        self.original_time_zone = dictionary['Original time zone']


class User:
    def __init__(self, name: str, events_lst: list[Event], email: str = ''):
        self.name = name
        self.email = email
        self.events = events_lst

    def get_free(self, specific_date) -> list[list[str]]:
        """this function returns the free times of the user on a specific date
        in the format of a list of lists where each list represents a time
        interval in the form of [start_time, end_time] in military time. If the
        user has no events on that day then it returns the whole day as free.
        It does this by checking the events of the user that happen on that day
        and then finding the free times between them. However, there are
        boundaries from 7am to 10pm, you return the free times between these
        boundaries.
        >>> user = User("Patrick", [Event({'start date': '2024-05-21', 'start time': '12:00', 'end date': '2024-05-21', 'end time': '13:00', 'Original time zone': '-04:00', 'description': 'Hello world'}), Event({'start date': '2024-05-21', 'start time': '15:00', 'end date': '2024-05-21', 'end time': '16:00', 'Original time zone': '-04:00', 'description': 'Hello world'})])
        >>> user.get_free("2024-05-21")
        [['07:00', '12:00'], ['13:00', '15:00'], ['16:00', '22:00']]
        """
        if not self.events:
            return [["07:00", "22:00"]]
        free_times = []
        for i in range(len(self.events) - 1):
            free_times.append(
                [self.events[i].end_time, self.events[i + 1].start_time])
        if self.events[0].start_time != "07:00":
            free_times.insert(0, ["07:00", self.events[0].start_time])
        if self.events[-1].end_time != "22:00":
            free_times.append([self.events[-1].end_time, "22:00"])
        return free_times


def time_overlap(lst: list[User], specific_date, duration: int = 0) -> list[
    list[str]]:
    """takes in a list of users and outputs the compatible times between all the
    people where they can have a meeting on a specific date with minimum duration
    <duration> which is in minutes. If duration == 0 or not specified then it
    outputs all the overlapping free times for the two."""
    lst_of_free_times_for_each_user = []
    for user in lst:
        lst_of_free_times_for_each_user.append(user.get_free(specific_date))
    return time_overlap_for_n_people(lst_of_free_times_for_each_user, duration)
# hello world
