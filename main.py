# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.lang import Builder
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# import random

Builder.load_file('main.kv')

# TODO list of dictionaries, containing the routine
routine_list = []

class Menu(Screen):
    pass


class Routines(Screen):
    def update_routines(self):
        for routine in routine_list:
            routine_button = Button(text=routine)
            self.routine_grid.add_widget(routine_button)

            print("added widget")


class Setting(Screen):
    pass


class AddRoutine(Screen):

    # Gets all of the data inputted by the user
    def get_vars(self):
        self.name = self.exercise_name.text
        self.sets = self.num_sets.text
        self.reps = self.num_reps.text
        self.weight = self.amt_weight.text

        #TODO remove prints, for testing
        print(self.name)
        print(self.sets)
        print(self.reps)
        print(self.weight)

        # Calls the next step
        AddRoutine.reset_fields(self)

    def reset_fields(self):

        # Resets all of the date fields to empty strings
        self.exercise_name.text = ""
        self.num_sets.text = ""
        self.num_reps.text = ""
        self.amt_weight.text = ""

        # Calls the next step
        AddRoutine.add_to_grid(self)

    def add_to_grid(self):

        # Sets all of the data to what the user inputted
        name_label = Label(text=self.name)
        sets_label = Label(text=self.sets)
        reps_label = Label(text=self.reps)
        weight_label = Label(text=self.weight)

        # Checks to make sure there is a name and numbers of sets as input
        if self.name and self.sets != "":
            self.add_routine_grid.add_widget(name_label)
            self.add_routine_grid.add_widget(sets_label)
            self.add_routine_grid.add_widget(reps_label)
            self.add_routine_grid.add_widget(weight_label)

        # TODO remove(TESTING ONLY)
        liftlist = ['curl', 'pushup', 'sit up', 'bench']
        for lifts in liftlist:
            name_label = Label(text=lifts)
            self.add_routine_grid.add_widget(name_label)
            sets_label = Label(text=str(random.randint(0, 4)))
            self.add_routine_grid.add_widget(sets_label)
            reps_label = Label(text=str(random.randint(8, 12)))
            self.add_routine_grid.add_widget(reps_label)
            weight_label = Label(text=str(random.randint(80, 120)))
            self.add_routine_grid.add_widget(weight_label)

    # TODO: Bug with adding to a different screen
    def save_and_create(self):
        # routine_button = Button(text=self.workout_name.text)
        routine_name = self.workout_name.text

        routine_list.append(routine_name)

        Routines.update_routines(self)





# Create the screen manager
sm = ScreenManager()
sm.add_widget(Menu(name='Menu'))
sm.add_widget(Routines(name='Routines'))
sm.add_widget(Setting(name='Setting'))
sm.add_widget(AddRoutine(name='AddRoutine'))


class TTLApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    TTLApp().run()
