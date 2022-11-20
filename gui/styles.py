from tkinter import *
from tkinter import ttk

# Constants
TRANSPARENT = '#010101'
PAD_X_Y = 10

# Style of 'sheet' frame in edit frame.
s_edit_sheet = ttk.Style()
s_edit_sheet.configure('EditSheet.TFrame', 
                       background='white', 
                       relief='groove', 
                       borderwidth=3)

# Style of 'dmc' frame in edit frame.
s_edit_dmc = ttk.Style()
s_edit_dmc.configure('EditDmc.TFrame', 
                     background='white', 
                     relief='groove', 
                     padidng=5, 
                     borderwidth=3)

# Style of 'dmc part' frame in edit frame.
s_edit_dmc_part = ttk.Style()
s_edit_dmc_part.configure('EditDmcPart.TFrame', 
                          background='white', 
                          relief='flat', 
                          padding=5, 
                          borderwidth=1)

# Style of 'label' widget used in edit frame.
s_sheet_label = ttk.Style()
s_sheet_label.configure('EditLabel.TLabel', 
                        background='white')

# Style of 'combobox' widget used in edit frame.
s_sheet_combobox = ttk.Style()
s_sheet_combobox.theme_use('alt') # needed to enable of backgrounds color change
s_sheet_combobox.configure('EditCombobox.TCombobox', 
                           background='white', 
                           fieldbackground='white')

# Style of 'entry' widget in edit frame.
s_sheet_entry = ttk.Style()
s_sheet_entry.configure('EditEntry.TEntry', 
                        background='white')


# Notebook - style for tab control.
s_notebook = ttk.Style()
s_notebook.configure('EditTabControl.TNotebook')#,
                  #   background='white')