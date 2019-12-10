class Assignment:
    def __init__(self, name, course, due_day, due_month, due_year):
        self.name = name
        self.course = course
        self.due_day = due_day
        self.due_month = due_month
        self.due_year = due_year


class AssignmentList:
    def __init__(self):
        self.assignment_list = []

    def add_assignment(self, assignment):
        self.assignment_list.append(assignment)

    def remove_assignment(self, assignment):
        self.assignment_list.remove(assignment)
