# This file runs the application.


# Imports
import tkinter as tk
from gui.gui import GuiApp

import project.cfg as cfg

def main():
    """ Creates tkinter object and runs application. """
    
    # cfg.root = GuiApp()
    # cfg.root.mainloop()
    GuiApp().run()

# Main
if __name__ == '__main__':
    main()


