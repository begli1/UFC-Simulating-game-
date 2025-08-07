from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch') 

import random
from kivy.app import App                    # Main app class
from kivy.uix.widget import Widget          # Base widget class
from kivy.uix.boxlayout import BoxLayout    # Horizontal or vertical box layout
from kivy.uix.gridlayout import GridLayout  # Grid layout with rows and columns
from kivy.uix.stacklayout import StackLayout # Stack widgets horizontally or vertically
from kivy.uix.floatlayout import FloatLayout # Absolute positioning layout
from kivy.uix.anchorlayout import AnchorLayout # Anchored positioning layout
from kivy.uix.label import Label             # Text labels
from kivy.uix.button import Button           # Buttons
from kivy.uix.textinput import TextInput     # Single-line text input
from kivy.uix.checkbox import CheckBox       # Checkbox
from kivy.uix.slider import Slider           # Slider bar
from kivy.uix.switch import Switch           # On/off switch toggle
from kivy.uix.image import Image             # Display images
from kivy.uix.scrollview import ScrollView   # Scrollable container
from kivy.uix.tabbedpanel import TabbedPanel # Tabbed interface container
from kivy.uix.carousel import Carousel       # Swipeable carousel of widgets
from kivy.uix.popup import Popup              # Popup dialog window
from kivy.clock import Clock                  # Scheduling events, timers
from kivy.properties import StringProperty, NumericProperty, BooleanProperty  # Reactive properties
from kivy.lang import Builder                  # Load kv files or strings
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.animation import Animation
from kivy.core.window import Window
import json
import os



from fighter_database import Fighter
from fighter_database import fighter_database
class Contract1:
    def __init__(self, fighter):
        self.fighter = fighter
        self.fighter_popularity = fighter.popularity
        self.contract = 0 

    def contract_maker(self):
        if self.fighter_popularity <= 25:
            self.contract = 20000
        elif self.fighter_popularity > 25 and self.fighter_popularity <= 40:
            self.contract = 100000
        elif self.fighter_popularity > 40 and self.fighter_popularity <= 60:
            self.contract = 300000
        elif self.fighter_popularity > 60 and self.fighter_popularity <= 70:
            self.contract = 500000
        elif self.fighter_popularity > 70 and self.fighter_popularity <= 80:
            self.contract = 800000
        elif self.fighter_popularity > 80 and self.fighter_popularity <= 85:
            self.contract = 1000000
        elif self.fighter_popularity > 85 and self.fighter_popularity <= 90:
            self.contract = 2000000
        elif self.fighter_popularity > 90 and self.fighter_popularity <= 95:
            self.contract = 3000000
        else:
            self.contract = 4000000
        return str(self.contract)


def generate_all_contracts():
    contracts = {}
    for fighter in fighter_database.values():
        contract = Contract1(fighter)
        contract_str = contract.contract_maker()
        contracts[fighter.name] = contract_str
    return contracts



DB_FILE = 'users.json'
fighter_data = 'fighters.json'
fighter_database_users = 'user_fighter.json'
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)


def load_fighter_stats():
    if os.path.exists(fighter_data):
        with open(fighter_data, 'r') as f:
            return json.load(f)
    else:
        return {}

def load_users_fighters():
    if os.path.exists(fighter_database_users):
        with open(fighter_database_users, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def save_users_fighters(fighter_user):
    with open(fighter_database_users, 'w') as f:
        json.dump(fighter_user, f, indent=4)







class LogIn(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.update_rect, pos=self.update_rect)

        ufc_logo = Image(source='ufc.png', size_hint=(None, None), size=(500, 250), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        layout.add_widget(ufc_logo)

        label = Label(text='Welcome to UFC Manager!', color=(0, 0, 0, 1), size_hint=(None, None), size=(400, 160), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=48)
        layout.add_widget(label)

        self.username = TextInput(hint_text='Username', multiline=False, size_hint=(0.6, None), height=40, pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.password = TextInput(hint_text='Password', password=True, multiline=False, size_hint=(0.6, None), height=40, pos_hint={'center_x': 0.5, 'center_y': 0.32})
        layout.add_widget(self.username)
        layout.add_widget(self.password)

        btn = Button(text='Log In', size_hint=(None, None), size=(200, 60), pos_hint={'center_x': 0.5, 'center_y': 0.18}, font_size=24, background_color=(1, 0, 0, 1))
        btn.bind(on_press=self.switch_to_game)
        layout.add_widget(btn)

        switch_to_signup = Button(text="[u]Don't have an account? Sign up [/u]", size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'center_y': 0.1},            markup=True,  # Enable underline via markup
            background_normal='',  # Removes default background image
            background_color=(1, 1, 1, 1),  # White background
            color=(0, 0, 0, 1))
        switch_to_signup.bind(on_press=self.go_to_signup)
        layout.add_widget(switch_to_signup)

        self.message = Label(text='', color=(1, 0, 0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.24}, size_hint=(None, None))
        layout.add_widget(self.message)

        self.add_widget(layout)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def switch_to_game(self, *args):
        users = load_users()
        uname = self.username.text
        pwd = self.password.text

        if uname in users and users[uname]["password"] == pwd:
            self.manager.get_screen('game').current_user = uname
            self.manager.current = 'game'
        else:
            self.message.text = "Invalid username or password."

    def go_to_signup(self, instance):
        self.manager.current = 'Signup'


# ---------- SIGNUP SCREEN ----------
class Signup(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.update_rect, pos=self.update_rect)

        ufc_logo = Image(source='ufc.png', size_hint=(None, None), size=(500, 250), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        layout.add_widget(ufc_logo)

        label = Label(text='Sign Up to enjoy the game!', color=(0, 0, 0, 1), size_hint=(None, None), size=(400, 160), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=48)
        layout.add_widget(label)

        self.new_username = TextInput(hint_text='New Username', multiline=False, size_hint=(0.6, None), height=40, pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.new_password = TextInput(hint_text='New Password', password=True, multiline=False,size_hint=(0.6, None), height=40, pos_hint={'center_x': 0.5, 'center_y': 0.32})

        signup_btn = Button(text='Sign Up', size_hint=(None, None), size=(200, 60), pos_hint={'center_x': 0.5, 'center_y': 0.18}, font_size=24, background_color=(1, 0, 0, 1))
        signup_btn.bind(on_press=self.signup)

        switch_to_login = Button(text="[u]Have an account? Log in [/u]", size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'center_y': 0.1},            markup=True,  # Enable underline via markup
            background_normal='',  # Removes default background image
            background_color=(1, 1, 1, 1),  # White background
            color=(0, 0, 0, 1))
        switch_to_login.bind(on_press=self.go_to_login)


        layout.add_widget(self.new_username)
        layout.add_widget(self.new_password)
        layout.add_widget(signup_btn)
        layout.add_widget(switch_to_login)

        self.message = Label(text='', color=(1, 0, 0, 1), pos_hint={'center_x': 0.5, 'center_y': 0.24}, size_hint=(None, None))
        layout.add_widget(self.message)

        self.add_widget(layout)

    def signup(self, instance):
        users = load_users()
        fighter_d = load_fighter_stats()
        fighters_database_users = load_users_fighters()
        uname = self.new_username.text.strip()
        pwd = self.new_password.text.strip()

        if uname in users:
            self.message.text = "Username already exists."
        elif uname == "" or pwd == "":
            self.message.text = "Fields can't be empty."
        else:
            users[uname] = {"password": pwd, "event":[], "contracts": generate_all_contracts(), "Money": 0}
            fighters_database_users[uname] = {"fighters": fighter_d}

            save_users(users)
            save_users_fighters(fighters_database_users)
            self.message.text = "Account created! Go log in."

    def go_to_login(self, instance):
        self.manager.current = 'LogIn'

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class History(Screen):
    current_user = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        self.layout = FloatLayout(size_hint_x=1, size_hint_y=None, height=15000)

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
        self.bind(current_user=self.update_history)

        # White background
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)


        # Title
        history = Label(
            text="History",
            font_size=36,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        self.layout.add_widget(history)


    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    def switch_to_games(self, *args):
            self.manager.current = 'game'
    def update_history(self, *args):
        # Remove old event labels (except the title)
        self.layout.clear_widgets()
        # Add the title again
        history = Label(
            text="History",
            font_size=36,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.99}
        )
        self.layout.add_widget(history)

        btn1 = Button(text='Back', size_hint=(None, None), size=(150, 60), pos_hint={'center_x': 0.08, 'center_y': 0.99}, font_size=20, background_color=(1, 0, 0, 1))
        btn1.bind(on_press=self.switch_to_games)
        self.layout.add_widget(btn1)

        users = load_users()
        events = []
        if self.current_user and self.current_user in users:
            events = users[self.current_user].get("event", [])

        # Display each event
        y = 0.97
        for event in events:
            event_label = Label(
                text=f"{event.get('name', 'Event')}: {event.get('summary', '')}",
                color=(0, 0, 0, 1),
                size_hint=(None, None),
                pos_hint={'center_x': 0.4, 'top': y},
                halign = 'left',
                valign = 'middle'
            )
            self.layout.add_widget(event_label)
            y -= 0.03  # Move down for next event



class Contract(Screen):
    current_user = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        self.layout = FloatLayout(size_hint_x=1, size_hint_y=None, height=18000)

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
        self.bind(current_user=self.update_history)

        # White background
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)


        # Title
        contract = Label(
            text="Contracts",
            font_size=36,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.995}
        )
        self.layout.add_widget(contract)


    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    def switch_to_games(self, *args):
            self.manager.current = 'game'
    def update_history(self, *args):
        # Remove old event labels (except the title)
        self.layout.clear_widgets()
        # Add the title again
        contract = Label(
            text="Contracts",
            font_size=36,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.995}
        )
        self.layout.add_widget(contract)

        btn1 = Button(text='Back', size_hint=(None, None), size=(150, 60), pos_hint={'center_x': 0.08, 'center_y': 0.995}, font_size=20, background_color=(1, 0, 0, 1))
        btn1.bind(on_press=self.switch_to_games)
        self.layout.add_widget(btn1)

        users = load_users()
        contracts = {}
        if self.current_user and self.current_user in users:
            contracts = users[self.current_user].get("contracts", {})

        y = 0.99
        for fighter_name, contract_value in contracts.items():
            event_label = Label(
                text= f"{fighter_name}: {contract_value}",
                color=(0, 0, 0, 1),
                size_hint=(None, None),
                size=(Window.width * 0.8, 40),
                pos_hint={'center_x': 0.5, 'top': y}
            )
            self.layout.add_widget(event_label)
            y -= 0.001655  # Move down for next event







from game import GameScreen

    
    
    






    


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LogIn(name='LogIn'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(Signup(name='Signup'))
        sm.add_widget(History(name='history'))
        sm.add_widget(Contract(name='contracts'))
        return sm

if __name__ == '__main__':
    MyApp().run()
