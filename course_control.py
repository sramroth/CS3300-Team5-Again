from assignment_control import *


class Course:
    def __init__(self, name):
        self.name = name
        self.assignment_list = AssignmentList()


class CourseList:
    def __init__(self):
        self.course_list = []

    def add_course(self, course):
        self.course_list.append(course)

    def remove_course(self, course):
        self.course_list.remove(course)
