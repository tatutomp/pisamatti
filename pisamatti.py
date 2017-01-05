# -*- coding: iso-8859-15 -*-
# Author: Tatu Tomppo
# copy free - Python 3.5 or later needed(tkinter, etc....)
# You need "pip install wx"

import random
import tkinter
from tkinter import ttk
import os
import configparser

ADDITION_TEXT = 'Plus'
APPLICATION_NAME_TEXT = 'Pisa Math'
CHECK_RESULT_BUTTON_TEXT = 'Tarkista'
# This is shown when correct answer is given
CORRECT_ANSWER_TEXT = "Oikein"
EQUALS_TEXT = "="
# This is shown when user have not entered answer and tries to check result (press enter)
GIVE_ANSWER_TEXT = 'Anna vastaus, kiitos.'
MULTIPLICATION_TEXT = 'Kerto'
RANDOM_MIN_MULTI = 2
RANDOM_MAX_MULTI = 9
RANDOM_MIN_ADDITION = 2
RANDOM_MAX_ADDITION = 100
START_STATUS_TEXT = 'Laske!'
TOTAL_SCORE_TEXT = 'Pisteet: '
STATUS_TEXT = 'Tilanne'
# This is shown when wrong answer is given
WRONG_TEXT = 'Väärin! '




class PisaMath(ttk.Frame):

    configfile_name = 'config.xml'
    # Check if there is already a configuration file
    first_number = 0
    second_number = 0

    def randomize_nums(self):

        if (self.v.get() == 1):
            self.first_number = random.randint(RANDOM_MIN_MULTI, RANDOM_MAX_MULTI)
            self.second_number = random.randint(RANDOM_MIN_MULTI, RANDOM_MAX_MULTI)
            self.equation_label['text'] = str(self.first_number) + str("*") + str(self.second_number)
        else:
            self.first_number = random.randint(RANDOM_MIN_ADDITION, RANDOM_MAX_ADDITION)
            self.second_number = random.randint(RANDOM_MIN_ADDITION, RANDOM_MAX_ADDITION)
            self.equation_label['text'] = str(self.first_number) + str("+") + str(self.second_number)

    if not os.path.isfile(configfile_name):
        # Create the configuration file as it doesn't exist yet
        cfgfile = open(configfile_name, 'w')
        Config = configparser.ConfigParser()
        Config.add_section('configs')
        Config.set('configs', 'correct_answers','0')
        Config.write(cfgfile)
        cfgfile.close()
    else:
        cfgfile = open(configfile_name, 'r')

    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    settings.read(configfile_name)
    correct_answers = int(settings.get('configs', 'correct_answers'))
    random.SystemRandom()
    random.seed()

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.OnPressEnter = None
        self.root = parent
        self.init_gui()
        self.equation_label['text'] = str(self.first_number) + str("*") + str(self.second_number)
        self.correct_answers_label['text'] = TOTAL_SCORE_TEXT + str(self.correct_answers)
        self.result_label['text'] = START_STATUS_TEXT
        self.rdbm.invoke()

    def on_quit(self):
       quit()

    def change_calc_type(self):
        self.randomize_nums()

    def calculate(self):

        try:
            given_answer = int(self.answer_entry.get())
        except:
            given_answer = 0

        textlen = len(self.answer_entry.get())

        self.answer_entry.delete(0, textlen)
        self.answer_entry.update()

        if(given_answer == 0):
            self.result_label['text'] = GIVE_ANSWER_TEXT
            return

        correct_answer = 0
        if (self.v.get() == 1):
            correct_answer = self.first_number*self.second_number
        else:
            correct_answer = self.first_number + self.second_number

        if(given_answer == correct_answer) :

            self.randomize_nums()
            self.correct_answers = self.correct_answers + 1
            self.randomize_nums()
            self.result_label.configure(foreground='green')
            self.result_label['text'] = CORRECT_ANSWER_TEXT

            self.correct_answers_label['text'] = TOTAL_SCORE_TEXT + str(self.correct_answers)

            self.cfgfile = open(self.configfile_name, 'w')
            self.Config = configparser.ConfigParser()
            self.Config.add_section('configs')
            self.Config.set('configs', 'correct_answers', str(self.correct_answers))
            self.Config.write(self.cfgfile)
            self.cfgfile.close()

        else:
            self.result_label.configure(foreground='red')
            self.result_label['text'] = WRONG_TEXT
            self.correct_answers_label['text'] = TOTAL_SCORE_TEXT + str(self.correct_answers)

    def on_enter(self, event):
        self.calculate()

    def init_gui(self):

        self.root.title(APPLICATION_NAME_TEXT)

        self.grid(column=0, row=0)
        self.equation_label = ttk.Label(self)
        self.equation_label.grid(column=0, row=2)
        ttk.Label(self, text=EQUALS_TEXT).grid(column=1, row=2)
        self.answer_entry = ttk.Entry(self, width=10)
        self.answer_entry.bind("<Return>", self.on_enter)
        self.answer_entry.grid(column=2, row=2)
        self.calc_button = ttk.Button(self, text=CHECK_RESULT_BUTTON_TEXT, command=self.calculate)
        self.calc_button.grid(column=2, row=3, columnspan=1)
        self.result_label = ttk.Label(self, text='')
        self.result_label.grid(column=0, row=4)

        ttk.Separator(self, orient='horizontal').grid(column=0, row=5, columnspan=4, sticky='ew')
        self.correct_answers_label = ttk.Label(self, text='')
        self.correct_answers_label.grid(column=0, row=6, sticky='we')
        # Labels that remain constant throughout execution.
        ttk.Label(self, text=APPLICATION_NAME_TEXT).grid(column=0, row=0, columnspan=4)
        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')

        self.v = tkinter.IntVar()
        self.rdbm = ttk.Radiobutton(self, text=MULTIPLICATION_TEXT,
                                    variable=self.v, value=1, command=self.change_calc_type)
        self.rdbm.grid(column=2, row=6, columnspan=4, sticky="w")
        self.rdba = ttk.Radiobutton(self, text=ADDITION_TEXT,
                                    variable=self.v, value=2, command=self.change_calc_type)
        self.rdba.grid(column=2, row=7, columnspan=4, sticky='w')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)



if __name__ == '__main__':
    root = tkinter.Tk()
    root.maxsize(330,250)
    PisaMath(root)
    root.mainloop()
