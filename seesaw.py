#!/usr/bin/python

from Tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SeesawApp:

    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

        self.graph_w = 200
        self.graph_h = 120

        self.number_of_groups = 5
        self.groups = []

        Label(self.frame, text="Treatment A").grid(row=0, column=0, columnspan=1)
        self.treatment_a_entry = Entry(self.frame)
        self.treatment_a_entry.grid(row=0, column=1, columnspan=3)
        Label(self.frame, text="Treatment B").grid(row=1, column=0, columnspan=1)
        self.treatment_b_entry = Entry(self.frame)
        self.treatment_b_entry.grid(row=1, column=1, columnspan=3)

        Label(self.frame, text="Goal").grid(row=2, column=1)
        Label(self.frame, text="Importance").grid(row=2, column=2)
        Label(self.frame, text="Probability A").grid(row=2, column=3)

        for group_number in range(0, self.number_of_groups):
            self.groups.append(GroupEntry(self.frame, group_number))
        
        b = Button(self.frame, text="Draw", command=self.button_callback)
        b.grid(row=self.number_of_groups+3, columnspan=4)
        
        p = plt.figure()
        
        # pass figure to tk and render
        canvas = FigureCanvasTkAgg(p, master=self.frame)
        canvas.show()
        canvas.get_tk_widget().grid(row=self.number_of_groups+4, columnspan=4)

    def button_callback(self):
        treatment_a_name = self.treatment_a_entry.get()
        treatment_b_name = self.treatment_b_entry.get()

        goal_list = []
        for group in self.groups:
            name = group.e1.get()
            importance = group.importance_slider.get()
            probability_a = group.prob_a_slider.get()
            goal_list.append(Goal(name, importance, probability_a))

        decision = Decision(treatment_a_name, treatment_b_name, goal_list)
        self.draw_decision(decision)


    def draw_decision(self, decision):
        ''' There will be an issue if a smaller importance is plotted before
        a large importance with the same probability'''
        x = [goal.prob_a for goal in decision.goals]
        y = [goal.importance for goal in decision.goals]

        # create figure instance
        p = plt.figure()
        
        # remove axis
        # plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)

        # plot bar chart
        barlist = plt.bar(x, y,width = 0.2,align='center')
        bar_col = ['b','g','r','c','m','y']
        i=0
        for cs in barlist:
            cs.set_color(bar_col[i])
            i=i+1

        # add bar names
        labels = [goal.name for goal in decision.goals]
        plt.xticks(x,labels)

        # plot lines
        plt.vlines(0,0,1,lw=5)
        plt.hlines(0,-1,1,lw=5)

        # set axis
        plt.axis([-1,1,0,1])

        # pass figure to tk and render
        canvas = FigureCanvasTkAgg(p, master=self.frame)
        canvas.show()
        canvas.get_tk_widget().grid(row=self.number_of_groups+4, columnspan=4)
        
        goal_list = []

class Decision:
    def __init__(self, treatment_a, treatment_b, goals):
        self.treatment_a = treatment_a
        self.treatment_b = treatment_b
        self.goals = goals
        
class Goal:
    def __init__(self, name, importance, probability_a):
        self.name = name
        self.importance = importance
        self.prob_a = probability_a

class GroupEntry:
    def __init__(self, master, group_number):
        row_number = group_number + 3

        label = Label(master, text="Goal " + str(group_number+1)).grid(row=row_number, column=0)

        self.e1 = Entry(master)
        self.e1.grid(row=row_number, column=1)

        self.importance_slider = Scale(master, from_=0, to=1, orient=HORIZONTAL, show=0, resolution=0.1)
        self.importance_slider.grid(row=row_number, column=2)

        self.prob_a_slider = Scale(master, from_=-1, to=1, orient=HORIZONTAL, show=0, resolution=0.1)
        self.prob_a_slider.grid(row=row_number, column=3)

example_decision = Decision("Dialysis", "Not dialysis", [
    Goal("Live as long as possible", 0.6, 0.5),
    Goal("Feel well day-to-day", 0.9, 0.3),
    Goal("Minimise symptoms", 0.8, 0.4)])

root = Tk()

seesaw_app = SeesawApp(root)

root.mainloop()

