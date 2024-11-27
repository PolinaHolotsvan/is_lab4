class Group:
    def __init__(self, name, students_num):
        self.name = name
        self.students_num = students_num

    def __repr__(self):
        return f'{self.name}'
