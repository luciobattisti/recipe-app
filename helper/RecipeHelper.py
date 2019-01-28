from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from collections import Counter
import random

# Functions
flatten = lambda l: [item for sublist in l for item in sublist]


class RecipeHelper:

    def __init__(self, root, db_helper, days, units):
        """

        :param root:
        :param db_helper:
        :param days:
        :param units:
        """

        # Init simple variables
        self.root = root
        self.db_helper = db_helper
        self.days = days
        self.units = units

        # Init set_day and checked_days variables
        set_day = StringVar()
        set_day.set("mon")
        self.set_day = set_day
        self.checked_days = dict([(day, IntVar(value=1)) for day in days])

        # Get recipes from db
        recipes = sorted([x[0] for x in db_helper.get_recipes()])
        recipe_var = StringVar(value=recipes)
        self.recipes = recipes
        self.recipe_var = recipe_var

        # Init day_to_recipe
        day_to_recipe = {"mon": StringVar(), "tue": StringVar(), "wed": StringVar(),
                         "thu": StringVar(), "fri": StringVar(), "sat": StringVar(),
                         "sun": StringVar()}
        self.day_to_recipe = day_to_recipe

        # Create initial schedule
        self.create_recipe_schedule()

        # Init ingredients list
        ingredients = self.db_helper.get_all_ingredients()
        self.ingredients_name = sorted([x[1] for x in ingredients])

    def create_recipe_schedule(self):
        """
        Generate recipe schedule for a full week and save
        corresponding variable.

        :return:
        """

        recipes = [x[0] for x in self.db_helper.get_recipes()]
        num_recipes = len(recipes)
        sequence = random.sample(range(num_recipes), num_recipes)
        recipe_sequence = [recipes[sequence[d]] for d in range(len(self.days))]
        recipe_sequence[:len(self.days)]

        self.recipe_schedule = dict(zip(self.days, recipe_sequence))

    def onselect_recipe(self, evt):
        """
        Set current day to selected recipe.

        :param evt: Event
        :type: ``tkinter.Event``
        :return:
        """
        w = evt.widget
        index = int(w.curselection()[0])
        new_recipe = w.get(index)
        self.day_to_recipe[self.set_day.get()].set(new_recipe)

    def create_main_grid(self):
        """
        Create main grid.
        c stands for canvas and it will be used throughout the class.

        :return:
        """
        c = ttk.Frame(self.root, padding=(5, 5, 12, 0))
        c.grid(column=0, row=0, sticky=(N, W, E, S))
        self.c = c
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def create_main_widgets(self, col_width):
        """
        Create widgets for main canvas.
        lbox stands for list of recipes box.
        lday stands for list of days.
        rday stands for radio days (days are selected via radio buttons)
        cday stands for checked days (checked days are dumped into the final recipe list)

        :return:
        """

        # Create widgets
        lbox = Listbox(self.c, listvariable=self.recipe_var, height=7)
        lbox.bind("<<ListboxSelect>>", lambda evt: self.onselect_recipe(evt))
        lday = {}
        rday = {}
        cday = {}
        for day in self.days:
            lday[day] = [ttk.Label(self.c, text=(day + ":").title()),
                         ttk.Label(self.c, textvariable=self.day_to_recipe[day])]
            self.day_to_recipe[day].set(self.recipe_schedule[day])
            rday[day] = ttk.Radiobutton(self.c, text="", variable=self.set_day, value=day)
            cday[day] = ttk.Checkbutton(self.c, text="", variable=self.checked_days[day])
        self.lbox = lbox
        self.lday = lday
        self.rday = rday
        self.cday = cday
        self.abutton = ttk.Button(self.c, text="Add recipe", command=lambda: self.add_recipe(), width=col_width[5])
        self.sbutton = ttk.Button(self.c, text="New Schedule", command=lambda: self.schedule(), width=col_width[5])
        self.ebutton = ttk.Button(self.c, text="Edit recipe", command=lambda: self.edit_recipe(), width=col_width[5])
        self.vbutton = ttk.Button(self.c, text="Save", command=lambda: self.save_shopping_list(), width=col_width[5])

    def grid_main_widgets(self):
        """
        Grid main widgets
        :return:
        """

        self.lbox.grid(column=0, row=0, rowspan=7, sticky=(N, S, E, W))
        row = 0
        for day in self.days:
            if day == "mon":
                self.lday[day][0].grid(column=1, row=row, padx=5, sticky=(N, W))
                self.lday[day][1].grid(column=2, row=row, padx=5, sticky=(N, W))
                self.rday[day].grid(column=3, row=row, sticky=(N))
                self.cday[day].grid(column=4, row=row, sticky=(N))
            else:
                self.lday[day][0].grid(column=1, row=row, padx=5, sticky=(W))
                self.lday[day][1].grid(column=2, row=row, padx=5, sticky=(W))
                self.rday[day].grid(column=3, row=row)
                self.cday[day].grid(column=4, row=row)
            row += 1
        self.abutton.grid(column=5, row=0, padx=5, sticky=(W))
        self.sbutton.grid(column=5, row=1, padx=5, sticky=(W))
        self.ebutton.grid(column=5, row=2, padx=5, sticky=(W))
        self.vbutton.grid(column=5, row=3, padx=5, sticky=(W))

        # Colorize alternating lines of the listbox
        for i in range(0,len(self.recipes),2):
            self.lbox.itemconfigure(i, background="#f0f0ff")

    def create_labels_for_recipe_widgets(self, w):
        """
        Create labels for recipe widgets.

        :param w: Widget root
        :type w: ``tkinter.Tk``
        :returns: list of Label objects
        :rtype: ``list``
        """

        nlbl = Label(w, text="Recipe Name")
        nlbl.configure(background="#ececec")
        ilbl = Label(w, text="Ingredient")
        ilbl.configure(background="#ececec")
        qlbl = Label(w, text="Quantity")
        qlbl.configure(background="#ececec")
        ulbl = Label(w, text="Unit")
        ulbl.configure(background="#ececec")

        return nlbl, ilbl, qlbl, ulbl

    def create_ingredient_row(self, w, row_id, name="", quantity=0, unit=""):
        """
        Create ingredient row.

        :param w: Widget root
        :type: ``tkinter.Tk``
        :param name: Ingredient's name
        :type: ``srt``
        :param quantity: Ingredient's quantity
        :type: ``float``
        :param unit: Ingredient's unit
        :type: ``str``
        :param row_id: Row id
        :type: ``int``
        :returns: Dictionary of ingredient
        :rtype: ``dict``
        """

        ivar = StringVar()
        qvar = StringVar()
        uvar = StringVar()
        ivar.set(name)
        qvar.set(quantity)
        uvar.set(unit)
        row_id = row_id

        imen = OptionMenu(w, ivar, *self.ingredients_name)
        imen.config(background="#ececec", width=25)
        qent = Entry(w, textvariable=qvar, width=5)
        qent.config(highlightthickness=0)
        umen = OptionMenu(w, uvar, *self.units.keys())
        umen.config(width=10)
        umen.config(background="#ececec")

        ingredient_row = {
            "ivar": ivar,
            "qvar": qvar,
            "uvar": uvar,
            "row_id": row_id,
            "imen": imen,
            "qent": qent,
            "umen": umen}

        return ingredient_row

    def grid_ingredient_row(ingredient_row):
        """
        Grid ingredient row.

        :param ingredient_row: Dictionary of ingredient
        :type: ``dict``
        :return:
        """

        ingredient_row["imen"].grid(column=0, row=ingredient_row["row_id"])
        ingredient_row["qent"].grid(column=1, row=ingredient_row["row_id"])
        ingredient_row["umen"].grid(column=2, row=ingredient_row["row_id"])

    def add_recipe(self):
        """
        Create Add Recipe widget.

        :return:
        """

        # Init
        w = Toplevel(self.root)
        w.title("Add recipe")
        w.resizable(False, False)
        w.configure(background="#ececec")

        # Create widgets
        nlbl, ilbl, qlbl, ulbl = self.create_labels_for_recipe_widgets(w)

        nvar = StringVar()
        nvar.set("")
        nent = Entry(w, textvariable=nvar, width=25)
        nent.configure(highlightthickness=0)

        # Starting ingredient row is 3 because there are 3 rows on top
        ingredient_row = self.create_ingredient_row(w, 3)
        curr_ingredients = [ingredient_row]

        sbutton = ttk.Button(w, text="Save Recipe",
                             command=lambda: self.save_recipe(w, nvar, curr_ingredients), width=15)
        abutton = ttk.Button(w, text="Add Ingredient",
                             command=lambda: self.add_ingredient_row(w, curr_ingredients), width=11)
        rbutton = ttk.Button(w, text="Remove Ingredient",
                             command=lambda: RecipeHelper.remove_ingredient_row(curr_ingredients), width=15)

        # Grid widgets
        nlbl.grid(column=0, row=0)
        sbutton.grid(column=2, row=0)
        nent.grid(column=0, row=1)
        abutton.grid(column=1, row=1)
        rbutton.grid(column=2, row=1)
        ilbl.grid(column=0, row=2)
        qlbl.grid(column=1, row=2)
        ulbl.grid(column=2, row=2)
        RecipeHelper.grid_ingredient_row(ingredient_row)

    def save_recipe(self, w, nvar, curr_ingredients, delete_recipe=False):
        """
        Save recipe to db

        :param w: Widget root
        :type: ``tkinter.Tk``
        :param nvar: Variable storing recipe name
        :type: ``tkinter.StringVar``
        :param curr_ingredients: Stack of current ingredients
        :type: ``list``
        :param: delete_recipe: Delete recipe from db
        :type: ``bool``
        :return:
        """

        recipe_name = nvar.get()
        ingredients = [dict(name=ingredient["ivar"].get(), quantity=ingredient["qvar"].get(), unit=ingredient["uvar"].get()) for ingredient in curr_ingredients]

        if delete_recipe:
            self.db_helper.delete_recipe(recipe_name)

        success = False
        if recipe_name is not None and recipe_name != "":
            success = self.db_helper.add_recipe(recipe_name.lower(), ingredients)

        if success:
            messagebox.showinfo("Add Recipe", "Recipe {} added successfully".format(recipe_name))
            w.destroy()
            updated_list = sorted([x[0] for x in self.db_helper.get_recipes()])
            self.recipes = updated_list
            self.recipe_var.set(updated_list)
        else:
            messagebox.showerror("Add Recipe", "Something went wrong when adding recipe {}".format(recipe_name))

    def add_ingredient_row(self, w, curr_ingredients):
        """
        Add ingredient row.

        :param w: Widget root
        :rtype: ``tkinter.Tk``
        :param curr_ingredients: Stack of ingredients
        :rtype: ``list``
        :return:
        """

        # Increment row_id and create ingredient row
        row_id = curr_ingredients[-1]["row_id"] + 1
        ingredient_row = self.create_ingredient_row(w, row_id)

        # Grid ingredient row
        RecipeHelper.grid_ingredient_row(ingredient_row)

        # Add newly created ingredient row
        curr_ingredients.append(ingredient_row)

    def remove_ingredient_row(curr_ingredients, min_threshold=1):
        """
        Remove ingredient row.

        :param curr_ingredients: Stack of ingredients
        :rtype: ``list``
        :param min_threshold: minimun number of ingredients to perform removal
        :type: ``int``
        :return:
        """

        num_ingredients = len(curr_ingredients)

        if num_ingredients > min_threshold:
            curr_ingredients[num_ingredients-1]["imen"].destroy()
            curr_ingredients[num_ingredients-1]["qent"].destroy()
            curr_ingredients[num_ingredients-1]["umen"].destroy()

            curr_ingredients.pop()

    def schedule(self):
        """
        Create new schedule.

        :return:
        """

        self.create_recipe_schedule()

        for day in self.days:
            self.day_to_recipe[day].set(self.recipe_schedule[day])
            self.day_to_recipe[day].set(self.recipe_schedule[day])
            self.day_to_recipe[day].set(self.recipe_schedule[day])

        messagebox.showinfo("Schedule Update", "Recipe schedule has been updated successfully")

    def edit_recipe(self):
        """
        Create Add Recipe widget.

        :return:
        """

        # Init
        w = Toplevel(self.root)
        w.title("Edit recipe")
        w.resizable(False, False)
        w.configure(background="#ececec")

        # Create widgets
        nlbl, ilbl, qlbl, ulbl = self.create_labels_for_recipe_widgets(w)

        ingredient_row = self.create_ingredient_row(w, 3)
        curr_ingredients = [ingredient_row]

        rvar = StringVar()
        rmen = OptionMenu(w, rvar, *self.recipes, command=lambda name: self.add_recipe_ingredients(w, name, curr_ingredients))
        rmen.config(background="#ececec", width=25)

        dbutton = ttk.Button(w, text="Remove Recipe",
                             command=lambda: self.delete_recipe(w, rvar), width=15)
        sbutton = ttk.Button(w, text="Save Recipe",
                             command=lambda: self.save_recipe(w, rvar, curr_ingredients, delete_recipe=True), width=15)
        abutton = ttk.Button(w, text="Add Ingredient",
                             command=lambda: self.add_ingredient_row(w, curr_ingredients), width=15)
        rbutton = ttk.Button(w, text="Remove Ingredient",
                             command=lambda: RecipeHelper.remove_ingredient_row(curr_ingredients), width=15)

        # Grid widgets
        nlbl.grid(column=0, row=0)
        rmen.grid(column=0, row=1)
        ilbl.grid(column=0, row=2)

        abutton.grid(column=1, row=1)
        qlbl.grid(column=1, row=2)

        dbutton.grid(column=1, row=0)
        sbutton.grid(column=2, row=0)
        rbutton.grid(column=2, row=1)
        ulbl.grid(column=2, row=2)

        RecipeHelper.grid_ingredient_row(ingredient_row)

    def add_recipe_ingredients(self, w, recipe_name, curr_ingredients):

        # Empty curr_ingredients stack
        for row_ingredient in curr_ingredients:
            RecipeHelper.remove_ingredient_row(curr_ingredients, min_threshold=0)

        # Get recipe ingredients and init row_id
        ingredients = self.db_helper.get_recipe_ingredients(recipe_name)
        row_id = 2

        for ingr in ingredients:

             # Incremenent row_id and create ingredient_row
             row_id += 1
             ingredient_row = self.create_ingredient_row(w, row_id, name=ingr["name"], quantity=ingr["quantity"], unit=ingr["unit"])

             # Grid ingredient row
             RecipeHelper.grid_ingredient_row(ingredient_row)

             # Add newly created ingredient row
             curr_ingredients.append(ingredient_row)

    def delete_recipe(self, w, nvar):
        """
        Delete recipe from database

        :param w: Widget root
        :type: ``tkinter.Tk``
        :param nvar: Variable storing recipe name
        :type: ``tkinter.StringVar``
        :return:
        """

        result = messagebox.askquestion("Delete Recipe", "Are You Sure?", icon='warning')
        if result:
            # Remove recipe from db
            recipe_name = nvar.get()
            self.db_helper.delete_recipe(recipe_name)
            # Destroy widget
            w.destroy()
            # Update recipes
            updated_list = sorted([x[0] for x in self.db_helper.get_recipes()])
            self.recipes = updated_list
            self.recipe_var.set(updated_list)

    def save_shopping_list(self):

        """
        Save Shopping List.

        :return:
        """

        ingredients = []
        day_to_recipe = dict([(k, v) for k, v in self.day_to_recipe.items() if self.checked_days[k].get() == 1])

        for (day, recipe_var) in day_to_recipe.items():
            recipe_name = recipe_var.get()
            ingredients.append(self.db_helper.get_recipe_ingredients(recipe_name))

        ingredients = flatten(ingredients)

        ingredient_to_unit = {}
        for ingredient in ingredients:
            if ingredient["name"] not in ingredient_to_unit and ingredient["unit"]:
                ingredient_to_unit[ingredient["name"]] = [ingredient["unit"]]
            elif ingredient["unit"]:
                ingredient_to_unit[ingredient["name"]].append(ingredient["unit"])
        for name in ingredient_to_unit.keys():
            ingredient_to_unit[name] = RecipeHelper.most_common(ingredient_to_unit[name])

        ingredient_to_quantity = {}
        ingredient_to_count = {}
        for ingredient in ingredients:
            if ingredient["name"] not in ingredient_to_quantity and ingredient["unit"]:
                ingredient_to_quantity[ingredient["name"]] = ingredient["quantity"] * self.units[ingredient["unit"]]
            elif ingredient["unit"]:
                ingredient_to_quantity[ingredient["name"]] += ingredient["quantity"] * self.units[ingredient["unit"]]

        for ingredient in ingredients:
            if ingredient["name"] not in ingredient_to_count and not ingredient["unit"]:
                ingredient_to_count[ingredient["name"]] = ingredient["quantity"]
            elif not ingredient["unit"]:
                ingredient_to_count[ingredient["name"]] += ingredient["quantity"]

        ingredient_to_all = {**ingredient_to_quantity, **ingredient_to_count}

        data = "Day,Recipe, \n"
        for k, v in day_to_recipe.items():
            data += "%s,%s\n" % (k, v.get())
        data += ",\n"

        data += "Ingredient,Quantity\n"
        for k, _ in ingredient_to_all.items():
            try:
                q = ingredient_to_quantity[k]
            except KeyError:
                pass

            try:
                c = ingredient_to_count[k]
            except KeyError:
                pass

            if k not in ingredient_to_count and k in ingredient_to_quantity:
                data += "%s,%.2f %s\n" % (k, q.m_as(ingredient_to_unit[k]), ingredient_to_unit[k])
            elif k in ingredient_to_count and k not in ingredient_to_quantity:
                data += "%s,%d items\n" % (k, c)
            elif k in ingredient_to_count and k in ingredient_to_quantity:
                data += "%s,%.2f %s and %d items\n" % (k, q.m_as(ingredient_to_unit[k]), ingredient_to_unit[k], c)

        f = filedialog.asksaveasfile(mode="w", defaultextension=".csv")
        if f is None:
            return
        f.write(data)
        f.close()

    def most_common(lst):
        """
        Return most common element from list.
        :param lst: Input list
        :type list: `list`
        :return: Most common item in list
        """
        data = Counter(lst)

        return data.most_common(1)[0][0]
