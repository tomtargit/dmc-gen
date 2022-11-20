# ----------------- IMPORTS ----------------------

import tkinter as tk
from tkinter import *  
from tkinter import ttk

import uuid
#from tkinter import filedialog
#from PIL import ImageTk, Image

import dmc.constants as c_dmc
from dmc.dmc import Dmc, DmcPartConstant, DmcPartCounter

from project.project import Project, Sheet
import project.constants as c_project

import project.cfg as cfg

# ----------------- BUILDING MAIN WINDOW ----------------------

class App(tk.Tk):
    """ Runs whole tkinter application """
    
    def __init__(self):
        super().__init__()

        # Import tkinter styles - must be done here, 
        # tk-window object must exist while importing,
        # other case creates new window at import
        import gui.styles as s
        s.s_edit_sheet.layout('EditSheet.TFrame')

        # Root window setting
        self.minsize(500,300)
        self.title('DataMatrixCode generator')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.option_add('*tearOff', "FALSE") # remove dash line from menu
        # self.wm_attributes('-transparentcolor','#010101') 
        # this color will be treated as transparent

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
        self.project = Project("New project")

        # Callback
        self.callback = self.register(validate_entry_int)

        # Display 
        self.data_display = []

    def assign_menu(self, menu_bar):
        self['menu'] = menu_bar

# ----------------- MENUBAR CREATION ----------------------

class MenuBar(tk.Menu):
    """ Menu Bar of the app window. """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def add_menu_list(self,menu_list,menu_label):
        self.add_cascade( menu=menu_list, label=menu_label)

class MenuFile(tk.Menu):
    """ File menu in app menubar. """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.add_command(label='New  project')#, command=close_window)
        self.add_command(label='Open project', command=open_project)
        self.add_separator()
        self.add_command(label='Close', command=close_window)

# ----------------- CREATING INTERNAL FRAMES ----------------------

class FrameMain(ttk.Frame):
    """ Manages main frame containing other frames. 
    
    Frame contents:
        - FrameEdit,
        - FrameButtons.
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky='nwse')

class FrameEdit(ttk.Frame):
    """ Manages frame containing project for edition. 
    
    Frame contents:
        - Tab control (ttk.notebook) for every sheet in project.
    """
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.width = 800
        self.configure(padding=2, relief='groove', borderwidth=2)
        self.grid(column=0, row=0, sticky='nwse')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0,weight=1)
        self.track_vars = []

        self.tab_control = ttk.Notebook(self)
        self.tab_control.columnconfigure(0, weight=1)
        self.tab_control.rowconfigure(0,weight=1)
        self.tab_control.configure(style='EditTabControl.TNotebook')
        self.tab_control.grid(column=0, row=0, sticky="nwse")

class FrameButtons(ttk.Frame):
    """ Manages frame with action buttons. """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        #self = ttk.Frame(parent, borderwidth=2, padding=10, relief='groove')
        self.grid(column=1, row=0, sticky='ne')
        self.columnconfigure(0, weight=0)
        self.configure(relief='groove', borderwidth=2, padding=2)

        self.add_sheet = ttk.Button(
            self, 
            text='Add new sheet', 
            width=30, command=add_new_sheet)
        self.add_sheet.grid(column=0, row=0)

        self.remove_sheet = ttk.Button(
            self, text='Remove sheet', 
            width=30, 
            command=remove_sheet)
        self.remove_sheet.grid(column=0, row=1)

        self.remove_sheet = ttk.Button(
            self, text='Unide sheet', 
            width=30, 
            command=lambda : cfg.root.sheet_frame[0].unhide(0))
        self.remove_sheet.grid(column=0, row=2)

        self.display_all = ttk.Button(
            self, text='Display all', 
            width=30, 
            command=display)
        self.display_all.grid(column=0, row=3)

        self.display_all = ttk.Button(
            self, text='Destroy all', 
            width=30, 
            command=destroy_all)
        self.display_all.grid(column=0, row=4)

        self.add_dmc = ttk.Button(
            self, text='Add DMC', 
            width=30, command=add_new_dmc)
        self.add_dmc.grid(column=0, row=5)

# ----------------- DISPLAYING PROJECT CONTENTS ----------------------

class DisplaySheet():
    """ Graphical representation of DMC.Sheet object. """

    def __init__(self, parent, sheet, sheet_idx, uuid):

        self.tab_control = parent.tab_control

        # Frame that contatins single sheet definition
        self.frame = ttk.Frame(parent)
        self.frame.configure(
            style='EditSheet.TFrame', 
            padding=5)
        
        # Sheet parameter - name 
        self.name = StringVar(
            value=sheet.name, 
            name=gen_track_name(uuid, 'name')
            )
        self.name.trace('w',edit_trace)
        self.name_box = ttk.Entry(
            self.frame, 
            textvariable=self.name
            )   
        self.name_label = ttk.Label(
            self.frame, 
            text='Name'
            )

        # Sheet parameter - size
        self.size = StringVar(
            value=sheet.size, 
            name=gen_track_name(uuid, 'size')
            ) 
        self.size.trace('w',edit_trace)
        self.size_box = ttk.Combobox(
            self.frame, 
            textvariable=self.size, 
            state='readonly', 
            width=10
            )
        self.size_box['values'] = c_project.SHEET_SIZES
        self.size_label = ttk.Label(
            self.frame, 
            text='Size', )

        # Sheet parameter - orientation
        self.orientation = StringVar(
            value=sheet.orientation, 
            name=gen_track_name(uuid, 'orientation')
            ) 
        self.orientation.trace('w',edit_trace)
        self.orientation_box = ttk.Combobox(
            self.frame, 
            textvariable=self.orientation, 
            state='readonly', width=10
            )
        self.orientation_box['values'] = c_project.SHEET_ORIENTATION
        self.orientation_label = ttk.Label(
            self.frame, text='Orientation')

        # Assign variables for tracing
        parent.track_vars.append(self.name)
        parent.track_vars.append(self.size)
        parent.track_vars.append(self.orientation)

        # Generate #########################
        self.dmcs = []
        for idx, dmc in enumerate(sheet.dmc_config):
            self.dmcs.append(DisplayDmc(parent, self.frame, dmc, idx, uuid))
            self.dmcs[idx].show(idx)
        #self.dmcs = []

    def show(self, index):
        # show Sheet frame
        self.unhide(index)

        # define and configure columns

        for idx in range(0,2):
            self.frame.grid_columnconfigure(idx,weight=0)
            self.frame.grid_rowconfigure(idx,weight=0)

        self.name_label.grid(column=0, row=0, sticky='nw')
        self.name_box.grid(column=1, row=0, sticky='nw', columnspan=2)
        self.size_label.grid(column=0, row=1, sticky='nw')
        self.size_box.grid(column=1, row=1, sticky='nw')
        self.orientation_label.grid(column=0, row=2, sticky='nw')
        self.orientation_box.grid(column=1, row=2, sticky='nw')

    def hide(self):
        print(self.frame.winfo_exists())
        self.frame.grid_forget()
        print(self.frame.winfo_exists())
        self.frame.destroy()
        print(self.frame.winfo_exists())       

    def unhide(self, index):
        self.tab_control.add(self.frame, text=self.name.get())
        # self.frame.grid(column=0, row=0, sticky='nwe', pady=(10,10))
        # self.frame.grid(column=0, row=index, sticky='nwe', pady=(10,10))

    def destroy(self):
        self.tab_control.forget(self.frame)
        # self.frame.destroy()

class DisplayDmc():
    """ Graphical representation of DMC.DMC object. """

    def __init__(self, parent_vars, parent, dmc, dmc_idx, uuid_id):

        # Frame thet contains single DMC config
        self.frame = ttk.Frame(parent)
        self.frame.configure(style='EditDmc.TFrame')

        # Name
        self.name = StringVar(
            master=self.frame,
            value=dmc.name, 
            name=gen_track_name(uuid_id, dmc_idx, 'name')
            ) 
        self.name.trace('w',edit_trace)
        self.name_box = ttk.Entry(
            self.frame, 
            textvariable=self.name, 
            style='EditEntry.TEntry'
            )
        self.name_label = ttk.Label(
            self.frame, 
            text='Name:', 
            style='EditLabel.TLabel'
            )

        # Size
        self.size = IntVar(
            master=self.frame,
            value=dmc.size, 
            name=gen_track_name(uuid_id, dmc_idx, 'size'),
            ) 
        self.size.trace('w',edit_trace)
        self.size_box = ttk.Entry(
            self.frame, 
            textvariable=self.size, 
            name = 'size',
            validate = 'all',
            validatecommand = (cfg.root.callback, '%P', '%W'),
            style='EditEntry.TEntry')
        self.size_label= ttk.Label(
            self.frame, text='Size:', 
            style='EditLabel.TLabel')

        # Quiet zone
        self.quiet_zone = IntVar(
            master=self.frame,
            value=dmc.quiet_zone, 
            name=gen_track_name(uuid_id, dmc_idx, 'quiet_zone')) 
        self.quiet_zone.trace('w',edit_trace)
        self.quiet_zone_box = ttk.Combobox(
            self.frame, 
            textvariable=self.
            quiet_zone, 
            state='readonly', 
            style='EditCombobox.TCombobox')
        self.quiet_zone_box['values'] = c_dmc.QUIET_ZONE
        self.quiet_zone_label = ttk.Label(
            self.frame, 
            text='Quiet zone:', 
            style='EditLabel.TLabel')

        # Assign variables for tracing
        parent_vars.track_vars.append(self.name)
        parent_vars.track_vars.append(self.size)
        parent_vars.track_vars.append(self.quiet_zone)

        self.dmc_parts = []
        for idx, dmc_part in enumerate(dmc.dmc_part):
            # print(dmc_part.type)
            self.dmc_parts.append(DisplayDmcPart(
                parent_vars, 
                self.frame, 
                dmc_part, 
                idx, 
                uuid_id, 
                dmc_idx))
            self.dmc_parts[idx].show(idx)

    def show(self, index):
        # show single DMC config frame
        self.frame.grid(
            column=3,
            row=index,
            padx=(30,0),
            pady=(10,10), 
            sticky='nwse')
        #self.frame.grid(column=0, row=index+1, columnspan=5, padx=(30,0), sticky='nwse')

        # define and configure columns
        for idx in range(0,5):
            self.frame.columnconfigure(idx,weight=1)

        self.name_label.grid(column=0, row=0, sticky='nw')
        self.name_box.grid(column=1, row=0, sticky='nw')
        self.size_label.grid(column=2, row=0, sticky='nw')
        self.size_box.grid(column=3, row=0, sticky='nw')
        self.quiet_zone_label.grid(column=4, row=0, sticky='nw')
        self.quiet_zone_box.grid(column=5, row=0, sticky='nw') 

    def destroy(self):
        self.frame.destroy()

class DisplayDmcPart():
    """ Graphical representation of DMC.DmcPart object. """
    def __init__(self, parent_vars, parent, dmc_part, dmc_part_idx, uuid, dmc_idx):
        # DMC Part display
        self.frame = ttk.Frame(parent)
        self.frame.configure(style='EditDmcPart.TFrame')

        # Type
        self.type = StringVar(
            master=self.frame,
            value=dmc_part.type, 
            name=gen_track_name(uuid, dmc_idx, dmc_part_idx, 'type')) 
        self.type.trace('w',edit_trace)
        self.type_box = ttk.Combobox(self.frame, textvariable=self.type, state='readonly')
        self.type_box['values'] = c_dmc.DMC_PART_TYPE

        parent_vars.track_vars.append(self.type)


        if isinstance(dmc_part, DmcPartConstant):
            # Phrase
            self.phrase = StringVar(
                master=self.frame,
                value=dmc_part.phrase, 
                name=gen_track_name(uuid, dmc_idx, dmc_part_idx, 'phrase')) 
            self.phrase.trace('w',edit_trace)
            self.phrase_box = ttk.Entry(self.frame, textvariable=self.phrase)
            self.phrase_label = ttk.Label(            
                self.frame, 
                text='Phrase:', 
                style='EditLabel.TLabel'
                )
            parent_vars.track_vars.append(self.phrase)

        if isinstance(dmc_part, DmcPartCounter):  
            # Start 
            self.start = IntVar(
                master=self.frame,
                value=dmc_part.start, 
                name=gen_track_name(uuid, dmc_idx, dmc_part_idx, 'start')) 
            self.start.trace('w',edit_trace)
            self.start_box = ttk.Entry(self.frame, textvariable=self.start)
            self.start_label = ttk.Label(            
                self.frame, 
                text='Start:', 
                style='EditLabel.TLabel'
                )
            parent_vars.track_vars.append(self.start)

            # Step
            self.step = IntVar(
                master=self.frame,
                value=dmc_part.step, 
                name=gen_track_name(uuid, dmc_idx, dmc_part_idx, 'step')) 
            self.step.trace('w',edit_trace)
            self.step_box = ttk.Entry(self.frame, textvariable=self.step)
            self.step_label = ttk.Label(            
                self.frame, 
                text='Step:', 
                style='EditLabel.TLabel'
                )
            parent_vars.track_vars.append(self.step)

            # Number of characters
            self.chars_num = IntVar(
                master=self.frame,
                value=dmc_part.chars_num, 
                name=gen_track_name(uuid, dmc_idx, dmc_part_idx, 'chars_num')) 
            self.chars_num.trace('w',edit_trace)
            self.chars_num_box = ttk.Entry(self.frame, textvariable=self.chars_num)
            self.chars_num_label = ttk.Label(            
                self.frame, 
                text='Chars num:', 
                style='EditLabel.TLabel'
                )
            parent_vars.track_vars.append(self.chars_num)

    def show(self, index):
        # show single DMC config frame
        self.frame.grid(column=0, row=index+3, columnspan=5, padx=(30,0), pady=(10,10), sticky='nwse')

        # define and configure columns
        for idx in range(0,5):
            self.frame.columnconfigure(idx,weight=0)

        self.type_box.grid(column=0, row=index+2, sticky='nw')

        # TODO try match/case
        if self.type.get() == c_dmc.DMC_PART_TYPE[0]:
            self.phrase_label.grid(column=1, row=index+1, sticky='nw')
            self.phrase_box.grid(column=1, row=index+2, sticky='nw')


        if self.type.get() == c_dmc.DMC_PART_TYPE[1]:
            self.start_label.grid(column=1, row=index+1, sticky='nw')
            self.start_box.grid(column=1, row=index+2, sticky='nw')

            self.step_label.grid(column=2, row=index+1, sticky='nw')
            self.step_box.grid(column=2, row=index+2, sticky='nw')

            self.chars_num_label.grid(column=3, row=index+1, sticky='nw')
            self.chars_num_box.grid(column=3, row=index+2, sticky='nw')          

        # match str(self.type.get()):
        #     case str(c.DMC_PART_TYPE(0)):
        #         print('type0')
        #     case str(c.DMC_PART_TYPE(1)):
        #         print('type1')    

    def destroy(self):
        self.frame.destroy()

# ----------------- USER ACTIONS ----------------------

def add_new_sheet():

    new_sheet = Sheet(f'test sheet','A4')

    cfg.root.project.add_sheet(new_sheet)
    # cfg.root.project.sheets[new_sheet_id].add_dmc('variant_no')
    # cfg.root.project.sheets[new_sheet_id].dmc_config[0].set_count(10)
    # cfg.root.project.sheets[new_sheet_id].dmc_config[0].set_size(10)
    # cfg.root.project.sheets[new_sheet_id].dmc_config[0].add_dmc_part(DmcPartConstant('4500000010'))
    # cfg.root.project.sheets[new_sheet_id].dmc_config[0].add_dmc_part(DmcPartCounter(1, 1, 3))
    # cfg.root.project.sheets[new_sheet_id].add_dmc('body')
    # cfg.root.project.sheets[new_sheet_id].dmc_config[1].set_count(10)
    # cfg.root.project.sheets[new_sheet_id].dmc_config[1].set_size(15)
    # cfg.root.project.sheets[new_sheet_id].dmc_config[1].add_dmc_part(DmcPartConstant('5555100030'))
    # cfg.root.project.sheets[new_sheet_id].dmc_config[1].add_dmc_part(DmcPartCounter(1, 1, 3))

    print('added')

    pass

def remove_sheet():
    cfg.root.project.remove_sheet()


def add_new_dmc(project: Project, sheet_uuid):
    cfg.root.project.sheets[0].add_dmc('test_dmc')
    print('added dmc')
    pass    

def gen_track_name(*args) -> str:
    """ Generates variable names for tracking of user changes. """

    name = '$'.join(map(str,args))
    return name


def validate_entry_int(value, name):
        print(f'validate {value} {name}')# {name}')
        try:
            int(value)
            if int(value) < 99:
                return True
            else:
                return False
        except:
            return False

def edit_trace(name,test,mode):
    """ Tracking changes made by user in EditFrame """

    print(f"{name},{test},{mode}")
    for idx,var in enumerate(cfg.root.frame_edit.track_vars):
        #print(f'idx:{idx}')
        if name == str(var):
            # retrieve name of var and its location from string varname
            vars = name.split('#')

            # sheet uuid - always first argument
            sheet_uuid = int(vars[0])

            # if dmc config related:
            dmc_idx = None
            if len(vars)>2:
                dmc_idx = int(vars[1])

            # if dmc_part config related
            dmc_part_idx = None
            if len(vars)>3:
                dmc_part_idx = int(vars[2])

            # changed variable name - always last argument
            var_name = vars[-1]

            # new passed value
            new_value = var.get()

            # print
            print(f'sheet_uuid: {sheet_uuid}, dmc_idx: {dmc_idx}, dmc_part_idx: {dmc_part_idx}, var_name: {var_name}, new_value: {new_value}')

            # Update project
            update_project(cfg.root.project, sheet_uuid, var_name, new_value,
                           dmc_idx, dmc_part_idx)

def update_project(project, sheet_uuid, var_name, new_value,  
                   dmc_idx=None, dmc_part_idx=None):

    for sheet in project.sheets:
        print (f'{sheet_uuid}: {sheet.uuid}')
        if sheet.uuid == sheet_uuid:
            print(f'inside, {dmc_idx}, {dmc_part_idx}')
            if dmc_part_idx is not None:
                match str(var_name):
                    case 'type':
                        sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].type = new_value
                    case 'phrase':
                        sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].phrase = new_value
                    case 'start':
                        sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].start = new_value
                    case 'step':
                        sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].step = new_value
                    case 'chars_num':
                        sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].chars_num = new_value 
                    case _: 
                        print(f'1 var name not valid: {var_name}')
            else:
                if dmc_idx is not None:
                    match str(var_name):
                        case 'name':
                            sheet.dmc_config[dmc_idx].name = new_value
                        case 'size':
                            sheet.dmc_config[dmc_idx].size = new_value
                        case 'quiet_zone':
                            sheet.dmc_config[dmc_idx].quiet_zone = new_value    
                        case _: 
                            print(f'2 var name not valid: {var_name}')
                else:
                    match str(var_name):
                        case 'name':
                            sheet.name = new_value
                        case 'size':
                            sheet.size = new_value
                        case 'orientation':
                            sheet.orientation = new_value    
                        case _: 
                            print(f'3 var name not valid: {var_name}')
            print('updated')
            break

def destroy_all():
    for sheet in cfg.root.sheet_frame:
        sheet.destroy()
           
def display():
    cfg.root.sheet_frame = []
    for id0x, sheet in enumerate(cfg.root.project.sheets):
        cfg.root.sheet_frame.append(DisplaySheet(cfg.root.frame_edit, 
                                    sheet, id0x, sheet.id))
        cfg.root.sheet_frame[id0x].show(id0x)

def open_project():
    filename = cfg.filedialog.askopenfilename()

def close_window():

    cfg.root.after(3000,cfg.root.destroy())

    # def close():
    #     #msg box if save?
    #     pass

