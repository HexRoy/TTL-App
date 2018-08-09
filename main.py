from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
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
    def display_all_routines(self):

        for file in os.listdir("routines/"):            # Looks through all saved routines
            if file.endswith(".csv"):                   # Makes sure its a .csv file
                current_row = 0
                newest_row = self.get_newest_line(file)
                # Loops to obtain data from the file
                with open('routines/' + file) as csv_file:  # Opens the file to read
                    csv_reader = csv.reader(csv_file, delimiter=',')  # Starts the csv reader
                    for row in csv_reader:
                        current_row += 1  # Increments once for each new row it loops through
                        if current_row != newest_row:  # Checks to see if you are not on the newest like
                            pass  # If your not, do nothing
                        else:  # If you are, add all the data
                            # Creates label that shows when the routine was last used
                            last_used = Label(text=row[1])  # Creates the label with the last time used
                            # Creates a button for the routines menu
                            new_button = Button(text=row[0], on_press=self.open_routine, id=row[0])

                            # Add the routine button and last used label to the Routines screen
                            self.routine_grid.add_widget(new_button)  # Creates/adds the button to Routines page
                            self.routine_grid.add_widget(last_used)  # Adds the label to the Routines page

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

    def clear_routines(self):
        self.routine_grid.clear_widgets()

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
        name_label = Label(text=self.exercise_name.text)        # Creates label with newest exercise name inputted
        sets_label = Label(text=self.num_sets.text)             # Creates label with newest number of sets inputted
        reps_label = Label(text=self.num_reps.text)             # Creates label with newest number of reps inputted
        weight_label = Label(text=self.amt_weight.text)         # Creates label with newest amount of weight inputted

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
            name_text = self.exercise_name.text                 # Stores the name of the exercise
            sets_text = self.num_sets.text                      # Stores the amount of sets
            reps_text = self.num_reps.text                      # Stores the amount of reps
            weight_text = self.amt_weight.text                  # Stores the amount of weight

            # Appends all the exercise info to the list (order important)
            workout_list.append(name_text)                      # Adds exercise name to list
            workout_list.append(sets_text)                      # Adds the number of sets to the list
            workout_list.append(reps_text)                      # Adds the number of reps to the list
            workout_list.append(weight_text)                    # Adds the amount of weight to the list

            # Calls the next step
            ScreenManager.reset_fields(self)

    def save_and_create(self):

        # Checks to make sure the routine name is not empty
        if self.workout_name.text != "":
            if workout_list:

                # Gets the name of the routine to be used as the button
                routine_name = self.workout_name.text

                # Creates list containing entire routine
                routine_name_list.append(routine_name)              # First entry is always the routine name
                routine_name_list.append('Not Used')                # Second entry is always the last used date
                routine_name_list.extend(workout_list)              # The rest is each exercise, set, rep, weight

                file_name = routine_name + '.csv'                   # Creates the file name (as .csv file)
                my_file = open("routines/" + file_name, 'w')        # Creates the file to store the routine

                # Dict headers to point to the data in the dict
                fieldnames = ['routine', 'last_used', 'name', 'sets', 'reps', 'weight']

                # Uses dictWriter to create a csv file with the data in its correct column
                writer = DictWriter(my_file, fieldnames=fieldnames, extrasaction='ignore', delimiter=',',
                                    lineterminator='\n')

                # Creates all of the titles for the .csv file
                csv_titles = ['Routine Name', 'Last Used']   # The first two titles will always be this
                number_exercises = int(len(workout_list)/4)  # Gets number of exercise names (not everything in list /4)
                for i in range(number_exercises):            # Loops through each one and adds titles for each
                    csv_titles.append('Exercise Name')       # Exercise Name title
                    csv_titles.append('Sets')                # Sets title
                    csv_titles.append('Reps')                # Reps title
                    csv_titles.append('Weight')              # Weight title

                # Dict writer writes to the file
                writer.writer.writerow(csv_titles)           # Writes the titles across the top row of csv file
                writer.writer.writerow(routine_name_list)    # Writes the routine underneath the titles
                my_file.close()                              # Closes file

                # Updates the Routines page and adds the new routine button to the page
                ScreenManager.update_routines(self)

                self.save_button.text = str('Saved')    # Change button to 'saved'

                # Resets the add_routine page so its ready for a new entry
                self.add_routine_grid.clear_widgets()   # Clears out the grid layout
                self.add_routine_grid.rows = 0          # Resets the rows in the add_routine grid

                # Changes screen to Routines
                self.transition.direction = 'right'     # Sets the transition direction
                self.current = "Routines"               # Which screen to change to

    # Adds the button and 'last used' to the Routines page
    def update_routines(self):
        # button properties
        new_button = Button(text=self.workout_name.text, on_press=self.open_routine, id=self.workout_name.text)

        # Add the routine button and last used label to the Routines screen
        self.routine_grid.add_widget(new_button)    # Creates/adds the button to Routines page
        last_used = Label(text="Not Used")          # Creates the label with the last time used
        self.routine_grid.add_widget(last_used)     # Adds the label to the Routines page

    # Clears out all of the entries to the Add Routine page
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

    # Checks to see if the filename of the .csv file is unique and does not conflict with an existing file
    def is_unique(self):
        if self.workout_name.text != "":                        # If there is a routine name entered
            if workout_list:                                    # And if there are entries to the workout list
                routine_name = self.workout_name.text           # Gets the name of the routine to be used as the button
                file_name = routine_name + '.csv'               # Creates the file name (as .csv file)
                for file in os.listdir("routines/"):            # Looks through all saved routines
                    if file.endswith(".csv"):                   # Makes sure its a .csv file
                        if file_name == file:                   # If there are matching file names
                            print("You already have a routine named:", file_name)  # Tell the user they need a new name
                            routine_name_list.clear()           # Clears the list for new data
                            return False                        # Not unique do not save
        # FIXME: Figure out where to put this.. in second, or third if
        return True                                             # It is unique, continue

    # =================================================================================================================
    # Functions for Display Routine
    # =================================================================================================================
    # What will happen when pressing a routine
    def open_routine(self, instance):
        # Changes screens to Display Routine
        self.transition.direction = 'left'                  # Changes the open direction to go left
        self.current = "DisplayRoutine"                     # Which screen it will change to

        self.display_name.text = str(instance.id)           # Changes the label to the current routine

        file_name = 'routines/' + instance.id + '.csv'      # Creates the full file name with extension

        self.display_grid.rows += 1  # Adds a row in the grid for the exercise

        # Creates titles for the Display Routine Page
        status_label = Label(text='Status')         # Creates status label
        self.display_grid.add_widget(status_label)  # Adds label to the grid
        name_label = Label(text='Exercise Name')    # Creates exercise name label
        self.display_grid.add_widget(name_label)    # Adds label to the grid

        newest_line_check = 0                                   # To check to make sure your on the newest line of data

        newest_line = self.get_newest_line(instance.id + '.csv')           # Gets the newest line in the file

        # Loops to obtain data from the file
        with open(file_name) as csv_file:                       # Opens the file to read
            csv_reader = csv.reader(csv_file, delimiter=',')    # Starts the csv reader
            for newest_row in csv_reader:                       # Loops through the rows in the file
                newest_line_check += 1                          # Increments once for each new row it loops through
                if newest_line_check != newest_line:            # Checks to see if you are not on the newest like
                    pass                                        # If your not, do nothing
                else:                                           # If you are, add all the data

                    # Variables to keep track of which element in the row you are on
                    element_index = 0                           # To get the first exercise name (two elements in)
                    exercise_number = 0                         # To get every exercise after (every four elements)

                    # Loops over each element in the row
                    for element in newest_row:
                        if element_index == 2:                   # If your on the second element (first exercise name)
                            self.display_grid.rows += 1          # Add a row to the grid
                            id_name = file_name + ',' + element  # Creates id_name with filename and exercise name

                            # Creates a label for the exercise name
                            my_label = Label(text=element, color=[1, 1, 1, 1])

                            # Creates a button for the status of completion for the exercise
                            my_button = Button(text="Not Completed", color=[0.502, 0, 0, 1],
                                               background_color=[0.502, 0, 0, 1], on_press=self.open_exercise,
                                               id=id_name)

                            self.display_grid.add_widget(my_button)  # Adds the button to the grid
                            self.display_grid.add_widget(my_label)   # Adds the label to the grid

                            # Resets the exercise number (first two loops increment it to 2)
                            exercise_number = 0

                        # To stop it for increasing element index past 3 (Needs to be higher than two)
                        if element_index < 4:
                            element_index += 1                      # Increments element index

                        # Every four elements, there is a exercise name
                        if exercise_number == 4:
                            self.display_grid.rows += 1          # Increment the number of rows in grid
                            id_name = file_name + ',' + element  # Creates id_name with filename and exercise name

                            # Creates a label for the exercise name
                            my_label = Label(text=element, color=[1, 1, 1, 1])

                            # Creates a button for the status of completion for the exercise
                            my_button = Button(text="Not Completed", color=[0.502, 0, 0, 1],
                                               background_color=[0.502, 0, 0, 1], on_press=self.open_exercise,
                                               id=id_name)

                            self.display_grid.add_widget(my_button)  # Adds the button to the grid
                            self.display_grid.add_widget(my_label)  # Adds the label to the grid
                            exercise_number = 1     # Sets to 1 because it only increments 3 times, and needs to reach 4
                        else:                       # If exercise number is not 4
                            exercise_number += 1    # Increment the exercise number

    # To reset the Display Routine page
    def reset_display(self):
        self.display_grid.clear_widgets()  # Clears out the grid layout
        self.display_grid.rows = 0         # Resets the gridZ

    # =================================================================================================================
    # Functions for Display Exercise
    # =================================================================================================================
    # To open each individual workout
    def open_exercise(self, instance):
        self.transition.direction = 'left'                   # Changes the open direction to go left
        self.current = "DisplayExercise"                     # Which screen it will change to
        file_name, exercise_name = instance.id.split(",")    # Separates the file name and exercise name from id
        self.display_ex_name.text = exercise_name            # Sets the label to the exercise name
        self.display_ex_grid.rows += 1                       # Adds the first row in the exercise grid
        blank_title_label = Label(text='')                   # Blank label for formatting
        weight_title_label = Label(text='Weight')            # Weight title
        reps_title_label = Label(text='Reps')                # Reps title
        self.display_ex_grid.add_widget(blank_title_label)   # Adds the blank label to the grid
        self.display_ex_grid.add_widget(reps_title_label)    # Adds the reps label to the grid
        self.display_ex_grid.add_widget(weight_title_label)  # Adds the weight title to the grid

        with open(file_name) as csv_file:                       # Opens the csv file
            csv_reader = csv.reader(csv_file, delimiter=',')    # Starts the csv reader
            for row in csv_reader:                              # Loops through rows in the file
                for i in range(len(row)-1):                     # Loops through each thing in the row
                    if row[i] == exercise_name:                 # If the element is the exercise name
                        total_sets = row[i+1]                   # The number of sets is the next element

        set_number = 1                                          # Counter for displaying the specific # set on the label
        for i in range(int(total_sets)):                        # Loops total_sets number of times
            self.display_ex_grid.rows += 1                      # Adds one to the grid rows each time
            sets_label = Label(text='Set ' + str(set_number))   # Creates a label for each set (Set 1:, Set 2:, ..ect)
            reps_input = TextInput(input_filter='int')          # Creates text input for number of completed reps
            weight_input = TextInput(input_filter='int')        # Creates text input for weight used
            self.display_ex_grid.add_widget(sets_label)         # Adds the sets label to grid
            self.display_ex_grid.add_widget(reps_input)         # Adds the reps text input to the grid
            self.display_ex_grid.add_widget(weight_input)       # Adds the weight text input to the grid
            set_number += 1                                     # Increments the set number

    def clear_exercise(self):
        self.display_ex_grid.clear_widgets()
        self.display_ex_grid.rows = 0

    def save_exercise(self):

        # Todo: set the id of reps input and sets input to | file, extenetion = file_name.split('.')
        # Todo: id = file + ',' + exercise_name + 'reps/sets' +  i ?

        # Todo: implement get_set():?

        # for i in range(int(total_sets)):
        
        pass

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
    # Helper Functions
    # =================================================================================================================
    def get_newest_line(self, file_name):

        newest_line = 0  # The number of the newest row of data

        with open('routines/' + file_name) as csv_file:                       # Opens the file to read
            csv_reader = csv.reader(csv_file, delimiter=',')    # Starts the csv reader
            for row in csv_reader:                              # Loops for each row in the file
                newest_line += 1                                # Increments to keep track of the newest line
        return newest_line

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
