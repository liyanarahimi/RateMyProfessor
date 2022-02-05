# Program: RateMyProfessor Visualization
# Author: Liyana Rahimi
# Description: This program visualizes data from RateMyProfessor

# Imports
import os
import ratemyprofessor as rmp
import plotly.graph_objects as go
import plotly.offline as pyo

class rmpCharts:
    def __init__(self):
        # Sets path for files to render
        self.path = os.path.dirname(os.path.realpath(__file__))

        # Data retrieval loop
        self.professor = None
        while self.professor is None:
            # Prompts user for school and professor name
            school = input("\n Please enter a valid school. ")
            name = input("\n Please enter your professor's name. ")

            # Retrieves data from RateMyProfessor if possible, continue iteration if not
            try:
                self.professor = rmp.get_professor_by_school_and_name(rmp.get_school_by_name(school), name)
            except:
                continue

            # Confirms with user that the correct professor is retrieved
            print("\n We've located this professor on RateMyProfessor: ")
            print(self)     ## Prints a brief description of the professor
            ans = input("\n Is this your professor? Y/N ")

            # Purges incorrent data and reinitiates data retrieval loop
            if ans.upper() != "Y":
                self.professor = None

        # Retrieves course data for visualization
        self.dataCourse()

        # Initializes visualizations
        self.radarRatings()
        self.barGrades()

    def __repr__(self):
        # Displays description of professor: Name, Department, School
        return "\n %s, %s Department of %s." % (self.professor.name, self.professor.department, self.professor.school.name)

    def dataCourse(self):
        # Retrieves and pre-processes course data

        self.courses = []
        self.ratings = []
        self.difficulty = []
        self.grades = []

        # Loops through courses taught by the professor
        for course in self.professor.courses:
            student_reviews = self.professor.get_ratings(course.name)

            student_rating = []
            student_difficulty = []
            student_grades = []

            # Loops through student review for each course
            for review in student_reviews:
                # Stores rating and difficulty rating for each student
                student_rating.append(review.rating)
                student_difficulty.append(review.difficulty)

                # Stores letter grades for each student if grade is available. Other notations such as withdrawal is omitted
                if review.grade != None and len(review.grade) > 0 and len(review.grade) <= 2:
                    student_grades.append(review.grade)

            # Calculates the average rating and difficulty rating for each course
            avg_rating = sum(student_rating) / len(student_rating)
            avg_difficulty = sum(student_difficulty) / len(student_difficulty)

            # Stores the average rating and difficulty rating for each course
            self.courses.append(course.name)
            self.ratings.append(avg_rating)
            self.difficulty.append(avg_difficulty)
            self.grades.append(student_grades)

    def radarRatings(self):
        # Visualizes the student ratings for all the courses taught by the professor on a radar chart

        # Loops the data to ensure the ends of the radar chart are connected
        courses = [*self.courses, self.courses[0]]
        ratings = [*self.ratings, self.ratings[0]]
        difficulty = [*self.difficulty, self.difficulty[0]]

        # Plots the course ratings and difficulty ratings on a radar chart
        radar = go.Figure(
            data = [
                go.Scatterpolar(r = ratings, theta = courses, fill = "toself", name = "Average Rating"),
                go.Scatterpolar(r = difficulty, theta = courses, fill = "toself", name = "Average Difficulty")
            ],
            layout = go.Layout(
                title = go.layout.Title(text = "Courses by %s in the %s Department of %s" % (self.professor.name, self.professor.department, self.professor.school.name)),
                polar = {"radialaxis": {"visible": True}},
                showlegend = True
            )
        )

        # Displays radar chart in browser
        pyo.plot(radar, filename = self.path + r"/" + self.professor.name + r" Courses.html")

    def barGrades(self):
        # Visualizes student grades for each course taught by the professor on a grouped bar chart              

        # Creates a grouped bar chart
        bar = go.Figure(
            layout = go.Layout(
                title = go.layout.Title(text = "Grade Distribution for Courses by %s in the %s Department of %s" % (self.professor.name, self.professor.department, self.professor.school.name)),
                barmode = "group",
                showlegend = True
            )
        )

        # Loops through courses and adds grades to chart
        for i in range(len(self.courses)):
            if len(self.grades[i]) > 0:
                bar.add_trace(go.Histogram(name = self.courses[i], x = self.grades[i]))

        # Displays bar chart in browser
        pyo.plot(bar, filename = self.path + r"/" + self.professor.name + r" Grades.html")

while True:
    run = input("\n Would you like to visualize new data from RateMyProfessor? Y/N ")
    if run.upper() == "Y":
        rmpCharts()
    else:
        break