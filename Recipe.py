"""

"""
# __author__ = "Alessandro Lusci"

# Import dependencies
import sqlite3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import random
from db.sqlite_helper.SQLiteHelper import SQLiteHelper
import pint
from collections import Counter
import _sysconfigdata_m_darwin_darwin

# Global variables
DB = "recipe.db"
ureg = pint.UnitRegistry()
units = {"tbs": ureg.tbs,
         "fl oz": ureg.floz,
         "gill": ureg.gill,
         "cup": ureg.cup,
         "pt": ureg.pt,
         "qt": ureg.qt,
         "gal": ureg.gal,
         "lb": ureg.lb,
         "oz": ureg.oz}
db_helper = SQLiteHelper(DB)
days = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

# Functions
flatten = lambda l: [item for sublist in l for item in sublist]


def most_common(lst):
    """
    Return most common element from list.
    :param lst: Input list
    :type list: `list`
    :return: Most common item in list
    """
    data = Counter(lst)
    return data.most_common(1)[0][0]


def get_ingredients():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM ingredient")
    rows = cur.fetchall()

    return rows


def add_ingredient_row(w, cur_ingredients, ingredients_name):
    ivar = StringVar()
    qvar = StringVar()
    uvar = StringVar()
    ivar.set("")
    qvar.set(0)
    uvar.set("")
    num_ingredients = len(cur_ingredients)
    row_id = cur_ingredients[num_ingredients-1]["row_id"] + 1

    imen = OptionMenu(w, ivar, *ingredients_name)
    imen.config(background="#ececec", width=25)
    qent = Entry(w, textvariable=qvar, width=5)
    qent.config(highlightthickness=0)
    umen = OptionMenu(w, uvar, *units.keys())
    umen.config(background="#ececec", width=10)

    ingredient_row = {
    "ivar":ivar,
    "qvar":qvar,
    "uvar":uvar,
    "row_id":row_id,
    "imen": imen,
    "qent": qent,
    "umen": umen}

    cur_ingredients.append(ingredient_row)

    imen.grid(column=0, row=row_id)
    qent.grid(column=1, row=row_id)
    umen.grid(column=2, row=row_id)


def remove_ingredient_row(w, cur_ingredients):
    num_ingredients = len(cur_ingredients)

    # Remove ingredients only there is more than 1.
    if num_ingredients > 1:
        row_id = cur_ingredients[num_ingredients-1]["row_id"]
        # Destroy widgets
        imen = cur_ingredients[num_ingredients-1]["imen"]
        imen.destroy()
        qent = cur_ingredients[num_ingredients-1]["qent"]
        qent.destroy()
        umen = cur_ingredients[num_ingredients-1]["umen"]
        umen.destroy()
        # Remove ingredient from list
        cur_ingredients.pop()


def save_recipe(w, recipe_name, cur_ingredients, main_recipe_names):
    """

    :param recipe_name:
    :param cur_ingredients:
    :return:
    """
    recipe_name = recipe_name.get()
    ingredients = []
    for ingredient in cur_ingredients:
        name = ingredient["ivar"].get()
        quantity = ingredient["qvar"].get()
        unit = ingredient["uvar"].get()
        ingredients.append({"name": name, "quantity": quantity, "unit": unit})

    success = db_helper.add_recipe(recipe_name, ingredients)

    if success:
        messagebox.showinfo("Add Recipe", "Recipe {} added successfully".format(recipe_name))
        w.destroy()
        main_recipe_names.set(sorted([x[0] for x in db_helper.get_recipes()]))
    else:
        messagebox.showerror("Add Recipe", "Something went wrong when adding recipe {}".format(recipe_name))


def add_recipe(root, recipe_names, lbox):
    # Init
    w = Toplevel(root)
    w.title("Add recipe")
    w.resizable(False, False)
    w.configure(background="#ececec")
    ingredients = get_ingredients()
    ingredients_name = sorted([x[1] for x in ingredients])

    # Create widgets
    nlbl = Label(w, text="Recipe Name")
    nlbl.configure(background="#ececec")
    ilbl = Label(w, text="Ingredient")
    ilbl.configure(background="#ececec")
    qlbl = Label(w, text="Quantity")
    qlbl.configure(background="#ececec")
    ulbl = Label(w, text="Unit")
    ulbl.configure(background="#ececec")

    nvar = StringVar()
    nvar.set("")
    nent = Entry(w, textvariable=nvar, width=25)
    nent.configure(highlightthickness=0)

    ivar = StringVar()
    qvar = StringVar()
    uvar = StringVar()
    ivar.set("")
    qvar.set(0)
    uvar.set("")
    row_id = 3

    imen = OptionMenu(w, ivar, *ingredients_name)
    imen.config(background="#ececec", width=25)
    qent = Entry(w, textvariable=qvar, width=5)
    qent.config(highlightthickness=0)
    umen = OptionMenu(w, uvar, *units.keys())
    umen.config(width=10)
    umen.config(background="#ececec")

    ingredient_row = {
    "ivar":ivar,
    "qvar":qvar,
    "uvar":uvar,
    "row_id":row_id,
    "imen": imen,
    "qent": qent,
    "umen": umen }

    curr_ingredients = [ingredient_row]
    sbutton = ttk.Button(w, text="Save Recipe",
                     command=lambda: save_recipe(w, nvar, curr_ingredients, recipe_names), width=15)
    abutton = ttk.Button(w, text="Add Ingredient",
                     command=lambda: add_ingredient_row(w, curr_ingredients, ingredients_name), width=11)
    rbutton = ttk.Button(w, text="Remove Ingredient",
                     command=lambda: remove_ingredient_row(w, curr_ingredients), width=15)

    # Grid widgets
    nlbl.grid(column=0, row=0)
    sbutton.grid(column=2, row=0)
    nent.grid(column=0, row=1)
    abutton.grid(column=1, row=1)
    rbutton.grid(column=2, row=1)
    ilbl.grid(column=0, row=2)
    qlbl.grid(column=1, row=2)
    ulbl.grid(column=2, row=2)

    imen.grid(column=0, row=row_id)
    qent.grid(column=1, row=row_id)
    umen.grid(column=2, row=row_id)

    # Colorize alternating lines of the listbox
    # recipes = [x[0] for x in db_helper.get_recipes()]
    # for i in range(0, len(recipes), 2):
    #   print("color")
    #   lbox.itemconfigure(i, background="#f0f0ff")


def get_sequence(days):
    recipes = [x[0] for x in db_helper.get_recipes()]
    num_recipes = len(recipes)
    sequence = random.sample(range(num_recipes), num_recipes)
    recipe_sequence = [recipes[sequence[d]] for d in range(len(days))]

    return recipe_sequence


def schedule(recipes, day_to_recipe, days):
    recipe_sequence = get_sequence(days)
    recipe_schedule = dict(zip(days, recipe_sequence))

    for day in days:
        day_to_recipe[day].set(recipe_schedule[day])
        day_to_recipe[day].set(recipe_schedule[day])
        day_to_recipe[day].set(recipe_schedule[day])

    messagebox.showinfo("Schedule Update", "Recipe schedule has been updated successfully")


def onselect_recipe(evt, set_day, day_to_recipe):
    w = evt.widget
    index = int(w.curselection()[0])
    new_recipe = w.get(index)
    day_to_recipe[set_day.get()].set(new_recipe)


def save_shopping_list(_day_to_recipe, checked_days):
    ingredients = []
    day_to_recipe = dict([(k,v) for k,v in _day_to_recipe.items() if checked_days[k].get() == 1])

    for (day, recipe_var) in day_to_recipe.items():
        recipe_name = recipe_var.get()
        ingredients.append(db_helper.get_recipe_ingredients(recipe_name))

    ingredients = flatten(ingredients)

    ingredient_to_unit = {}
    for ingredient in ingredients:
        if ingredient["name"] not in ingredient_to_unit:
            ingredient_to_unit[ingredient["name"]] = [ingredient["unit"]]
        else:
            ingredient_to_unit[ingredient["name"]].append(ingredient["unit"])
    for name in ingredient_to_unit.keys():
        ingredient_to_unit[name] = most_common(ingredient_to_unit[name])

    ingredient_to_quantity = {}
    for ingredient in ingredients:
        if ingredient["name"] not in ingredient_to_quantity:
            ingredient_to_quantity[ingredient["name"]] = ingredient["quantity"]*units[ingredient["unit"]]
        else:
            ingredient_to_quantity[ingredient["name"]] += ingredient["quantity"]*units[ingredient["unit"]]

    data = "Day,Recipe, \n"
    for k, v in day_to_recipe.items():
        data += "%s,%s\n" % (k, v.get())
    data += ",\n"
    data += "Ingredient,Quantity\n"
    for k, v in ingredient_to_quantity.items():
        data += "%s,%.2f %s\n" % (k, v.m_as(ingredient_to_unit[k]), ingredient_to_unit[k])

    f = filedialog.asksaveasfile(mode="w", defaultextension=".csv")
    if f is None:
        return
    f.write(data)
    f.close()


def main():
    # Init tkinter root
    root = Tk()
    root.title("Recipe App")
    root.resizable(False, False)

    # Init set_day and checked_days variables
    set_day = StringVar()
    set_day.set("mon")
    checked_days = dict([(day, IntVar(value=1)) for day in days])

    # Get recipes from db
    recipes = sorted([x[0] for x in db_helper.get_recipes()])
    recipe_names = StringVar(value=recipes)
    # Init day_to_recipe
    day_to_recipe = {"mon": StringVar(), "tue": StringVar(), "wed": StringVar(),
                     "thu": StringVar(), "fri": StringVar(), "sat": StringVar(),
                     "sun": StringVar()}

    # Get initial schedule
    recipe_sequence = get_sequence(days)[:len(days)]
    recipe_schedule = dict(zip(days, recipe_sequence))

    # Create grid
    c = ttk.Frame(root, padding=(5, 5, 12, 0))
    c.grid(column=0, row=0, sticky=(N, W, E, S))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Create widgets
    lbox = Listbox(c, listvariable=recipe_names, height=7)
    lbox.bind("<<ListboxSelect>>", lambda evt: onselect_recipe(evt, set_day, day_to_recipe))
    lday = {}
    rday = {}
    cday = {}
    for day in days:
        lday[day] = [ttk.Label(c, text=(day + ":").title()),
                     ttk.Label(c, textvariable=day_to_recipe[day])]
        day_to_recipe[day].set(recipe_schedule[day])
        rday[day] = ttk.Radiobutton(c, text="", variable=set_day, value=day)
        cday[day] = ttk.Checkbutton(c, text="", variable=checked_days[day])
    abutton = ttk.Button(c, text="Add recipe", command=lambda: add_recipe(root, recipe_names, lbox), width=10)
    sbutton = ttk.Button(c, text="Schedule", command=lambda: schedule(recipes, day_to_recipe, days), width=10)
    vbutton = ttk.Button(c, text="Save", command=lambda: save_shopping_list(day_to_recipe, checked_days), width=10)

    # Grid widgets
    lbox.grid(column=0, row=0, rowspan=7, sticky=(N, S, E, W))
    row = 0
    for day in days:
        if day == "mon":
            lday[day][0].grid(column=1, row=row, padx=5, sticky=(N, W))
            lday[day][1].grid(column=2, row=row, padx=5, sticky=(N, W))
            rday[day].grid(column=3, row=row, sticky=(N))
            cday[day].grid(column=4, row=row, sticky=(N))
        else:
            lday[day][0].grid(column=1, row=row, padx=5, sticky=(W))
            lday[day][1].grid(column=2, row=row, padx=5, sticky=(W))
            rday[day].grid(column=3, row=row)
            cday[day].grid(column=4, row=row)
        row += 1
    abutton.grid(column=5, row=0, padx=5, sticky=(W))
    sbutton.grid(column=5, row=1, padx=5, sticky=(W))
    vbutton.grid(column=5, row=2, padx=5, sticky=(W))

    # Colorize alternating lines of the listbox
    # for i in range(0,len(recipes),2):
    #    lbox.itemconfigure(i, background="#f0f0ff")

    root.mainloop()

if __name__ == "__main__":
    main()