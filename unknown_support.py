#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.2
#  in conjunction with Tcl version 8.6
#    Feb 06, 2022 11:44:12 AM IST  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import GUI

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = GUI.Toplevel1(_top1)
    root.mainloop()

if __name__ == '__main__':
    GUI.start_up()




