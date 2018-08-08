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

test_list1 = []
test_list = []

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


            #FIXME
            test_list1.append(name_text)
            test_list1.append(sets_text)
            test_list1.append(reps_text)
            test_list1.append(weight_text)



            # Calls the next step
            ScreenManager.reset_fields(self)

    def save_and_create(self):

        # Checks to make sure the routine name is not empty
        if self.workout_name.text != "":
            if workout_list:
                # Gets the name of the routine to be used as the button
                routine_name = self.workout_name.text

                # Adds the routine name and string to the list
                routine_name_list.append({'routine': routine_name, 'last_used': "Not Used"})

                # FIXME TEST LIST WORKS, replace other list
                test_list.append(routine_name)
                test_list.append('Not Used')
                test_list.extend(test_list1)
                print(test_list)

                file_name = routine_name + '.csv'                   # Creates the file name (as .csv file)
                my_file = open("routines/" + file_name, 'w')        # Creates the file to store the routine

                # Dict headers to point to the data in the dict
                fieldnames = ['routine', 'last_used', 'name', 'sets', 'reps', 'weight']

                # Uses dictWriter to create a csv file with the data in its correct column
                writer = DictWriter(my_file, fieldnames=fieldnames, extrasaction='ignore', delimiter=',',
                                    lineterminator='\n')

                csv_titles = ['Routine Name', 'Last Used']  # The first two titles will always be this
                number_exercises = len(workout_list)        # Gets the number of exercises in the routine
                for i in range(number_exercises):           # Loops through each one and adds titles for each
                    csv_titles.append('Exercise Name')      # Exercise Name title
                    csv_titles.append('Sets')               # Sets title
                    csv_titles.append('Reps')               # Reps title
                    csv_titles.append('Weight')             # Weight title

                print("csvtitles: ", csv_titles)
                print("test list: ", test_list)
                # Write titles
                writer.writer.writerow(csv_titles)      # Writes the titles across the top row of csv file

                writer.writer.writerow(test_list)

                # FIXME: commented out for testing above code
                #writer.writerows(routine_name_list)     # First writes the routine name and last used date
                #writer.writerows(workout_list)          # Then writes each workout
                my_file.close()                         # Closes file

                # Updates the Routines page with the new routine button
                ScreenManager.update_routines(self)

                self.save_button.text = str('Saved')    # Change button to 'saved'

                self.add_routine_grid.clear_widgets()  # Clears out the grid layout
                self.add_routine_grid.rows = 0          # Resets the rows in the add_routine grid

                self.transition.direction = 'right'     # Sets the transition direction
                self.current = "Routines"               # Which screen to change to

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

    def is_unique(self):
        if self.workout_name.text != "":
            if workout_list:
                # Gets the name of the routine to be used as the button
                routine_name = self.workout_name.text
                file_name = routine_name + '.csv'  # Creates the file name (as .csv file)
                for file in os.listdir("routines/"):  # Looks through all saved routines
                    if file.endswith(".csv"):  # Makes sure its a .csv file
                        if file_name == file:  # If there are matching file names
                            print("You already have a routine named:", file_name)  # Tell the user they need a new name
                            routine_name_list.clear()  # Clears the list for new data
                            return False
        return True

    # =================================================================================================================
    # Functions for Display Routine
    # =================================================================================================================
    # What will happen when pressing a routine
    def open_routine(self, instance):
        self.transition.direction = 'left'                  # Changes the open direction to go left
        self.current = "DisplayRoutine"                     # Which screen it will change to
        self.display_name.text = str(instance.id)           # Changes the label to the current routine
        file_name = 'routines/' + instance.id + '.csv'      # Creates the full file name with extension

        with open(file_name) as csv_file:                       # Opens the file to read
            csv_reader = csv.reader(csv_file, delimiter=',')    # Starts the csv reader
            line_count = 0                                      # To keep track of what line of the file were on
            for row in csv_reader:                              # Loops for each row in the file
                self.display_grid.rows += 1                     # Adds a row in the grid for the exercise
                if line_count == 0:                             # On the first line
                    status_label = Label(text='Status')             # Creates status label
                    self.display_grid.add_widget(status_label)      # Adds label to the grid
                    name_label = Label(text='Exercise Name')        # Creates exercise name label
                    self.display_grid.add_widget(name_label)        # Adds label to the grid
                    line_count += 1                                 # Increments the line counter
                elif line_count == 1:                           # On the second line
                    line_count += 1                                 # No data is need here, increment line counter
                else:                                           # On the rest of the lines
                    name = row[2]                                   # Exercise name is set to 'name'
                    id_name = file_name + ',' + row[2]              # Creates id_name with filename and exercise name

                    # Creates a label for the exercise name
                    my_label = Label(text=name, color=[1, 1, 1, 1])
                    # Creates a button for the status of completion for the exercise
                    my_button = Button(text="Not Completed",  color=[0.502, 0, 0, 1], background_color=[0.502, 0, 0, 1],
                                       on_press=self.open_exercise, id=id_name)
                    self.display_grid.add_widget(my_button)     # Adds the button to the grid
                    self.display_grid.add_widget(my_label)      # Adds the label to the grid

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

    def clear_exercise(self):
        self.display_ex_grid.clear_widgets()
        self.display_ex_grid.rows = 0

    def save_exercise(self):


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
