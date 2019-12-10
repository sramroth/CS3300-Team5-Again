import tkinter as tk
from tkinter import *
from tkinter import ttk
from course_control import *


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Initialize the size of the whole application, its title, and the little icon
        # that appears at the top left of the window
        self.geometry('600x700')
        self.title("Student Planner")
        self.iconbitmap(r'favicon.ico')

        # Initialize the navigation bar and the main content frame
        NavigationBar(self)
        self.main_window = Frame(self)
        self.main_window.pack(side=TOP, fill=BOTH, expand=True)
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)
        self.course_list = CourseList()
        self.assignment_list = AssignmentList()

        # Open both input files for reading, to gather saved information
        with open('courses.txt', 'r') as courses_file:
            for line in courses_file:
                course = Course(line.rstrip())
                self.course_list.add_course(course)

        with open('assignments.txt', 'r') as assignments_file:
            for line in assignments_file:
                assignment_info = line.rstrip().split()
                assignment = Assignment(assignment_info[1], assignment_info[0],
                                        assignment_info[3], assignment_info[2], assignment_info[4])
                self.assignment_list.add_assignment(assignment)

        for course in self.course_list.course_list:
            for assignment in self.assignment_list.assignment_list:
                if assignment.course == course.name:
                    course.assignment_list.add_assignment(assignment)

        # Load each of the available pages and put them into a list for use
        self.pages = {}
        for page in (MyCoursesPage, AddRemoveCoursePage, AddAssignmentPage):
            window = page(self.main_window, self.course_list)
            self.pages[page] = window
            window.grid(row=0, column=0, sticky="nsew")

        # Show the MyCourses page by default
        self.show_page(MyCoursesPage)

    # Function for showing a page over the others
    # All pages are showing all the time, this function
    # simply puts one on top of the others
    def show_page(self, page):
        active_page = self.pages[page]
        active_page.tkraise()

    # Updates the course/assignment lists and files and reloads the pages
    def update(self):
        for page in (MyCoursesPage, AddRemoveCoursePage, AddAssignmentPage):
            window = page(self.main_window, self.course_list)
            self.pages[page] = window
            window.grid(row=0, column=0, sticky="nsew")

        with open('courses.txt', 'w') as courses_file:
            for course in self.course_list.course_list:
                courses_file.write(course.name + '\n')

        with open('assignments.txt', 'w') as assignments_file:
            for course in self.course_list.course_list:
                for assignment in course.assignment_list.assignment_list:
                    assignments_file.write(assignment.course + ' ' + assignment.name + ' ' + str(assignment.due_month) +
                                           ' ' + str(assignment.due_day) + ' ' + str(assignment.due_year) + '\n')


class NavigationBar:
    def __init__(self, parent):
        # Set up the navigation bar in a frame widget
        self.nav_frame = Frame(bg='gray', relief='groove')
        self.nav_frame.pack(fill=BOTH)

        # My Courses button
        self.my_courses_button = Button(self.nav_frame, text="My Courses", font=("Verdana", 12, "bold"),
                                        fg='white', bg='gray', relief='groove', padx=5, pady=5,
                                        command=lambda: self.call_back(parent, MyCoursesPage))
        self.my_courses_button.pack(fill=BOTH, side=LEFT, expand=True)

        # add/remove course
        self.add_remove_course_button = Button(self.nav_frame, text="Add/Remove Course", font=("Verdana", 12, "bold"),
                                               fg='white', bg='gray', relief='groove', padx=5, pady=5,
                                               command=lambda: self.call_back(parent, AddRemoveCoursePage))
        self.add_remove_course_button.pack(fill=BOTH, side=LEFT, expand=True)

        # add assignment
        self.add_assignment_button = Button(self.nav_frame, text="Add Assignment", font=("Verdana", 12, "bold"),
                                            fg='white', bg='gray', relief='groove', padx=5, pady=5,
                                            command=lambda: self.call_back(parent, AddAssignmentPage))
        self.add_assignment_button.pack(fill=BOTH, side=LEFT, expand=True)

    @staticmethod
    def call_back(parent, page):
        parent.update()
        parent.show_page(page)


class MyCoursesPage(tk.Frame):
    def __init__(self, parent, course_list):
        tk.Frame.__init__(self, parent)

        # Make a "notebook" with tabs. Each tab has a respective frame
        tab_parent = ttk.Notebook(self)
        for course in course_list.course_list:
            tab = ttk.Frame(tab_parent)

            # Course name labels
            course_name_label = Label(tab, text=course.name, font=("Verdana", 25, "bold"),
                                      bg="white", relief=GROOVE)
            course_name_label.pack(fill=BOTH)

            # Assignments label
            assignments_label = Label(tab, text="Assignments", font=("Verdana", 18, "bold"),
                                      bg="orange", relief=GROOVE, anchor=W)
            assignments_label.pack(fill=BOTH)

            for assignment in course.assignment_list.assignment_list:
                assignment_frame = Frame(tab, height=20, relief=SUNKEN, bg="grey")
                assignment_frame.pack(fill=BOTH)

                # Assignment name
                name_label = Label(assignment_frame, text=assignment.name, font=("Verdana", 8, "bold"),
                                   relief=GROOVE, anchor=W)
                name_label.pack(fill=BOTH, side=LEFT, expand=True)

                # Assignment Due Date
                due_label = Label(assignment_frame,
                                  text="Due: " + str(assignment.due_month) + '/' + str(assignment.due_day) + '/' + str(assignment.due_year),
                                  font=("Verdana", 8, "bold"), relief=GROOVE, anchor=W)
                due_label.pack(fill=BOTH, side=LEFT, expand=True)

                # Mark Complete Button
                mark_complete_btn = Button(assignment_frame, text="Mark Complete", font=("Verdana", 8, "bold"),
                                           fg="white", bg="green")
                mark_complete_btn.pack(fill=BOTH, side=LEFT, expand=True)

                # Delete assignment button
                delete_btn = Button(assignment_frame, text="Remove", font=("Verdana", 8, "bold"),
                                    fg="white", bg="red",
                                    command=lambda:
                                    self.delete_assign_btn_command(parent, course_list, assignment.name, assignment.course))
                delete_btn.pack(fill=BOTH, side=LEFT, expand=True)

            try:
                tab_parent.add(tab, text=course.name)
            except IndexError:
                tab.destroy()

        tab_parent.pack(expand=True, fill=BOTH)

    # Delete assignment button command
    @staticmethod
    def delete_assign_btn_command(parent, course_list, assignment_name, assignment_course):
        for course in course_list.course_list:
            for assignment in course.assignment_list.assignment_list:
                if assignment_name == assignment.name and course.name == assignment_course:
                    course.assignment_list.remove_assignment(assignment)

        parent.update()


class AddRemoveCoursePage(tk.Frame):
    def __init__(self, parent, course_list):
        tk.Frame.__init__(self, parent)

        # Add course section ================================================================================
        add_course_title = Label(self, text="Add a Course", font=("Verdana", 25, "bold"), fg="black",
                                 bg="white", relief=GROOVE)
        add_course_title.pack(fill=BOTH)

        # Course Prefix Select Label and dropdown menu
        course_prefix_label = Label(self, text="Select a course prefix:", font=("Verdana", 10))
        course_prefix_label.pack(padx=3, pady=3)
        course_prefix_options = ['CS', 'MATH', 'ENGL', 'PES', 'CHEM', 'BIO']

        self.course_prefix = StringVar(self)
        self.course_prefix.set("SELECT")
        course_prefix_dropdown = OptionMenu(self, self.course_prefix, *course_prefix_options)
        course_prefix_dropdown.pack(padx=3, pady=3)

        # Course Number select label and dropdown menu
        course_number_label = Label(self, text="Select a course number:", font=("Verdana", 10))
        course_number_label.pack(padx=3, pady=3)
        course_number_options = ['1100', '2200', '3300', '4400', '5500']

        self.course_number = StringVar(self)
        self.course_number.set("SELECT")
        course_number_dropdown = OptionMenu(self, self.course_number, *course_number_options)
        course_number_dropdown.pack(padx=3, pady=3)

        # Add course button
        add_course_button = Button(self, text="Add Course", font=("Verdana", 12, "bold"), fg="white",
                                   bg="blue", command=lambda: self.add_course_button_command(course_list))
        add_course_button.pack(padx=3, pady=3)

        # Remove Course section ==============================================================================
        remove_course_title = Label(self, text="Remove a Course", font=("Verdana", 25, "bold"), fg="black",
                                    bg="white", relief=GROOVE)
        remove_course_title.pack(fill=BOTH)

        course_list_label = Label(self, text="Select a course to remove:", font=("Verdana", 10))
        course_list_label.pack(padx=3, pady=3)

        self.course_selection = StringVar(self)
        self.course_selection.set("SELECT")

        # Course choice dropdown menu
        course_choices = []
        for course in course_list.course_list:
            course_choices.append(course.name)

        if course_choices:
            course_list_dropdown = OptionMenu(self, self.course_selection, *course_choices)
            course_list_dropdown.pack(padx=3, pady=3)
        else:
            course_list_dropdown = OptionMenu(self, self.course_selection, 'You have no courses!')
            course_list_dropdown.pack(padx=3, pady=3)

        add_course_button = Button(self, text="Remove Course", font=("Verdana", 12, "bold"), fg="white",
                                   bg="red", command=lambda: self.remove_course_button_command(course_list))
        add_course_button.pack(padx=3, pady=3)

    # Add the selected options as a course option to the global course list
    def add_course_button_command(self, course_list):
        course_name = (self.course_prefix.get() + self.course_number.get())
        course = Course(course_name)
        course_list.add_course(course)

        confirmation_label = Label(self, text=(course_name + " has been added!"), bg="green", fg="white",
                                   font=("Verdana", 10, "bold"))
        confirmation_label.pack(padx=3, pady=3)

    # Removes the selected course option from the global course list
    def remove_course_button_command(self, course_list):

        for course in course_list.course_list:
            if course.name == self.course_selection.get():
                course_list.remove_course(course)

        confirmation_label = Label(self, text=(self.course_selection.get() + " has been removed!"),
                                   bg="orange", fg="white", font=("Verdana", 10, "bold"))
        confirmation_label.pack(padx=3, pady=3)


class AddAssignmentPage(tk.Frame):
    def __init__(self, parent, course_list):
        tk.Frame.__init__(self, parent)

        add_assignment_title = Label(self, text="Add an Assignment", font=("Verdana", 25, "bold"), fg="black",
                                     bg="white", relief=GROOVE)
        add_assignment_title.pack(fill=BOTH)

        # Course choice dropdown menu
        course_list_label = Label(self, text="Select a course to add an assignment to:", font=("Verdana", 10))
        course_list_label.pack(padx=3, pady=3)

        self.course_selection = StringVar(self)
        self.course_selection.set("SELECT")

        course_choices = []
        for course in course_list.course_list:
            course_choices.append(course.name)

        if course_choices:
            course_list_dropdown = OptionMenu(self, self.course_selection, *course_choices)
            course_list_dropdown.pack(padx=3, pady=3)
        else:
            course_list_dropdown = OptionMenu(self, self.course_selection, 'You have no courses!')
            course_list_dropdown.pack(padx=3, pady=3)

        # Assignment name entry
        assignment_name_entry_label = Label(self, text="Enter the name of the assignment:", font=("Verdana", 10))
        assignment_name_entry_label.pack(padx=3, pady=3)

        self.assignment_name_entry = Entry(self)
        self.assignment_name_entry.pack(padx=3, pady=3)

        # Assignment due date entry
        self.assignment_due_label = Label(self, text="Due date:", font=("Verdana", 10))
        self.assignment_due_label.pack(padx=3, pady=3)

        month_choices = range(1, 13)

        self.month_selection = IntVar(self)
        self.month_selection.set("MONTH")

        month_dropdown = OptionMenu(self, self.month_selection, *month_choices)
        month_dropdown.pack(padx=3, pady=3)

        day_choices = range(1, 32)

        self.day_selection = IntVar(self)
        self.day_selection.set("DAY")

        day_dropdown = OptionMenu(self, self.day_selection, *day_choices)
        day_dropdown.pack(padx=3, pady=3)

        year_choices = range(2019, 2024)

        self.year_selection = IntVar(self)
        self.year_selection.set("YEAR")

        year_dropdown = OptionMenu(self, self.year_selection, *year_choices)
        year_dropdown.pack(padx=3, pady=3)

        # Add assignment button
        add_assign_btn = Button(self, text="Add Assignment", font=("Verdana", 12, "bold"), fg="white", bg="blue",
                                command=lambda: self.add_assignment_button_command(course_list))
        add_assign_btn.pack(padx=3, pady=3)

    # Adds the assignment information to the selected course
    def add_assignment_button_command(self, course_list):
        assignment = Assignment(self.assignment_name_entry.get(),
                                self.course_selection.get(), self.day_selection.get(), self.month_selection.get(),
                                self.year_selection.get())

        for course in course_list.course_list:
            if course.name == assignment.course:
                course.assignment_list.add_assignment(assignment)

        confirmation_label = Label(self, text=(assignment.name + " has been added to " + assignment.course + "!"),
                                   bg="green", fg="white", font=("Verdana", 10, "bold"))
        confirmation_label.pack(padx=3, pady=3)
