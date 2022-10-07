# This file runs application.

# basic functions
import os

# gui building
import tkinter as tk
from tkinter import *  
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

# dmc objects
from dmc.dmc import DmcCfg, DmcSheet, DmcCfgConstant, DmcCfgCounter
import dmc.constants as c

# project handler
from project.project import Project

def main():
    global root
    root = App()
    root.mainloop()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Root window setting
        self.minsize(500,300)
        self.title('Datamatrix generator')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.option_add('*tearOff', FALSE) # remove dash line from menu

        # Generate frames
        self.frame_main = FrameMain(self)
        self.frame_edit = FrameEdit(self.frame_main)
        self.frame_buttons = FrameButtons(self.frame_main)

        # Generate menu
        self.menu_bar = MenuBar(self)
        self.menu_file = MenuFile(self.menu_bar)
        self.menu_bar.add_menu_list(self.menu_file,'File')
        self.assign_menu(self.menu_bar)

        # Empty project 
        self.project = Project('New_project')
        self.project.id = 0

        # Display 
        self.data_display = []


    @property
    def unique_id(self):
        self.project.id += 1
        return str(self.project.id)

    def assign_menu(self, menu_bar):
        self['menu'] = menu_bar

class DisplaySheet():
    def __init__(self, parent, sheet, sheet_idx, unique_id):

        # Frame that contatins single sheet definition
        self.frame = ttk.Frame(parent)
        self.frame.configure(relief='groove', borderwidth=1, padding=5)

        # self.frame.columnconfigure(0, weight=2)
        # self.frame.columnconfigure(1, weight=3)
        # self.frame.columnconfigure(2, weight=4)

        # Sheet parameter - name 
        self.name = StringVar(value=sheet.name, name=f'{unique_id}_name') 
        self.name.trace('w',simple_trace)
        self.name_box = ttk.Entry(self.frame, textvariable=self.name)   # entry field definition

        # Sheet parameter - size
        self.size = StringVar(value=sheet.size, name=f'{unique_id}_size')
        self.size.trace('w',simple_trace)
        self.size_box = ttk.Entry(self.frame, textvariable=self.size)

        # Sheet parameter - oriantation
        self.orientation = StringVar(value=sheet.orientation, name=f'{unique_id}_orientation')
        self.orientation.trace('w',simple_trace)
        self.orientation_box = ttk.Entry(self.frame, textvariable=self.orientation)

        # Assign variables for tracing
        parent.inputvars.append(self.name)
        parent.inputvars.append(self.size)
        parent.inputvars.append(self.orientation)

        # Generate #########################
        self.dmcs = []
        for idx, dmc in enumerate(sheet.dmc_config):
            self.dmcs.append(DisplayDmc(parent, self.frame, dmc, idx, unique_id))
            self.dmcs[idx].show(idx)
        #self.dmcs = []

    def show(self, index):
        self.frame.grid(column=0, row=index)
        self.frame.columnconfigure(0,weight=2)
        self.name_box.grid(column=0, row=0, sticky='nw')
        self.size_box.grid(column=1, row=0, sticky='nw')
        self.orientation_box.grid(column=2, row=0, sticky='nw')

class DisplayDmc():
    def __init__(self, parent_vars, parent, dmc, dmc_idx, unique_id):
        self.frame = ttk.Frame(parent)
        self.frame.configure(relief='groove', borderwidth=2, padding=5)
        self.name = StringVar(value=dmc.name, name=f'{unique_id}_dmc_{dmc_idx}_name')
        self.name.trace('w',simple_trace)
        self.size = IntVar(value=dmc.size, name=f'{unique_id}_dmc_{dmc_idx}_size')
        self.size.trace('w',simple_trace)
        self.quiet_zone = IntVar(value=dmc.size, name=f'{unique_id}_dmc_{dmc_idx}_quiet_zone')
        self.size.trace('w',simple_trace)
        self.name_box = ttk.Entry(self.frame, textvariable=self.name)
        self.size_box = ttk.Entry(self.frame, textvariable=self.size)
        self.quiet_zone_box = ttk.Entry(self.frame, textvariable=self.quiet_zone)
        parent_vars.inputvars.append(self.name)
        parent_vars.inputvars.append(self.size)
        parent_vars.inputvars.append(self.quiet_zone)

        self.dmc_parts = []
        for idx, dmc_part in enumerate(dmc.dmc_part):
            # print(dmc_part.type)
            self.dmc_parts.append(DisplayDmcPart(parent_vars, self.frame, dmc_part, idx, unique_id, dmc_idx))
            self.dmc_parts[idx].show(idx)

    def show(self, index):
        self.frame.grid(column=0, row=index+1, columnspan=3, padx=(30,0))
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_columnconfigure(1,weight=1)
        self.frame.grid_columnconfigure(2,weight=1)
        self.name_box.grid(column=0, row=0, sticky='nw')
        self.size_box.grid(column=1, row=0, sticky='nw')
        self.quiet_zone_box.grid(column=2, row=0, sticky='nw')

class DisplayDmcPart():
    def __init__(self, parent_vars, parent, dmc_part, dmc_part_idx, unique_id, dmc_idx):
        
        #self.typeint = DMC_PART_TYPE.index(dmc_part.type)
        #print(f'xx_{self.typeint}')
        # Type
        self.type = StringVar(value=dmc_part.type, name=f'{unique_id}_dmc_{dmc_idx}_part_{dmc_part_idx}_type')
        self.type.trace('w',simple_trace)
        self.type_box = ttk.Combobox(parent, textvariable=self.type)
        self.type_box['values'] = c.DMC_PART_TYPE

        parent_vars.inputvars.append(self.type)


        if isinstance(dmc_part, DmcCfgConstant):
            # Phrase
            self.phrase = StringVar(value=dmc_part.phrase, name=f'{unique_id}_dmc_{dmc_idx}_part_{dmc_part_idx}_phrase')
            self.phrase.trace('w',simple_trace)
            self.phrase_box = ttk.Entry(parent, textvariable=self.phrase)
            parent_vars.inputvars.append(self.phrase)

        if isinstance(dmc_part, DmcCfgCounter):  
            # Start 
            self.start = IntVar(value=dmc_part.start, name=f'{unique_id}_dmc_{dmc_idx}_part_{dmc_part_idx}_start')
            self.start.trace('w',simple_trace)
            self.start_box = ttk.Entry(parent, textvariable=self.start)
            parent_vars.inputvars.append(self.start)

            # Step
            self.step = IntVar(value=dmc_part.step, name=f'{unique_id}_dmc_{dmc_idx}_part_{dmc_part_idx}_step')
            self.step.trace('w',simple_trace)
            self.step_box = ttk.Entry(parent, textvariable=self.step)
            parent_vars.inputvars.append(self.step)

            # Number of characters
            self.chars_num = IntVar(value=dmc_part.chars_num, name=f'{unique_id}_dmc_{dmc_idx}_part_{dmc_part_idx}_chars_num')
            self.chars_num.trace('w',simple_trace)
            self.chars_num_box = ttk.Entry(parent, textvariable=self.chars_num)
            parent_vars.inputvars.append(self.chars_num)

    def show(self, index):
        #self.frame.grid(column=0, row=index+1, columnspan=3, padx=(30,0))
        # self.frame.grid_columnconfigure(0,weight=1)
        # self.frame.grid_columnconfigure(1,weight=1)
        # self.frame.grid_columnconfigure(2,weight=1)
        self.type_box.grid(column=1, row=index+1, sticky='nw')

        if self.type.get() == c.DMC_PART_TYPE[0]:
            self.phrase_box.grid(column=2, row=index+1, sticky='nw')

        if self.type.get() == c.DMC_PART_TYPE[1]:
            self.start_box.grid(column=2, row=index+1, sticky='nw')
            self.step_box.grid(column=3, row=index+1, sticky='nw')
            self.chars_num_box.grid(column=4, row=index+1, sticky='nw')          


 

#Display


# class DisplayDmcConfig
#         self

class MenuBar(tk.Menu):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def add_menu_list(self,menu_list,menu_label):
        # Add menu lists to menu
        self.add_cascade( menu=menu_list, label=menu_label)


class MenuFile(tk.Menu):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.add_command(label='New  project')#, command=close_window)
        self.add_command(label='Open project', command=open_project)
        self.add_separator()
        self.add_command(label='Close', command=close_window)


class FrameMain(ttk.Frame):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.columnconfigure(0, weight=5)
        self.grid(column=0, row=0)


class FrameEdit(ttk.Frame):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.width = 800
        self.configure(padding=2, relief='groove', borderwidth=2)
        self.grid(column=0, row=0, sticky='nw')
        self.columnconfigure(0, weight=1)
        self.inputvars = []


        # Bigger Grids as sheets


        # # generate Treeview
        # self.tree = self.ProjectTree(self)

    # class ProjectTree(ttk.Treeview):
    #     def __init__(self, parent):
    #         super().__init__()
    #         self.parent=parent
    #         self.show = 'tree'
    #         self.grid(column=0, row=0, sticky='nw')
    #         self.columnconfigure(0, weight=1)


class FrameButtons(ttk.Frame):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        #self = ttk.Frame(parent, borderwidth=2, padding=10, relief='groove')
        self.grid(column=1, row=0, sticky='ne')
        self.columnconfigure(0, weight=0)
        self.configure(relief='groove', borderwidth=2, padding=2)

        self.add_sheet = ttk.Button(self, text='Add new sheet', width=30, command=add_new_sheet)
        self.add_sheet.grid(column=0, row=0)

        self.remove_sheet = ttk.Button(self, text='Remove sheet', width=30, command=display)
        self.remove_sheet.grid(column=0, row=1)

        self.add_dmc = ttk.Button(self, text='Add DMC', width=30, command=add_new_dmc)
        self.add_dmc.grid(column=0, row=2)

def add_new_sheet():

    new_sheet_id = len(root.project.sheets) 

    root.project.AddSheet(DmcSheet(f'test sheet {new_sheet_id}','A4'))
    root.project.sheets[new_sheet_id].add_dmc('variant_no')
    root.project.sheets[new_sheet_id].dmc_config[0].set_count(10)
    root.project.sheets[new_sheet_id].dmc_config[0].set_size(10)
    root.project.sheets[new_sheet_id].dmc_config[0].add_dmc_part(DmcCfgConstant('4500000010'))
    root.project.sheets[new_sheet_id].dmc_config[0].add_dmc_part(DmcCfgCounter(1, 1, 3))
    root.project.sheets[new_sheet_id].add_dmc('body')
    root.project.sheets[new_sheet_id].dmc_config[1].set_count(10)
    root.project.sheets[new_sheet_id].dmc_config[1].set_size(15)
    root.project.sheets[new_sheet_id].dmc_config[1].add_dmc_part(DmcCfgConstant('5555100030'))
    root.project.sheets[new_sheet_id].dmc_config[1].add_dmc_part(DmcCfgCounter(1, 1, 3))

    print('added')

    pass

def add_new_dmc():
    root.project.sheets[0].add_dmc('test_dmc')
    print('added dmc')
    pass    

# Tracing edit area changes
def simple_trace(name,test,mode):
    print(f"{name},{test},{mode}")
    for idx,var in enumerate(root.frame_edit.inputvars):
        #print(f'idx:{idx}')
        if name == str(var):
            print(var.get())
    

def display():
    #root.project.sheets[0].display_sheet()
    # for id0x, sheet in enumerate(project.sheets):
    #     root.frame_edit.tree.insert('','end',f'id0_{id0x}'.zfill(3), text=sheet.name)
    #     for id1x, dmc in enumerate(sheet.dmc_config):
    #         root.frame_edit.tree.insert(f'id0_{id0x}'.zfill(3),'end',f'id1_{id1x}_name'.zfill(3), text=dmc.name)
    # pass
    root.sheet_frame = []
    for id0x, sheet in enumerate(root.project.sheets):
        root.sheet_frame.append(DisplaySheet(root.frame_edit, sheet, id0x, root.unique_id))
        root.sheet_frame[id0x].show(id0x)

        # root.sheet_frame[id0x].grid(column=0, row=id0x)
        # root.sheet_frame.main.append(ttk.Label(root.sheet_frame[id0x], text=sheet.name))
        # root.sheet_frame.main.append(ttk.Label(root.sheet_frame[id0x], text=sheet.size))
        # root.sheet_frame.main.append(ttk.Label(root.sheet_frame[id0x], text=sheet.orientation))
        # root.sheet_frame.main[id0x].grid(column=0,row=0, sticky='wn')
        # test_label = []
        # for id1x, dmc in enumerate(sheet.dmc_config):
        #     test_label.append(ttk.Label(root.sheet_frame[id0x], text=dmc.name))
        #     test_label[id1x].grid(column=1, row=id1x+1, sticky='wn')
        # for id1x, dmc in enumerate(sheet.dmc_config):
        #     root.frame_edit.sheet[id0x]


def open_project():
    filename = filedialog.askopenfilename()


def close_window():
    # msgbox ?
    root.after(3000,root.destroy())

    # def close():
    #     #msg box if save?
    #     pass

  
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


# Main
if __name__ == '__main__':
    #root = Tk()
    main()


