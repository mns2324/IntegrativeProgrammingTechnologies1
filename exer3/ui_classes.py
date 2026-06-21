from kivy.graphics import Color, Rectangle, Line
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

# for selecting countries and recipes
class ClickableRow(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

        # update pos and size when being moved
        self.bind(
            pos=lambda instance, value:
            setattr(self.bg, "pos", value),

            size=lambda instance, value:
            setattr(self.bg, "size", value)
        )

# for creating line dividers between clickable rows
class Divider(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 1

        with self.canvas:
            Color(0.88, 0.88, 0.88, 1)
            self.line = Line(points=[])

        # update line size when being moved
        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        self.line.points = [
            self.x + 20,
            self.center_y,
            self.right - 20,
            self.center_y
        ]

# reusable label + input box
class InputRow(BoxLayout):
    def __init__(self, label_text, input_widget, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.width = 600
        self.height = 45
        self.spacing = 20

        label = Label(
            text=label_text,
            size_hint=(None, 1),
            width=160,
            halign="left",
            valign="middle"
        )

        # update size
        label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        self.add_widget(label)
        self.add_widget(input_widget)

# for centering labels      
class CenterRow(BoxLayout):
    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = widget.height
        
        # update height (for minimum height setters)
        widget.bind(
            height=lambda instance, value:
            setattr(self, "height", value)
        )

        self.add_widget(Widget())
        self.add_widget(widget)
        self.add_widget(Widget())

# colored containers        
class ColoredBox(BoxLayout):
    def __init__(self, bg_color=(0.2, 0.2, 0.2, 1), **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*bg_color)
            self.bg = Rectangle(
                pos=self.pos,
                size=self.size
            )

        # update bg color
        self.bind(
            pos=lambda instance, value:
            setattr(self.bg, "pos", value),

            size=lambda instance, value:
            setattr(self.bg, "size", value)
        )
        
class HeroLabel(Label):
    def __init__(self, color=(0.1, 0.45, 0.2, 1), font_size=32, **kwargs):
        super().__init__(**kwargs)
    
        self.color = color
        self.font_size = font_size
        self.bold = True
        self.halign = "center"
        self.valign = "middle"

        # update size
        self.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

class Footer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 50
        self.padding = 10

        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

        # update pos and size
        self.bind(
            pos=lambda instance, value:
            setattr(self.bg, "pos", value),

            size=lambda instance, value:
            setattr(self.bg, "size", value)
        )

        self.message_label = Label(
            text="",
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle"
        )

        self.message_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        self.add_widget(self.message_label)

    def set_message(self, message, color=(1, 1, 1, 1)):
        self.message_label.text = message
        self.message_label.color = color
        self.height = 50
    
    def hide_footer(self):
        self.message_label.text = ""
        self.height = 0
          
    def show_footer(self):
        self.height = 50