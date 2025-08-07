from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.animation import Animation
import os
import random
import json
from kivy.uix.widget import WidgetException

db_FILE = 'users.json'
fighter_data = 'fighters.json'
fighter_database_users = 'user_fighter.json'

with open(db_FILE, 'r') as f:
    data = json.load(f)


def load_users():
    if os.path.exists(db_FILE):
        with open(db_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(db_FILE, 'w') as f:
        json.dump(users, f , indent=4)



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


from fighter_database import Fighter
from fighter_database import fighter_database








def simulate_ppv(fighter1, fighter2):


    # Base revenue for any UFC PPV event
    popularity_revenue = 0  # Represents gate, sponsorships, etc. (can be adjusted)

    # Revenue from popularity: Higher multiplier for higher popularity
    # This scales popularity more, so a fight between two 100 pop fighters is huge.
    if fighter1.get('popularity') >= 85:
        popularity_revenue += (fighter1.get('popularity')**1.6 * 1000) 

    elif fighter1.get('popularity') < 85 and fighter1.get('popularity') >= 70:
        popularity_revenue += (fighter1.get('popularity')**1.6 * 500)

    elif fighter1.get('popularity') < 70 and fighter1.get('popularity') >= 50:
        popularity_revenue += (fighter1.get('popularity')**1.6 * 200)
    
    else:
        popularity_revenue += (fighter1.get('popularity')**1.6 * 50)



    if fighter2.get('popularity') >= 85:
        popularity_revenue += (fighter2.get('popularity')**1.6 * 1000) 

    elif fighter2.get('popularity') < 85 and fighter2.get('popularity') >= 70:
        popularity_revenue += (fighter2.get('popularity')**1.6 * 500)

    elif fighter2.get('popularity') < 70 and fighter2.get('popularity') >= 50:
        popularity_revenue += (fighter2.get('popularity')**1.6 * 200)
    
    else:
        popularity_revenue += (fighter2.get('popularity')**1.6 * 50)


    # Fight Style Appeal: Fights with higher overall skill/excitement potential generate more interest.
    # We'll average their key attributes (Power, Speed, Grappling)
    # A higher average means a potentially more exciting or competitive fight.
    fighter1_skill_average = (fighter1.get('power') + fighter1.get('speed') + fighter1.get('grappling')) / 3
    fighter2_skill_average = (fighter2.get('power') + fighter2.get('speed') + fighter2.get('grappling')) / 3

    # Multiplier based on combined skill average. Scale this to have a meaningful impact.
    # For example, an average skill of 80 could give a bonus, 90 an even larger one.
    skill_appeal_multiplier = ((fighter1_skill_average + fighter2_skill_average) / 200) * 50000



    random_bonus_potential = random.uniform(0, 0.25) 
    random_bonus_value = (fighter1.get('popularity') + fighter2.get('popularity')) * 50000 * random_bonus_potential



    revenue = popularity_revenue + skill_appeal_multiplier + random_bonus_value

    return revenue

def update_fighter_stats(winner_name, loser_name):
    if winner_name in fighter_data1:
        fighter_data1[winner_name]['popularity'] += random.randint(0,4)
        fighter_data1[winner_name]['power'] += random.randint(0,4)
        fighter_data1[winner_name]['grappling'] += random.randint(0,4)
        fighter_data1[winner_name]['speed'] += random.randint(0,4)
    if loser_name in fighter_data1:
        fighter_data1[loser_name]['popularity'] -= random.randint(0,4)
        fighter_data1[loser_name]['power'] -= random.randint(0,4)
        fighter_data1[loser_name]['grappling'] -= random.randint(0,4)
        fighter_data1[loser_name]['speed'] -= random.randint(0,4)
    


def simulate_fight(fighter1, fighter2):
    fighter_1_chance = fighter1.get('speed') + fighter1.get('power') + fighter1.get('grappling')
    fighter_2_chance = fighter2.get('speed') + fighter2.get('power') + fighter2.get('grappling')
    total = fighter_1_chance + fighter_2_chance
    prob1 = fighter_1_chance / total

    rand_num = random.random()  # random float between 0.0 and 1.
    if rand_num <= prob1:
        winner = fighter1
    else:
        winner = fighter2
    return winner
class Match:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.winner = None
        self.revenue= None
        self.loser = None

    def simulate(self):
        self.winner = simulate_fight(self.fighter1, self.fighter2)
        if self.fighter1 == self.winner:
            self.loser = self.fighter2
        else:
            self.loser = self.fighter1
        return self.winner, self.loser
    def ppv(self):
        self.revenue = simulate_ppv(self.fighter1, self.fighter2)
        return round(self.revenue)
 
class Event:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.revenue = 0
        self.ppv_buys = 0

    def add_match(self, match):
        self.matches.append(match)

    def run_event(self):
        print(f"Running event: {self.name}")
        results= []
        for match in self.matches:
            winner, loser = match.simulate()
            update_fighter_stats(winner.get('name'),loser.get('name'))
            results.append(f"{match.fighter1.get('name')} vs {match.fighter2.get('name')} - {winner.get('name')} defeated {loser.get('name')}")
        return "\n".join(results)

    def event_summary(self):
        summary = [f"Event: {self.name}", f"Total Matches: {len(self.matches)}"]
        for i, match in enumerate(self.matches, 1):
            winner_name = match.winner.get("name") if match.winner else "Not fought yet"
            summary.append(f"Match {i}: {match.fighter1.get('name')} vs {match.fighter2.get('name')} - Winner: {winner_name}")
        for match in self.matches:
            revenue = match.ppv()
            self.revenue += revenue
            self.ppv_buys += (revenue)/80 
        rounded_ppv = round(self.ppv_buys)
        summary.append(f"Total PPV Buys: {rounded_ppv}")
        summary.append(f"Total Revenue: ${self.revenue - total_fighter_pay}")
        return "\n".join(summary)
    def get_revenue(self):
        total_revenue = 0
        for match in self.matches:
            total_revenue += match.ppv()
        return total_revenue - total_fighter_pay

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        global current_user
        current_user = self.current_user 
        self.db_FILE = db_FILE
        
        
        
        self.data = {
    "Heavyweight": [
        "Tom Aspinall", "Ciryl Gane", "Alexander Volkov", "Sergei Pavlovich",
        "Curtis Blaydes", "Jailton Almeida", "Waldo Cortes-Acosta", "Marcin Tybura", "Serghei Spivac",
        "Derrick Lewis", "Tai Tuivasa", "Shamil Gaziev", "Mick Parkin", "Tallison Teixeira",
        "Jhonata Diniz", "Martin Buday", "Kennedy Nzechukwu", "Mario Pinto", "Hamdy Abdelwahab", 
        "Thomas Petersen", "Valter Walker", "Ryan Spann", "Junior Tafa", "Chris Barnett", 
        "Sean Sharaf", "Austen Lane", "Mohammed Usman", "Justin Tafa", "Lukasz Brzeski"
    ],
    "Light Heavyweight": [
        "Magomed Ankalaev","Alex Pereira", "Jiri Prochazka", "Carlos Ulberg", "Jamahal Hill", "Jan Blachowicz",
        "Aleksandar Rakic", "Khalil Rountree Jr.", "Dominick Reyes", "Volkan Oezdemir", "Nikita Krylov",
        "Azamat Murzakanov", "Johnny Walker", "Bogdan Guskov", "Zhang Mingyang", "Alonzo Menifield",
        "Navajo Stirling", "Rodolfo Bellato", "Nicolae Negumereanu", "Ibo Aslan",
        "Oumar Sy", "Ozzy Diaz", "Billy Elekana", "Bruno Lopes", "Ryan Spann",
        "Ion Cutelaba", "Julius Walker", "Paul Craig", "Rafael Cerqueira", "Diyar Nurgozhay",
        "Brendson Ribeiro", "Marcin Prachnio", "Vitor Petrino", "Ivan Erslan", "Jimmy Crute"
    ],
    "Middleweight": [
        "Dricus Du Plessis", "Nassourdine Imavov", "Sean Strickland", "Khamzat Chimaev", "Israel Adesanya",
        "Robert Whittaker", "Caio Borralho", "Jared Cannonier", "Roman Dolidze", "Anthony Hernandez",
        "Brendan Allen", "Marvin Vettori", "Reinier de Ridder", "Paulo Costa", "Roman Kopylov",
        "Abus Magomedov", "Joe Pyfer", "Nursulton Ruziboev", "Jack Hermansson", "Michel Pereira",
        "Bo Nickal", "Gregory Rodrigues", "Ikram Aliskerov", "Michael Page", "Mansur Abdul-Malik",
        "Kelvin Gastelum", "Azamat Bekoev", "Brunno Ferreira", "Shara Magomedov", "Jacob Malkoun",
        "Marco Tulio", "Cesar Almeida", "Chris Curtis", "Ozzy Diaz", "Ateba Gautier",
        "Rodolfo Vieira", "Aliaskhab Khizriev", "Torrez Finney", "Ismail Naurdiev", "Edmen Shahbazyan",
        "JunYong Park", "Christian Leroy Duncan", "Andre Petroski", "Cody Brundage", "Andre Muniz",
        "Paul Craig", "Zachary Reese", "Eric McConico", "Nick Klein", "Tresean Gore",
        "Eryk Anders", "Robert Bryczek", "Ryan Loder", "Nick Diaz", "Andrey Pulyaev",
        "Michal Oleksiejczuk", "Sedriques Dumas", "Kamaru Usman", "Robert Valentin", "Antonio Trocoli",
        "Dustin Stoltzfus", "Gerald Meerschaert", "Jose Daniel Medina", "Marc-Andre Barriault", "Dusko Todorovic"
    ],
    "Welterweight": [
        "Jack Della Maddalena","Islam Makhachev", "Belal Muhammad", "Sean Brady", "Shavkat Rakhmonov", "Leon Edwards",
        "Kamaru Usman", "Ian Machado Garry", "Joaquin Buckley", "Michael Morales", "Colby Covington",
        "Gilbert Burns", "Geoff Neal", "Stephen Thompson", "Carlos Prates", "Kevin Holland",
        "Michael Page", "Gabriel Bonfim", "Randy Brown", "Rinat Fakhretdinov", "Bryan Battle", 
        "Neil Magny", "Andreas Gustafsson", "Vicente Luque", "Mike Malott", "Michael Chiesa", 
        "Khaos Williams", "Sam Patterson", "Chidi Njokuani", "Trey Waters", "Oban Elliott", 
        "Daniel Rodriguez", "Jake Matthews", "Punahele Soriano", "Jonny Parsons", "Nicolas Dalby", 
        "Jacobe Smith", "Jonathan Micallef", "Max Griffin", "Gunnar Nelson", "Muslim Salikhov", 
        "Li Jingliang", "Ramiz Brahimaj", "Adam Fugitt", "Carlos Leal", "Gilbert Urbina", 
        "Themba Gorimbo", "Charles Radtke", "Carlston Harris", "Uros Medic", "Bassil Hafez", 
        "Elizeu Zaleski dos Santos", "Ismail Naurdiev", "Lyman Good", "Danny Barlow", "Evan Elder", 
        "Phil Rowe", "Santiago Ponzinibbio", "Sheldon Westcott", "Jeremiah Wells", "Rhys McKee", 
        "Daniel Frunza", "Matt Brown", "Gabe Green", "Pete Rodriguez", "Francisco Prado", 
        "Billy Ray Goff", "Rafael Dos Anjos", "Niko Price", "Preston Parsons", "Rolando Bedoya", 
        "Song Kenan", "Kiefer Crosbie", "Trevin Giles", "Ange Loosa", "Yusaku Kinoshita", 
        "Wellington Turman", "Darrius Flowers", "Tim Means", "Court McGee", "Mickey Gall", 
        "Alex Morono"
    ],
    "Lightweight": [
        "Ilia Topuria", "Arman Tsarukyan", "Charles Oliveira", "Justin Gaethje", "Max Holloway",
        "Dustin Poirier", "Dan Hooker", "Mateusz Gamrot", "Paddy Pimblett", "Beneil Dariush",
        "Renato Moicano", "Rafael Fiziev", "Michael Chandler", "Benoit Saint Denis", "Grant Dawson",
        "Joel Alvarez", "Ignacio Bahamondes", "Mauricio Ruffy", "Fares Ziam", "Nasrat Haqparast", 
        "Chase Hooper", "King Green", "Ludovit Klein", "Mateusz Rebecki", "Nazim Sadykhov", 
        "Manuel Torres", "Rafael Dos Anjos", "Jared Gordon", "Chris Duncan", "Chris Padilla", 
        "MarQuel Mederos", "Drakkar Klose", "Jim Miller", "Esteban Ribovics", "Charlie Campbell", 
        "Myktybek Orolbai", "Mike Davis", "Quillan Salkilld", "Nurullo Aliev", "Ismael Bonfim", 
        "Nikolas Motta", "Matt Frevola", "Daniel Zellhuber", "Gabe Green", "Francis Marshall", 
        "Alexander Hernandez", "Thiago Moises", "Diego Ferreira", "Rafa Garcia", "Evan Elder", 
        "Francisco Prado", "David Teymur", "Tom Nolan", "Kaue Fernandes", "Jordan Leavitt", 
        "Mason Jones", "Bolaji Oki", "Mark Choinski", "AJ Cunningham", "Mitch Ramirez", 
        "Trey Ogden", "David Onama", "Yanal Ashmouz", "Dennis Buzukja", "Michael Johnson", 
        "Joe Lauzon", "Matheus Camilo", "Elves Brener", "Rongzhu", "Terrance McKinney", 
        "Vagner Rocha", "Kody Steele", "Gauge Young", "Roberto Romero", "Abdul-Kareem Al-Selwady", 
        "Jai Herbert", "Darrius Flowers", "Loik Radzhabov", "Claudio Puelles", "Anshul Jubli", 
        "Viacheslav Borshchev", "Trevor Peek", "Joaquim Silva", "Damir Hadzovic", "Austin Hubbard", 
        "Al Iaquinta", "Brad Riddell", "Kurt Holobaugh", "Alex Reyes", "Rolando Bedoya", 
        "Mohammad Yahya", "Jordan Vucenic", "Jamie Mullarkey", "Lando Vannata", "Maheshate", 
        "Victor Martinez", "Drew Dober", "Ottman Azaitar", "Kyle Prepolec", "Jeremy Stephens"
    ],
    "Featherweight": [
        "Alexander Volkanovski", "Max Holloway", "Diego Lopes", "Movsar Evloev", "Aaron Pico",
        "Yair Rodriguez", "Arnold Allen", "Brian Ortega", "Lerone Murphy", "Aljamain Sterling",
        "Josh Emmett", "Jean Silva", "Youssef Zalal", "David Onama", "Dan Ige","Patricio Pitbull",
        "Calvin Kattar", "Hyder Amil", "William Gomis", "Bryce Mitchell", "Chepe Mariscal", 
        "Steve Garcia", "Pat Sabatini", "Edson Barboza", "Felipe Lima", "Melquizael Costa", 
        "Giga Chikadze", "Mairon Santos", "Nathaniel Wood", "Danny Silva", "Sean Woodson", 
        "Dooho Choi", "Ryan Hall", "Bogdan Grad", "Nathan Fletcher", "Nate Landwehr", 
        "Joanderson Brito", "Daniel Santos", "JooSang Yoo", "Jose Delgado", "Kevin Vallejos", 
        "Kyle Nelson", "Cub Swanson", "Morgan Charriere", "Jamall Emmers", "Isaac Dulgarian", 
        "Gabriel Santos", "Melsik Baghdasaryan", "Miles Johns", "Patricio Freire", "Andre Fili", 
        "Julian Erosa", "Westin Wilson", "Fernando Padilla", "Christian Rodriguez", "Vagner Rocha", 
        "Manolo Zecchini", "Lando Vannata", "Steven Nguyen", "Dennis Buzukja", "Jack Jenkins", 
        "Alex Caceres", "Francis Marshall", "Darren Elkins", "Lucas Almeida", "Timmy Cuamba", 
        "John Castaneda", "Sodiq Yusuff", "Billy Quarantillo", "JeongYeong Lee", "Kaan Ofli", 
        "Charles Jourdain", "Shayilan Nuerdanbieke", "Gavin Tucker", "Yizha", "Ricardo Ramos", 
        "Erik Silva", "Roberto Romero"
    ],
    "Bantamweight": [
        "Merab Dvalishvili", "Sean O'Malley", "Umar Nurmagomedov", "Petr Yan", "Cory Sandhagen",
        "Song Yadong", "Deiveson Figueiredo", "Marlon Vera", "Rob Font", "Mario Bautista",
        "Henry Cejudo", "Aiemann Zahabi", "Kyler Phillips", "Marcus McGhee", "Montel Jackson",
        "Vinicius Oliveira", "Raoni Barcelos", "Chris Gutierrez", "Jonathan Martinez", "Daniel Marcos", 
        "Farid Basharat", "Raul Rosas Jr.", "Said Nurmagomedov", "Charles Jourdain", "Brady Hiestand", 
        "Payton Talbott", "SuYoung You", "Tim Elliott", "Cody Garbrandt", "ChangHo Lee", 
        "Muin Gafurov", "Malcolm Wellmaker", "Miles Johns", "Da'Mon Blackshear", "Rinya Nakamura", 
        "Serhiy Sidey", "Jean Matsumoto", "Daniel Santos", "David Martinez", "Aleksandre Topuria", 
        "Adrian Yanez", "Cody Haddon", "Elijah Smith", "John Castaneda", "Davey Grant", 
        "Victor Henry", "Carlos Vera", "Bekzat Almakhan", "Benardo Sopaj", "Alatengheili", 
        "Pedro Munhoz", "Xiao Long", "Patchy Mix", "Aoriqileng", "Ricky Simon", 
        "Quang Le", "AJ Cunningham", "Colby Thicknesse", "Baergeng Jieleyisi", "Gaston Bolanos", 
        "Ramon Taveras", "Douglas Silva de Andrade", "Steven Koslow", "Nathan Fletcher", "Angel Pacheco", 
        "Josias Musasa", "Toshiomi Kazama", "Frankie Saenz", "Rani Yahya", "Matt Schnell", 
        "Ricky Turcios", "Cristian Quinonez", "Javid Basharat", "Chad Anheliger", "Cody Gibson", 
        "Brad Katona", "Garrett Armfield", "Luan Lacerda", "Cameron Smotherman", "Kris Moutinho", 
        "Saimon Oliveira", "Cameron Saaiman", "Vince Morales"
    ],
    "Flyweight": [
        "Alexandre Pantoja", "Brandon Moreno", "Brandon Royval", "Manel Kape", "Amir Albazi",
        "Ramazan Temirov", "Tatsuro Taira", "Kai Kara-France", "Joshua Van", "Tagir Ulanbekov",
        "Allan Nascimento", "Andre Lima", "HyunSung Park", "Charles Johnson", "Rafael Estevam",
        "Lone'er Kavanagh", "Asu Almabayev", "Clayton Carpenter", "DongHun Choi", "Tim Elliott",
        "Alessandro Costa", "Edgar Chairez", "Jafel Filho", "Felipe Bunes", "Kevin Borjas",
        "Rei Tsuruya", "Kai Asakura", "Jose Ochoa", "Jesus Aguilar", "Stewart Nicoll",
        "Lucas Rocha", "Matt Schnell", "Azat Maksum", "SeungGuk Choi", "Alex Perez",
        "Ronaldo Rodriguez", "Kiru Sahota", "Nyamjargal Tumendemberel", "Ode Osbourne",
        "Daniel Barez", "Sumudaerji", "Luis Gurule", "Felipe dos Santos", "Mitch Raposo",
        "Steve Erceg", "Cody Durden"
    ],
    "Women's Bantamweight": [
        "Kayla Harrison", "Julianna Pena", "Raquel Pennington", "Ketlen Vieira", "Norma Dumont",
        "Macy Chiasson", "Irene Aldana", "Ailin Perez", "Mayra Bueno Silva", "Yana Santos",
        "Karol Rosa", "Jacqueline Cavalcanti", "Nora Cornolle", "Miesha Tate", "Joselyne Edwards",
        "Chelsea Chandler", "Daria Zhelezniakova", "Montserrat Rendon", "Ravena Oliveira",  
        "Melissa Mullins", "Priscila Cachoeira", "Tainara Lisboa", "Irina Alekseeva", 
        "Klaudia Sygula", "Hailey Cowan", "Josiane Nunes"
    ],
    "Women's Flyweight": [
        "Valentina Shevchenko", "Natalia Silva", "Manon Fiorot", "Alexa Grasso", "Erin Blanchfield",
        "Maycee Barber", "Jasmine Jasudavicius", "Rose Namajunas", "Viviane Araujo", "Jessica Andrade",
        "Tracy Cortez", "Miranda Maverick", "Karine Silva", "Casey O'Neill", "Wang Cong",
        "JJ Aldrich", "Eduarda Moura", "Gabriella Fernandes", "Katlyn Cerminara", "Luana Carolina", 
        "Tereza Bleda", "Carli Judice", "Ernesta Kareckaite", "Dione Barbosa", "Luana Santos", 
        "Amanda Ribas", "Jamey-Lyn Horth", "Veronica Hardy", "Julija Stoliarenko", "Nicolle Caliari", 
        "Bruna Brasil", "Fatima Kline", "Yuneisy Duben", "Melissa Gatto", "Brogan Walker", 
        "Juliana Miller", "Maryna Moroz", "Vanessa Demopoulos", "Ariane da Silva"
    ],
    "Women's Strawweight": [
        "Zhang Weili", "Virna Jandiroba", "Tatiana Suarez", "Yan Xiaonan", "Amanda Lemos",
        "Jessica Andrade", "Mackenzie Dern", "Amanda Ribas", "Iasmin Lucindo", "Gillian Robertson",
        "Tabatha Ricci", "Loopy Godinez", "Angela Hill", "Tecia Pennington", "Loma Lookboonmee",
        "Denise Gomes", "Ketlen Souza", "Shi Ming", "Alexia Thainara", 
        "Shauna Bannon", "Fatima Kline", "Piera Rodriguez", "Mizuki", "Bruna Brasil", 
        "Talita Alencar", "Ariane Carnelossi", "Yazmin Jauregui", "Stephanie Luciano", "Julia Polastri", 
        "Melissa Martinez", "Cheyanne Vlismas", "Feng Xiaocan", "Puja Tomar", "Elise Reed", 
        "Vanessa Demopoulos", "Marnic Mann", "Alice Ardelean", "Karolina Kowalkiewicz", "Luana Pinheiro", 
        "Montserrat Conejo Ruiz", "Polyana Viana", "Rayanne dos Santos"
    ]
}
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        layout = FloatLayout(size_hint_x=1, size_hint_y=None, height=2000)
        self.layout = layout
        # White background
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        def update_rect(instance, value):
            self.rect.size = instance.size
            self.rect.pos = instance.pos

        layout.bind(size=update_rect, pos=update_rect)

        # Title label
        welcome = Label(
            text='Create Your UFC PPV Card',
            font_size=35,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(400, 60),
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        layout.add_widget(welcome)


        # Main Card Label
        global main_card
        main_card = TextInput(
            hint_text="Name your event",
            multiline=False, 
            size_hint=(0.6, None),
            height=60,
            pos_hint={'center_x': 0.5, 'top': 0.96}
        )
        layout.add_widget(main_card)
        main_card.bind(on_text_validate= self.name_card)

#------------------------------------------------------------------------------------------------------


        money_button = Button(
            text='Show Money',
            size_hint=(None, None),
            size=(150, 60),
            pos_hint={'center_x': 0.5, 'top': 0.93},
            font_size=20,
            background_color=(0, 1, 0, 1)
        )
        money_button.bind(on_press=self.update_money_label)
        layout.add_widget(money_button)



        btn = Button(text='History', size_hint=(None, None), size=(150, 60), pos_hint={'center_x': 0.92, 'center_y': 0.97}, font_size=20, background_color=(1, 0, 0, 1))
        btn.bind(on_press=self.switch_to_history)
        layout.add_widget(btn)

        btn = Button(text='Contracts', size_hint=(None, None), size=(150, 60), pos_hint={'center_x': 0.92, 'center_y': 0.93}, font_size=20, background_color=(1, 0, 0, 1))
        btn.bind(on_press=self.switch_to_contracts)
        layout.add_widget(btn)

        main = Label(
            text="Main Event",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.8885}
        )
        layout.add_widget(main)

        # Fight 1
        # Weightclass + Fighter 1
        self.category_spinner = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.9},
            self.update_items
        )
        layout.add_widget(self.category_spinner)

        self.item_spinner = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.877}
        )
        layout.add_widget(self.item_spinner)

        # Weightclass + Fighter 2
        self.category_spinner1 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.9},
            self.update_items1
        )
        layout.add_widget(self.category_spinner1)

        self.item_spinner1 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.877}
        )
        layout.add_widget(self.item_spinner1)


#------------------------------------------------------------------------------------------------------
        comain = Label(
            text="Co-main Event",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.8185}
        )
        layout.add_widget(comain)






        # Fight 2
        # Weightclass + Fighter 1
        self.category_spinner2 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.83},
            self.update_items2
        )
        layout.add_widget(self.category_spinner2)

        self.item_spinner2 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.807}
        )
        layout.add_widget(self.item_spinner2)

        # Weightclass + Fighter 2
        self.category_spinner3 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.83},
            self.update_items3
        )
        layout.add_widget(self.category_spinner3)

        self.item_spinner3 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.807}
        )
        layout.add_widget(self.item_spinner3)


#------------------------------------------------------------------------------------------------------

        fight3 = Label(
            text="Fight 3",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.7635}
        )
        layout.add_widget(fight3)
        # Fight 3 --------------------------------------------------------------------------


        self.category_spinner4 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.775},
            self.update_items4
        )
        layout.add_widget(self.category_spinner4)

        self.item_spinner4 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.752}
        )
        layout.add_widget(self.item_spinner4)

        self.category_spinner5 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.775},
            self.update_items5
        )
        layout.add_widget(self.category_spinner5)

        self.item_spinner5 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.752}
        )
        layout.add_widget(self.item_spinner5)

# Fight 4 --------------------------------------------------------------------------
        fight4 = Label(
            text="Fight 4",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.7085}
        )
        layout.add_widget(fight4)

        self.category_spinner6 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.72},
            self.update_items6
        )
        layout.add_widget(self.category_spinner6)

        self.item_spinner6 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.697}
        )
        layout.add_widget(self.item_spinner6)

        self.category_spinner7 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.72},
            self.update_items7
        )
        layout.add_widget(self.category_spinner7)

        self.item_spinner7 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.697}
        )
        layout.add_widget(self.item_spinner7)

# Fight 5 --------------------------------------------------------------------------
        fight4 = Label(
            text="Fight 5",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.6535}
        )
        layout.add_widget(fight4)

        self.category_spinner8 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.665},
            self.update_items8
        )
        layout.add_widget(self.category_spinner8)

        self.item_spinner8 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.642}
        )
        layout.add_widget(self.item_spinner8)

        self.category_spinner9 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.665},
            self.update_items9
        )
        layout.add_widget(self.category_spinner9)

        self.item_spinner9 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.642}
        )
        layout.add_widget(self.item_spinner9)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        prelims_label = Label(
            text="Prelims",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.62}
        )
        layout.add_widget(prelims_label)

        # Prelim Fight 1 (Fight 6)
        fight6_label = Label(
            text="Fight 6",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.5835} # Adjusted position
        )
        layout.add_widget(fight6_label)

        self.category_spinner10 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.595}, # Adjusted position
            self.update_items10
        )
        layout.add_widget(self.category_spinner10)

        self.item_spinner10 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.572} # Adjusted position
        )
        layout.add_widget(self.item_spinner10)

        self.category_spinner11 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.595}, # Adjusted position
            self.update_items11
        )
        layout.add_widget(self.category_spinner11)

        self.item_spinner11 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.572} # Adjusted position
        )
        layout.add_widget(self.item_spinner11)

        # Prelim Fight 2 (Fight 7)
        fight7_label = Label(
            text="Fight 7",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.5285} # Adjusted position
        )
        layout.add_widget(fight7_label)

        self.category_spinner12 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.54}, # Adjusted position
            self.update_items12
        )
        layout.add_widget(self.category_spinner12)

        self.item_spinner12 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.517} # Adjusted position
        )
        layout.add_widget(self.item_spinner12)

        self.category_spinner13 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.54}, # Adjusted position
            self.update_items13
        )
        layout.add_widget(self.category_spinner13)

        self.item_spinner13 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.517} # Adjusted position
        )
        layout.add_widget(self.item_spinner13)

        # Prelim Fight 3 (Fight 8)
        fight8_label = Label(
            text="Fight 8",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.4735} # Adjusted position
        )
        layout.add_widget(fight8_label)

        self.category_spinner14 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.485}, # Adjusted position
            self.update_items14
        )
        layout.add_widget(self.category_spinner14)

        self.item_spinner14 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.462} # Adjusted position
        )
        layout.add_widget(self.item_spinner14)

        self.category_spinner15 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.485}, # Adjusted position
            self.update_items15
        )
        layout.add_widget(self.category_spinner15)

        self.item_spinner15 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.462} # Adjusted position
        )
        layout.add_widget(self.item_spinner15)

        # Prelim Fight 4 (Fight 9)
        fight9_label = Label(
            text="Fight 9",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.4185} # Adjusted position
        )
        layout.add_widget(fight9_label)

        self.category_spinner16 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.43}, # Adjusted position
            self.update_items16
        )
        layout.add_widget(self.category_spinner16)

        self.item_spinner16 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.407} # Adjusted position
        )
        layout.add_widget(self.item_spinner16)

        self.category_spinner17 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.43}, # Adjusted position
            self.update_items17
        )
        layout.add_widget(self.category_spinner17)

        self.item_spinner17 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.407} # Adjusted position
        )
        layout.add_widget(self.item_spinner17)

        # Prelim Fight 5 (Fight 10)
        fight10_label = Label(
            text="Fight 10",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5, 'top': 0.3635} # Adjusted position
        )
        layout.add_widget(fight10_label)

        self.category_spinner18 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.2, 'top': 0.375}, # Adjusted position
            self.update_items18
        )
        layout.add_widget(self.category_spinner18)

        self.item_spinner18 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.2, 'top': 0.352} # Adjusted position
        )
        layout.add_widget(self.item_spinner18)

        self.category_spinner19 = self.make_spinner(
            'Select Weightclass',
            list(self.data.keys()),
            {'center_x': 0.8, 'top': 0.375}, # Adjusted position
            self.update_items19
        )
        layout.add_widget(self.category_spinner19)

        self.item_spinner19 = self.make_spinner(
            'Select Fighter',
            [],
            {'center_x': 0.8, 'top': 0.352} # Adjusted position
        )
        layout.add_widget(self.item_spinner19)

        self.result_label = Label(
            text="Select fighters and simulate!",
            font_size=28,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(400, 40),
            pos_hint={'center_x': 0.5, 'top': 0.19} 
        )
        layout.add_widget(self.result_label)

        self.payout_label = Label(
            text="Total Fighter Payout: $0",
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(400, 40),
            pos_hint={'center_x': 0.5, 'top': 0.15}
        )
        layout.add_widget(self.payout_label)

        simulate_btn = Button(
            text="Simulate Fight",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'top': 0.05}
        )
        simulate_btn.bind(on_press=self.simulate_fight)
        layout.add_widget(simulate_btn)

        start_new_btn = Button(
            text="New Card",
            size_hint=(None, None),
            size=(150, 60),
            font_size=20,
            background_color=(0, 1, 0, 1), 
            pos_hint={'center_x': 0.1, 'top': 0.98}
        )
        start_new_btn.bind(on_press=self.start_new)
        layout.add_widget(start_new_btn)

        #connecting fighter payout to the screen
        self.item_spinner.bind(text=self.update_total_payout)
        self.item_spinner1.bind(text=self.update_total_payout)
        self.item_spinner2.bind(text=self.update_total_payout)
        self.item_spinner3.bind(text=self.update_total_payout)
        self.item_spinner4.bind(text=self.update_total_payout)
        self.item_spinner5.bind(text=self.update_total_payout)
        self.item_spinner6.bind(text=self.update_total_payout)
        self.item_spinner7.bind(text=self.update_total_payout)
        self.item_spinner8.bind(text=self.update_total_payout)
        self.item_spinner9.bind(text=self.update_total_payout)
        self.item_spinner10.bind(text=self.update_total_payout)
        self.item_spinner11.bind(text=self.update_total_payout)
        self.item_spinner12.bind(text=self.update_total_payout)
        self.item_spinner13.bind(text=self.update_total_payout)
        self.item_spinner14.bind(text=self.update_total_payout)
        self.item_spinner15.bind(text=self.update_total_payout)
        self.item_spinner16.bind(text=self.update_total_payout)
        self.item_spinner17.bind(text=self.update_total_payout)
        self.item_spinner18.bind(text=self.update_total_payout)
        self.item_spinner19.bind(text=self.update_total_payout)
    
        
        scroll.add_widget(layout)
        self.add_widget(scroll)


        

    def name_card(self,instance):
        self.text1 = instance.text
        self.layout.remove_widget(instance)
        global label12
        label12 = Label(text= self.text1,pos_hint={'center_x': 0.5, 'top': 0.96},font_size=32,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 40),)
        self.layout.add_widget(label12)

    
    def update_money_label(self, instance):
        self.layout.remove_widget(instance)
        try:
            with open(self.db_FILE, 'r') as f:
                money_data = json.load(f)
            money = money_data.get(self.current_user, {}).get("Money", 0)
        except Exception:
            money = 0

        self.money_label = Label(
            text=f"Current Money ${money}",
            font_size=25,
            color=(0, 1, 0, 1),
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'top': 0.94}
        )
        self.layout.add_widget(self.money_label)
        
    def update_money_shown(self):
        try:
            with open(self.db_FILE, 'r') as f:
                money_data = json.load(f)
            money = money_data.get(self.current_user, {}).get("Money", 0)
        except Exception:
            money = 0
        self.money_label.text = f"Current Money ${money}"

    def start_new(self, instance):
        try:
            self.result_label.text = ""
        except WidgetException:
            pass

        try:
            self.layout.add_widget(self.payout_label)
        except WidgetException:
            pass
        try:
            self.layout.remove_widget(label12)
        except (WidgetException,NameError):
            pass
        try:
            self.layout.add_widget(main_card)
        except WidgetException:
            pass

        spinner_pairs = [
        (self.category_spinner, self.item_spinner),
        (self.category_spinner1, self.item_spinner1),
        (self.category_spinner2, self.item_spinner2),
        (self.category_spinner3, self.item_spinner3),
        (self.category_spinner4, self.item_spinner4),
        (self.category_spinner5, self.item_spinner5),
        (self.category_spinner6, self.item_spinner6),
        (self.category_spinner7, self.item_spinner7),
        (self.category_spinner8, self.item_spinner8),
        (self.category_spinner9, self.item_spinner9),
        (self.category_spinner10, self.item_spinner10),
        (self.category_spinner11, self.item_spinner11),
        (self.category_spinner12, self.item_spinner12),
        (self.category_spinner13, self.item_spinner13),
        (self.category_spinner14, self.item_spinner14),
        (self.category_spinner15, self.item_spinner15),
        (self.category_spinner16, self.item_spinner16),
        (self.category_spinner17, self.item_spinner17),
        (self.category_spinner18, self.item_spinner18),
        (self.category_spinner19, self.item_spinner19),
        ]

        for cat_spinner, item_spinner in spinner_pairs:
            try:
                cat_spinner.text = "Select Weightclass"
            except WidgetException:
                pass
            try:
                item_spinner.text = "Select Fighter"
            except WidgetException:
                pass

        
        



    
    def simulate_fight(self, instance):
        global fighter_data_users
        fighter_data_users = load_users_fighters()

        if self.current_user and self.current_user in fighter_data_users:
            global fighter_data1
            fighter_data1 = fighter_data_users[self.current_user]["fighters"]
        

        fighter1 = fighter_data1.get(self.item_spinner.text)
        fighter2 = fighter_data1.get(self.item_spinner1.text)
        fighter3 = fighter_data1.get(self.item_spinner2.text)
        fighter4 = fighter_data1.get(self.item_spinner3.text)
        fighter5 = fighter_data1.get(self.item_spinner4.text)
        fighter6 = fighter_data1.get(self.item_spinner5.text)
        fighter7 = fighter_data1.get(self.item_spinner6.text)
        fighter8 = fighter_data1.get(self.item_spinner7.text)
        fighter9 = fighter_data1.get(self.item_spinner8.text)
        fighter10 = fighter_data1.get(self.item_spinner9.text)
        fighter11 = fighter_data1.get(self.item_spinner10.text)
        fighter12 = fighter_data1.get(self.item_spinner11.text)
        fighter13 = fighter_data1.get(self.item_spinner12.text)
        fighter14 = fighter_data1.get(self.item_spinner13.text)
        fighter15 = fighter_data1.get(self.item_spinner14.text)
        fighter16 = fighter_data1.get(self.item_spinner15.text)
        fighter17 = fighter_data1.get(self.item_spinner16.text)
        fighter18 = fighter_data1.get(self.item_spinner17.text)
        fighter19 = fighter_data1.get(self.item_spinner18.text)
        fighter20 = fighter_data1.get(self.item_spinner19.text)



        if not all([fighter1, fighter2, fighter3, fighter4, fighter5, fighter6, fighter7, fighter8, fighter9, fighter10,
                    fighter11, fighter12, fighter13, fighter14, fighter15, fighter16, fighter17, fighter18, fighter19, fighter20]):
            self.result_label.text = "Please select fighters for all matchups."
            return
        
        match = Match(fighter1, fighter2)
        match1 = Match(fighter3, fighter4)
        match2 = Match(fighter5, fighter6)
        match3 = Match(fighter7, fighter8)
        match4 = Match(fighter9, fighter10)
        match5 = Match(fighter11, fighter12)
        match6 = Match(fighter13, fighter14)
        match7 = Match(fighter15, fighter16)
        match8 = Match(fighter17, fighter18)
        match9 = Match(fighter19, fighter20)
        self.layout.remove_widget(self.payout_label)


        event= Event(f'{self.text1}')
        event.add_match(match)
        event.add_match(match1)
        event.add_match(match2)
        event.add_match(match3)
        event.add_match(match4)
        event.add_match(match5)
        event.add_match(match6)
        event.add_match(match7)
        event.add_match(match8)
        event.add_match(match9)
        event.run_event()
        revenue = event.get_revenue()
        summary = event.event_summary()
        global users
        users = load_users()
        if self.current_user and self.current_user in users:
            if "event" not in users[self.current_user]:
                users[self.current_user]["event"] = []
            users[self.current_user]["event"].append({
                "name": self.text1,
                "summary": summary
            })
            save_users(users)
        self.result_label.text = f"{summary}"
        
        if self.current_user and self.current_user in fighter_data_users:
            fighter_data_users[self.current_user]["fighters"] = fighter_data1
        save_users_fighters(fighter_data_users)


        reload = load_users()
        if self.current_user and self.current_user in reload:
            contracts = reload[self.current_user]["contracts"]
            money = reload.get(self.current_user).get("Money")
            new_money = int(money) + int(revenue)
            print(revenue)
            print(money)
            print(new_money)
            reload[self.current_user]["Money"] = new_money
            for fighter in contracts:
                popularity = fighter_data1.get(fighter, {}).get('popularity', 0)
                if popularity <= 25:
                    contracts[fighter] = "20000"
                elif popularity > 25 and popularity <= 40:
                    contracts[fighter] = "100000"
                elif popularity > 40 and popularity <= 60:
                    contracts[fighter] = "300000"
                elif popularity > 60 and popularity <= 70:
                    contracts[fighter] = "500000"
                elif popularity > 70 and popularity <= 80:
                    contracts[fighter] = "800000"
                elif popularity > 80 and popularity <= 85:
                    contracts[fighter] = "1000000"
                elif popularity > 85 and popularity <= 90:
                    contracts[fighter] = "2000000"
                elif popularity > 90 and popularity <= 95:
                    contracts[fighter] = "3000000"
                else:
                    contracts[fighter] = "4000000"
            save_users(reload)
            self.update_money_shown()


        

             


        
        
    def update_total_payout(self, *args):
        # Get all selected fighter names from the spinners
        fighter_names = [
            self.item_spinner.text, self.item_spinner1.text, self.item_spinner2.text, self.item_spinner3.text,
            self.item_spinner4.text, self.item_spinner5.text, self.item_spinner6.text, self.item_spinner7.text,
            self.item_spinner8.text, self.item_spinner9.text, self.item_spinner10.text, self.item_spinner11.text,
            self.item_spinner12.text, self.item_spinner13.text, self.item_spinner14.text, self.item_spinner15.text,
            self.item_spinner16.text, self.item_spinner17.text, self.item_spinner18.text, self.item_spinner19.text
        ]
        global total_fighter_pay
        users = load_users()
        total_fighter_pay = 0
        if self.current_user and self.current_user in users:
            contracts = users[self.current_user].get("contracts", {})
            for name in fighter_names:
                payout_str = contracts.get(name)
                if payout_str and payout_str.isdigit():
                    total_fighter_pay += int(payout_str)
        self.payout_label.text = f"Total Fighter Payout: ${total_fighter_pay:,}"

    def switch_to_history(self, *args):
        self.manager.get_screen('history').current_user = self.current_user
        self.manager.current = 'history'

    def switch_to_contracts(self, *args):
        self.manager.get_screen('contracts').current_user = self.current_user
        self.manager.current = 'contracts'
    
    def update_items(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner.values = items
            self.item_spinner.text = items[0]  # default select first item
        else:
            self.item_spinner.values = []
            self.item_spinner.text = 'No items'

    def update_items1(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner1.values = items
            self.item_spinner1.text = items[0]  # default select first item
        else:
            self.item_spinner1.values = []
            self.item_spinner1.text = 'No items'

    def update_items2(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner2.values = items
            self.item_spinner2.text = items[0]  # default select first item
        else:
            self.item_spinner2.values = []
            self.item_spinner2.text = 'No items'
    
    def update_items3(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner3.values = items
            self.item_spinner3.text = items[0]  # default select first item
        else:
            self.item_spinner3.values = []
            self.item_spinner3.text = 'No items'
    def update_items4(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner4.values = items
            self.item_spinner4.text = items[0]  # default select first item
        else:
            self.item_spinner4.values = []
            self.item_spinner4.text = 'No items'
    def update_items5(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner5.values = items
            self.item_spinner5.text = items[0]  # default select first item
        else:
            self.item_spinner5.values = []
            self.item_spinner5.text = 'No items'
    def update_items6(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner6.values = items
            self.item_spinner6.text = items[0]  # default select first item
        else:
            self.item_spinner6.values = []
            self.item_spinner6.text = 'No items'

    def update_items7(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner7.values = items
            self.item_spinner7.text = items[0]  # default select first item
        else:
            self.item_spinner7.values = []
            self.item_spinner7.text = 'No items'

    def update_items8(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner8.values = items
            self.item_spinner8.text = items[0]  # default select first item
        else:
            self.item_spinner8.values = []
            self.item_spinner8.text = 'No items'
    def update_items9(self, spinner, text):
        # Update second spinner options based on first spinner choice
        items = self.data.get(text, [])
        if items:
            self.item_spinner9.values = items
            self.item_spinner9.text = items[0]  # default select first item
        else:
            self.item_spinner9.values = []
            self.item_spinner9.text = 'No items'
    
    def update_items10(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner10.values = items
            self.item_spinner10.text = items[0]
        else:
            self.item_spinner10.values = []
            self.item_spinner10.text = 'No items'

    def update_items11(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner11.values = items
            self.item_spinner11.text = items[0]
        else:
            self.item_spinner11.values = []
            self.item_spinner11.text = 'No items'

    def update_items12(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner12.values = items
            self.item_spinner12.text = items[0]
        else:
            self.item_spinner12.values = []
            self.item_spinner12.text = 'No items'

    def update_items13(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner13.values = items
            self.item_spinner13.text = items[0]
        else:
            self.item_spinner13.values = []
            self.item_spinner13.text = 'No items'

    def update_items14(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner14.values = items
            self.item_spinner14.text = items[0]
        else:
            self.item_spinner14.values = []
            self.item_spinner14.text = 'No items'

    def update_items15(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner15.values = items
            self.item_spinner15.text = items[0]
        else:
            self.item_spinner15.values = []
            self.item_spinner15.text = 'No items'

    def update_items16(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner16.values = items
            self.item_spinner16.text = items[0]
        else:
            self.item_spinner16.values = []
            self.item_spinner16.text = 'No items'

    def update_items17(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner17.values = items
            self.item_spinner17.text = items[0]
        else:
            self.item_spinner17.values = []
            self.item_spinner17.text = 'No items'

    def update_items18(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner18.values = items
            self.item_spinner18.text = items[0]
        else:
            self.item_spinner18.values = []
            self.item_spinner18.text = 'No items'

    def update_items19(self, spinner, text):
        items = self.data.get(text, [])
        if items:
            self.item_spinner19.values = items
            self.item_spinner19.text = items[0]
        else:
            self.item_spinner19.values = []
            self.item_spinner19.text = 'No items'

    def on_press(self, instance):
        anim = Animation(size=(220, 50), duration=0.2)
        anim += Animation(size=(200, 44), duration=0.2)
        anim.start(instance)
    
    def make_spinner(self, text, values, pos, on_text=None):
        spinner = Spinner(
            text=text,
            values=values,
            background_normal='',
            background_down='',
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint=pos
        )
        if on_text:
            spinner.bind(text=on_text)
        spinner.bind(on_press=self.on_press)
        return spinner