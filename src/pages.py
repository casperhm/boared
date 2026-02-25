from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.core.window import Window


import data
import menus


# Main content area for the home page, which includes a search bar and a list of climbs.
# Each climb in the list is represented by a ThreeLineRightIconListItem, which includes the climb name, setter, and repeat count.
# The right side of each list item includes a custom container RightVerticalContainer.
class HomePage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = 0.9

        # Create the upper menu
        self.add_widget(menus.UpperMenu())

        # Create seach bar
        self.add_widget(menus.SearchBar().createSearchBar())

        # Create list of climbs
        scroll = ScrollView()

        # Add the climb list to the scroll view and then add the scroll view to the layout
        scroll.add_widget(data.get_climb_list("./data/tensiondata"))
        self.add_widget(scroll)


class FilterPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.9
        self.orientation = "vertical"

        # Add upper menu
        self.add_widget(menus.UpperMenu())

        # "Sort by" dropdown
        self.sort_dropdown = DropDown()
        # Populate the dropdown with default sort options
        for sort_option in [
            "Most repeats",
            "Least repeats",
            "Highest grade",
            "Lowest grade",
            "Newest",
            "Oldest",
            "Random",
        ]:
            btn = Button(text=sort_option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.sort_dropdown.select(btn.text))
            self.sort_dropdown.add_widget(btn)

        # Main button to open the dropdown
        sort_button = Button(text="Sort by", size_hint_x=0.6)
        sort_button.bind(on_release=self.sort_dropdown.open)
        self.sort_dropdown.bind(
            on_select=lambda instance, x: setattr(
                sort_button, "text", "Sort by " + x.lower()
            )
        )
        # Set button size
        sort_button.size_hint = (1, 0.1)
        self.add_widget(sort_button)

        # Filter selection layout
        filter_layout = StackLayout()
        filter_layout.size_hint_x = 0.8
        filter_layout.pos_hint = {"right": 0.9}

        # Populate the filter layout with default filter options
        for filter_option in [
            "Benchmark",
            "In my ascents",
            "Not in my ascents",
            "Unsent",
            "Beta video",
        ]:
            # Set initial button color on menu open - TODO fix bug where on REENTERING the filter menu using the FILTER button the first filter will be grey -
            # still in root.filters but grey. this does not happen when reentering the filter menu through the back button
            if btn.text in App.get_running_app().root.filters:
                color = (0, 1, 0, 1)
            else:
                color = (1, 1, 1, 1)
            btn = Button(
                text=filter_option,
                size_hint=(0.33, None),
                height=44,
                background_color=color,
            )
            btn.bind(on_release=lambda btn: self.add_filter(btn))
            filter_layout.add_widget(btn)

        self.add_widget(filter_layout)

    def add_filter(self, filter):
        root = App.get_running_app().root
        if filter.text not in root.filters:
            # Add filter
            root.filters.append(filter.text)
            filter.background_color = (0, 1, 0, 1)
        else:
            # Remove filter
            root.filters.remove(filter.text)
            filter.background_color = (1, 1, 1, 1)
        print(root.filters)
