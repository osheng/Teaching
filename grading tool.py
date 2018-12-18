"""I teach a Chinese class and I wanted a quick way to calculate my students'
grades and to be able to weight their higher-mark work more favourably. Doing
this in Sheets looked complicated so I came up with this program which takes in
a csv file (with some formatting constraints) and prints out the students'
grades and warns me of any work that they may have not handed in."""

# TODO: Create a function to write to a CSV so that you can save the results
# TODO: figure out how to encode Chinese characters


from typing import List, TextIO, Dict


# define constants used to determine the weighting of marked work

PARTICIPATION = 0.2
PRESENTATION = 0.2
RECORDING = 0
SCRIPT = 0.15
ASSIGNMENTS = {0: 0.12, 1: 0.08}
QUIZZES = {0: 0.09, 1: 0.07, 2: 0.05, 3: 0.03, 4: 0.01}

# evaluations for the term
WORKLIST = ['Assignment 1', 'Assignment 2', 'Script', 'Participation',
            'Pinyin Quiz 1', 'Pinyin Quiz 2', 'Pinyin Quiz 3',
            'Pinyin Quiz 4', 'Pinyin Quiz 5', 'Pinyin Quiz 6',
            'Presentation']


class MarkedWork:
    """Quizzes or assignments or the final project"""

    name: str
    kind: str
    mark: float

    def __init__(self, name: str, kind: str, mark: float) -> None:
        """Initialize a new piece of MarkedWork with the kind of work it is (quiz,
        assignment, etc) and the mark it received.
        a1 = MarkedWork("Assignment 1","a", 10)
        """
        self.name = name
        self.kind = kind
        self.mark = mark

    def __str__(self) -> str:
        return self.name


class Student:
    """A class to keep track of Students"""

    def __init__(self, english_name: str, traditional_name=None,
                 simplified_name=None) -> None:
        """
        Initialize a new student with the English name english_name and
        the Chinese name traditional_name.
# TODO: figure out how to encode Chinese characters in python
        >>> julian = Student("Julian Cheng","�����")
        """
        self.e_name = english_name
        self.tc_name = traditional_name
        self.sc_name = simplified_name
        if simplified_name is None:
            self.sc_name = self.tc_name
        self.work = []

    def __str__(self) -> str:
        """Return a string representaion of this student
        >>> julian = Student("Julian Cheng","")
        >>> print(julian)
        English name: Julian Cheng
        Traditional Chinese name: 
        Simplified Chinese name: 
        Completed work:

        >>> julian = Student("Julian Cheng","","֣")
        >>> print(julian)
        English name: Julian Cheng
        Traditional Chinese name: 
        Simplified Chinese name: ֣
        Completed work:

        """
        lst = []
        for item in self.work:
            lst.append(item.name)
        lst.sort()
        script, presentation, recording, participation = 0, 0, 0, 0
        for work in self.work:
            if work.kind == 'script':
                script = work.mark
            elif work.kind == 'presentation':
                presentation = work.mark
            elif work.kind == 'recording':
                recording = work.mark
            elif work.kind == 'participation':
                participation = work.mark

        return "English name: {}\nTraditional Chinese name: " \
               "{}\nSimplified Chinese name: {}\nMissing work: " \
               "{}\nScript: {}\nPresentation: {}\nRecording: {}" \
               "\nParticipation: {}\nAssignments: {}\nQuizzes: {}\nFinal Project: {}\n" \
               "Final Grade: {}\n".\
            format(self.e_name, self.tc_name, self.sc_name,
                   self.find_missing_work(), int(script), int(presentation),
                   int(recording), int(participation),
                   int(self.assignment_total() * 5),
                   int(self.quiz_total() * 4),
                   int(int(script) * 15 / 35 + int(presentation) * 20 / 35),
                   int(self.calculate_grade()))

    def append(self, work: "MarkedWork") -> None:
        """Define append to work with class, MarkedWork, the same way it does
        with class, list.
        """
        self.work.append(work)

    def find_missing_work(self) -> list:
        """Return a list of the work not yet completed.
        """
        work_list = WORKLIST
        missing_work = []
        completed_work = []
        for item in self.work:
            if item.mark > 0:
                completed_work.append(item.name)
        for item in work_list:
            if item not in completed_work:
                missing_work.append(item)
        if missing_work != []:
            return missing_work
        return missing_work

    def calculate_grade(self) -> float:
        """Calculate and return the weighted final grade for self, a Student
        """
        total = 0
        for item in self.work:
            if item.kind == 'presentation':
                total += item.mark * PRESENTATION
            elif item.kind == 'script':
                total += item.mark * SCRIPT
            elif item.kind == 'recording':
                total += item.mark * RECORDING
            elif item.kind == 'participation':
                total += item.mark * PARTICIPATION

        return total + self.quiz_total() + self.assignment_total()

    def assignment_total(self) -> float:
        """
        Return the weighted average of all assignments
        """
        total = 0
        assignments = []
        for item in self.work:
            if item.kind == 'assignment':
                assignments.append(item.mark)
        assignments = sorted(assignments, reverse=True)
        i = 0
        while i < len(assignments) and i < len(ASSIGNMENTS):
            total += assignments[i] * ASSIGNMENTS[i]
            i += 1
        return total

    def quiz_total(self)-> float:
        """
        Return the weighted average of all quizzes
        """
        total = 0
        quizzes = []
        for item in self.work:
            if item.kind == 'quiz':
                quizzes.append(item.mark)
        quizzes = sorted(quizzes, reverse=True)
        i = 0
        while i < len(quizzes) and i < len(QUIZZES):
            total += quizzes[i] * QUIZZES[i]
            i += 1

        return total

# I never ended up using the predict_grade function
    def predict_grade(self) -> float:
        """
        Predict final grade based on what work has been completed
        """
        q_total, a_total = 0, 0
        if self.work == []:
            return -1
        for item in self.work:
            if item.kind == 'a':
                a_total += item.mark

        return -1


def harvest_data(csv_file: TextIO) -> dict:
    """Read an opened csv file and return a dictionary of Students """

    course = {}
    line = csv_file.readline().split(sep=',')
    columns = {}
    for column in range(len(line)):
        columns[column] = line[column].strip()

    while len(line) >= 3:

        line = csv_file.readline().split(sep=',')
        if len(line) >= 3:
            student = (line[0]+'_'+line[1]).lower()
            course[student] = Student(line[0]+' '+line[1])
            for i in range(len(line)):
                if 'assignment' in columns[i].lower().strip() \
                        and line[i].strip().isdigit():
                    marked_work = MarkedWork(columns[i], 'assignment',
                                             float(line[i]))
                    course[student].append(marked_work)
                elif 'quiz' in columns[i].lower() and line[i].isdigit():
                    marked_work = MarkedWork(columns[i], 'quiz', float(line[i]))
                    course[student].append(marked_work)
                elif 'participation' in columns[i].lower() and \
                        line[i].strip().isdigit():
                    marked_work = MarkedWork(columns[i], 'participation',
                                             float(line[i]))
                    course[student].append(marked_work)
                elif 'script' in columns[i].lower() and \
                        line[i].strip().isdigit():
                    marked_work = MarkedWork(columns[i],
                                             'script', float(line[i]))
                    course[student].append(marked_work)
                elif 'presentation' in columns[i].lower() and \
                        line[i].strip().isdigit():
                    marked_work = MarkedWork(columns[i], 'presentation',
                                             float(line[i]))
                    course[student].append(marked_work)
                elif 'recording' in columns[i].lower() and \
                        line[i].strip().isdigit():
                    marked_work = MarkedWork(columns[i], 'recording',
                                             float(line[i]))
                    course[student].append(marked_work)
    return course






data_file = open("Spring 2018 Marks.csv")
course_data = harvest_data(data_file)
for student in course_data:
    print(course_data[student])

for student in course_data:
    if course_data[student].find_missing_work() != []:
        print(course_data[student].e_name)
        print(course_data[student].find_missing_work())
        print()  # just for an extra blank line

data_file.close()



