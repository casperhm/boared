from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivymd.uix.slider import MDSlider
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

import data
import menus


# Main content area for the home page, which includes a search bar and a list of climbs.
# Each climb in the list is represented by a ThreeLineRightIconListItem, which includes the climb name, setter, and repeat count.
# The right side of each list item includes a custom container RightVerticalContainer.
class HomePage(BoxLayout):
    def __init__(self, filters, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = 0.9
        self.filters = filters
        self.name = "home_page"

        # Create the upper menu
        self.add_widget(menus.UpperMenu())

        # Create seach bar
        self.add_widget(menus.SearchBar().createSearchBar())

        # Create list of climbs
        scroll = ScrollView()

        # Add the climb list to the scroll view and then add the scroll view to the layout
        scroll.add_widget(data.get_climb_list("./data/tensiondata", self.filters))
        self.add_widget(scroll)


# Content area containing a grade slider, a sort by dropdown, and toggleable filter buttons
# Also has the same upper menu as HomePage
class FilterPage(BoxLayout):
    def __init__(self, filters, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.9
        self.orientation = "vertical"
        self.name = "filter_page"
        self.filters = filters

        # Add upper menu
        self.add_widget(menus.UpperMenu())

        # Add the grade slider for controlling the grade_max and grad_min filters
        grade_slider = RangeSlider()
        self.add_widget(grade_slider)

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

        # Populate the filter layout with default filter options TODO maybe? benchmark filter shows only benchmarks,
        # but when not selected benchmarks can still appear. might change
        for filter_option in [
            "Benchmark",
            "No match",
            "In my ascents",
            "Not in my ascents",
            "Unsent",
            "Beta video",
        ]:
            # Set initial button color on menu open
            if filter_option in self.filters:
                color = (0, 1, 0, 1)
            else:
                color = (1, 1, 1, 1)
            btn = Button(
                text=filter_option,
                size_hint=(0.33, None),
                height=44,
                background_color=color,
            )
            btn.bind(
                on_release=lambda instance, option=filter_option: update_button_filters(
                    self, instance
                )
            )
            filter_layout.add_widget(btn)

        self.add_widget(filter_layout)


# Two MDSliders stacked on top of each other with a rectanglular highlight drawn between them
# Contains logic to manage touch between the overlapping sliders and prevent them from crossing over each other,
# as well as resize the highlight rectangle according to the min and max thumb values
class RangeSlider(MDFloatLayout):
    # Wait until all kv rules have been applied to the widget before proceeding
    def on_kv_post(self, base_widget):
        # This prevents one slider from 'stealing' touches meant for the other
        self.ids.slider_min.on_touch_down = self.filter_touch_min
        self.ids.slider_max.on_touch_down = self.filter_touch_max

        # Update the min and max thumb values to prevent them from crossing each other
        self.ids.slider_min.bind(value=self.update_min)
        self.ids.slider_max.bind(value=self.update_max)

        # Create rectangle highlight between the thumbs
        with self.canvas.after:
            Color(0, 1, 0, 1)
            self.highlight = Rectangle()

        # Update rect when sliders move or window resizes to keep it in place between the thumbs
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.ids.slider_min.bind(value_pos=self.update_rect)
        self.ids.slider_max.bind(value_pos=self.update_rect)

        # Set thumb values according to filters
        self.set_initial_values()

    # Set thumb values according to filters
    def set_initial_values(self):
        root = App.get_running_app().root

        grade_min = None
        grade_max = None

        for f in root.filters:
            if f.startswith("grade_min="):
                grade_min = float(f.split("=")[1].strip())

            if f.startswith("grade_max="):
                grade_max = float(f.split("=")[1].strip())

        # Apply filters to the thumb values
        if grade_min is not None:
            self.ids.slider_min.value = grade_min

        if grade_max is not None:
            self.ids.slider_max.value = grade_max

        # Update highlight after setting values
        self.update_rect()

    # Handle touches closer to the min handle and ignore those closer to the max handle and update the grade filter
    def filter_touch_min(self, touch):
        # If the touch is closer to the MAX handle, ignore it here
        if abs(touch.x - self.ids.slider_max.value_pos[0]) < abs(
            touch.x - self.ids.slider_min.value_pos[0]
        ):
            return False  # Let the touch pass to slider_max
        return MDSlider.on_touch_down(self.ids.slider_min, touch)

    # Handle touches closer to the max handle and ignore those closer to the min handle and update the grade filter
    def filter_touch_max(self, touch):
        # If the touch is closer to the MIN handle, ignore it here
        if abs(touch.x - self.ids.slider_min.value_pos[0]) < abs(
            touch.x - self.ids.slider_max.value_pos[0]
        ):
            return False  # Let the touch pass to slider_min
        return MDSlider.on_touch_down(self.ids.slider_max, touch)

    # Prevent the min thumb from crossing the max thumb
    def update_min(self, instance, value):
        if value > self.ids.slider_max.value:
            self.ids.slider_min.value = self.ids.slider_max.value
        # Update grade filter
        update_grade_filters(self, f"grade_min= {self.ids.slider_min.value}")

    # Prevent the max thumb from crossing the min thumb
    def update_max(self, instance, value):
        if value < self.ids.slider_min.value:
            self.ids.slider_max.value = self.ids.slider_min.value
        # Update grade filter
        update_grade_filters(self, f"grade_max= {self.ids.slider_max.value}")

    # Adjust the size of the highlight in between the thumbs
    def update_rect(self, *args):
        # Manually calculate the highlighted bar position
        self.highlight.pos = (
            self.x + (self.ids.slider_min.value_pos[0] - dp(8)),
            self.center_y - dp(4),
        )
        self.highlight.size = (
            self.ids.slider_max.value_pos[0] - self.ids.slider_min.value_pos[0],
            dp(4),
        )


# Add or remove a filter from the button grid
def update_button_filters(self, filter):
    root = App.get_running_app().root

    if filter.text not in root.filters:
        # Add filter
        root.filters.append(filter.text)
        filter.background_color = (0, 1, 0, 1)
    else:
        # Remove filter
        root.filters.remove(filter.text)
        # If filter is a button (needs color change)
        if type(filter) is not str:
            filter.background_color = (1, 1, 1, 1)


# Remove the old and add the new for the grade_max or grade_min filter
def update_grade_filters(self, filter):
    root = App.get_running_app().root

    # Remove old grade filter
    if "grade_min" in filter:
        root.filters = [f for f in root.filters if "grade_min" not in f]

    if "grade_max" in filter:
        root.filters = [f for f in root.filters if "grade_max" not in f]

    # Add new grade filter
    root.filters.append(filter)
