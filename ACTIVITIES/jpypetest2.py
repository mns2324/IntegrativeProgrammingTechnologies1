from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import jpype


class HomeScreenApp(App):

    def start_java(self):
        if not jpype.isJVMStarted():
            jvm_path = r"C:\Program Files\Java\jdk-21.0.10\bin\server\jvm.dll"
            sample_jar = r"C:\Users\mnsbartolata\Documents\NetBeansProjects\Sample\target\Sample-1.0-SNAPSHOT.jar"
            mysql_jar = r"C:\Users\mnsbartolata\.m2\repository\mysql\mysql-connector-java\5.1.49\mysql-connector-java-5.1.49.jar"

            jpype.startJVM(
                jvm_path,
                classpath=[
                    sample_jar,
                    mysql_jar
                ]
            )

        self.DBConnect = jpype.JClass("com.mycompany.sample.DBConnect")
        self.Sample = jpype.JClass("com.mycompany.sample.Sample")

        self.DBConnect.connect()
        self.java_obj = self.Sample()

    def build(self):
        self.start_java()

        main_layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title = Label(
            text="My Mobile App",
            font_size=30,
            size_hint=(1, 0.10)
        )

        logo = Image(
            source="logo.png",
            size_hint=(1, 0.20)
        )

        self.id_input = TextInput(
            hint_text="Enter Student ID",
            multiline=False,
            font_size=20,
            size_hint=(1, 0.08)
        )

        self.name_input = TextInput(
            hint_text="Enter Student Name",
            multiline=False,
            font_size=20,
            size_hint=(1, 0.08)
        )

        menu_layout = GridLayout(
            cols=2,
            spacing=10,
            size_hint=(1, 0.20)
        )

        save_button = Button(text="Save")
        clear_button = Button(text="Clear")

        save_button.bind(on_press=self.save_record)
        clear_button.bind(on_press=self.clear_inputs)

        menu_layout.add_widget(save_button)
        menu_layout.add_widget(clear_button)

        self.footer = Label(
            text="Ready",
            font_size=18,
            size_hint=(1, 0.20)
        )

        main_layout.add_widget(title)
        main_layout.add_widget(logo)
        main_layout.add_widget(self.id_input)
        main_layout.add_widget(self.name_input)
        main_layout.add_widget(menu_layout)
        main_layout.add_widget(self.footer)

        return main_layout

    def save_record(self, instance):
        student_id = self.id_input.text
        student_name = self.name_input.text

        if student_id == "" or student_name == "":
            self.footer.text = "Please enter student ID and name."
            return

        try:
            self.java_obj.SaveRecord(
                int(student_id),
                student_name,
                "",
                "",
                "",
                ""
            )

            self.footer.text = "Record saved using Java JAR!"
            self.clear_inputs(instance)

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def clear_inputs(self, instance):
        self.id_input.text = ""
        self.name_input.text = ""

    def on_stop(self):
        if jpype.isJVMStarted():
            jpype.shutdownJVM()


HomeScreenApp().run()
