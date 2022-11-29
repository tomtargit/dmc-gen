# ----------------- IMPORTS ----------------------

import tkinter as tk
from tkinter import *  
from tkinter import ttk

import uuid
#from tkinter import filedialog
#from PIL import ImageTk, Image

#import project.cfg as cfg
import project.constants as c
from project.project import (Project, Sheet, Dmc, 
                             DmcPartConstant, DmcPartCounter, DisplaySheet)


# ----------------- BUILDING MAIN WINDOW ----------------------

class GuiApp(tk.Tk):
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
        self.frame_edit = FrameEdit(self.frame_main, self)
        self.frame_buttons = FrameButtons(self.frame_main, self)

        # Generate menu
        self.menu_bar = MenuBar(self)
        self.menu_file = MenuFile(self.menu_bar, self)
        self.menu_bar.add_menu_list(self.menu_file,'File')
        self.assign_menu(self.menu_bar)

        # Empty project 
        self.project = Project(self.frame_edit, "New project")

        # Callback
        self.callback = self.register(validate_entry_int)

        # Display 
        self.data_display = []

    def run(self):
        self.mainloop()    

    def assign_menu(self, menu_bar):
        self['menu'] = menu_bar

    def add_new_dmc(project: Project, sheet_uuid):
        project.sheets[0].add_dmc('test_dmc')
        print('added dmc')
        pass    

    # def edit_trace(name,test,mode):
    #     """ Tracking changes made by user in EditFrame """
    #     pass
    #     # print(f"{name},{test},{mode}")
    #     # for idx,var in enumerate(cfg.root.frame_edit.track_vars):
    #     #     #print(f'idx:{idx}')
    #     #     if name == str(var):
    #     #         # retrieve name of var and its location from string varname
    #     #         vars = name.split('#')

    #     #         # sheet uuid - always first argument
    #     #         sheet_uuid = int(vars[0])

    #     #         # if dmc config related:
    #     #         dmc_idx = None
    #     #         if len(vars)>2:
    #     #             dmc_idx = int(vars[1])

    #     #         # if dmc_part config related
    #     #         dmc_part_idx = None
    #     #         if len(vars)>3:
    #     #             dmc_part_idx = int(vars[2])

    #     #         # changed variable name - always last argument
    #     #         var_name = vars[-1]

    #     #         # new passed value
    #     #         new_value = var.get()

    #     #         # print
    #     #         print(f'sheet_uuid: {sheet_uuid}, dmc_idx: {dmc_idx}, dmc_part_idx: {dmc_part_idx}, var_name: {var_name}, new_value: {new_value}')

    #     #         # Update project
    #     #         update_project(cfg.root.project, sheet_uuid, var_name, new_value,
    #     #                        dmc_idx, dmc_part_idx)

    # def update_project(self, project, sheet_uuid, var_name, new_value,  
    #                 dmc_idx=None, dmc_part_idx=None):

    #     for sheet in project.sheets:
    #         print (f'{sheet_uuid}: {sheet.uuid}')
    #         if sheet.uuid == sheet_uuid:
    #             print(f'inside, {dmc_idx}, {dmc_part_idx}')
    #             if dmc_part_idx is not None:
    #                 match str(var_name):
    #                     case 'type':
    #                         sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].type = new_value
    #                     case 'phrase':
    #                         sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].phrase = new_value
    #                     case 'start':
    #                         sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].start = new_value
    #                     case 'step':
    #                         sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].step = new_value
    #                     case 'chars_num':
    #                         sheet.dmc_config[dmc_idx].dmc_part[dmc_part_idx].chars_num = new_value 
    #                     case _: 
    #                         print(f'1 var name not valid: {var_name}')
    #             else:
    #                 if dmc_idx is not None:
    #                     match str(var_name):
    #                         case 'name':
    #                             sheet.dmc_config[dmc_idx].name = new_value
    #                         case 'size':
    #                             sheet.dmc_config[dmc_idx].size = new_value
    #                         case 'quiet_zone':
    #                             sheet.dmc_config[dmc_idx].quiet_zone = new_value    
    #                         case _: 
    #                             print(f'2 var name not valid: {var_name}')
    #                 else:
    #                     match str(var_name):
    #                         case 'name':
    #                             sheet.name = new_value
    #                         case 'size':
    #                             sheet.size = new_value
    #                         case 'orientation':
    #                             sheet.orientation = new_value    
    #                         case _: 
    #                             print(f'3 var name not valid: {var_name}')
    #             print('updated')
    #             break

    def destroy_all(self):
        for sheet in self.project.sheet_frame:
            sheet.destroy()
            
    def display(self, frame, prj: Project):
        self.Project.display_sheets()

    def new_project(self):
        self.Project = Project(self.frame_edit, "New project")

    def open_project(self):
        filename = self.filedialog.askopenfilename()

    def close_window(self):

        self.after(3000,self.destroy())

        # def close():
        #     #msg box if save?
        #     pass


    # ----------------- USER ACTIONS ----------------------

    def add_new_sheet(self):

        new_sheet = Sheet(f'test sheet','A4')

        self.project.add_sheet(new_sheet)
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

    def remove_sheet(self):
        self.project.remove_sheet()


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

    def __init__(self, parent_menu, parent_obj):
        super().__init__()
        self.parent = parent_menu

        self.add_command(label='New  project', command=parent_obj.new_project)
        self.add_command(label='Open project', command=parent_obj.open_project)
        self.add_separator()
        self.add_command(label='Close', command=parent_obj.close_window)

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
    
    def __init__(self, parent_frame, parent_obj):
        super().__init__()
        self.parent = parent_frame
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

    def __init__(self, parent_frame, parent_obj):
        super().__init__()
        self.parent = parent_frame
        #self = ttk.Frame(parent, borderwidth=2, padding=10, relief='groove')
        self.grid(column=1, row=0, sticky='ne')
        self.columnconfigure(0, weight=0)
        self.configure(relief='groove', borderwidth=2, padding=2)

        self.add_sheet = ttk.Button(
            self, 
            text='Add new sheet', 
            width=30, 
            command=parent_obj.add_new_sheet)
        self.add_sheet.grid(column=0, row=0)

        self.remove_sheet = ttk.Button(
            self, text='Remove sheet', 
            width=30, 
            command=parent_obj.remove_sheet)
        self.remove_sheet.grid(column=0, row=1)

        self.remove_sheet = ttk.Button(
            self, text='Unide sheet', 
            width=30, 
            command=lambda : cfg.root.sheet_frame[0].unhide(0))
        self.remove_sheet.grid(column=0, row=2)

        self.display_all = ttk.Button(
            self, text='Display all', 
            width=30, 
            command= lambda : parent_obj.project.display_sheets())
        self.display_all.grid(column=0, row=3)

        self.destroy_all = ttk.Button(
            self, text='Destroy all', 
            width=30, 
            command=parent_obj.destroy_all)
        self.display_all.grid(column=0, row=4)

        self.add_dmc = ttk.Button(
            self, text='Add DMC', 
            width=30, 
            command=parent_obj.add_new_dmc)
        self.add_dmc.grid(column=0, row=5)


    # ----------------- OTHER FUNCTIONS ----------------------



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


