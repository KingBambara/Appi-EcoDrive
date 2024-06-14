import kivy.uix.image
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image
import os
import pickle
import numpy as np
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.scatter import Scatter
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.app import MDApp
from kivy.lang import Builder
from navigation_drawer13 import navigation_helper
from kivy.uix.image import Image
from kivy_garden.mapview import MapView
Window.size = (300, 500)

class PredictionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "10dp"
        self.spacing = "10dp"

        # Charger le modèle XGBoost
        with open('model.pickle', 'rb') as f:
            self.model = pickle.load(f)

        # Définir les options du menu déroulant pour le type de carburant
        self.fuel_type = ""
        self.menu_items = [
            {"viewclass": "OneLineListItem", "text": "Diesel", "on_release": lambda x="Diesel": self.set_fuel_type(x)},
            {"viewclass": "OneLineListItem", "text": "Ethanol", "on_release": lambda x="Ethanol": self.set_fuel_type(x)},
            {"viewclass": "OneLineListItem", "text": "Regular Gazoline", "on_release": lambda x="Regular Gazoline": self.set_fuel_type(x)},
            {"viewclass": "OneLineListItem", "text": "Premium Gazoline", "on_release": lambda x="Premium Gazoline": self.set_fuel_type(x)},
        ]

        self.fuel_type_button = MDRaisedButton(
            text="Select Fuel Type",
            on_release=self.open_fuel_menu
        )

        self.ids = {
            'engine_size_input': MDTextField(hint_text="Engine Size", mode="rectangle", icon_right="engine", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)),
            'cylinders_input': MDTextField(hint_text="Cylinders", mode="rectangle", icon_right="numeric", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)),
            'fuel_consumption_input': MDTextField(hint_text="Fuel Consumption", mode="rectangle", icon_right="gas-station", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)),
            'fuel_type_button': self.fuel_type_button,
            'kilometers_input': MDTextField(hint_text="Kilometers", mode="rectangle", icon_right="road-variant", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1))
        }
        self.menu = MDDropdownMenu(
            caller=self.fuel_type_button,
            items=self.menu_items,
            width_mult=4,
            max_height=200  # Set a maximum height for the dropdown menu
        )

        # Définir les filtres d'entrée pour chaque champ de texte
        self.ids['engine_size_input'].input_filter = "float"
        self.ids['cylinders_input'].input_filter = "int"
        self.ids['fuel_consumption_input'].input_filter = "float"
        self.ids['kilometers_input'].input_filter = "float"

    def open_fuel_menu(self):
        # Ajuster la position pour que le menu ne disparaisse pas à gauche ou à droite
        caller = self.ids['fuel_type_button']
        window_width = Window.size[0]

        if caller.center_x + self.menu.width / 2 > window_width:
            self.menu.position = 'center'
        else:
            self.menu.position = 'auto'

        self.menu.caller = caller  # Ensure the menu is attached to the correct widget
        self.menu.open()

    def set_fuel_type(self, fuel_type):
        self.fuel_type = fuel_type
        self.ids['fuel_type_button'].text = fuel_type
        self.menu.dismiss()
        fuel_type = self.fuel_type.lower()
    def make_prediction(self, *args):
        try:
            engine_size = float(self.ids['engine_size_input'].text)
            cylinders = int(self.ids['cylinders_input'].text)
            fuel_consumption = float(self.ids['fuel_consumption_input'].text)
            fuel_type = self.fuel_type.lower()
            kilometers = float(self.ids['kilometers_input'].text)

            if fuel_type not in ["diesel", "ethanol", "regular gazoline", "premium gazoline"]:
                self.show_prediction_result_dialog("Invalid Fuel Type", "Fuel Type must be one of the following: diesel, ethanol, regular gazoline, premium gazoline.")
                return

            features = [
                engine_size,
                cylinders,
                fuel_consumption,
                1 if fuel_type == "diesel" else 0,
                1 if fuel_type == "ethanol" else 0,
                1 if fuel_type == "regular gazoline" else 0,
                1 if fuel_type == "premium gazoline" else 0
            ]

            # Load the model and make a prediction
            with open('model.pickle', 'rb') as f:
                model = pickle.load(f)
            prediction = model.predict(np.array(features).reshape(1, -1))[0]

            total_emission = prediction * kilometers

            if kilometers > 10:
                message = ("Given the distance you intend to travel, you have a long trip ahead. We recommend the following simple practices to reduce your carbon footprint:\n"
                          "1.Drive smoothly: Avoid rapid acceleration and braking, and maintain a steady speed.\n"
                          "2.Regularly service your car and check  tire pressure.\n"
                          "3.Check tire pressure often.\n"
                          "4.Use public transport when possible.\n")

            else:
                message = (
                    "Given the distance you have entered, which is relatively short, we recommend the following simple practices to reduce your carbon footprint:\n"
                     "1.Walk or bike whenever possible.\n"
                     "2.Try electric bikes or scooters.\n"
                     "3.Consider electric vehicles.\n"
                     "4.lan walking routes efficiently for multiple stops.\n"


                )

            self.show_dialog( f"C02 Emission: {total_emission:.2f} g.\n\n{message}")


        except ValueError:
            self.show_dialog("Veuillez entrer des valeurs numériques valides pour toutes les caractéristiques.")

    def show_dialog(self, message):
        dialog6 = MDDialog(
            title="Your car carbonfootprint",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="Close",
                    md_bg_color="darkgreen",
                    on_release=lambda x: dialog6.dismiss()
                ),
            ],
            auto_dismiss=False
        )
        dialog6.open()


class FuelTypeDropDown(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        fuel_types = ["Diesel", "Ethanol", "Regular Gazoline", "Premium Gazoline"]
        for fuel_type in fuel_types:
            btn = OneLineListItem(text=fuel_type)
            btn.bind(on_release=lambda btn: self.select(btn.text))
            self.add_widget(btn)




class ProfileContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        self.size_hint_y = None
        self.height = dp(400)

        self.new_username = MDTextField(
            hint_text="New Username", mode="rectangle", icon_right="account", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)
        )
        self.new_password = MDTextField(
            hint_text="New Password", password=True, mode="rectangle", icon_right="lock", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)
        )
        self.engine_size = MDTextField(
            hint_text="Engine Size", mode="rectangle", input_filter="float", icon_right="engine", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)
        )
        self.cylinders = MDTextField(
            hint_text="Cylinders", mode="rectangle", input_filter="int", icon_right="numeric", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)
        )
        self.fuel_consumption = MDTextField(
            hint_text="Fuel Consumption", mode="rectangle", input_filter="float", icon_right="gas-station", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)
        )
        self.fuel_type = Spinner(
            text='Fuel Type',
            values=["Diesel", "Ethanol", "Regular Gazoline", "Premium Gazoline"],
            background_color=(0, 0.5, 0, 1),  # Dark green background
            background_normal= '',
            background_down= '',
            color= (1, 1, 1, 1) # White text
        )

        self.add_widget(self.new_username)
        self.add_widget(self.new_password)
        self.add_widget(self.engine_size)
        self.add_widget(self.cylinders)
        self.add_widget(self.fuel_consumption)
        self.add_widget(self.fuel_type)



class PredictionContent(BoxLayout):
    def __init__(self, username, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        self.size_hint_y = None
        self.height = dp(400)
        self.ids = {
            'engine_size_input': MDTextField(hint_text="Engine Size", mode="rectangle", icon_right="engine", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)),
            'cylinders_input': MDTextField(hint_text="Cylinders", mode="rectangle", icon_right="numeric", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)),
            'fuel_consumption_input': MDTextField(hint_text="Fuel Consumption", mode="rectangle", icon_right="gas-station", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)),
            'fuel_type_input': MDTextField(hint_text="Fuel Type", mode="rectangle", readonly=True, icon_right="gas-station", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1)),
            'kilometers_input': MDTextField(hint_text="Kilometers", mode="rectangle", icon_right="road-variant", line_color_normal=(0, 0.5, 0, 1), text_color=(0, 0, 0, 1), hint_text_color=(0, 0, 0, 0.5), color_mode='custom', fill_color=(0, 0, 0, 0.1))
        }

        for key, widget in self.ids.items():
            self.add_widget(widget)

        self.result_label = MDLabel(text="", halign="center", font_style="H6", theme_text_color="Custom", text_color=(0, 0.5, 0, 1))  # Dark green text
        self.add_widget(self.result_label)

        self.add_widget(MDRaisedButton(
            text="Predict",
            md_bg_color=(0, 0.5, 0, 1),  # Dark green background
            text_color=(1, 1, 1, 1),  # White text
            on_release=self.make_prediction
        ))

        self.load_user_data()

    def load_user_data(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                users = f.readlines()
            for user in users:
                saved_username, _, engine_size, cylinders, fuel_consumption, fuel_type = user.strip().split(',')
                if saved_username == self.username:
                    self.ids['engine_size_input'].text = engine_size
                    self.ids['cylinders_input'].text = cylinders
                    self.ids['fuel_consumption_input'].text = fuel_consumption
                    self.ids['fuel_type_input'].text = fuel_type
                    break

    def show_prediction_result_dialog(self, title, message):
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(
                    text="CLOSE",
                    md_bg_color=(0, 0.5, 0, 1),  # Dark green background
                    text_color=(1, 1, 1, 1),  # White text
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def make_prediction(self, instance):
        try:
            engine_size = float(self.ids['engine_size_input'].text)
            cylinders = int(self.ids['cylinders_input'].text)
            fuel_consumption = float(self.ids['fuel_consumption_input'].text)
            fuel_type = self.ids['fuel_type_input'].text.lower()
            kilometers = float(self.ids['kilometers_input'].text)

            if fuel_type not in ["diesel", "ethanol", "regular gazoline", "premium gazoline"]:
                self.show_prediction_result_dialog("Invalid Fuel Type", "Fuel Type must be one of the following: diesel, ethanol, regular gazoline, premium gazoline.")
                return

            features = [
                engine_size,
                cylinders,
                fuel_consumption,
                1 if fuel_type == "diesel" else 0,
                1 if fuel_type == "ethanol" else 0,
                1 if fuel_type == "regular gazoline" else 0,
                1 if fuel_type == "premium gazoline" else 0
            ]

            # Load the model and make a prediction
            with open('model.pickle', 'rb') as f:
                model = pickle.load(f)
            prediction = model.predict(np.array(features).reshape(1, -1))[0]

            total_emission = prediction * kilometers

            if kilometers > 10:
                message = ("Given the distance you intend to travel, you have a long trip ahead. We recommend the following simple practices to reduce your carbon footprint:\n"
                          "1.Drive smoothly: Avoid rapid acceleration and braking, and maintain a steady speed.\n"
                          "2.Regularly service your car and check  tire pressure.\n"
                          "3.Check tire pressure often.\n"
                          "4.Use public transport when possible.\n")

            else:
                message = (
                    "Given the distance you have entered, which is relatively short, we recommend the following simple practices to reduce your carbon footprint:\n"
                     "1.Walk or bike whenever possible.\n"
                     "2.Try electric bikes or scooters.\n"
                     "3.Consider electric vehicles.\n"
                     "4.lan walking routes efficiently for multiple stops.\n"


                )

            self.show_prediction_result_dialog("Your car carbonfootprint", f"C02 Emission: {total_emission:.2f} g.\n\n{message}")

        except ValueError:
            self.show_prediction_result_dialog("Invalid Input", "All input fields must be filled with valid values.")
        except FileNotFoundError:
            self.show_prediction_result_dialog("Model Not Found", "Model file not found. Please ensure 'model.pickle' is available.")
        except Exception as e:
            self.show_prediction_result_dialog("Error", f"An error occurred: {str(e)}")



class EcoDrive(MDApp):
    dialog = None
    dialog1 = None
    dialog2 = None
    dialog3 = None
    dialog5 = None
    dialog4 = None
    dialog6 = None
    dialog7 = None
    drop_item_menu = None

    class ContentNavigationDrawer(BoxLayout):
        pass

    class DrawerList(MDList, ThemableBehavior):
        pass

    def build(self):
        return Builder.load_string(navigation_helper)
        self.theme_cls.accent_color = "green"
        return PredictionScreen()

    def login(self, username, password):
        if not username or not password:
            self.show_dialog("Login Failed", "Please enter your username and password.")
            return

        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                users = f.readlines()
            for user in users:
                saved_username, saved_password, *_ = user.strip().split(',')
                if saved_username == username:
                    if saved_password == password:
                        self.show_prediction_dialog(username)
                        return
                    else:
                        self.show_dialog("Login Failed", "Incorrect password")
                        return
            self.show_dialog("Login Failed", "User not found")
        else:
            self.show_dialog("Login Failed", "No users found. Please create a profile.")

    def show_create_profile_dialog(self):
        self.dialog4 = MDDialog(
            title="Create Profile",
            type="custom",
            content_cls=ProfileContent(),
            size_hint=(0.9, 0.9),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    text_color=(0, 0.5, 0, 1),  # Dark green text
                    on_release=lambda x: self.dialog4.dismiss()
                ),
                MDFlatButton(
                    text="SAVE",
                    text_color=(0, 0.5, 0, 1),  # Dark green text
                    on_release=self.save_profile
                ),
            ]
        )
        self.dialog4.open()

    def show_prediction_dialog(self, username):
        self.dialog5 = MDDialog(
            title="Prediction",
            type="custom",
            content_cls=PredictionContent(username),
            size_hint=(0.9, 0.9),
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    text_color=(0, 0.5, 0, 1),  # Dark green text
                    on_release=lambda x: self.dialog5.dismiss()
                )
            ]
        )
        self.dialog5.open()

    def save_profile(self, instance):
        content = self.dialog4.content_cls
        username = content.new_username.text
        password = content.new_password.text
        engine_size = content.engine_size.text
        cylinders = content.cylinders.text
        fuel_consumption = content.fuel_consumption.text
        fuel_type = content.fuel_type.text.lower()

        print(f"Saving profile for {username} with password {password}")
        print(f"Engine Size: {engine_size}, Cylinders: {cylinders}, Fuel Consumption: {fuel_consumption}, Fuel Type: {fuel_type}")

        if not all([username, password, engine_size, cylinders, fuel_consumption, fuel_type]):
            self.show_dialog("Profile Creation Failed", "All fields must be filled out.")
            return

        # Vérification que les champs sont numériques
        try:
            engine_size = float(engine_size)
            cylinders = int(cylinders)
            fuel_consumption = float(fuel_consumption)
        except ValueError:
            self.show_dialog("Profile Creation Failed", "Engine Size, Cylinders, and Fuel Consumption must be numeric.")
            return

        # Vérification que le type de carburant est valide
        #valid_fuel_types = ["diesel", "ethanol  ", "regular gazoline", "premium gazoline"]
        #if fuel_type not in valid_fuel_types:
            #self.show_dialog("Profile Creation Failed", f"Fuel Type must be one of the following: {', '.join(valid_fuel_types)}.")
           # return

        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                users = f.readlines()
            for user in users:
                saved_username, *_ = user.strip().split(',')
                if saved_username == username:
                    self.show_dialog("Profile Creation Failed", "Username already exists. Please choose another one.")
                    return

        with open('users.txt', 'a') as f:
            f.write(f"{username},{password},{engine_size},{cylinders},{fuel_consumption},{fuel_type}\n")
        self.dialog4.dismiss()
        self.show_dialog("Profile Created", "Profile created successfully")

    def show_dialog(self, title, message):
        dialog3 = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    text_color=(0, 0.5, 0, 1),  # Dark green text
                    on_release=lambda x: dialog3.dismiss()
                )
            ]
        )
        dialog3.open()






    def Help(self):
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title='Help',
                text='Create your profile by entering your username, password, engine size, cylinders co, fuel consumption, and selecting your fuel type,If you prefer not to create a profile, you can simply use our direct calculator.',

                buttons=[
                    MDFlatButton(
                        text='CANCEL',
                        on_release=self.close_dialog1
                    ),
                ],
            )
        self.dialog1.open()

    def close_dialog1(self, *args):
        self.dialog1.dismiss(force=True)

    def contact_us(self):
        if not self.dialog2:
            self.dialog2 = MDDialog(
                title='Contact us',
                text='Manal Ait Azarine\n@:manal.ait-azarine@capgemini.com.\nMohamed Diarra\n@:mohamed.diarra@capgemini.com\n',
                buttons=[
                    MDFlatButton(
                        text='CANCEL',
                        on_release=self.close_dialog2
                    ),
                ],
            )
        self.dialog2.open()

    def close_dialog2(self, *args):
        self.dialog2.dismiss(force=True)




    def about_us(self):
         if not self.dialog:
            self.dialog = MDDialog(
                title='About us',
                text='EcoDrive is a mobile app that uses artificial intelligence to calculate your car''s carbon footprint. It helps you see how your driving impacts the environment and offers tips to reduce your emissions. Make greener choices and help protect the planet. ',
                buttons=[
                    MDFlatButton(
                        text='CANCEL',
                        on_release=self.close_dialog
                    ),
                ],
            )
         self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss(force=True)

    def logout(self):
        self.stop()

    def CO2(self):
        if not self.dialog7:
            self.dialog7 = MDDialog(
                title="what is a car carbonfootrprint? ",
                text="A car's carbon footprint is the total amount of carbon dioxide (CO2) emissions produced by driving the vehicle. Calculating it helps drivers understand their contribution to climate change and identify ways to reduce their impact.By measuring and reducing our car's carbon footprint, we can help  protect the planet for future generations.",
                buttons=[
                    MDRaisedButton(
                        text="CLOSE",
                        md_bg_color=(0, 0.5, 0, 1),
                        on_release=self.close_dialog7
                    )
                ]
            )
        self.dialog7.open()

    def close_dialog7(self, *args):
        self.dialog7.dismiss()
if __name__ == "__main__":
    EcoDrive().run()
