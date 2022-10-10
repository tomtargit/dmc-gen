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

        # Import tkinter styles - must be done here, tk-window object must exists while importing
        import gui.styles as s
        s.s_edit_sheet.layout('EditSheet.TFrame')

        # Root window setting
        self.minsize(500,300)
        self.title('Datamatrix generator')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.option_add('*tearOff', FALSE) # remove dash line from menu
        #self.wm_attributes('-transparentcolor','#010101') # this color will be treated as transparent

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
    def generate_uid(self):
        self.project.id += 1
        return str(self.project.id)

    def assign_menu(self, menu_bar):
        self['menu'] = menu_bar

class DisplaySheet():
    def __init__(self, parent, sheet, sheet_idx, uid):

        # Frame that contatins single sheet definition
        self.frame = ttk.Frame(parent)
        self.frame.configure(style='EditSheet.TFrame', padding=10)
        

        # Sheet parameter - name 
        self.name = StringVar(value=sheet.name, name=generate_varname(uid, 'name')) 
        self.name.trace('w',edit_trace)
        self.name_box = ttk.Entry(self.frame, textvariable=self.name)   # entry field definition
        self.name_label = ttk.Label(self.frame, text='Name')

        # Sheet parameter - size
        self.size = StringVar(value=sheet.size, name=generate_varname(uid, 'size')) 
        self.size.trace('w',edit_trace)
        self.size_box = ttk.Combobox(self.frame, textvariable=self.size, state='readonly')
        self.size_box['values'] = c.SHEET_SIZES
        self.size_label = ttk.Label(self.frame, text='Size')

        # Sheet parameter - oriantation
        self.orientation = StringVar(value=sheet.orientation, name=generate_varname(uid, 'orientation')) 
        self.orientation.trace('w',edit_trace)
        self.orientation_box = ttk.Combobox(self.frame, textvariable=self.orientation, state='readonly')
        self.orientation_box['values'] = c.SHEET_ORIENTATION
        self.orientation_label = ttk.Label(self.frame, text='Orientation')


        # Assign variables for tracing
        parent.inputvars.append(self.name)
        parent.inputvars.append(self.size)
        parent.inputvars.append(self.orientation)

        # Generate #########################
        self.dmcs = []
        for idx, dmc in enumerate(sheet.dmc_config):
            self.dmcs.append(DisplayDmc(parent, self.frame, dmc, idx, uid))
            self.dmcs[idx].show(idx)
        #self.dmcs = []

    def show(self, index):
        # show Sheet frame
        self.unhide(index)

        # define and configure columns

        for idx in range(0,5):
            self.frame.columnconfigure(idx,weight=1)

        self.name_label.grid(column=0, row=0, sticky='nwse')
        self.name_box.grid(column=1, row=0, sticky='nwse')
        self.size_label.grid(column=2, row=0, sticky='nwse')
        self.size_box.grid(column=3, row=0, sticky='nwse')
        self.orientation_label.grid(column=4, row=0, sticky='nwse')
        self.orientation_box.grid(column=5, row=0, sticky='nwse')

    def hide(self):
        print(self.frame.winfo_exists())
        self.frame.grid_forget()
        print(self.frame.winfo_exists())
        self.frame.destroy()
        print(self.frame.winfo_exists())       

    def unhide(self, index):
        self.frame.grid(column=0, row=index, sticky='nwse', pady=(10,10))


class DisplayDmc():
    def __init__(self, parent_vars, parent, dmc, dmc_idx, uid_id):

        # Frame thet contains single DMC config
        self.frame = ttk.Frame(parent)
        self.frame.configure(style='EditDmc.TFrame')

        # Name
        self.name = StringVar(value=dmc.name, name=generate_varname(uid_id, dmc_idx, 'name')) 
        self.name.trace('w',edit_trace)
        self.name_box = ttk.Entry(self.frame, textvariable=self.name, style='EditEntry.TEntry')
        self.name_label = ttk.Label(self.frame, text='Name:', style='EditLabel.TLabel')

        # Size
        self.size = IntVar(value=dmc.size, name=generate_varname(uid_id, dmc_idx, 'size')) 
        self.size.trace('w',edit_trace)
        self.size_box = ttk.Entry(self.frame, textvariable=self.size, style='EditEntry.TEntry')
        self.size_label= ttk.Label(self.frame, text='Size:', style='EditLabel.TLabel')

        # Quiet zone
        self.quiet_zone = IntVar(value=dmc.quiet_zone, name=generate_varname(uid_id, dmc_idx, 'quiet_zone')) 
        self.quiet_zone.trace('w',edit_trace)
        self.quiet_zone_box = ttk.Combobox(self.frame, textvariable=self.quiet_zone, state='readonly', style='EditCombobox.TCombobox')
        self.quiet_zone_box['values'] = c.QUIET_ZONE
        self.quiet_zone_label = ttk.Label(self.frame, text='Quiet zone:', style='EditLabel.TLabel')

        # Assign variables for tracing
        parent_vars.inputvars.append(self.name)
        parent_vars.inputvars.append(self.size)
        parent_vars.inputvars.append(self.quiet_zone)

        self.dmc_parts = []
        for idx, dmc_part in enumerate(dmc.dmc_part):
            # print(dmc_part.type)
            self.dmc_parts.append(DisplayDmcPart(parent_vars, self.frame, dmc_part, idx, uid_id, dmc_idx))
            self.dmc_parts[idx].show(idx)

    def show(self, index):
        # show single DMC config frame
        self.frame.grid(column=0, row=index+1, columnspan=5, padx=(30,0), sticky='nwse')

        # define and configure columns
        for idx in range(0,5):
            self.frame.columnconfigure(idx,weight=1)

        self.name_label.grid(column=0, row=0, sticky='nwse')
        self.name_box.grid(column=1, row=0, sticky='nwse')
        self.size_box.grid(column=2, row=0, sticky='nwse')
        self.quiet_zone_box.grid(column=3, row=0, sticky='nwse')  

class DisplayDmcPart():
    def __init__(self, parent_vars, parent, dmc_part, dmc_part_idx, uid, dmc_idx):
        # DMC Part display
        self.frame = ttk.Frame(parent)
        self.frame.configure(style='EditDmcPart.TFrame')

        # Type
        self.type = StringVar(value=dmc_part.type, name=generate_varname(uid, dmc_idx, dmc_part_idx, 'type')) 
        self.type.trace('w',edit_trace)
        self.type_box = ttk.Combobox(self.frame, textvariable=self.type, state='readonly')
        self.type_box['values'] = c.DMC_PART_TYPE

        parent_vars.inputvars.append(self.type)


        if isinstance(dmc_part, DmcCfgConstant):
            # Phrase
            self.phrase = StringVar(value=dmc_part.phrase, name=generate_varname(uid, dmc_idx, dmc_part_idx, 'phrase')) 
            self.phrase.trace('w',edit_trace)
            self.phrase_box = ttk.Entry(self.frame, textvariable=self.phrase)
            parent_vars.inputvars.append(self.phrase)

        if isinstance(dmc_part, DmcCfgCounter):  
            # Start 
            self.start = IntVar(value=dmc_part.start, name=generate_varname(uid, dmc_idx, dmc_part_idx, 'start')) 
            self.start.trace('w',edit_trace)
            self.start_box = ttk.Entry(self.frame, textvariable=self.start)
            parent_vars.inputvars.append(self.start)

            # Step
            self.step = IntVar(value=dmc_part.step, name=generate_varname(uid, dmc_idx, dmc_part_idx, 'step')) 
            self.step.trace('w',edit_trace)
            self.step_box = ttk.Entry(self.frame, textvariable=self.step)
            parent_vars.inputvars.append(self.step)

            # Number of characters
            self.chars_num = IntVar(value=dmc_part.chars_num, name=generate_varname(uid, dmc_idx, dmc_part_idx, 'chars_num')) 
            self.chars_num.trace('w',edit_trace)
            self.chars_num_box = ttk.Entry(self.frame, textvariable=self.chars_num)
            parent_vars.inputvars.append(self.chars_num)

    def show(self, index):
        # show single DMC config frame
        self.frame.grid(column=0, row=index+1, columnspan=5, padx=(30,0), sticky='nwse')

        # define and configure columns
        for idx in range(0,5):
            self.frame.columnconfigure(idx,weight=0)

        self.type_box.grid(column=0, row=index+1, sticky='nw')

        # TODO try match/case
        if self.type.get() == c.DMC_PART_TYPE[0]:
            self.phrase_box.grid(column=1, row=index+1, sticky='nw')

        if self.type.get() == c.DMC_PART_TYPE[1]:
            self.start_box.grid(column=1, row=index+1, sticky='nw')
            self.step_box.grid(column=2, row=index+1, sticky='nw')
            self.chars_num_box.grid(column=3, row=index+1, sticky='nw')          

        # match str(self.type.get()):
        #     case str(c.DMC_PART_TYPE(0)):
        #         print('type0')
        #     case str(c.DMC_PART_TYPE(1)):
        #         print('type1')    


 # TODO add validation function to entries.


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
        self.columnconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky='nwse')


class FrameEdit(ttk.Frame):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.width = 800
        self.configure(padding=2, relief='groove', borderwidth=2)
        self.grid(column=0, row=0, sticky='nwse')
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

        self.remove_sheet = ttk.Button(self, text='Remove sheet', width=30, command=lambda : root.sheet_frame[0].hide)
        self.remove_sheet.grid(column=0, row=1)

        self.remove_sheet = ttk.Button(self, text='Unide sheet', width=30, command=lambda : root.sheet_frame[0].unhide(0))
        self.remove_sheet.grid(column=0, row=2)

        self.display_all = ttk.Button(self, text='Display all', width=30, command=display)
        self.display_all.grid(column=0, row=3)

        self.add_dmc = ttk.Button(self, text='Add DMC', width=30, command=add_new_dmc)
        self.add_dmc.grid(column=0, row=4)

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

# Generates variable names for tracking of user changes. 
def generate_varname(uid, *args):
    name = str(uid)
    for a in args:
        name += f'#{a}'
    return name

# Tracing edit area changes
def edit_trace(name,test,mode):
    print(f"{name},{test},{mode}")
    for idx,var in enumerate(root.frame_edit.inputvars):
        #print(f'idx:{idx}')
        if name == str(var):
            # retrieve name of var and its location from string varname
            vars = name.split('#')

            # project uid - always first argument
            project_uid = vars[0]

            # if dmc config related:
            dmc_idx = ''
            if len(vars)>2:
                dmc_idx = vars[1]

            # if dmc_part config related
            dmc_part_idx = ''
            if len(vars)>3:
                dmc_part_idx = vars[2]

            # changed variable name - always last argument
            var_name = vars[-1]

            # new passed value
            var_new_value = var.get()

            # print
            print(f'project_uid: {project_uid}, dmc_idx: {dmc_idx}, dmc_part_idx: {dmc_part_idx}, var_name: {var_name}, new_value: {var_new_value}')





def display():
    #root.project.sheets[0].display_sheet()
    # for id0x, sheet in enumerate(project.sheets):
    #     root.frame_edit.tree.insert('','end',f'id0_{id0x}'.zfill(3), text=sheet.name)
    #     for id1x, dmc in enumerate(sheet.dmc_config):
    #         root.frame_edit.tree.insert(f'id0_{id0x}'.zfill(3),'end',f'id1_{id1x}_name'.zfill(3), text=dmc.name)
    # pass
    root.sheet_frame = []
    for id0x, sheet in enumerate(root.project.sheets):
        root.sheet_frame.append(DisplaySheet(root.frame_edit, sheet, id0x, root.generate_uid))
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


