from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import mysql.connector

class HomeScreenApp(App):
    def build(self):
        main_layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="smartinventory"
        )

        title = Label(
            text="Customer Profile",
            font_size=30,
            size_hint=(1, 0.15)
        )

        # Image Widget
        logo = Image(
            source="logo.png",
            size_hint=(1, 0.25)
        )

        id_layout = BoxLayout(size_hint=(1, None), height=50)
        id_label = Label(text="ID:", size_hint=(0.6, 1))
        self.id_input = TextInput(
            hint_text="Enter ID",
            font_size=22
        )

        id_layout.add_widget(id_label)
        id_layout.add_widget(self.id_input)
        
        name_layout = BoxLayout(size_hint=(1, None), height=50)
        name_label = Label(text="Name:", size_hint=(0.6, 1))
        self.name_input = TextInput(
            hint_text="Enter Name",
            font_size=22
        )

        name_layout.add_widget(name_label)
        name_layout.add_widget(self.name_input)

        menu_layout = GridLayout(
            cols=2,
            spacing=10,
            size_hint=(1, 0.4)
        )

        save_btn = Button(text="Save", background_color=(0, 1, 0, 1))
        edit_btn = Button(text="Edit", background_color=(1, 1, 0, 1))
        delete_btn = Button(text="Delete", background_color=(1, 0, 0, 1))
        search_btn = Button(text="Search", background_color=(0, 0, 1, 1))

        save_btn.bind(on_press=self.save_record)
        edit_btn.bind(on_press=self.edit_record)
        delete_btn.bind(on_press=self.delete_record)
        search_btn.bind(on_press=self.search_record)

        menu_layout.add_widget(save_btn)
        menu_layout.add_widget(edit_btn)
        menu_layout.add_widget(delete_btn)
        menu_layout.add_widget(search_btn)

        self.footer = Label(
            text="",
            font_size=18,
            size_hint=(1, 0.2)
        )

        # create user table
        self.table = GridLayout(cols=2, spacing=2)
        headers = ["ID", "Name"]
        for header in headers:
            self.table.add_widget(Label(text=header, bold=True, color=(0, 1, 1, 1)))
        cursor = self.db.cursor()
        cursor.execute("select * from users")
        data = cursor.fetchall()
        cursor.close()
        for row in data:
            for cell in row:
                self.table.add_widget(Label(text=str(cell)))

        main_layout.add_widget(title)
        main_layout.add_widget(logo)
        main_layout.add_widget(id_layout)
        main_layout.add_widget(name_layout)
        main_layout.add_widget(menu_layout)
        main_layout.add_widget(self.footer)
        main_layout.add_widget(self.table)

        return main_layout

    def save_record(self, instance):
        uid = self.id_input.text
        name = self.name_input.text

        if uid == "" or name == "":
            self.footer.text = "please input all fields"
            return

        try:
            cursor = self.db.cursor()

            sql = "insert into users (uid, name) values (%s, %s)"
            values = (uid, name)

            cursor.execute(sql, values)
            self.db.commit()

            self.load_users()

            self.footer.text = "record saved successfully"
            self.id_input.text = ""
            self.name_input.text = ""

        except Exception as e:
            self.footer.text = "Error " +str(e)

        finally:
            try:
                cursor.close()
            except:
                pass

    def edit_record(self, instance):
        uid = self.id_input.text
        name = self.name_input.text

        if uid == "" or name == "":
            self.footer.text = "Please enter ID and Name"
            return

        try:
            cursor = self.db.cursor()

            sql = "update users set name=%s where uid=%s"
            values = (name, uid)

            cursor.execute(sql, values)
            self.db.commit()

            self.load_users()

            if cursor.rowcount > 0:
                self.footer.text = "record updated successfully"
            else:
                self.footer.text = "id not found"

            cursor.close()

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def delete_record(self, instance):
        uid = self.id_input.text.strip()

        if uid == "":
            self.footer.text = "Please enter ID"
            return

        try:
            cursor = self.db.cursor()

            sql = "delete from users where uid=%s"
            cursor.execute(sql, (uid,))
            self.db.commit()

            self.load_users()

            if cursor.rowcount > 0:
                self.footer.text = "record deleted successfully"
                self.id_input.text = ""
                self.name_input.text = ""
            else:
                self.footer.text = "id not found"

            cursor.close()

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def search_record(self, instance):
        uid = self.id_input.text.strip()

        if uid == "":
            self.footer.text = "please enter id"
            return

        try:
            cursor = self.db.cursor()

            sql = "select name from users where uid=%s"
            cursor.execute(sql, (uid,))

            result = cursor.fetchone()

            if result:
                self.name_input.text = result[0]
                self.footer.text = "record found"
            else:
                self.name_input.text = ""
                self.footer.text = "id not found"

            cursor.close()

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def load_users(self):
        # clear existing table data
        self.table.clear_widgets()
        
        self.table.add_widget(Label(text="ID"))
        self.table.add_widget(Label(text="Name"))

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT uid, name FROM users")
            rows = cursor.fetchall()
            cursor.close()

            for uid, name in rows:
                self.table.add_widget(Label(text=str(uid)))
                self.table.add_widget(Label(text=str(name)))

        except Exception as e:
            self.footer.text = "Error loading users: " + str(e)

HomeScreenApp().run()
