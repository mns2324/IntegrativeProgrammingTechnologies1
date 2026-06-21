import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty

KV = """
BoxLayout:
    orientation: "vertical"
    padding: 20
    spacing: 10

    TextInput:
        id: fullname
        hint_text: "Full Name"

    TextInput:
        id: username
        hint_text: "Username"

    TextInput:
        id: password
        hint_text: "Password"
        password: True

    TextInput:
        id: contact
        hint_text: "Contact"

    TextInput:
        id: address
        hint_text: "Address"

    Button:
        text: "Register"
        on_press: app.register_user()

    Label:
        id: result
        text: ""
"""
class RegisterApp(App):
    def build(self):
        return Builder.load_string(KV)
    
    def register_user(self):
        threading.Thread(
            target=self.send_registration,
            daemon=True
        ).start()
        
    def update_result(self, message):
        self.root.ids.result.text = message
    
    def send_registration(self):
        url = "http://192.168.254.103:21497/Register.aspx"

        data = {
            "fullname": self.root.ids.fullname.text,
            "username": self.root.ids.username.text,
            "password": self.root.ids.password.text,
            "contact": self.root.ids.contact.text,
            "address": self.root.ids.address.text
        }

        try:
            response = requests.post(
                url, # send to iis aspx file
                data=data, # send the dict
                timeout=10 
            )

            if response.status_code == 200:
                Clock.schedule_once(
                    lambda dt: self.update_result(response.text)
                )

            else:
                Clock.schedule_once(
                    lambda dt: self.update_result("Server Error")
                )

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            Clock.schedule_once(
                lambda dt: self.update_result(error_msg)
            )   

# don't forget to have register.aspx running before running this file
RegisterApp().run()
