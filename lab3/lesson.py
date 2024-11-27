class Lesson:  # ген

    def __init__(self, subject, lecturer, group, room, timeslot):
        self.subject = subject
        self.lecturer = lecturer
        self.group = group
        self.room = room
        self.timeslot = timeslot

    def __repr__(self):
        return f"({self.subject}, {self.lecturer}, {self.group.name}, {self.room.name}, {self.timeslot})"
