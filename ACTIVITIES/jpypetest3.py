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

            # home pc path
            sample_jar = r"D:\netbeans\nbprojects\Sample\target\Sample-1.0-SNAPSHOT.jar"          
            mysql_jar = r"C:\Users\Owner\.m2\repository\mysql\mysql-connector-java\5.1.49\mysql-connector-java-5.1.49.jar"

            # school pc path
            # sample_jar = r"C:\Users\mnsbartolata\Documents\NetBeansProjects\Sample\target\Sample-1.0-SNAPSHOT.jar"
            # mysql_jar = r"C:\Users\mnsbartolata\.m2\repository\mysql\mysql-connector-java\5.1.49\mysql-connector-java-5.1.49.jar" 

            jpype.startJVM(
                jvm_path,
                classpath=[
                    sample_jar,
                    mysql_jar
                ]
            )

        # connect the java classes to these vars
        self.DBConnect = jpype.JClass("com.mycompany.sample.DBConnect")
        self.Sample = jpype.JClass("com.mycompany.sample.Sample")

        # connect to mysql with this function
        self.DBConnect.connect()

        # instantiate the sample class to this object
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

        # declare layouts
        studid_inputbox = BoxLayout(size_hint=(1, None), height=50)
        studname_inputbox = BoxLayout(size_hint=(1, None), height=50)
        studadd_inputbox = BoxLayout(size_hint=(1, None), height=50)
        studcrs_inputbox = BoxLayout(size_hint=(1, None), height=50)
        studgender_inputbox = BoxLayout(size_hint=(1, None), height=50)
        yrlvl_inputbox = BoxLayout(size_hint=(1, None), height=50)

        # declare labels and text inputs
        studid_label = Label(text="ID:", size_hint=(0.6, 1))
        studname_label = Label(text="Name:", size_hint=(0.6, 1))
        studadd_label = Label(text="Address:", size_hint=(0.6, 1))
        studcrs_label = Label(text="Course:", size_hint=(0.6, 1))
        studgender_label = Label(text="Gender:", size_hint=(0.6, 1))
        yrlvl_label = Label(text="Year Level:", size_hint=(0.6, 1))

        self.studid_input = TextInput(multiline=False, font_size=20, size_hint=(1, 0.8))  
        self.studname_input = TextInput(multiline=False, font_size=20, size_hint=(1, 0.8))
        self.studadd_input = TextInput(multiline=False, font_size=20, size_hint=(1, 0.8))  
        self.studcrs_input = TextInput(multiline=False, font_size=20, size_hint=(1, 0.8))
        self.studgender_input = TextInput(multiline=False, font_size=20, size_hint=(1, 0.8))  
        self.yrlvl_input = TextInput(multiline=False, font_size=20, size_hint=(1, 0.8))

        # attach labels and text inputs to respective layouts
        studid_inputbox.add_widget(studid_label)
        studid_inputbox.add_widget(self.studid_input)
        studname_inputbox.add_widget(studname_label)
        studname_inputbox.add_widget(self.studname_input)
        studadd_inputbox.add_widget(studadd_label)
        studadd_inputbox.add_widget(self.studadd_input)
        studcrs_inputbox.add_widget(studcrs_label)
        studcrs_inputbox.add_widget(self.studcrs_input)
        studgender_inputbox.add_widget(studgender_label)
        studgender_inputbox.add_widget(self.studgender_input)
        yrlvl_inputbox.add_widget(yrlvl_label)
        yrlvl_inputbox.add_widget(self.yrlvl_input)
        

        # declare layout for the 4 btns
        menu_layout = GridLayout(cols=2, spacing=10,size_hint=(1, 0.20))

        # declare and bind btns to respective methods
        save_btn = Button(text="Save", background_color=(0, 1, 0, 1))
        edit_btn = Button(text="Edit", background_color=(1, 1, 0, 1))
        delete_btn = Button(text="Delete", background_color=(1, 0, 0, 1))
        search_btn = Button(text="Search", background_color=(0, 0, 1, 1))
        
        save_btn.bind(on_press=self.save_record)
        edit_btn.bind(on_press=self.edit_record)
        delete_btn.bind(on_press=self.delete_record)
        search_btn.bind(on_press=self.search_record)

        # attach btns to menu layout
        menu_layout.add_widget(save_btn)
        menu_layout.add_widget(edit_btn)
        menu_layout.add_widget(delete_btn)
        menu_layout.add_widget(search_btn)


        self.footer = Label(
            text="Ready",
            font_size=18,
            size_hint=(1, 0.20)
        )

        # build main layout
        main_layout.add_widget(title)
        main_layout.add_widget(logo)
        
        main_layout.add_widget(studid_inputbox)
        main_layout.add_widget(studname_inputbox)
        main_layout.add_widget(studadd_inputbox)
        main_layout.add_widget(studcrs_inputbox)
        main_layout.add_widget(studgender_inputbox)
        main_layout.add_widget(yrlvl_inputbox)
        
        main_layout.add_widget(menu_layout)
        main_layout.add_widget(self.footer)

        return main_layout

    def save_record(self, instance):
        student_id = self.studid_input.text
        student_name = self.studname_input.text
        student_address = self.studadd_input.text
        student_course = self.studcrs_input.text
        student_gender = self.studgender_input.text
        year_level = self.yrlvl_input.text

        if student_id == "" or student_name == "" or student_address == "" or student_course == "" or student_gender == "" or year_level == "" :
            self.footer.text = "please fill in all fields"
            return

        try:
            # insert to table
            self.java_obj.SaveRecord(
                int(student_id),
                student_name,
                student_address,
                student_course,
                student_gender,
                year_level
            )

            self.footer.text = "record saved using java jar!"
            self.clear_inputs(instance)

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def edit_record(self, instance):
        student_id = self.studid_input.text
        student_name = self.studname_input.text
        student_address = self.studadd_input.text
        student_course = self.studcrs_input.text
        student_gender = self.studgender_input.text
        year_level = self.yrlvl_input.text

        if student_id == "" or student_name == "" or student_address == "" or student_course == "" or student_gender == "" or year_level == "" :
            self.footer.text = "please fill in all fields"
            return

        try:
            # update values based on id entered
            rowcount = self.java_obj.EditRecord(
                int(student_id),
                student_name,
                student_address,
                student_course,
                student_gender,
                year_level
            )

            if rowcount > 0:
                self.footer.text = "record edited successfully"
            else:
                self.footer.text = "id not found"
            self.clear_inputs(instance)

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def delete_record(self, instance):
        student_id = self.studid_input.text.strip()

        if student_id == "":
            self.footer.text = "Please enter ID"
            return

        try:
            # delete row based on id entered
            rowcount = self.java_obj.DeleteRecord(int(student_id))

            if rowcount > 0:
                self.footer.text = "record deleted successfully"
            else:
                self.footer.text = "id not found"
            self.clear_inputs(instance)

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def search_record(self, instance):
        student_id = self.studid_input.text.strip()

        if student_id == "":
            self.footer.text = "Please enter ID"
            return

        try:
            # show data in input boxes if id exists
            # typecast first since java str cant be concatenated with python str
            result = str(self.java_obj.SearchRecord(int(student_id)))

            if result is not None:
                data = result.split("|")
                
                self.studid_input.text = data[0]
                self.studname_input.text = data[1]
                self.studadd_input.text = data[2]
                self.studcrs_input.text = data[3]
                self.studgender_input.text = data[4]
                self.yrlvl_input.text = data[5]
                self.footer.text = "record found"
            else:
                self.clear_inputs(instance)
                self.footer.text = "id not found"

        except Exception as e:
            self.footer.text = "Error: " + str(e)

    def clear_inputs(self, instance):
        self.studid_input.text = ""
        self.studname_input.text = ""
        self.studadd_input.text = ""
        self.studcrs_input.text = ""
        self.studgender_input.text = ""
        self.yrlvl_input.text = ""
    
    def on_stop(self):
        if jpype.isJVMStarted():
            jpype.shutdownJVM()


HomeScreenApp().run()
