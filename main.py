import math
import random

from csv_db import export_day_to_csv, export_schedule_to_csv
from lesson import Lesson

from lists import SUBJECTS, ROOMS, TIMESLOTS, GROUPS, LECTURERS

POP_SIZE = 100
MUT_RATE = 0.2
GENERATIONS = 50


def generate_random_lesson():
    subject = random.choice(SUBJECTS)
    subject_name = subject.name
    lecturer = subject.get_random_teacher()
    group = random.choice(GROUPS)
    room = random.choice(ROOMS)
    timeslot = random.choice(TIMESLOTS)
    return Lesson(subject_name, lecturer, group, room, timeslot)


def generate_random_day():
    day = []

    for _ in range(10):
        lesson = generate_random_lesson()
        day.append(lesson)
    return day


def fitness(day):
    penalty = 0

    # Жорсткі обмеження
    lecturer_times = {}
    group_times = {}
    room_times = {}
    lecturer_slots = {lecturer: [] for lecturer in LECTURERS}
    group_slots = {group: [] for group in GROUPS}

    for lesson in day:
        # Викладач не може викладати в двох місцях одночасно
        if (lesson.lecturer, lesson.timeslot) in lecturer_times:
            return math.inf
        lecturer_times[(lesson.lecturer, lesson.timeslot)] = lesson.room

        # Група не може мати кілька занять одночасно
        if (lesson.group, lesson.timeslot) in group_times:
            return math.inf
        group_times[(lesson.group, lesson.timeslot)] = lesson.room

        # Аудиторія не може бути зайнята більше одного разу в один час
        if (lesson.room, lesson.timeslot) in room_times:
            return math.inf
        room_times[(lesson.room, lesson.timeslot)] = lesson.group

        lecturer_slots[lesson.lecturer].append(lesson.timeslot)
        group_slots[lesson.group].append(lesson.timeslot)

    # М'які обмеження
    # Зменшення "вікон" (чим менше вікон, тим краще)
    for slots in lecturer_slots.values():
        if len(slots) > 1:
            slots.sort()
            for i in range(len(slots) - 1):
                index1 = TIMESLOTS.index(slots[i])
                index2 = TIMESLOTS.index(slots[i + 1])
                window = index2 - index1
                penalty += window * 10

    for slots in group_slots.values():
        if len(slots) > 1:
            slots.sort()
            for i in range(len(slots) - 1):
                index1 = TIMESLOTS.index(slots[i])
                index2 = TIMESLOTS.index(slots[i + 1])
                window = index2 - index1
                penalty += window * 10

    # Заняття не може проводитися, якщо група більша за кількість місць в аудиторії.
    for lesson in day:
        students_num = lesson.group.students_num
        room_capacity = lesson.room.capacity

        if students_num > room_capacity:
            penalty += (students_num - room_capacity) * 5

    return penalty


def crossover(parent1, parent2):
    child1, child2 = parent1, parent2
    if random.random() < MUT_RATE:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


def mutate(day):
    for i in range(len(day)):
        if random.random() < MUT_RATE:
            day[i] = generate_random_lesson()
    return day


def genetic_algorithm(logging=False):
    penalty = math.inf
    population = []

    while penalty == math.inf:
        population = [generate_random_day() for _ in range(POP_SIZE)]
        penalty = min([fitness(p) for p in population])

    for generation in range(GENERATIONS):
        population.sort(key=lambda x: fitness(x))
        parents = population[:2]

        penalty = math.inf
        new_population = []

        while penalty == math.inf:
            for _ in range(POP_SIZE // 2):
                child1, child2 = crossover(parents[0], parents[1])
                new_population.extend([mutate(child1), mutate(child2)])
            penalty = min([fitness(p) for p in new_population])

        population = new_population
        population.sort(key=lambda x: fitness(x))
        best_penalty = fitness(population[0])
        if logging:
            print(f"Generation {generation + 1}, Best fitness: {best_penalty}")
        # if best_penalty == 0:
    population[0].sort(key=lambda x: x.timeslot)
    return population[0]


def generate_schedule(logging=False):
    best_schedule = []
    for _ in range(5):
        best_schedule.append(genetic_algorithm(logging))
    return best_schedule


print("Generating week 1")

best_schedule1 = generate_schedule()
print(best_schedule1)

print("Generating week 2")
best_schedule2 = generate_schedule()
print(best_schedule2)

export_schedule_to_csv(best_schedule1, "week1_schedule.csv")
export_schedule_to_csv(best_schedule2, filename='week2_schedule.csv')
