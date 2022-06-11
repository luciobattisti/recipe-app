"""

"""
# __author__ = "Alessandro Lusci"

# Import dependencies
import sqlite3

from tkinter import *
from db.sqlite_helper.SQLiteHelper import SQLiteHelper
from helper.RecipeHelper import RecipeHelper
from pathlib import Path
import pint
import sys
import os

if getattr( sys, "frozen", False ) :
        # print("running in a bundle")
        # print(sys._MEIPASS)
        home = str(Path.home())
        DB = os.path.join(home, ".recipe-app", "db", "recipe.db")
else:
        # print("running live")
        DB = "./recipe.db"

# Global variables

ureg = pint.UnitRegistry()
units = {"tbs": ureg.tbs,
         "fl oz": ureg.floz,
         "gill": ureg.gill,
         "cup": ureg.cup,
         "pt": ureg.pt,
         "qt": ureg.qt,
         "gal": ureg.gal,
         "lb": ureg.lb,
         "oz": ureg.oz,
         "":None}
db_helper = SQLiteHelper(DB)
days = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


def main():
    # Init tkinter root
    root = Tk()
    root.title("Recipe App")
    root.resizable(False, False)

    # Init Recipe Helper
    helper = RecipeHelper(root, db_helper, days, units)
    helper.create_main_grid()
    helper.create_main_widgets({5: 12})
    helper.grid_main_widgets()

    # Execute mainloop
    helper.root.mainloop()

if __name__ == "__main__":
    main()
