# This file runs the application.


# Imports
import tkinter as tk
from gui.gui import App

import project.cfg as cfg

def main():
    """ Creates tkinter object and runs application. """
    
    cfg.root = App()
    cfg.root.mainloop()

# Main
if __name__ == '__main__':
    main()


