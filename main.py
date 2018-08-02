from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
import random

Builder.load_file('main.kv')

# TODO list of dictionaries, containing the routine
routine_list = []


class ScreenManager(ScreenManager):

    # Gets all of the data inputted by the user
    def get_vars(self):
        self.name = self.exercise_name.text
        self.sets = self.num_sets.text
        self.reps = self.num_reps.text
        self.weight = self.amt_weight.text

        # TODO remove prints, for testing
        print(self.name)
        print(self.sets)
        print(self.reps)
        print(self.weight)

        # Calls the next step
        ScreenManager.reset_fields(self)

    # To reset the data fields to get ready for new entries
    def reset_fields(self):

        # Resets all of the date fields to empty strings
        self.exercise_name.text = ""
        self.num_sets.text = ""
        self.num_reps.text = ""
        self.amt_weight.text = ""

        # Calls the next step
        ScreenManager.add_to_grid(self)

    # To add the data to the gri
    def add_to_grid(self):

        # Sets all of the data to what the user inputted
        name_label = Label(text=self.name)
        sets_label = Label(text=self.sets)
        reps_label = Label(text=self.reps)
        weight_label = Label(text=self.weight)

        # Checks to make sure there is a name and numbers of sets as input
        if self.name and self.sets != "":

            # Something new was add, changed back to save
            self.save_button.text = str('Save')

            # Increase the number of rows to allow space for new input
            self.add_routine_grid.rows += 1

            # Adds the input to the grid
            self.add_routine_grid.add_widget(name_label)
            self.add_routine_grid.add_widget(sets_label)
            self.add_routine_grid.add_widget(reps_label)
            self.add_routine_grid.add_widget(weight_label)



    def save_and_create(self):
        # routine_button = Button(text=self.workout_name.text)
        routine_name = self.workout_name.text
        if routine_name != "":
            routine_list.append(({'routine': routine_name, 'last_used': "You have not used this workout routine"}))

            # routine_list.append({'last_used': ""})
            ScreenManager.update_routines(self)

            # Change button to 'saved'
            self.save_button.text = str('Saved')

    def update_routines(self):
        for data in routine_list:
            self.routine_grid.add_widget(Button(text=data["routine"]))
            last_used = Label(text=data["last_used"])
            self.routine_grid.add_widget(last_used)
            print("added widget")

    def quotes(self):
        quote_list = ["What do you mean", "Not a problem", "She's not fat", "Why are you like this"]
        i = random.randint(0, len(quote_list) - 1)
        print(quote_list[i])


class Menu(Screen):
    pass


class Routines(Screen):
    pass


class Setting(Screen):
    pass


class AddRoutine(Screen):
    pass


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
