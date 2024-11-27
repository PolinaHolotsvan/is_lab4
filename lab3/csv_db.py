import csv

from lesson import Lesson
from lists import GROUPS, ROOMS


def export_day_to_csv(schedule, filename='day.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'Lecturer', 'Group', 'Room', 'Timeslot'])

        for lesson in schedule:
            writer.writerow([lesson.subject, lesson.lecturer, lesson.group.name, lesson.room.name, lesson.timeslot])


def import_day_from_csv(filename='day.csv'):
    schedule = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            subject = row['Subject']
            lecturer = row['Lecturer']
            group = next(g for g in GROUPS if g.name == row['Group'])
            room = next(r for r in ROOMS if r.name == row['Room'])
            timeslot = row['Timeslot']

            schedule.append(Lesson(subject, lecturer, group, room, timeslot))
    return schedule



def export_schedule_to_csv(schedule, filename='schedule.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Day", "Subject", "Lecturer", "Group", "Room", "Timeslot"])

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day_index, day in enumerate(schedule):
            for lesson in day:
                writer.writerow([days[day_index], lesson.subject, lesson.lecturer, lesson.group.name, lesson.room.name,
                                 lesson.timeslot])

    print(f"Schedule exported to {filename}")
