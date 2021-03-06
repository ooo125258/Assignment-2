# Assignment 2 - Course Planning!
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# <full name>, <utorid>
#
#
#
# ---------------------------------------------
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
from course import Course


def parse_course_data(filename):
    """ (str) -> Course

    Read in prerequisite data from the file called filename,
    create the Course data structures for the data,
    and then return the root (top-most) course.

    See assignment handout for details.
    """
    courses = {}
    with open(filename,'r') as source:
        for line in source:
            classes = line.split()
            if classes[0] not in courses:
                courses[classes[0]] = Course(classes[0])
            if classes[1] not in courses:
                courses[classes[1]] = Course(classes[1])
            if courses[classes[0]] not in courses[classes[1]].prereqs:
                courses[classes[1]].add_prereq(courses[classes[0]])
    top = None
    for cour in courses:
        boo = True
        for compare in courses:
            if courses[cour] in courses[compare].prereqs:
                boo = False
        if boo:
            return courses[cour]

class TermPlanner:
    """Tool for planning course enrolment over multiple terms.

    Attributes:
    - course (Course): tree containing all available courses
    """

    def __init__(self, filename):
        """ (TermPlanner, str) -> NoneType

        Create a new term planning tool based on the data in the file
        named filename.

        You may not change this method in any way!
        """
        self.course = parse_course_data(filename)
        self.filename = filename

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """
        actually_taken = []
        if schedule == []:
            return True
        else:
            for sch in schedule:
                for cour in sch:
                    if cour not in self.course:
                        restore(self.course)
                        return False
                    else:
                        if prereqs_taken(cour, self.course):
                            take(cour, self.course)
                            actually_taken.append(cour)
                        else:
                            restore(self.course)
                            return False
            for i in range(len(actually_taken)):
                for j in range(i+1,len(actually_taken)):
                    if actually_taken[i] == actually_taken[j]:
                        restore(self.course)
                        return False
            restore(self.course)
            return True


    def generate_schedule(self, selected_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.

        You may assume that all the courses in selected_courses appear in
        self.course.

        If no valid schedule can be formed from these courses, return an
        empty list.
        """
        copy_want = selected_courses[:]
        schedule = []
        for i in range(len(selected_courses)):
            sch = []
            for cour in copy_want:
                if prereqs_taken(cour, self.course) and len(sch) < 5:
                    sch.append(cour)
            for course in sch:
                take(course, self.course)
                copy_want.remove(course)
            sch.sort()
            if sch != []:
                schedule.append(sch)
        if len(copy_want) != 0:
            schedule.append(copy_want)
        restore(self.course)
        if self.is_valid(schedule):
            return schedule
        else:
            return []




def restore(course):
    if course.prereqs == []:
        if course.taken == True:
            course.taken = False
    else:
        for prereq in course.prereqs:
            if prereq.taken == True:
                prereq.taken = False
                restore(prereq)
            else:
                restore(prereq)


def take(code, course):
    if course.name == code:
        course.take()
    elif course.prereqs == []:
        pass
    else:
        for cour in course.prereqs:
            take(code,cour)

def prereqs_taken(code,course):
    if course.name == code:
        for cour in course.prereqs:
            if cour.taken == False:
                return False
        return True
    elif course.prereqs == []:
        return True
    else:
        for cour in course.prereqs:
            if not prereqs_taken(code,cour):
                return False
        return True