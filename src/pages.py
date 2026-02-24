from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button

import data
import menus


# Main content area for the home page, which includes a search bar and a list of climbs.
# Each climb in the list is represented by a ThreeLineRightIconListItem, which includes the climb name, setter, and repeat count.
# The right side of each list item includes a custom container RightVerticalContainer.
class HomeLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = 1

        # Create the upper menu
        self.add_widget(menus.UpperMenu())

        # Create seach bar
        self.add_widget(menus.SearchBar().createSearchBar())

        # Create list of climbs
        scroll = ScrollView()

        # Add the climb list to the scroll view and then add the scroll view to the layout
        scroll.add_widget(data.get_climb_list("./data/tensiondata", None))
        self.add_widget(scroll)


class FilterPage(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "lr-tb"

        # Add upper menu
        self.add_widget(menus.UpperMenu())

        # Placeholder content for the filter page
        self.add_widget(
            Button(text="Filter options will go here", size_hint=(1, None), height=50)
        )
        self.add_widget(
            Button(
                text="Filter options will go here", size_hint=(0.5, None), height=150
            )
        )
        self.add_widget(
            Button(
                text="Filter options will go here", size_hint=(0.5, None), height=150
            )
        )
