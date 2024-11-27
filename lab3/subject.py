import random


class Subject:
    def __init__(self, name, teachers):
        self.name = name
        self.teachers = teachers

    def get_random_teacher(self):
        return random.choice(self.teachers)


class ExtendedSubject(Subject):
    def __init__(self, name, teachers, hours):
        super().__init__(name, teachers)
        self.hours = hours
