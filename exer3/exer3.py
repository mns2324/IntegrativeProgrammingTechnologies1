# main.py
# pip install kivy requests

import requests
import threading
import mysql.connector
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image 
from kivy.graphics.texture import Texture

from ui_classes import ClickableRow, Divider, InputRow, CenterRow, ColoredBox, HeroLabel, Footer

# fruit recog imports
import cv2
import numpy as np
import json
import time
from keras.models import load_model
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # point to exer3/

DEBUG_MODE = 1

### main
class RecipeApp(App):
    def build(self):     
        self.all_meals = []
        self.loaded_countries = []
        self.loaded_meals = []
        self.selected_country = ""
        self.selected_ingredient = ""
        self.current_recipe_meal = None 
        self.fruitrecog_home_btn = None 
        
        # detection state
        self.model = load_model(os.path.join(BASE_DIR, 'fruit_recognition_model.h5'))
        with open(os.path.join(BASE_DIR, 'class_indices.json'), 'r') as f:
            self.fruit_classes = json.load(f)

        self.main_layout = BoxLayout(
            orientation="vertical"
        )

        self.content_area = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )
        self.footer = Footer()
        
        self.main_layout.add_widget(self.content_area)
        self.main_layout.add_widget(self.footer)
        
        if DEBUG_MODE == 1:
            self.logged_in_name = "Madeline"
            self.logged_in_role = "customer"
            self.user_id = 1
            self.display_home()
        elif DEBUG_MODE == 2:
            self.display_ingredient_details()
        else:
            self.display_login()

        return self.main_layout

    # global footer message
    def show_message(self, message, error=False):
        color = (1, 0.4, 0.4, 1) if error else (1, 1, 1, 1)

        if hasattr(self, "footer"):
            self.footer.set_message(message, color)

    # wrap text automatically (for paragraphs)
    def add_wrapped_label(self, text, font_size=16, bold=False, height=None, target=None):
        label = Label(
            text=text,
            font_size=font_size,
            bold=bold,
            size_hint_y=None,
            text_size=(700, None),
            halign="left",
            valign="top",
            color=(0.8, 0.8, 0.8, 1)
        )
     
        if height:
            label.height = height
        else:
            # use dynamic height if unspecified
            label.bind(
                texture_size=lambda instance, size:
                setattr(instance, "height", size[1] + 10)
            )

        # for scroll layout
        target.add_widget(label)
        return label

    def get_flag_url(self, country):
        flag_codes = {
            "American": "us",
            "Argentinian": "ar",
            "Australian": "au",
            "British": "gb",
            "Canadian": "ca",
            "Chinese": "cn",
            "Croatian": "hr",
            "Dutch": "nl",
            "Egyptian": "eg",
            "Filipino": "ph",
            "France": "fr",
            "Greek": "gr",
            "Indian": "in",
            "Irish": "ie",
            "Italian": "it",
            "Japanese": "jp",
            "Kenyan": "ke",
            "Malaysian": "my",
            "Mexican": "mx",
            "Moroccan": "ma",
            "Polish": "pl",
            "Portuguese": "pt",
            "Russian": "ru",
            "Spanish": "es",
            "Syrian": "sy",
            "Thai": "th",
            "Tunisian": "tn",
            "Turkish": "tr",
            "Vietnamese": "vn",
            "Jamaican": "jm",
            "Ukrainian": "ua",
            "Uruguayan": "uy"
        }

        code = flag_codes.get(country)
        return f"https://flagcdn.com/w80/{code}.png" if code else ""

    def display_login(self):
        """ 
        fruitapp label
        recognize. order. cook label
        username label + input box 
        password label + input box (password: True to hide text)
        login button
        "dont have an account? register" label (bind to redirect to display_register)
        """
        
        self.content_area.clear_widgets()
        login_box = BoxLayout(orientation="vertical",spacing=10,size_hint=(1, None))
        # makes the layout height grow depending on its contents  
        login_box.bind(minimum_height=login_box.setter("height"))
        
        title = HeroLabel(text="FruitApp", size_hint=(1, None), height=50)
        subtitle = Label(text="Recognize. Order. Cook.", font_size=16, size_hint=(1, None), height=25)

        self.username_input = TextInput(hint_text="Enter username", multiline=False, size_hint=(None, None), width=400, height=45)
        self.password_input = TextInput(hint_text="Enter password", multiline=False, password=True, size_hint=(None, None), width=400, height=45)

        login_btn = Button(text="Login", size_hint=(None, None), width=400, height=45)
        login_btn.bind(on_press=self.handle_login)

        self.result_label = Label(text="", size_hint=(1, None), height=30)

        register_label = Label(text="Don't have an account?", size_hint=(None, None), height=30)
        register_label.texture_update()
        register_label.width = register_label.texture_size[0]

        register_btn = Button(
            text="Register",
            size_hint=(None, None),
            height=30,
            width=80,
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=(0.1, 0.45, 0.2, 1),
            bold=True
        )
        register_btn.bind(on_press=lambda x: self.display_register())

        register_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=30, spacing=5)
        register_row.add_widget(Widget())
        register_row.add_widget(register_label)
        register_row.add_widget(register_btn)
        register_row.add_widget(Widget())

        for widget in [
            title,
            subtitle,
            CenterRow(InputRow("Username", self.username_input)),
            CenterRow(InputRow("Password", self.password_input)),
            CenterRow(login_btn),
            self.result_label,
            register_row
        ]:
            login_box.add_widget(widget)

        self.content_area.add_widget(Widget())
        self.content_area.add_widget(login_box)
        self.content_area.add_widget(Widget())
            
    ### verify input boxes before running send_login on new thread
    def handle_login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username:
            Clock.schedule_once(lambda x: self.update_result("Username cannot be empty"))
            return
        if not password:
            Clock.schedule_once(lambda x: self.update_result("Password cannot be empty"))
            return
        
        # same threading pattern as register
        threading.Thread(target=self.send_login, daemon=True).start()
    
    ### send login data to this aspx file
    def send_login(self):
        url = "http://localhost:21497/Login.aspx"
        data = {
            "username": self.username_input.text,
            "password": self.password_input.text
        }
        try:
            response = requests.post(url, data=data, timeout=10)
            
            # show success message if status code is 200 (success)
            if response.status_code == 200:
                rsp = response.text
                
                if rsp.startswith("OK:"):
                    # server returns "OK:user_id:fullname:role"
                    parts = rsp.split(":")
                    user_id = parts[1]
                    full_name = parts[2]
                    role = parts[3]
                    Clock.schedule_once(lambda x: self.on_login_success(user_id, full_name, role))
                else:
                    Clock.schedule_once(lambda x: self.update_result(rsp, success=False))
            else:
                Clock.schedule_once(lambda x: self.update_result("Server error", success=False))
        except Exception as e:
            error_msg = f"Error: {e}"
            Clock.schedule_once(lambda x: self.update_result(error_msg, success=False))

    # redirect to home page once login is successful
    def on_login_success(self, user_id, full_name, role):
        self.user_id = int(user_id)
        self.logged_in_name = full_name
        self.logged_in_role = role
        self.display_home()
        
    def display_register(self):
        """
        fullname label + input box 
        username label + input box 
        password label + input box (password: True to hide text)
        confirm password label + input box  (password: True to hide text)
        contact number label + input box 
        address label + input box 
        register button (pass credentials to iis -> aspx -> java -> mysql, look at sample.py)
        "already have an account? log in" label (bind to redirect to display_login)
        """      

        self.content_area.clear_widgets()

        register_box = BoxLayout(orientation="vertical",spacing=10,size_hint=(1, None))
        # makes the layout height grow depending on its contents 
        register_box.bind(minimum_height=register_box.setter("height"))

        title = HeroLabel(text="Register",size_hint=(1, None),height=60)

        self.fullname_input = TextInput(hint_text="Enter full name",    multiline=False,size_hint=(None, None),width=400,height=45)
        self.username_input = TextInput(hint_text="Enter username",     multiline=False,size_hint=(None, None),width=400,height=45)
        self.password_input = TextInput(hint_text="Enter password",     multiline=False,password=True,size_hint=(None, None),width=400,height=45)
        self.confirm_input = TextInput(hint_text="Confirm password",    multiline=False,password=True,size_hint=(None, None),width=400,height=45)
        self.contact_input = TextInput(hint_text="Enter contact number",multiline=False,size_hint=(None, None),width=400,height=45)
        self.address_input = TextInput(hint_text="Enter address",       multiline=False,size_hint=(None, None),width=400,height=45)

        register_btn = Button(
            text="Register",
            size_hint=(None, None),
            width=400,
            height=45
        )

        register_btn.bind(on_press=lambda x: self.register_user())

        self.result_label = Label(text="",size_hint=(1, None),height=30)

        login_label = Label(text="Already have an account?",size_hint=(None, None),height=30)
        login_label.texture_update()
        login_label.width = login_label.texture_size[0]

        login_btn = Button(
            text="Log in",
            size_hint=(None, None),
            width=60,
            height=30,
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=(0.1, 0.45, 0.2, 1),
            bold=True
        )

        login_btn.bind(
            on_press=lambda x: self.display_login()
        )

        login_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=30,
            spacing=5
        )

        login_row.add_widget(Widget())
        login_row.add_widget(login_label)
        login_row.add_widget(login_btn)
        login_row.add_widget(Widget())

        for widget in [
            title,
            CenterRow(InputRow("Full Name", self.fullname_input)),
            CenterRow(InputRow("Username", self.username_input)),
            CenterRow(InputRow("Password", self.password_input)),
            CenterRow(InputRow("Confirm Password", self.confirm_input)),
            CenterRow(InputRow("Contact Number", self.contact_input)),
            CenterRow(InputRow("Address", self.address_input)),
            CenterRow(register_btn),
            self.result_label,
            login_row
        ]:
            register_box.add_widget(widget)

        self.content_area.add_widget(Widget())
        self.content_area.add_widget(register_box)
        self.content_area.add_widget(Widget())
        
    # start a new thread to send the registration
    def register_user(self):
        threading.Thread(
            target=self.send_registration,
            daemon=True
        ).start()
        
    # status message updater for login/register
    def update_result(self, message, success=False):
        self.result_label.text = message
        self.result_label.color = (0, 1, 1, 1) if success else (1, 0.3, 0.3, 1)  # cyan or red
        
    def send_registration(self):
        url = "http://localhost:21497/Register.aspx"
        confirm = self.confirm_input.text
        pw = self.password_input.text
        
        if confirm != pw:
            Clock.schedule_once(
                lambda x: self.update_result("Confirm password must match password", success=False)
            )
            return
            
        data = {
            "fullname": self.fullname_input.text,
            "username": self.username_input.text,
            "password": self.password_input.text,
            "role":     "customer",
            "contact":  self.contact_input.text,
            "address":  self.address_input.text
        }

        try:
            response = requests.post(
                url, # send to iis aspx file
                data=data, # send the dict
                timeout=10 
            )

            # show success message if status code is 200 (success)
            if response.status_code == 200:
                rsp = response.text

                Clock.schedule_once(
                    lambda x: self.update_result(rsp, success=True)
                )

            else:
                Clock.schedule_once(
                    lambda x: self.update_result("Server Error", success=False)
                )

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            Clock.schedule_once(
                lambda x: self.update_result(error_msg, success=False)
            )      
    
    def display_home(self):
        """
        home label
        "hello, username!" label
        fruit recognition button (bind to redirect to display_fruitrecog)
        order fruits button (bind to redirect to display_orderfruits)
        your recent orders label
        show 3 most recent orders
        """  
        self.content_area.clear_widgets()
        self.footer.hide_footer()
        
        if getattr(self, "fruitrecog_home_btn", None) is not None:
            self.footer.remove_widget(self.fruitrecog_home_btn)
            self.fruitrecog_home_btn = None

        home_box = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(1, None)
        )
        
        # redirect to fruitrecog or order fruits
        options_box = ColoredBox(
            orientation="vertical",
            spacing=20,
            padding=12,
            size_hint=(None, None),
            width=300
        )
        
        recentorders_box = ColoredBox(
            orientation="vertical",
            spacing=20,
            padding=12,
            size_hint=(None, None),
            width=500
        )

        # makes the layout height grow depending on its contents 
        home_box.bind(minimum_height=home_box.setter("height"))
        options_box.bind(minimum_height=options_box.setter("height"))
        recentorders_box.bind(minimum_height=recentorders_box.setter("height"))

        title = HeroLabel(text="Home Page",size_hint=(1, None),height=60)
        hello = Label(text=f"Hello, {self.logged_in_name}!",size_hint=(1, None),height=40)

        options_label = Label(text="What would you like to do?",size_hint=(1, None),height=30)
        recog_btn = Button(text="Fruit Recognition",size_hint=(1, None),height=40)
        order_btn = Button(text="Order Fruits",size_hint=(1, None),height=40)   
        recog_btn.bind(on_press=lambda x: self.display_fruitrecog())
        order_btn.bind(on_press=lambda x: self.display_orderfruits())

        options_box.add_widget(options_label)
        options_box.add_widget(recog_btn)
        options_box.add_widget(order_btn)
        
        orders_label = Label(text="Your Recent Orders",size_hint=(None, None),height=30)
        orders_label.texture_update()
        orders_label.width = orders_label.texture_size[0]
        viewallorders_btn = Button(
            text="View All",
            size_hint=(None, None),
            height=30,
            width=80,
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=(0.1, 0.45, 0.2, 1),
            bold=True
        )
        viewallorders_btn.bind(on_press=lambda x: self.display_myorders())

        recentorders_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=30, spacing=5)
        recentorders_header.add_widget(Widget())
        recentorders_header.add_widget(orders_label)
        recentorders_header.add_widget(viewallorders_btn)
        recentorders_header.add_widget(Widget())

        recentorders_box.add_widget(recentorders_header)
        
        # fetch the 3 most recently placed orders for this user
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="fruitinventory"
        )
        cursor = db.cursor()
        cursor.execute(
            "SELECT order_id, order_date, total_amount, order_status "
            "FROM orders WHERE user_id = %s "
            "ORDER BY order_date DESC LIMIT 3",
            (self.user_id,)
        )
        recent_orders = cursor.fetchall()

        if not recent_orders:
            recentorders_box.add_widget(Label(text="No orders yet.", size_hint=(1, None), height=30))
        else:
            for order_id, order_date, total_amount, order_status in recent_orders:
                cursor.execute(
                    "SELECT f.fruit_name, f.image_path, oi.quantity "
                    "FROM order_items oi "
                    "JOIN fruits f ON oi.fruit_id = f.fruit_id "
                    "WHERE oi.order_id = %s",
                    (order_id,)
                )
                items = cursor.fetchall()
                recentorders_box.add_widget(
                    self.make_order_row(order_id, order_date, total_amount, order_status, items)
                )

        cursor.close()
        db.close()

        home_box.add_widget(title)
        home_box.add_widget(hello)
        home_box.add_widget(CenterRow(options_box))
        home_box.add_widget(CenterRow(recentorders_box))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(home_box)
        self.content_area.add_widget(scroll)
    
    ### order flow: order fruits -> confirm order page, place order -> my orders page showing pending orders (exer 2 admin dashboard will confirm)
    def display_orderfruits(self):
        """
        order fruits label
        select up to 3 fruits label (only the ones that were trained)
        apple image + label and price per pc
        calamansi image + label and price per pc
        lemon image + label and price per pc
        quantity label, +/- buttons for quantity
        subtotal price
        """     
        self.content_area.clear_widgets()
        self.footer.hide_footer()
        
        db = mysql.connector.connect(
            host="localhost",      # IP address of the PC with MySQL
            user="root",
            password="root",
            database="fruitinventory"
        )         
        cursor = db.cursor()
        cursor.execute("SELECT * FROM fruits")
        rows = cursor.fetchall()

        orderfruits_box = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(1, None)
        )

        # makes the layout height grow depending on its contents 
        orderfruits_box.bind(minimum_height=orderfruits_box.setter("height"))
        
        # top row: back button on the left
        top_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50
        )
        back_btn = Button(
            text="< Home",
            size_hint=(None, None),
            size=(100, 40)
        )
        back_btn.bind(on_release=lambda inst: self.display_home())
        top_row.add_widget(back_btn)
        top_row.add_widget(Widget())

        title = HeroLabel(text="Order Fruits",size_hint=(1, None),height=60)
        subtitle = Label(text="Order up to 3 fruits.",font_size=16,size_hint=(1, None),height=60)
        fruitsbox = ColoredBox(
            orientation="vertical",
            spacing=20,
            padding=12,
            size_hint=(None, None),
            width=400
        )
        fruitsbox.bind(minimum_height=fruitsbox.setter("height"))
        
        # store full info per fruit so checkout can build an order summary
        self.fruit_data = {}  # fruit_id -> {"name", "price", "qty_label"}
        
        for row_data in rows:
            fruit_id = row_data[0]
            fruit_name = row_data[1]
            price = row_data[3]
            stock_quantity = row_data[4]
            image_path = row_data[5]

            fruit_row, qty_label = self.make_fruit_row(fruit_name, price, image_path, stock_quantity)
            fruitsbox.add_widget(fruit_row)
            
            self.fruit_data[fruit_id] = {
                "name": fruit_name,
                "price": price,
                "qty_label": qty_label,
                "image_path": image_path
            }
        
        checkout_btn = Button(text="Proceed to Checkout",size_hint=(None, None),size=(200, 50))
        checkout_btn.bind(on_release=self.display_confirmorder)
        
        # bottom row: spacer pushes the button to the right
        checkout_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=60,
            padding=(0, 0, 12, 0)  # right padding so it's not glued to the edge
        )
        checkout_row.add_widget(Widget())       
        checkout_row.add_widget(checkout_btn)

        orderfruits_box.add_widget(top_row)
        orderfruits_box.add_widget(title)
        orderfruits_box.add_widget(subtitle)
        orderfruits_box.add_widget(CenterRow(fruitsbox))
        orderfruits_box.add_widget(checkout_row)
        
        self.content_area.add_widget(Widget())
        self.content_area.add_widget(orderfruits_box)
        self.content_area.add_widget(Widget())
    
    def make_fruit_row(self, name, price, image_path, stock_quantity):
        row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=80,
            spacing=10,
            padding=10
        )

        # Left: fruit image
        img = Image(
            source=image_path,
            size_hint=(None, None),
            size=(60, 60)
        )

        # Middle: name + price + stock quantity, stacked vertically
        info_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1)
        )
        name_label = Label(text=name, font_size=18, halign="left", valign="middle")
        price_label = Label(text=f"{price:.2f} / pc", font_size=14, halign="left", valign="middle")

        if stock_quantity > 5:
            stock_text = f"Stock: {stock_quantity}"
            stock_color = (1, 1, 1, 1)  # normal/white
        elif stock_quantity > 0:
            stock_text = f"Stock: {stock_quantity}"
            stock_color = (0.8, 0.8, 0.1, 1)  # yellow
        else:
            stock_text = "Out of stock"
            stock_color = (1, 0.3, 0.3, 1)  # reddish

        stock_label = Label(
            text=stock_text,
            font_size=14,
            halign="left",
            valign="middle",
            color=stock_color
        )
            
        # bind text_size so halign actually left-aligns instead of centering
        for label in (name_label, price_label, stock_label):
            label.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        info_box.add_widget(name_label)
        info_box.add_widget(price_label)
        info_box.add_widget(stock_label)
        
        # Right: quantity controls
        qty_box = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(140, 40),
            spacing=5
        )

        qty_label = Label(text="0", size_hint=(None, None), size=(40, 40))
        def decrease(instance, qty_label=qty_label):
            current = int(qty_label.text)
            if current > 0:
                qty_label.text = str(current - 1)
        def increase(instance, qty_label=qty_label):
            current = int(qty_label.text)
            if current < stock_quantity: 
                qty_label.text = str(current + 1)

        minus_btn = Button(text="-", size_hint=(None, None), size=(40, 40))
        minus_btn.bind(on_release=decrease)
        plus_btn = Button(text="+", size_hint=(None, None), size=(40, 40))
        plus_btn.bind(on_release=increase)
    
        # disable ordering if fruit is out of stock
        if stock_quantity <= 0:
            minus_btn.disabled = True
            plus_btn.disabled = True

        qty_box.add_widget(minus_btn)
        qty_box.add_widget(qty_label)
        qty_box.add_widget(plus_btn)

        row.add_widget(img)
        row.add_widget(info_box)
        row.add_widget(qty_box)

        return row, qty_label
    
    ### confirm orders page
    def display_confirmorder(self, instance):
        self.content_area.clear_widgets()
        self.footer.hide_footer()
        
        # re-check stock against the database in case it changed since the order page loaded
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="fruitinventory"
        )
        cursor = db.cursor()
        cursor.execute("SELECT fruit_id, stock_quantity FROM fruits")
        current_stock = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        db.close()
        
        # build order list from fruit_data, skipping anything with qty 0
        order_items = []
        stock_warnings = []
        total = 0.0
        
        for fruit_id, data in self.fruit_data.items():
            qty = int(data["qty_label"].text)
            if qty > 0:
                # check available stock for each item
                available = current_stock.get(fruit_id, 0)
                
                if qty > available:
                    stock_warnings.append(
                        f"{data['name']}: only {available} left (you selected {qty})"
                    )
                    
                    # skip the item if theres none left
                    if available <= 0:
                        continue
                    qty = available

                # build the order item
                price = float(data["price"])
                subtotal = price * qty
                total += subtotal
                order_items.append({
                    "fruit_id": fruit_id,
                    "name": data["name"],
                    "price": price,
                    "qty": qty,
                    "subtotal": subtotal,
                    "image_path": data.get("image_path", "")
                })
        
        self.current_order = order_items
        self.current_order_total = total

        confirm_box = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(1, None)
        )
        confirm_box.bind(minimum_height=confirm_box.setter("height"))

        # top row: back button on the left
        top_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50
        )
        back_btn = Button(
            text="< Back",
            size_hint=(None, None),
            size=(100, 40)
        )
        back_btn.bind(on_release=lambda inst: self.display_orderfruits())
        top_row.add_widget(back_btn)
        top_row.add_widget(Widget())

        title = HeroLabel(text="Confirm Order", size_hint=(1, None), height=60)

        confirm_box.add_widget(top_row)
        confirm_box.add_widget(title)

        # show a warning if any item's quantity had to be adjusted
        if stock_warnings:
            warning_text = "Some items changed due to stock:\n" + "\n".join(stock_warnings)
            warning_label = Label(
                text=warning_text,
                font_size=14,
                color=(1, 0.6, 0.2, 1),
                size_hint=(1, None),
                halign="left",
                valign="top"
            )
            warning_label.bind(
                width=lambda inst, val: setattr(inst, "text_size", (val, None)),
                texture_size=lambda inst, size: setattr(inst, "height", size[1] + 10)
            )
            confirm_box.add_widget(warning_label)

        items_box = ColoredBox(
            orientation="vertical",
            spacing=15,
            padding=12,
            size_hint=(None, None),
            width=450
        )
        items_box.bind(minimum_height=items_box.setter("height"))

        if not order_items:
            items_box.add_widget(Label(text="No items selected.", size_hint=(1, None), height=40))
        else:
            for item in order_items:
                items_box.add_widget(self.make_confirm_row(item))

        confirm_box.add_widget(CenterRow(items_box))

        if order_items:
            total_label = Label(
                text=f"Total: {total:.2f}",
                font_size=18,
                size_hint=(1, None),
                height=50
            )
            confirm_box.add_widget(total_label)

            place_order_row = BoxLayout(
                orientation="horizontal",
                size_hint=(1, None),
                height=60,
                padding=(0, 0, 12, 0)
            )
            place_order_btn = Button(
                text="Place Order",
                size_hint=(None, None),
                size=(200, 50)
            )
            place_order_btn.bind(on_release=self.place_order)
            place_order_row.add_widget(Widget())
            place_order_row.add_widget(place_order_btn)
            confirm_box.add_widget(place_order_row)

        self.content_area.add_widget(Widget())
        self.content_area.add_widget(confirm_box)
        self.content_area.add_widget(Widget())
        
    def make_confirm_row(self, item):
        row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=70,
            spacing=10,
            padding=8
        )

        # Left: fruit image
        img = Image(
            source=item["image_path"],
            size_hint=(None, None),
            size=(50, 50)
        )

        # Middle: name + price per pc
        info_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1)
        )
        name_label = Label(
            text=f"{item['name']}  x{item['qty']}",
            font_size=16,
            halign="left",
            valign="middle"
        )
        price_label = Label(
            text=f"{item['price']:.2f} / pc",
            font_size=13,
            halign="left",
            valign="middle"
        )
        for label in (name_label, price_label):
            label.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        info_box.add_widget(name_label)
        info_box.add_widget(price_label)

        # Right: subtotal
        subtotal_label = Label(
            text=f"{item['subtotal']:.2f}",
            font_size=16,
            size_hint=(None, None),
            size=(90, 50),
            halign="right",
            valign="middle"
        )
        subtotal_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        row.add_widget(img)
        row.add_widget(info_box)
        row.add_widget(subtotal_label)

        return row
    
    ### update database upon placing orders (decrease stock, insert in orders/order_items table)
    def place_order(self, instance):
        if not self.current_order:
            return

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="fruitinventory"
        )
        cursor = db.cursor()
        
        placed_items = []
        skipped_items = []
        actual_total = 0.0

        try:
            # insert into orders first to get an order_id
            cursor.execute(
                "INSERT INTO orders (user_id, order_date, total_amount, order_status) "
                "VALUES (%s, NOW(), %s, %s)",
                (self.user_id, self.current_order_total, "Pending")
            )
            order_id = cursor.lastrowid

            for item in self.current_order:
                cursor.execute(
                    "UPDATE fruits SET stock_quantity = stock_quantity - %s "
                    "WHERE fruit_id = %s AND stock_quantity >= %s",
                    (item["qty"], item["fruit_id"], item["qty"])
                )

                # if rowcount is 0, not enough stock -> skip
                if cursor.rowcount == 0:
                    skipped_items.append(item["name"])
                    continue

                cursor.execute(
                    "INSERT INTO order_items (order_id, fruit_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, item["fruit_id"], item["qty"])
                )
                placed_items.append(item)
                actual_total += item["subtotal"]

            if not placed_items:
                # nothing could be ordered at all, cancel the order row 
                db.rollback()
                cursor.close()
                db.close()
                self.show_message("Sorry, none of the selected items are in stock anymore.", error=True)
                return

            # update the order's total to reflect only what actually got placed
            cursor.execute(
                "UPDATE orders SET total_amount = %s WHERE order_id = %s",
                (actual_total, order_id)
            )
            db.commit()

        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error placing order: {err}")
            cursor.close()
            db.close()
            self.show_message(f"Error placing order: {err}", error=True)
            return

        cursor.close()
        db.close()

        # clear stored order state
        self.current_order = []
        self.current_order_total = 0.0

        if skipped_items:
            names = ", ".join(skipped_items)
            self.show_message(f"Order placed. Skipped (out of stock): {names}", error=True)
        else:
            self.show_message("Order placed successfully!")

        self.display_myorders()
    
    ### my orders page
    def display_myorders(self):
        self.content_area.clear_widgets()
        self.footer.hide_footer()

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="fruitinventory"
        )
        cursor = db.cursor()
        cursor.execute(
            "SELECT order_id, order_date, total_amount, order_status "
            "FROM orders WHERE user_id = %s AND order_status = 'Pending' "
            "ORDER BY order_date DESC",
            (self.user_id,)
        )
        orders = cursor.fetchall()

        myorders_box = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint=(1, None)
        )
        myorders_box.bind(minimum_height=myorders_box.setter("height"))

        # top row: back button on the left
        top_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50
        )
        back_btn = Button(
            text="< Back",
            size_hint=(None, None),
            size=(100, 40)
        )
        back_btn.bind(on_release=lambda x: self.display_orderfruits())
        top_row.add_widget(back_btn)
        top_row.add_widget(Widget())

        title = HeroLabel(text="My Orders", size_hint=(1, None), height=60)

        myorders_box.add_widget(top_row)
        myorders_box.add_widget(title)

        orders_box = ColoredBox(
            orientation="vertical",
            spacing=15,
            padding=12,
            size_hint=(None, None),
            width=500
        )
        orders_box.bind(minimum_height=orders_box.setter("height"))

        if not orders:
            orders_box.add_widget(Label(text="No active orders.", size_hint=(1, None), height=40))
        else:
            for order_id, order_date, total_amount, order_status in orders:
                # fetch items for this order, joined with fruits for name/image
                cursor.execute(
                    "SELECT f.fruit_name, f.image_path, oi.quantity "
                    "FROM order_items oi "
                    "JOIN fruits f ON oi.fruit_id = f.fruit_id "
                    "WHERE oi.order_id = %s",
                    (order_id,)
                )
                items = cursor.fetchall()
                orders_box.add_widget(
                    self.make_order_row(order_id, order_date, total_amount, order_status, items)
                )

        myorders_box.add_widget(CenterRow(orders_box))

        cursor.close()
        db.close()

        self.content_area.add_widget(Widget())
        self.content_area.add_widget(myorders_box)
        self.content_area.add_widget(Widget())

    def make_order_row(self, order_id, order_date, total_amount, order_status, items):
        row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=100,
            spacing=10,
            padding=10
        )

        # Left: order # and date, stacked vertically
        info_box = BoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=160
        )
        order_label = Label(
            text=f"Order #{order_id}",
            font_size=16,
            bold=True,
            halign="left",
            valign="middle"
        )
        date_label = Label(
            text=order_date.strftime("%b %d, %Y\n%I:%M %p"),
            font_size=13,
            halign="left",
            valign="top",
            color=(0.8, 0.8, 0.8, 1)
        )
        for label in (order_label, date_label):
            label.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        info_box.add_widget(order_label)
        info_box.add_widget(date_label)

        # Middle: fruit images for what was ordered, plus item count / total
        middle_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            spacing=5
        )

        images_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50,
            spacing=8
        )
        total_qty = 0
        for fruit_name, image_path, quantity in items:
            total_qty += quantity
            fruit_img = Image(
                source=image_path,
                size_hint=(None, None),
                size=(40, 40)
            )
            images_row.add_widget(fruit_img)

        summary_label = Label(
            text=f"{total_qty} item(s)  •  {total_amount:.2f}",
            font_size=14,
            halign="left",
            valign="middle",
            color=(0.85, 0.85, 0.85, 1)
        )
        summary_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        middle_box.add_widget(images_row)
        middle_box.add_widget(summary_label)

        # Right: order status
        status_box = BoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=100
        )
        status_label = Label(
            text=order_status,
            font_size=14,
            bold=True,
            color=(0.8, 0.8, 0.1, 1),  # yellow for pending
            halign="right",
            valign="top"
        )
        status_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        status_box.add_widget(status_label)
        status_box.add_widget(Widget())  # pushes label to the top

        row.add_widget(info_box)
        row.add_widget(middle_box)
        row.add_widget(status_box)

        return row
    
    def display_fruitrecog(self):
        """
        use the june5act file contents here
        """     
        self.content_area.clear_widgets()
        self.show_message("Info: Detecting loads countries automatically.")

        self.cap = None
        self.fruit_locked = False
        self.stable_confidence_count = 0
        self.confidence_thresh = 0.85
        self.required_frames = 15

        fruitrecog_box = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=10, spacing=10)

        # camera preview
        self.camera_image = Image(size_hint=(1, 0.4))

        # camera buttons row
        camera_buttons = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, None), height=50)

        self.start_camera_button = Button(text="Start Camera", size_hint=(0.5, 1))
        self.start_camera_button.bind(on_press=self.start_camera)

        self.detect_another_button = Button(text="Detect Another Fruit", size_hint=(0.5, 1), disabled=True)
        self.detect_another_button.bind(on_press=self.reset_detection)

        camera_buttons.add_widget(self.start_camera_button)
        camera_buttons.add_widget(self.detect_another_button)

        # detected fruit display (read only)
        self.detected_box = TextInput(
            background_color = (1, 1, 1, 0.2),
            foreground_color = (1, 1, 1, 1),
            hint_text_color=(0.8, 0.8, 0.8, 1),
            hint_text="Detected fruit will show up here",
            multiline=False,
            readonly=True,
            size_hint=(1, None),
            height=40
        )
        
        or_label = Label(text="- - - - - or type manually - - - - -",size_hint=(1, None),height=30,color=(0.5, 0.5, 0.5, 1))
        
        search_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50,
            spacing=10,
        )

        self.input_box = TextInput(
            hint_text="Search for an ingredient...",
            multiline=False,
            # size_hint=(0.5, 1),
            background_color = (1, 1, 1, 0.2),
            foreground_color = (1, 1, 1, 1),
            cursor_color=(0.1, 0.1, 0.1, 1),
            hint_text_color=(0.8, 0.8, 0.8, 1),
        )
        self.fetch_button = Button(
            text="Fetch Countries",
            # size_hint=(0.15, 1),
            background_normal="",
            background_down="",
            background_color=(0.1, 0.45, 0.2, 1),
        )
        
        self.input_box.bind(on_text_validate=self.load_countries_for_ingredient)
        self.fetch_button.bind(on_press=self.load_countries_for_ingredient)
        search_layout.add_widget(self.input_box)
        search_layout.add_widget(self.fetch_button)
        
        self.select_country_button = Button(
            text="Select Country",
            size_hint=(1, None),
            height=50,
            background_color=(0.05, 0.67, 0.98, 1),
            disabled=True
        )

        self.select_country_button.bind(on_press=self.show_loaded_countries)
        
        fruitrecog_box.add_widget(self.camera_image)
        fruitrecog_box.add_widget(camera_buttons)
        fruitrecog_box.add_widget(self.detected_box)    # readonly detected fruit input box 
        fruitrecog_box.add_widget(or_label)
        fruitrecog_box.add_widget(search_layout)   # manual type input & select country
        fruitrecog_box.add_widget(self.select_country_button)
        
        # remove any leftover "Back to Home" buttons from a previous visit before adding a new one, so they don't stack up
        if getattr(self, "fruitrecog_home_btn", None) is not None:
            self.footer.remove_widget(self.fruitrecog_home_btn)

        self.fruitrecog_home_btn = Button(
            text="Back to Home",
            size_hint=(None, 1), 
            size=(150, 40)
        )
        self.fruitrecog_home_btn.bind(on_release=lambda x: self.go_home_from_fruitrecog())
        self.footer.add_widget(self.fruitrecog_home_btn)
        
        self.content_area.add_widget(fruitrecog_box)
        
    def go_home_from_fruitrecog(self):
        self.stop_camera()
        self.display_home()
    
    def start_camera(self, instance):
        if self.cap is not None:
            return
        self.cap = cv2.VideoCapture(0)
        self.fruit_locked = False
        self.stable_confidence_count = 0
        self.start_camera_button.disabled = True
        self.show_message("Camera started. Hold a fruit up to the camera.")
        Clock.schedule_interval(self.update_camera, 1.0 / 30.0)
    
    def stop_camera(self):
        if self.cap is not None:
            Clock.unschedule(self.update_camera)
            self.cap.release()
            self.cap = None

    def update_camera(self, dt):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        if not self.fruit_locked:
            resized = cv2.resize(frame, (100, 100))
            normalized = resized / 255.0
            input_tensor = np.expand_dims(normalized, axis=0)

            predictions = self.model.predict(input_tensor, verbose=0)
            class_idx = np.argmax(predictions)
            confidence = np.max(predictions)
            fruit_name = self.fruit_classes[class_idx]

            # no fruit detected if confidence falls below thresh for 15 frames
            if confidence >= self.confidence_thresh:
                self.stable_confidence_count += 1
            else:
                self.stable_confidence_count = 0
                fruit_name = "No fruit detected"

            if confidence >= self.confidence_thresh:
                label = f"{fruit_name} ({confidence:.2f})"
                cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No fruit detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if self.stable_confidence_count >= self.required_frames:
                self.stable_confidence_count = 0
                self.fruit_locked = True
                self.detected_box.text = fruit_name
                self.detect_another_button.disabled = False
                self.load_countries_for_ingredient()

        # push frame to Kivy image widget
        buf = cv2.flip(frame, 0).tobytes()
        tex = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        tex.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_image.texture = tex

    def reset_detection(self, instance):
        self.fruit_locked = False
        self.stable_confidence_count = 0
        self.detected_box.text = ""
        self.input_box.text = ""
        self.recipe_options = {}
        self.detect_another_button.disabled = True
        self.show_message("Detection reset. Hold a fruit up to the camera.")       
        
    ### search flow: enter -> load countries (show loading msg while fetching) -> fetch countries -> build ui for countries
    # instance is optional (can call with either camera detection or button press bind)
    def load_countries_for_ingredient(self, instance=None):
        self.loaded_countries = []
        self.loaded_meals = []
        ingredient = self.detected_box.text.strip() or self.input_box.text.strip() 

        if not ingredient:
            self.show_message("Please detect or enter an ingredient first.")
            return

        self.selected_ingredient = ingredient
        self.show_message("Loading countries with available recipes...") 
        self.select_country_button.disabled = True
        self.select_country_button.text = "Loading..."

        threading.Thread(
            target=self.fetch_countries_for_ingredient,
            args=(ingredient,),
            daemon=True
        ).start()

    def fetch_countries_for_ingredient(self, ingredient):
        try:
            # prevent from calling multiple get requests
            self.fetch_button.disabled = True 
            self.fruitrecog_home_btn.disabled = True
            search_url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
            response = requests.get(search_url, timeout=10)
            response.raise_for_status()

            meals = response.json().get("meals")
            if not meals:
                self.loaded_countries = []
                self.loaded_meals = []
                Clock.schedule_once(
                    lambda dt: self.update_country_button(0, ingredient)
                )
                return

            countries = set()
            full_meals = []

            for item in meals[:30]:   
                meal_id = item["idMeal"]
                print(f"Fetching meal ID: {meal_id}")
                detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"

                detail_response = requests.get(detail_url, timeout=10)
                detail_response.raise_for_status()

                meal = detail_response.json()["meals"][0]
                full_meals.append(meal)

                area = meal.get("strArea")
                if area:
                    countries.add(area)

            self.loaded_countries = sorted(countries)
            self.loaded_meals = full_meals

            Clock.schedule_once(
                lambda dt: self.update_country_button(len(countries), ingredient)
            )

        except Exception as e:
            self.loaded_countries = []
            self.loaded_meals = []
            
            error_msg = f"Error loading countries:\n{e}"
            print(error_msg)
            Clock.schedule_once(
                lambda dt: self.show_message(error_msg, error=True)
            )

            # disable if theres an error
            Clock.schedule_once(
                lambda dt: setattr(self.select_country_button, "disabled", True)
            )
            Clock.schedule_once(
                lambda dt: setattr(self.select_country_button, "text", "Select Country")
            )
            Clock.schedule_once(
                lambda dt: setattr(self.fetch_button, "disabled", False)
            )
            Clock.schedule_once(
                lambda dt: setattr(self.fruitrecog_home_btn, "disabled", False)
            )
    
    ### wait for button press before displaying country rows
    def show_loaded_countries(self, instance=None):
        if not self.loaded_countries:
            self.show_message(
                "No country data loaded yet. Detect or enter a fruit first."
            )
            return

        self.stop_camera()
        self.display_country_rows(self.loaded_countries,self.loaded_meals)
    
    ### update message showing country count
    def update_country_button(self, count=0, ingredient=""):
        # re enable after fetching
        self.fetch_button.disabled = False 
        self.fruitrecog_home_btn.disabled = False
        
        if count > 0:
            self.show_message(
                f"Found {count} countries with recipes containing '{ingredient}'. Press Select Country."
            )

            self.select_country_button.disabled = False
        else:
            self.show_message(
                f"Unfortunately, there are no countries found with recipes that use '{ingredient}'. Detect or input a different fruit."
            )

            self.select_country_button.disabled = True

        self.select_country_button.text = "Select Country"
                   
    def display_ingredient_details(self, ingredient=None):
        """
        fruit label
        price per pc
        fruit details (use sample 8 contents, wikipedia api fetch)
        """
        self.content_area.clear_widgets()
        self.footer.hide_footer()

        # remember which ingredient we're showing
        if ingredient:
            self.selected_ingredient = ingredient

        ingredient_box = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12,
            size_hint=(None, None),
            width=500
        )
        ingredient_box.bind(minimum_height=ingredient_box.setter("height"))

        title = HeroLabel(text="Ingredient Details", size_hint=(1, None), height=60)

        self.ingredient_image = AsyncImage(
            source="",
            size_hint_y=None,
            height=250,
            allow_stretch=True,
            keep_ratio=True
        )
        self.ingredient_name_label = Label(
            text="",
            font_size=28,
            bold=True,
            color=(0, 0.35, 0.1, 1),
            size_hint_y=None,
            height=45
        )
        self.ingredient_info_label = Label(
            text="",
            font_size=16,
            color=(1, 1, 1, 1),
            halign="left",
            valign="top",
            size_hint_y=None
        )
        self.ingredient_info_label.bind(
            width=lambda instance, value: setattr(instance, "text_size", (value, None)),
            texture_size=lambda instance, size: setattr(instance, "height", size[1] + 10)
        )

        # back button returns to whichever recipe the ingredient was opened from
        back_row = ClickableRow(orientation="horizontal",padding=[15, 8, 15, 8],size_hint_y=None,height=60)
        back_row.add_widget(Label(text="‹ Back to Recipe",font_size=18,bold=True,color=(0.1, 0.65, 0.3, 1)))
        back_row.bind(on_press=lambda instance: self.go_back_to_recipe())

        ingredient_box.add_widget(back_row)
        ingredient_box.add_widget(title)
        ingredient_box.add_widget(self.ingredient_image)
        ingredient_box.add_widget(self.ingredient_name_label)
        ingredient_box.add_widget(self.ingredient_info_label)

        self.content_area.add_widget(Widget())
        self.content_area.add_widget(CenterRow(ingredient_box))
        self.content_area.add_widget(Widget())

        self.search_fruit()

    def go_back_to_recipe(self):
        if self.current_recipe_meal is not None:
            self.display_recipe(self.current_recipe_meal)
        else:
            self.display_home()
    
    def search_fruit(self):
        if DEBUG_MODE == 2:
            fruit = "lemon"
        else:
            fruit = self.selected_ingredient

        self.ingredient_image.source = ""
        self.ingredient_name_label.text = "Loading..."
        self.ingredient_info_label.text = "Getting fruit information from the internet..."
        
        # create a worker thread away from the main/ui thread to execute the func
        # without this, ui would freeze when executing the target func
        threading.Thread(
            target=self.get_fruit_info,
            args=(fruit,),
            daemon=True     # kill thread when program exits
        ).start()
        
    def get_fruit_info(self, fruit):
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{fruit}"
            headers = {"User-Agent": "FruitInfoApp/1.0"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                name = data.get("title", "Unknown")
                info = data.get("extract", "No information found.")
                image = data.get("thumbnail", {}).get("source", "")
                
                db = mysql.connector.connect(
                    host="localhost",      # IP address of the PC with MySQL
                    user="root",
                    password="root",
                    database="fruitinventory"
                )         
                cursor = db.cursor()
                cursor.execute("SELECT price FROM fruits WHERE LOWER(fruit_name) = LOWER(%s)", (fruit,))
                row = cursor.fetchone()
                price = row[0] if row else None
                
                # append the real price if the fruit is present in the db
                if row:
                    name += f" - {row[0]}/pc"

                # safely update the interface on the main thread
                Clock.schedule_once(
                    lambda dt: self.update_ingredient_details_ui(name, info, image)
                )
            else:
                Clock.schedule_once(
                    lambda dt: self.update_ingredient_details_ui(
                        "Fruit not found",
                        "Try another fruit.",
                        ""
                    )
                )

        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.update_ingredient_details_ui(
                    "Internet Error",
                    f"Could not get fruit data.\n{e}",
                    ""
                )
            )
    
    def update_ingredient_details_ui(self, name, info, image):
        self.ingredient_name_label.text = name
        self.ingredient_info_label.text = info
        self.ingredient_image.source = image
     
    ### ui flow: detect fruit -> country rows -> recipe rows -> recipe details
    def display_country_rows(self, countries, full_meals):
        self.content_area.clear_widgets()
        self.show_message("")
        self.all_meals = full_meals
        
        # build the scroll layout first before adding to content_area
        scroll = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        scroll.add_widget(layout)
        
        # header row: title + back button
        header_row = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=55
        )
        title_label = Label(
            text=f"Countries with {self.selected_ingredient}",
            font_size=24,
            bold=True,
            halign="left",
            color=(0.8, 0.8, 0.8, 1)
        )
        title_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )
        back_btn = Button(
            text="‹ Back to Fruit Recognition",
            font_size=16,
            bold=True,
            halign="right",
            size_hint=(None, 1),
            background_color=(0, 0, 0, 0),
            color=(0.1, 0.65, 0.3, 1)      
        )
        back_btn.texture_update()
        back_btn.width = back_btn.texture_size[0] + 20  # +20 for padding
        back_btn.bind(on_press=lambda instance: self.display_fruitrecog())

        header_row.add_widget(title_label)
        header_row.add_widget(back_btn)       
        layout.add_widget(header_row)

        # make a clickable row for each country with recipes containing the detected/inputted fruit
        for country in countries:
            row = ClickableRow(
                orientation="horizontal",
                spacing=12,
                padding=[15, 8, 15, 8],
                size_hint_y=None,
                height=75
            )

            flag_url = self.get_flag_url(country)
            if flag_url:
                row.add_widget(AsyncImage(source=flag_url,size_hint=(0.22, 1)))
            else:
                row.add_widget(Label(text="No Flag",font_size=24,size_hint=(0.22, 1),color=(0.4, 0.4, 0.4, 1)))

            country_label = Label(
                text=country,
                font_size=18,
                bold=True,
                halign="left",
                valign="middle",
                size_hint=(0.63, 1),
                color=(0.8, 0.8, 0.8, 1)
            )
            country_label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )

            row.add_widget(country_label)

            row.add_widget(
                Label(
                    text="›",
                    font_size=34,
                    size_hint=(0.15, 1),
                    color=(0.55, 0.55, 0.55, 1)
                )
            )

            row.bind(
                on_press=lambda instance, c=country:
                self.display_recipe_rows(c)
            )
            
            layout.add_widget(row)
            layout.add_widget(Divider())
            
        self.content_area.add_widget(scroll)

    def display_recipe_rows(self, country):
        self.content_area.clear_widgets()
        self.selected_country = country

        # get all recipes from the selected country
        matching_recipes = [
            meal for meal in self.all_meals
            if meal.get("strArea") == country
        ]
        
        # build the scroll layout first before adding to content_area
        scroll = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        scroll.add_widget(layout)

        self.add_wrapped_label(
            text=f"List of {country} recipes",
            font_size=24,
            bold=True,
            height=55,
            target=layout
        )

        if not matching_recipes:
            self.content_area.add_widget(scroll)
            self.show_message(f"No recipes found for {country}.")
            return

        # make a clickable row for each recipe containing the detected/inputted fruit
        for meal in matching_recipes:
            row = ClickableRow(
                orientation="horizontal",
                spacing=12,
                padding=[15, 8, 15, 8],
                size_hint_y=None,
                height=95
            )

            image_url = meal.get("strMealThumb")
            if image_url:
                row.add_widget(AsyncImage(source=image_url,size_hint=(0.28, 1)))

            recipe_label = Label(
                text=meal["strMeal"],
                font_size=16,
                bold=True,
                halign="left",
                valign="middle",
                size_hint=(0.57, 1),
                color=(0.8, 0.8, 0.8, 1)
            )
            recipe_label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )
            row.add_widget(recipe_label)

            row.add_widget(
                Label(
                    text="›",
                    font_size=34,
                    size_hint=(0.15, 1),
                    color=(0.55, 0.55, 0.55, 1)
                )
            )
            row.bind(
                on_press=lambda instance, m=meal:
                self.display_recipe(m)
            )
            layout.add_widget(row)
            layout.add_widget(Divider())

        # back button to go back to countries page
        back_row = ClickableRow(orientation="horizontal",padding=[15, 8, 15, 8],size_hint_y=None,height=60)
        back_row.add_widget(Label(text="‹ Back to Countries",font_size=18,bold=True,color=(0.1, 0.65, 0.3, 1)) )
        back_row.bind(
            on_press=lambda instance:
            self.display_country_rows(
                sorted(set(
                    meal.get("strArea")
                    for meal in self.all_meals
                    if meal.get("strArea")
                )),
                self.all_meals
            )
        )
        layout.add_widget(back_row)

        self.content_area.add_widget(scroll)

    ### for ingredient list: fruit name is a link only if there's stock, otherwise its a label
    def display_recipe(self, meal):
        self.content_area.clear_widgets()
        
        # build the scroll layout first before adding to content_area
        scroll = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        scroll.add_widget(layout)
        
        # remember the recipe currently being viewed, so ingredient details can navigate back here
        self.current_recipe_meal = meal

        image_url = meal.get("strMealThumb")
        if image_url:
            layout.add_widget(
                AsyncImage(
                    source=image_url,
                    size_hint_y=None,
                    height=250,
                    allow_stretch=True,
                    keep_ratio=True
                )
            )

        self.add_wrapped_label(
            text=f"Recipe: {meal['strMeal']}",
            font_size=24,
            bold=True,
            height=60,
            target=layout
        )

        country = meal.get("strArea", "Unknown")
        country_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=40
        )

        flag_url = self.get_flag_url(country)
        if flag_url:
            country_layout.add_widget(
                AsyncImage(
                    source=flag_url,
                    size_hint=(None, None),
                    size=(40, 30)
                )
            )

        country_layout.add_widget(
            Label(
                text=f"Country Cuisine: {country}",
                font_size=16,
                color=(1, 1, 1, 1),
                halign="left",
                valign="middle"
            )
        )

        layout.add_widget(country_layout)

        back_row = ClickableRow(orientation="horizontal",padding=[15, 8, 15, 8],size_hint_y=None,height=60)
        back_row.add_widget(Label(text="‹ Back to Recipe List",font_size=18,bold=True,color=(0.1, 0.65, 0.3, 1)))
        back_row.bind(
            on_press=lambda instance:
            self.display_recipe_rows(meal.get("strArea"))
        )

        layout.add_widget(back_row)

        self.add_wrapped_label(
            text="Ingredients",
            font_size=20,
            bold=True,
            height=45,
            target=layout
        )

        ingredients_grid = GridLayout(cols=2, spacing=5, size_hint_y=None)
        # makes the layout height grow depending on its contents 
        ingredients_grid.bind(minimum_height=ingredients_grid.setter("height"))

        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")

            if ingredient and ingredient.strip():
                # measurements
                ingredients_grid.add_widget(
                    Label(
                        text=measure.strip() if measure else "",
                        size_hint_y=None,
                        height=30,
                        color=(0, 1, 1, 1)
                    )
                )
                
                ingredient_clean = ingredient.strip()

                # ingredients: only link out to details for fruits we actually sell (apple, calamansi, lemon)
                if ingredient_clean.lower() in self.fruit_classes:
                    link_row = ClickableRow(
                        orientation="horizontal",
                        size_hint_y=None,
                        height=30
                    )
                    linked_label = Label(
                        text=ingredient_clean,
                        size_hint_y=None,
                        height=30,
                        halign="left",
                        valign="middle",
                        color=(0.2, 0.8, 1, 1),
                        underline=True
                    )
                    linked_label.bind(
                        size=lambda instance, value:
                        setattr(instance, "text_size", value)
                    )
                    link_row.add_widget(linked_label)
                    link_row.bind(
                        on_press=lambda instance, name=ingredient_clean:
                        self.display_ingredient_details(name)
                    )
                    ingredients_grid.add_widget(link_row)
                else:
                    ingredients_grid.add_widget(
                        Label(
                            text=ingredient.strip(),
                            size_hint_y=None,
                            height=30,
                            color=(1, 1, 1, 1)
                        )
                    )
                    
        layout.add_widget(ingredients_grid)

        self.add_wrapped_label(
            text="Instructions",
            font_size=20,
            bold=True,
            height=45,
            target=layout
        )

        instructions_grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        # makes the layout height grow depending on its contents 
        instructions_grid.bind(minimum_height=instructions_grid.setter("height"))
        
        # enumerate the recipe steps
        instructions = meal.get("strInstructions", "")
        steps = [step.strip() for step in instructions.split(".") if step.strip()]
        for index, step in enumerate(steps, start=1):
            step_label = Label(
                text=f"{index}. {step}.",
                size_hint_y=None,
                text_size=(700, None),
                halign="left",
                valign="top",
                color=(1, 1, 1, 1)
            )

            step_label.bind(
                texture_size=lambda instance, size:
                setattr(instance, "height", size[1] + 10)
            )

            instructions_grid.add_widget(step_label)
        layout.add_widget(instructions_grid)
        
        self.content_area.add_widget(scroll)

if __name__ == "__main__":
    RecipeApp().run()
