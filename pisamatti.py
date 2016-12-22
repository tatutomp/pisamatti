# Author: Tatu Tomppo
# copy free
import random
import tkinter
from tkinter import ttk
import os
import configparser
 

import wx
class Adder(ttk.Frame):


    random.SystemRandom()
    random.seed()

    configfile_name = 'configgi.xml'

    # Check if there is already a configurtion file
    if not os.path.isfile(configfile_name):
        # Create the configuration file as it doesn't exist yet
        cfgfile = open(configfile_name, 'w')
        Config = configparser.ConfigParser()

        Config.add_section('tulokset')
        Config.set('tulokset', 'oikeat','0')
        Config.write(cfgfile)
        cfgfile.close()
    else:
        cfgfile = open(configfile_name, 'r')

    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    settings.read(configfile_name)
    oikeat = int(settings.get('tulokset', 'oikeat'))



    eka_luku = random.randint(2,9)
    toka_luku = random.randint(2,9)





    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.OnPressEnter = None
        self.root = parent

        self.init_gui()
        self.num1_entry['text'] = str(self.eka_luku) + str("*") + str(self.toka_luku)

        self.answer_label['text'] = "Pisteet: " + str(self.oikeat)

    def on_quit(self):
       quit()



    def calculate(self):

        try:
            num2 = int(self.num2_entry.get())
        except:
            num2 = 0;

        textlen =  len(self.num2_entry.get())

        self.num2_entry.delete(0, textlen)
        self.num2_entry.update()

        if(num2 == 0):
            self.answer_label['text'] = "Anna vastaus"
            return

        if( num2 == self.eka_luku*self.toka_luku) :
            self.answer_label['text'] = "Oikein"

            self.eka_luku =  random.randint(2,9)
            self.toka_luku =  random.randint(2,9)

            self.oikeat = self.oikeat + 1
            self.num1_entry['text'] = str(self.eka_luku) + str("*") + str(self.toka_luku)
            self.answer_label['text'] = "Oikein! Pisteet: " + str(self.oikeat)

            self.cfgfile = open(self.configfile_name, 'w')
            self.Config = configparser.ConfigParser()

            self.Config.add_section('tulokset')
            self.Config.set('tulokset', 'oikeat', str(self.oikeat))
            self.Config.write(self.cfgfile)
            self.cfgfile.close()

        else:
            self.answer_label['text'] = "V‰‰rin! Pisteet: " +str(self.oikeat)

    def OnEnter(self, event):
        self.calculate()



    def init_gui(self):
        """Builds GUI."""
        self.root.title('Pisa Matti')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='nsew')
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self.on_quit)
        self.menu_edit = tkinter.Menu(self.menubar)
       # self.menubar.add_cascade(menu=self.menu_file, label='File')
       # self.menubar.add_cascade(menu=self.menu_edit, label='Edit')
        self.root.config(menu=self.menubar)
        self.num1_entry = ttk.Label(self, width=20)
        self.num1_entry.grid(column=1, row = 2)

        self.num2_entry = ttk.Entry(self, width=5)
        self.num2_entry.bind("<Return>", self.OnEnter)
        self.num2_entry.grid(column=3, row=2)

        self.calc_button = ttk.Button(self, text='Tarkista', command=self.calculate)

        

        self.calc_button.grid(column=0, row=3, columnspan=4)

        self.answer_frame = ttk.LabelFrame(self, text='Tilanne',height=100)
        self.answer_frame.grid(column=0, row=4, columnspan=4, sticky='nesw')


        self.answer_label = ttk.Label(self.answer_frame, text='')
        self.answer_label.grid(column=0, row=0)
        # Labels that remain constant throughout execution.
        ttk.Label(self, text='Pisa Matti').grid(column=0, row=0, columnspan=4)
        ttk.Label(self, text='Laske').grid(column=0, row=2, sticky='w')
        ttk.Label(self, text='Vastaus').grid(column=2, row=2, sticky='w')
        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)



if __name__ == '__main__':
    root = tkinter.Tk()
    Adder(root)
    root.mainloop()
