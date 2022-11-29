# ----------------- IMPORTS ----------------------

from uuid import uuid4, UUID
from PIL import Image
from fpdf import FPDF
from abc import ABC
from pylibdmtx.pylibdmtx import encode, decode
import json

import tkinter as tk
from tkinter import *  
from tkinter import ttk


from . import constants as c

# ------- CLASS DEFINITIONS FOR PROJECT CONTENTS ----

class DmcPart:
    """ Common class to inherit from for different DmcPart classes"""

class DmcPartCounter(DmcPart):
    """ Counter - part of single DMC config. """
    
    def __init__(self, start=0, step=1, chars_num=1):
        self.type = 'Counter'
        self.uuid = uuid4()
        self.start = start
        self.step = step
        self.chars_num = chars_num

class DmcPartConstant(DmcPart):
    """ Constant - part of single DMC config. """

    def __init__(self, phrase='text'):
        self.type = 'Constant'
        self.uuid = uuid4()
        self.phrase = phrase


# TODO: define if number should be printed beneath code
class Dmc:
    """ Contains single DMC configuration """

    def __init__(self, name):
        self.name = name
        self.uuid = uuid4()
        self.size = 1
        self.quiet_zone = 1
        self.count = 0
        self.dmc_parts = {}
        self.dmc_parts_order = []
        self.dmcs = []

    def to_json(self):
        json.dumps(self.__dict__)

    def get_dmcs(self):
        self.dmcs = []
        for x in range(self.count):
            result_dmc = ''
            for item in self.dmc_parts:
                if isinstance(item,DmcPartConstant):
                    result_dmc += item.phrase
                if isinstance(item,DmcPartCounter):
                    result_dmc += str(int(item.start)+x*int(item.step)).zfill(item.chars_num)
            print(result_dmc)
            self.dmcs.append(result_dmc)
        return self.dmcs

    def set_size(self, size):
        self.size = size

    def set_count(self, count):
        self.count = count

    def set_quiet_zone(self, arg_quiet_zone):
        self.quiet_zone = arg_quiet_zone

    # def add_dmc_part(self, arg_data):
    #     if isinstance(arg_data,DmcPartConstant) \
    #             or isinstance(arg_data,DmcPartCounter):
    #         self.dmc_part.append(arg_data)
    #     else:
    #         print('----Data not valid')

    def add_part(self, dmc_part: DmcPart = DmcPartConstant()):
        """ Adds dmc_part to dmc. 
        
        If dmc_part is not passed as argument, 
        creates empty "constant" dmc part.
        """
        self.dmc_parts[dmc_part.id] = dmc_part
        self.dmc_parts_order.append(dmc_part.id)
        print(f'Added dmc: {dmc_part.id}')

    def remove_part(self, dmc_part_id: UUID):
        """ Removes dmc from sheet. """
        
        # TODO ask user for confirmation

        self.dmc_parts.pop(dmc_part_id)
        self.dmc_parts_order.remove(dmc_part_id)
        print(f'Removed dmc data: {dmc_part_id}')

    def display_config(self):
        print('\t', self.name, self.size, self.quiet_zone, self.count)
        for item in self.dmc_part:
            if isinstance(item,DmcPartConstant):
                print('\t\t', item.type, item.phrase)
            if isinstance(item,DmcPartCounter):
                print('\t\t', item.type, 'start', item.start, 'by', item.step, 'characters', item.chars_num)

        # def main():
        #     pdf = FPDF()
        #     pdf.add_page()
        #     pdf.set_font('helvetica', size=12)
        #     pdf.cell(txt="hello world")
        #     pdf.output("hello_world.pdf")


class Sheet:  
    """ Manages single sheet definition.
    
    Contains single DMC parameters and lower level contents
    """

    def __init__(self, arg_name,  arg_size='A4', orientation='P'):
        self.id = uuid4()
        self.name = arg_name
        self.size = arg_size
        self.orientation = orientation
        self.dmcs = {}
        self.dmcs_order = []
        self.saved = False

    # def add_dmc(self, name):
    #     self.dmcs.append(Dmc(name))

    def add_dmc(self, dmc: Dmc = Dmc('New')):
        """ Adds dmc to sheet. 
        
        If dmc is not passed as argument, creates empty dmc.
        """
        self.dmcs[dmc.id] = dmc
        self.sheets_order.append(dmc.id)
        print(f'Added dmc: {dmc.id}')

    def remove_dmc(self, dmc_id: UUID):
        """ Removes dmc from sheet. """
        
        # TODO ask user for confirmation

        self.dmcs.pop(dmc_id)
        self.sheets_order.remove(dmc_id)
        print(f'Removed dmc data: {dmc_id}')

    def display_sheet(self):
        print('Sheet config: ', self.name, self.size)
        for item in self.dmcs:
            item.display_config()

    def generate(data):

        encoded = encode(data.encode('utf8'), size='SquareAuto')
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        return img
        # img.show()
        # img.save('dmtx.png')
        # print(decode(Image.open('dmtx.png')))
        # TODO: add size definition for DMC genertion or DMC sizing when printing to PDF


    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size=12)
        x_start = 10
        y_start = 10
        interline = 4
        header_size = 8
        for dmc_idx, dmc_config in enumerate(self.dmcs):
            pdf.set_font('helvetica', size=header_size)
            header_length = pdf.get_string_width(dmc_config.name)

            x_increment = dmc_config.size
            y_increment = dmc_config.size + interline

            x_pos = x_start + x_increment * dmc_idx

            pdf.set_xy(x_pos, y_start)
            pdf.cell(0, 0, dmc_config.name, 0, 0)

            pdf.line(x_pos-0.2, 0, x_pos-0.2, 297)
            for dmc_idx2, dmcs in enumerate(dmc_config.get_dmcs()):
                tmp_img = self.generate(dmcs)
                # tmp_img.show()
                # tmp_img.save('dmtx.png')
                y_pos = y_start + header_size + y_increment*dmc_idx2
                pdf.image(tmp_img, x_pos, y_pos, h=dmc_config.size, type='PNG')
                pdf.set_font('helvetica', size=dmc_config.size/3)
                pdf.set_xy(x_pos, y_pos+1.05*dmc_config.size)
                pdf.cell(0, 0, dmcs, 0, 2)

        pdf.output("hello_world.pdf")

class Project:
    """ Manages single project definition.
    
    Contains single project parameters and lower-level components.
    """
    def __init__(self, tab_control, arg_name: str = "NewProject"):
        self.id = uuid4()
        self.name = arg_name
        self.sheets_order = []
        self.sheets = {}
        self.sheets_gui = {}
        self.tab_control = tab_control

        self.saved = False
        self.location = ''

    def add_sheet(self, sheet: Sheet = Sheet('Empty')):
        """ Adds sheet to project. 
        
        If sheet is not passed as argument, creates empty sheet.
        """
        self.sheets[sheet.id] = sheet
        self.sheets_gui[sheet.id] = DisplaySheet(
            self.tab_control, 
            sheet
        )
        self.sheets_order.append(sheet.id)
        print(f'Added sheet: {sheet.id}')

    def remove_sheet(self, sheet_id: UUID):
        """ Removes sheet from project. """
        
        # TODO ask user for confirmation

        self.sheets.pop(sheet_id)
        self.sheets_order.remove(sheet_id)
        print(f'Removed sheet data: {sheet_id}')

    def display_sheets(self):
        for idx, sheet_id in enumerate(self.sheets_order):                                            
             self.sheets_gui[sheet_id].show(idx)    


def gen_track_name(*args) -> str:
    """ Generates variable names for tracking of user changes. """

    name = '$'.join(map(str,args))
    return name

def edit_trace(*args):
    pass

# ----------------- DISPLAYING PROJECT CONTENTS ----------------------

class DisplaySheet():
    """ Graphical representation of Sheet object. """

    def __init__(self, parent, sheet):

        self.tab_control = parent.tab_control

        # Frame that contatins single sheet definition
        self.frame = ttk.Frame(self.tab_control)
        self.frame.configure(
            style='EditSheet.TFrame', 
            padding=5)
        
        # Sheet parameter - name 
        self.name = StringVar(
            value=sheet.name, 
            name=gen_track_name(sheet.id, 'name')
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
            name=gen_track_name(sheet.id, 'size')
            ) 
        self.size.trace('w',edit_trace)
        self.size_box = ttk.Combobox(
            self.frame, 
            textvariable=self.size, 
            state='readonly', 
            width=10
            )
        self.size_box['values'] = c.SHEET_SIZES
        self.size_label = ttk.Label(
            self.frame, 
            text='Size', )

        # Sheet parameter - orientation
        self.orientation = StringVar(
            value=sheet.orientation, 
            name=gen_track_name(sheet.id, 'orientation')
            ) 
        self.orientation.trace('w',edit_trace)
        self.orientation_box = ttk.Combobox(
            self.frame, 
            textvariable=self.orientation, 
            state='readonly', width=10
            )
        self.orientation_box['values'] = c.SHEET_ORIENTATION
        self.orientation_label = ttk.Label(
            self.frame, text='Orientation')

        # Assign variables for tracing
        parent.track_vars.append(self.name)
        parent.track_vars.append(self.size)
        parent.track_vars.append(self.orientation)

        # Generate #########################
        self.dmcs = []
        for idx, dmc in enumerate(sheet.dmcs):
            self.dmcs.append(DisplayDmc(parent, self.frame, dmc, idx, self.uuid))
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
        if index >= len(self.tab_control.tabs()):
            self.tab_control.add(self.frame, text=f'{index}_{self.name.get()}')



    def destroy(self):
        self.tab_control.forget(self.frame)
        # self.frame.destroy()

class DisplayDmc():
    """ Graphical representation of DMC object. """

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
        self.quiet_zone_box['values'] = c.QUIET_ZONE
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
    """ Graphical representation of DmcPart object. """
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
        self.type_box['values'] = c.DMC_PART_TYPE

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
        if self.type.get() == c.DMC_PART_TYPE[0]:
            self.phrase_label.grid(column=1, row=index+1, sticky='nw')
            self.phrase_box.grid(column=1, row=index+2, sticky='nw')


        if self.type.get() == c.DMC_PART_TYPE[1]:
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















if __name__ == '__main__':
    pass
