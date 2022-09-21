# This file runs application.

import os
from re import T
from turtle import title, width
import tkinter as tk
from tkinter import *  #Tk, Button, Menu
from tkinter import ttk
from PIL import ImageTk, Image

from dmc.dmc import DmcCfg, DmcSheet, DmcCfgConstant, DmcCfgCounter
from project.project import Project


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #self = tk.Tk()
        self.minsize(500,300)
        self.title('Datamatrix generator')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.option_add('*tearOff', FALSE)

        frame_main = self.FrameMain(self)
        frame_edit = self.FrameEdit(frame_main)
        frame_buttons = self.FrameButtons(frame_main)

        menu_bar = self.MenuBar(self)
        menu_file = self.MenuFile(menu_bar)

        menu_bar.add_menu_list(menu_file,'File')
        self.assign_menu(menu_bar)


    def assign_menu(self, menu_bar):
        self['menu'] = menu_bar


    class MenuBar(tk.Menu):

        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            # File menu
            #self= tk.Menu(parent)


        def add_menu_list(self,menu_list,menu_label):
            # Add menu lists to menu
            self.add_cascade( menu=menu_list, label=menu_label)


    class MenuFile(tk.Menu):

        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            # File menu
            #self= tk.Menu(parent)

            self.add_command(label='New  project')#, command=self.dummy)
            self.add_command(label='Open project')#, command=self.dummy)
            self.add_separator()
            self.add_command(label='Close')#, command=self.dummy)


    class FrameMain(ttk.Frame):

        def __init__(self, parent):
            super().__init__()
            # Generate single one main frame
            #self= ttk.Frame(parent)
            self.parent = parent
            self.grid(column=0, row=0)
            self.columnconfigure(0, weight=5)

    class FrameEdit(ttk.Frame):

        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            #self = ttk.Frame(parent, width=800, borderwidth=2, padding=10, relief='sunken')
            self.grid(column=0, row=0, sticky='nw')
            self.columnconfigure(0, weight=1)

    class FrameButtons(ttk.Frame):

        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            #self = ttk.Frame(parent, borderwidth=2, padding=10, relief='groove')
            self.grid(column=1, row=0, sticky='ne')
            self.columnconfigure(0, weight=0)

            self.add_sheet = ttk.Button(self, text='Add new sheet', width=30)#, command=dummy, width=30)
            self.add_sheet.grid(column=0, row=0)

            self.remove_sheet = ttk.Button(self, text='Remove sheet', width=30)#, command=self.dummy, width=30)
            self.remove_sheet.grid(column=0, row=1)

    def dummy():
        pass

def main():

    root = App()
    root.mainloop()

    # frame_main = FrameMain(root)
    # frame_edit = FrameEdit(frame_main)
    # frame_buttons = FrameButtons(frame_main)

    # menu_bar = MenuBar(root)
    # menu_file = MenuFile(menu_bar)

    # menu_bar.add_menu_list(menu_file,'File')
    # root.assign_menu(menu_bar)

    #menu_bar = Menu(root)
    #root['menu'] = menu_bar


    # global project
    # project = Project('test')


    # def close_window():
    #     root.after(3000,root.destroy())



    # def close():
    #     #msg box if save?
    #     pass

    

    #label_test = ttk.Label(frame_edit, text='test')
    #label_test.grid(column=0, row=0)





    # btn_add_sheet = ttk.Button(frame_buttons, text='Add new sheet', command=dummy, width=btn_size)
    # btn_add_sheet.grid(column=0, row=0)

    # btn_remove_sheet = ttk.Button(frame_buttons, text='Remove sheet', command=dummy, width=btn_size)
    # btn_remove_sheet.grid(column=0, row=1)
    # sheets = []
    # sheets.append(DmcSheet('jeden', 'A4'))

    # sheets[0].add_dmc('variant_no')
    # sheets[0].dmc_config[0].set_count(10)
    # sheets[0].dmc_config[0].set_size(10)
    # sheets[0].dmc_config[0].add_dmc_part(DmcConfigConstant('4500000010'))
    # sheets[0].dmc_config[0].add_dmc_part(DmcConfigCounter(1, 1, 3))
    # sheets[0].add_dmc('body')
    # sheets[0].dmc_config[1].set_count(10)
    # sheets[0].dmc_config[1].set_size(15)
    # sheets[0].dmc_config[1].add_dmc_part(DmcConfigConstant('5555100030'))
    # sheets[0].dmc_config[1].add_dmc_part(DmcConfigCounter(1, 1, 3))


    # selector = 0

    # while selector != 9:

    #     match selector:
    #         case 0:
    #             os.system('cls||clear')
    #             print('Sheets: ', len(sheets))
    #             for idx, sheet in enumerate(sheets):
    #                 print('\t', idx, ":", sheet.name)
    #             print("\n")
    #             print("1: Create new sheet")
    #             print("2: Display sheet")
    #             print("4: Delete sheet")

    #         case 1:
    #             tmp_name = str(input('Insert name '))
    #             tmp_format = str(input('Insert format '))
    #             sheets.append(DmcSheet(tmp_name, tmp_format))

    #         case 2:
    #             tmp_sheet_idx = int(input('Insert sheet id: '))
    #             #sheets[tmp_sheet_idx].display_sheet()
    #             sheets[tmp_sheet_idx].generate_pdf()

    #         case 3:
    #             sheets[0].dmc_config[0].to_json()

    #         case 5:
    #             dmcs = sheets[0].dmc_config[0].get_dmcs()
    #             print(dmcs)
    #            # generate(dmcs)

    #         case 9:
    #             break


    #     selector = int(input('Select option '))

    # print('end')

    # pass


if __name__ == '__main__':
    main()


