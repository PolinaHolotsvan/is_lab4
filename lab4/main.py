from itertools import product

from lab3.lesson import Lesson
from lab3.lists import ROOMS, WEEK, GROUPS, MI_SUBJECTS, TIMESLOTS
from lab4.scp import CSP, CSPExtended


def generate_domain(group, subjects, timeslot):
    domain = []
    for subject in subjects:
        for teacher in subject.teachers:
            for room in ROOMS:
                lesson = Lesson(subject.name, teacher, group, room, timeslot)
                domain.append([lesson, subject.hours])
    return domain


domains = {}
constraints = []
variables = []

for day, group, timeslot in product(WEEK, GROUPS[0:2], TIMESLOTS):
    var = (day, group, timeslot)
    variables.append(var)
    domains[var] = generate_domain(group, subjects=MI_SUBJECTS, timeslot=timeslot)

for day in WEEK:
    for timeslot in TIMESLOTS:
        constraints.append([
            (day, group, timeslot)
            for group in GROUPS[0:2]
        ])

csp = CSP(domains, variables, constraints)
solution = csp.backtracking_search()

if solution:
    print("Рішення знайдене:")
    for key, value in solution.items():
        print(f"{key}: {value[0]}")
    print(csp.way_length)
else:
    print("Рішення не знайдене :(")
