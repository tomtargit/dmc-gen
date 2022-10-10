from tkinter import *
from tkinter import ttk

# Constants
TRANSPARENT = '#010101'
PAD_X_Y = 10


# edit - sheet 
s_edit_sheet = ttk.Style()
s_edit_sheet.configure('EditSheet.TFrame', background='white', relief='groove', borderwidth=3)

# edit frame - dmc config
s_edit_dmc = ttk.Style()
s_edit_dmc.configure('EditDmc.TFrame', background='white', relief='flat', padidng=5, borderwidth=3)

# edit frame - dmc part
s_edit_dmc_part = ttk.Style()
s_edit_dmc_part.configure('EditDmcPart.TFrame', background='white', relief='flat', padding=5, borderwidth=1)

# sheet - label
s_sheet_label = ttk.Style()
s_sheet_label.configure('EditLabel.TLabel', background='white')

# sheet - combobox
s_sheet_combobox = ttk.Style()
s_sheet_combobox.theme_use('alt') # needed to enable of backgrounds color change
s_sheet_combobox.configure('EditCombobox.TCombobox', background='white', fieldbackground='white')

# sheet - entry
s_sheet_entry = ttk.Style()
s_sheet_entry.configure('EditEntry.TEntry', background='white')