from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.list import IRightBodyTouch, MDList, ThreeLineRightIconListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

import data


# Main content area for the home page, which includes a search bar and a list of climbs.
# Each climb in the list is represented by a ThreeLineRightIconListItem, which includes the climb name, setter, and repeat count.
# The right side of each list item includes a custom container RightVerticalContainer.
class HomeLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create seach bar
        self.add_widget(TextInput(size_hint_y=0.075, hint_text="Search"))

        # Create list of climbs
        scroll = ScrollView()
        climb_list = MDList()

        # Populate the climb list with climbs
        for i in range(20):
            # Get climb data from the database
            climb_data = data.getClimbList("./data/tensiondata")

            item = ThreeLineRightIconListItem(
                text=climb_data[i][0],  # Climb name
                secondary_text=f"Set by {climb_data[i][1]}",  # Setter name
                tertiary_text=f"{climb_data[i][2]} repeats",  # Repeat count
            )
            # Add the custom right container to each list item
            item.add_widget(GradeContainer().getGrade(climb_data[i][3]))  # Climb grade
            climb_list.add_widget(item)

        # Add the climb list to the scroll view and then add the scroll view to the layout
        scroll.add_widget(climb_list)
        self.add_widget(scroll)


# Custom container for the right side of each climb list item, which includes the climb's grade and a placeholder for more info icons (has instagram beta, benchmark/classic)
class GradeContainer(IRightBodyTouch, MDBoxLayout):
    def getGrade(self, grade):
        self.orientation = "vertical"
        self.size_hint_x = None

        self.add_widget(MDLabel(text=str(grade), halign="left"))

        return self
