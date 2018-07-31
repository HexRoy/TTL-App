from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, StringProperty

Builder.load_file('main.kv')


class Menu(Screen):
    pass


class Routines(Screen):
    pass


class Setting(Screen):
    pass


class AddRoutine(Screen):
    grid_rows = 0

    def get_vars(self):

        self.name = self.exercise_name.text
        self.sets = self.num_sets.text
        self.reps = self.num_reps.text
        self.weight = self.amt_weight.text

        print(self.name)
        print(self.sets)
        print(self.reps)
        print(self.weight)
        AddRoutine.reset_fields(self)

    def reset_fields(self):
        AddRoutine.add_to_grid(self)

    def add_to_grid(self):
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
