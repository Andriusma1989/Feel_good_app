#importing all the necessary objects from Kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
from datetime import datetime
import glob
from pathlib import Path
import random

Builder.load_file('design.kv')

#creating empty classes with the same name as the rules in the design file
class LoginScreen(Screen):
# creating a function for sign up
    def sign_up(self):
        # switching between screens
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        #condition to check if the username and password matches  in the json file
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        #if the first condition is wrong, I'a assinging text
        else:
        #self is pointing the class we are using
            self.ids.login_wrong.text = "Wrong username or password!"



class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
    # opening users file and loading users info to the file
        with open("users.json") as file:
            users = json.load(file)
         # assining dictionary for users input
        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%y-%m-%d %H-%M-%S")}
        #overwritting users file and adding new users dictionary
        with open("users.json", 'w') as file:
            json.dump(users, file)
         # switching between screens
        self.manager.current = "sign_up_screen_success"
#creating class for sighn up screen
class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        #changing transition direction
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_screen"

#creating class for log in screen
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "Login_screen"
    def get_quote(self, feel):
        feel = feel.lower()
        available_feeling = glob.glob("quotes/*txt")


        available_feeling = [Path(filename).stem for filename in
                             available_feeling]
        # I am checking if feel is in the name of a txt file
        if feel in available_feeling:
            with open(f"quotes/{feel}.txt",encoding="utf-8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"
            #print(random.choice(quotes))

class ImageButton(ButtonBehavior, HoverBehavior, Image ):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()

#calling main app class,
if __name__ == "__main__":
    MainApp().run()