import requests
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage


class RecipeApp(App):
    def build(self):
        self.recipe_options = {}

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        search_widget = BoxLayout(orientation="horizontal", padding=4, spacing=10, size_hint=(1, None), height=50)
        select_widget = BoxLayout(orientation="horizontal", padding=4, spacing=10, size_hint=(1, None), height=50)

        self.input_box = TextInput(
            hint_text="Enter ingredient, e.g. chicken",
            multiline=False,
            size_hint=(0.8, 1)
        )

        self.load_country_button = Button(text="Load Countries", size_hint=(0.2, 1))
        self.load_country_button.bind(on_press=self.load_countries_for_ingredient)
        
        search_widget.add_widget(self.input_box)
        search_widget.add_widget(self.load_country_button)

        self.country_spinner = Spinner(
            text="Select Country Cuisine",
            values=["Select Country Cuisine"],
            size_hint=(1, 1)
        )

        # runs after selecting country
        self.country_spinner.bind(text=self.load_recipes_for_country)

        self.recipe_spinner = Spinner(
            text="Select Recipe",
            values=["Select Recipe"],
            size_hint=(1, 1)
        )

        # runs after selecting recipe
        self.recipe_spinner.bind(text=self.show_selected_recipe)
        
        select_widget.add_widget(self.country_spinner)
        select_widget.add_widget(self.recipe_spinner)

        self.recipe_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.recipe_layout.bind(minimum_height=self.recipe_layout.setter("height"))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.recipe_layout)

        main_layout.add_widget(search_widget)
        main_layout.add_widget(select_widget)
        main_layout.add_widget(scroll)

        self.show_message("Enter ingredient, load countries, then load recipes.")
        return main_layout

    def show_message(self, message):
        self.recipe_layout.clear_widgets()
        self.recipe_layout.add_widget(Label(text=message, size_hint_y=None, height=60))

    def add_wrapped_label(self, text, font_size=16, bold=False, height=None):
        label = Label(
            text=text,
            font_size=font_size,
            bold=bold,
            size_hint_y=None,
            text_size=(700, None),
            halign="left",
            valign="top"
        )

        if height:
            label.height = height
        else:
            label.bind(
                texture_size=lambda instance, size:
                setattr(instance, "height", size[1] + 10)
            )

        self.recipe_layout.add_widget(label)

    # step 1: take ingredient from input box and load countries that have recipes that use this ingredient
    def load_countries_for_ingredient(self, instance):
        ingredient = self.input_box.text.strip()

        if not ingredient:
            self.show_message("Please enter an ingredient first.")
            return

        self.show_message("Loading countries...")
        self.country_spinner.text = "Select Country Cuisine"
        self.country_spinner.values = ["Select Country Cuisine"]
        self.recipe_spinner.text = "Select Recipe"
        self.recipe_spinner.values = ["Select Recipe"]
        self.recipe_options = {}

        threading.Thread(
            target=self.fetch_countries_for_ingredient,
            args=(ingredient,),
            daemon=True
        ).start()

    def fetch_countries_for_ingredient(self, ingredient):
        try:
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            meals = response.json().get("meals")

            if not meals:
                Clock.schedule_once(
                    lambda dt: self.show_message(f"No recipes found for '{ingredient}'.")
                )
                return

            countries = set()

            for item in meals[:30]:
                meal_id = item["idMeal"]
                detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"

                detail_response = requests.get(detail_url, timeout=10)
                detail_response.raise_for_status()

                meal = detail_response.json()["meals"][0]
                area = meal.get("strArea")

                if area:
                    countries.add(area)

            country_list = ["Select Country Cuisine"] + sorted(countries)

            Clock.schedule_once(
                lambda dt: self.update_country_spinner(country_list)
            )

        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.show_message(f"Error loading countries:\n{e}")
            )

    def update_country_spinner(self, countries):
        self.country_spinner.values = countries
        self.country_spinner.text = countries[0]

        if len(countries) == 1:
            self.show_message("No countries found for this ingredient.")
        else:
            self.show_message("Countries loaded. Select a country, then load recipes.")

    ### this was rebound to a spinner value, so value must be included in the args
    # step 2: after the countries are loaded, load the recipes from that country
    def load_recipes_for_country(self, instance, country):
        ingredient = self.input_box.text.strip()

        if not ingredient:
            self.show_message("Please enter an ingredient.")
            return

        if country == "Select Country Cuisine":
            self.show_message("Please select a country.")
            return

        self.show_message("Loading recipes...")
        self.recipe_spinner.text = "Select Recipe"
        self.recipe_spinner.values = ["Select Recipe"]
        self.recipe_options = {}

        threading.Thread(
            target=self.fetch_recipes_for_country,
            args=(ingredient, country),
            daemon=True
        ).start()

    def fetch_recipes_for_country(self, ingredient, country):
        try:
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            meals = response.json().get("meals")
            recipe_options = {}

            for item in meals[:30]:
                meal_id = item["idMeal"]
                detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"

                detail_response = requests.get(detail_url, timeout=10)
                detail_response.raise_for_status()

                meal = detail_response.json()["meals"][0]

                if meal.get("strArea") == country:
                    recipe_options[meal["strMeal"]] = meal

            Clock.schedule_once(
                lambda dt: self.update_recipe_spinner(recipe_options)
            )

        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.show_message(f"Error loading recipes:\n{e}")
            )

    def update_recipe_spinner(self, recipe_options):
        self.recipe_options = recipe_options

        if not recipe_options:
            self.recipe_spinner.values = ["Select Recipe"]
            self.recipe_spinner.text = "Select Recipe"
            self.show_message("No recipes found for that ingredient and country.")
            return

        recipe_names = ["Select Recipe"] + sorted(recipe_options.keys())
        self.recipe_spinner.values = recipe_names
        self.recipe_spinner.text = recipe_names[0]

        self.show_message("Recipes have been loaded.")

    ### this was rebound to a spinner value, so value must be included in the args
    # step 3: show the recipe's ingredients and instructions after it has been selected from the spinner
    def show_selected_recipe(self, instance, recipe):
        if recipe == "Select Recipe":
            self.show_message("Please select a recipe first.")
            return

        meal = self.recipe_options.get(recipe)

        if meal:
            self.display_recipe(meal)
        else:
            self.show_message("Recipe details not found.")

    def display_recipe(self, meal):
        self.recipe_layout.clear_widgets()

        image_url = meal.get("strMealThumb")

        if image_url:
            self.recipe_layout.add_widget(
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
            height=60
        )

        self.add_wrapped_label(
            text=f"Country Cuisine: {meal.get('strArea', 'Unknown')}",
            font_size=16,
            height=35
        )

        self.add_wrapped_label(
            text="Ingredients",
            font_size=20,
            bold=True,
            height=45
        )

        ingredients_grid = GridLayout(cols=2, spacing=5, size_hint_y=None)
        ingredients_grid.bind(minimum_height=ingredients_grid.setter("height"))

        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")

            if ingredient and ingredient.strip():
                ingredients_grid.add_widget(
                    Label(
                        text=measure.strip() if measure else "",
                        size_hint_y=None,
                        height=30
                    )
                )

                ingredients_grid.add_widget(
                    Label(
                        text=ingredient.strip(),
                        size_hint_y=None,
                        height=30
                    )
                )

        self.recipe_layout.add_widget(ingredients_grid)

        self.add_wrapped_label(
            text="Instructions",
            font_size=20,
            bold=True,
            height=45
        )

        instructions_grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        instructions_grid.bind(minimum_height=instructions_grid.setter("height"))

        instructions = meal.get("strInstructions", "")
        steps = [step.strip() for step in instructions.split(".") if step.strip()]

        for index, step in enumerate(steps, start=1):
            step_label = Label(
                text=f"{index}. {step}.",
                size_hint_y=None,
                text_size=(700, None),
                halign="left",
                valign="top"
            )

            step_label.bind(
                texture_size=lambda instance, size:
                setattr(instance, "height", size[1] + 10)
            )

            instructions_grid.add_widget(step_label)

        self.recipe_layout.add_widget(instructions_grid)


if __name__ == "__main__":
    RecipeApp().run()
