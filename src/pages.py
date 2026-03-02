from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.core.window import Window
from kivymd.uix.slider import MDSlider
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.slider import MDSlider
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.lang import Builder

import data
import menus


# KV = """
# <MDSliderHandle>:
#     # 1. Standard elevation removal
#     elevation: 0

#     # 2. Force shadow colors to fully transparent
#     shadow_color: 0, 0, 0, 0
#     shadow_soft_color: 0, 0, 0, 0
#     shadow_hard_color: 0, 0, 0, 0

#     # 3. Remove the blur/softness entirely
#     shadow_softness: 0

#     # 4. Remove the "halo" glow when touched
#     state_layer_size: 0

#     """

# Builder.load_string(KV)


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


class FilterPage(BoxLayout):
    def __init__(self, filters, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.9
        self.orientation = "vertical"
        self.name = "filter_page"
        self.filters = filters

        # Add upper menu
        self.add_widget(menus.UpperMenu())

        # Add double slider layout (two sliders on the same position)
        grade_slider = RangeSlider(
            size_hint_x=1,
        )
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
                on_release=lambda instance, option=filter_option: self.add_filter(
                    instance
                )
            )
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


class RangeSlider(MDFloatLayout):
    def on_kv_post(self, base_widget):
        # This prevents one slider from 'stealing' touches meant for the other
        self.ids.slider_min.on_touch_down = self.filter_touch_min
        self.ids.slider_max.on_touch_down = self.filter_touch_max

        # Bind logic
        self.ids.slider_min.bind(value=self.update_min)
        self.ids.slider_max.bind(value=self.update_max)

        # Create rectangle highlight
        with self.canvas.after:
            Color(0, 1, 0, 1)
            self.highlight = Rectangle()

        # Update rect when sliders move or window resizes
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.ids.slider_min.bind(value_pos=self.update_rect)
        self.ids.slider_max.bind(value_pos=self.update_rect)

    def filter_touch_min(self, touch):
        # If the touch is closer to the MAX handle, ignore it here
        if abs(touch.x - self.ids.slider_max.value_pos[0]) < abs(
            touch.x - self.ids.slider_min.value_pos[0]
        ):
            return False  # Let the touch pass to slider_max
        return MDSlider.on_touch_down(self.ids.slider_min, touch)

    def filter_touch_max(self, touch):
        # If the touch is closer to the MIN handle, ignore it here
        if abs(touch.x - self.ids.slider_min.value_pos[0]) < abs(
            touch.x - self.ids.slider_max.value_pos[0]
        ):
            return False  # Let the touch pass to slider_min
        return MDSlider.on_touch_down(self.ids.slider_max, touch)

    def update_min(self, instance, value):
        if value > self.ids.slider_max.value:
            self.ids.slider_min.value = self.ids.slider_max.value

    def update_max(self, instance, value):
        if value < self.ids.slider_min.value:
            self.ids.slider_max.value = self.ids.slider_min.value

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
