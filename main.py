from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
import random
from csv import DictWriter
import csv
import os

Builder.load_file('main.kv')

routine_name_list = []
workout_list = []

class ScreenManager(ScreenManager):

    # =================================================================================================================
    # Functions for Menu
    # =================================================================================================================
    def routine_grid(self):
        pass

    # =================================================================================================================
    # Functions for Routines
    # =================================================================================================================
    # to clear all previous entries in Add Routines
    def reset_add_routine(self):
        if self.save_button.text == 'Saved':            # Check to see if you saved the workout
            self.add_routine_grid.clear_widgets()       # Clears out the grid layout
            self.workout_name.text = ""                 # Clears out the routine name text box
            self.exercise_name.text = ""                # Clears out the exercise name text box
            self.num_sets.text = ""                     # Clears out the sets text box
            self.num_reps.text = ""                     # Clears out the reps text box
            self.amt_weight.text = ""                   # Clears out the weight text box
            self.save_button.text = str('Save')         # Changes the 'saved' button back to save
            routine_name_list.clear()                   # Empties the routine list to prepare for new data
            workout_list.clear()                        # Empties the workout list to prepare for new data

    # =================================================================================================================
    # Functions for AddRoutine
    # =================================================================================================================
    # To reset the data fields to get ready for new entries
    def reset_fields(self):

        # Resets all of the date fields to empty strings
        self.exercise_name.text = ""
        self.num_sets.text = ""
        self.num_reps.text = ""
        self.amt_weight.text = ""

    # To add the data to the gri
    def add_to_grid(self):

        # Sets all of the data to what the user inputted
        name_label = Label(text=self.exercise_name.text)
        sets_label = Label(text=self.num_sets.text)
        reps_label = Label(text=self.num_reps.text)
        weight_label = Label(text=self.amt_weight.text)

        # Checks to make sure there is a name and numbers of sets as input
        if self.exercise_name.text and self.num_sets.text != "":

            # Something new was add, changed back to save
            self.save_button.text = str('Save')

            # Increase the number of rows to allow space for new input
            self.add_routine_grid.rows += 1

            # Adds the input to the grid
            self.add_routine_grid.add_widget(name_label)        # Adds the name to the grid
            self.add_routine_grid.add_widget(sets_label)        # Adds the sets to the grid
            self.add_routine_grid.add_widget(reps_label)        # Adds the reps to the grid
            self.add_routine_grid.add_widget(weight_label)      # Adds the weight to the grid

            # Creates variables to store routine data
            name_text = self.exercise_name.text
            sets_text = self.num_sets.text
            reps_text = self.num_reps.text
            weight_text = self.amt_weight.text

            # Creates the data item for the excel sheet
            single_exercise = {'name': name_text, 'sets': sets_text, 'reps': reps_text, 'weight': weight_text}

            # Adds the data item to the list
            workout_list.append(single_exercise)

            # Calls the next step
            ScreenManager.reset_fields(self)

    def save_and_create(self):

        # Checks to make sure the routine name is not empty
        if self.workout_name.text != "":
            if workout_list != []:
                # Gets the name of the routine to be used as the button
                routine_name = self.workout_name.text

                # Adds the routine name and string to the list
                routine_name_list.append({'routine': routine_name, 'last_used': "You have not used this workout routine"})

                file_name = routine_name + '.csv'                                   # Creates the file name (as .csv file)
                for file in os.listdir("routines/"):                                # Looks through all saved routines
                    if file.endswith(".csv"):                                       # Makes sure its a .csv file
                        if file_name == file:                                       # If there are matching file names
                            print("You already have a routine named:", file_name)   # Tell the user they need a new name
                            return

                my_file = open("routines/" + file_name, 'w')        # Creates the file to store the routine

                # Dict headers to point to the data in the dict
                fieldnames = ['routine', 'last_used', 'name', 'sets', 'reps', 'weight']

                # Uses dictWriter to create a csv file with the data in its correct column
                writer = DictWriter(my_file, fieldnames=fieldnames, extrasaction='ignore', delimiter=',',
                                    lineterminator='\n')

                # Write titles
                writer.writer.writerow(['Routine Name', 'Last Used', 'Exercise Name', 'Sets', 'Reps', 'Weight'])
                writer.writerows(routine_name_list)     # First writes the routine name and last used date
                writer.writerows(workout_list)          # Then writes each workout
                my_file.close()                         # Closes file

                # Updates the Routines page with the new routine button
                ScreenManager.update_routines(self)

                self.save_button.text = str('Saved')    # Change button to 'saved'
                #self.add_routine_grid.rows = 0          # Resets the rows in the add_routine grid

    # Adds the button and 'last used' to the Routines page
    def update_routines(self):
        # button properties
        new_button = Button(text=self.workout_name.text, on_press=self.open_routine, id=self.workout_name.text)

        self.routine_grid.add_widget(new_button)                            # Creates/adds the button to Routines page
        last_used = Label(text="You have not used this workout routine")    # Creates the label with the last time used
        self.routine_grid.add_widget(last_used)                             # Adds the label to the Routines page

    def clear_all(self):
        self.add_routine_grid.clear_widgets()       # Clears out the grid layout
        self.add_routine_grid.rows = 0              # Resets the row count
        self.workout_name.text = ""                 # Clears out the routine name text box
        self.exercise_name.text = ""                # Clears out the exercise name text box
        self.num_sets.text = ""                     # Clears out the sets text box
        self.num_reps.text = ""                     # Clears out the reps text box
        self.amt_weight.text = ""                   # Clears out the weight text box
        self.save_button.text = str('Save')         # Changes the 'saved' button back to save
        routine_name_list.clear()                   # Empties the routine list to prepare for new data
        workout_list.clear()                        # Empties the workout list to prepare for new data

    def is_entries(self):
        if self.workout_name.text != "":
            if workout_list != []:
                return True
        return False

    # =================================================================================================================
    # Functions for Display Routine
    # =================================================================================================================
    # What will happen when pressing a routine
    def open_routine(self, instance):
        self.transition.direction = 'left'  # Changes the open direction to go left
        self.current = "DisplayRoutine"  # Which screen it will change to
        self.display_name.text = str(instance.id)  # Changes the label to the current routine
        filename = 'routines/' + instance.id + '.csv'

        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.display_grid.rows += 1
                if line_count == 0:
                    status_label = Label(text='Status')
                    self.display_grid.add_widget(status_label)
                    name_label = Label(text='Exercise Name')
                    self.display_grid.add_widget(name_label)
                    line_count += 1
                elif line_count == 1:
                    line_count += 1
                else:
                    my_button = Button(text="Not Completed",  color=[0.502, 0, 0, 1], background_color=[0.502, 0, 0, 1])
                    self.display_grid.add_widget(my_button)
                    name = row[2]
                    my_label = Label(text=name, color=[1, 1, 1, 1])
                    self.display_grid.add_widget(my_label)

    def reset_display(self):
        self.display_grid.clear_widgets()  # Clears out the grid layout
        self.display_grid.rows = 0

    # =================================================================================================================
    # Functions for Settings
    # =================================================================================================================
    # To display notifications on your device
    def notifications(self):
        pass

    # To auto increase the weight after completing the sets/reps goal
    def auto_increase_weight(self):
        pass

    # To display quotes when you do not reach your sets/reps goal
    def quotes(self):
        quote_list = ["What do you mean", "Not a problem", "She's not fat", "Why are you like this"]
        i = random.randint(0, len(quote_list) - 1)
        print(quote_list[i])

    # FIXME
    # To change colors of app between dark and light
    def color_mode(self):
        if self.dark_light.text == "Dark":
            self.change_color = (1.0, 0.0, 0.0, 1.0)
        if self.dark_light.text == "Light":
            self.change_color = (1.0, 1.0, 1.0, 1.0)


# =================================================================================================================
# Different Screen classes
# =================================================================================================================
class Menu(Screen):
    pass


class Routines(Screen):
    pass


class Setting(Screen):
    pass


class AddRoutine(Screen):
    pass


class DisplayRoutine(Screen):
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
