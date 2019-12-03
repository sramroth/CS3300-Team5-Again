class Assignment:
    def __init__(self, name, course, due_date):
        self.name = name
        self.course = course
        self.due_date = due_date


class AssignmentList:
    def __init__(self):
        self.assignment_list = []

    def add_assignment(self, assignment):
        self.assignment_list.append(assignment)

    def remove_assignment(self, assignment):
        self.assignment_list.remove(assignment)
