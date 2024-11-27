class CSP:
    def __init__(self, domains, variables, constraints):
        self.domains = domains
        self.variables = variables
        self.constraints = constraints
        self.way_length = 0

    def is_schedule_consistent(self, var, value, assignment):
        lesson, _ = value
        assignment[var] = value
        day = var[0]

        # Перевірка жорстких обмежень
        for other_var, other_value in assignment.items():
            other_day = other_var[0]
            if var == other_var:
                continue

            other_lesson, _ = other_value
            if day == other_day:
                # Викладач не може викладати у двох місцях одночасно
                if lesson.lecturer == other_lesson.lecturer and lesson.timeslot == other_lesson.timeslot:
                    del assignment[var]
                    return False

                # Група не може бути на двох заняттях одночасно
                if lesson.group == other_lesson.group and lesson.timeslot == other_lesson.timeslot:
                    del assignment[var]
                    return False

                # Аудиторія не може бути зайнята одночасно
                if lesson.room == other_lesson.room and lesson.timeslot == other_lesson.timeslot:
                    del assignment[var]
                    return False

        # В кабінеті не може бути більше людей, ніж є місця
        if lesson.group.students_num > lesson.room.capacity:
            del assignment[var]
            return False

        del assignment[var]
        return True

    def least_constraining_value(self, var, assignment):
        def has_hours_left(value):
            hours = value[1]
            subj_count = 0

            for assigned_var in assignment:
                lesson = assignment[assigned_var][0]
                if lesson.group == var[1] and lesson.subject == value[0].subject:
                    subj_count += 1
            return hours > subj_count

        def find_constraints(var):
            for constraint in self.constraints:
                if var in constraint:
                    return constraint

        def count_conflicts(value):
            lesson, _ = value
            assignment[var] = value
            conflicts = 0
            for other_var in find_constraints(var):
                if other_var in assignment:
                    continue
                for other_value in self.domains[other_var]:
                    if not self.is_schedule_consistent(other_var, other_value, assignment):
                        conflicts += 1
            del assignment[var]
            return conflicts

        available_domain = [v for v in self.domains[var] if has_hours_left(v)]
        return sorted(available_domain, key=count_conflicts)

    def degree_heuristic(self, assignment):
        unassigned = [var for var in self.variables if var not in assignment]
        max_lim_count = {var: 0 for var in unassigned}
        for var in unassigned:
            for constraint in self.constraints:
                if var in constraint:
                    unassigned_vars = [v for v in constraint if v not in assignment]
                    if unassigned_vars:
                        max_lim_count[var] += 1

        return min(unassigned, key=lambda var: max_lim_count[var])

    def minimum_remaining_values(self, assignment):
        unassigned = [var for var in self.variables if var not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def backtracking_search(self):

        assignment = {}

        def backtrack():

            if len(assignment) == len(self.variables):
                return assignment

            var = self.minimum_remaining_values(assignment)
            values = self.least_constraining_value(var, assignment)

            for value in values:
                self.way_length += 1

                if self.is_schedule_consistent(var, value, assignment):
                    assignment[var] = value

                    result = backtrack()
                    if result:
                        return result
                    del assignment[var]
            return None

        return backtrack()


class CSPExtended(CSP):
    def __init__(self, domains, variables, constraints):
        super().__init__(domains, variables, constraints)

    def least_constraining_value(self, var, assignment):
        def find_constraints(var):
            for constraint in self.constraints:
                if var in constraint:
                    return constraint

        def count_conflicts(value):
            lesson, _ = value
            assignment[var] = value
            conflicts = 0
            for other_var in find_constraints(var):
                if other_var in assignment:
                    continue
                for other_value in self.domains[other_var]:
                    if not self.is_schedule_consistent(other_var, other_value, assignment):
                        conflicts += 1
            del assignment[var]
            return conflicts

        return sorted(self.domains[var], key=count_conflicts)
