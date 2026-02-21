from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


# Upper menu with board switch, angle change, reset filters, and create climb buttons
class UpperMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = 0.1

        # Board switch dropdown
        self.board_dropdown = DropDown()
        # Populate the dropdown with placeholder boards
        for board in ["Board 1", "Board 2", "Board 3"]:
            btn = Button(text=board, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.board_dropdown.select(btn.text))
            self.board_dropdown.add_widget(btn)

        # Main button to open the dropdown
        mainbutton = Button(text="Select Board", size_hint_x=0.65)
        mainbutton.bind(on_release=self.board_dropdown.open)
        self.board_dropdown.bind(
            on_select=lambda instance, x: setattr(mainbutton, "text", x)
        )
        self.add_widget(mainbutton)

        # Angle change button
        self.add_widget(Button(text="Angle Change", size_hint_x=0.15))

        # Reset filters button
        self.add_widget(Button(text="Reset Filters", size_hint_x=0.15))

        # Create climb button
        self.add_widget(Button(text="Create Climb", size_hint_x=0.15))


# Lower menu with settings, home, and profile buttons
class LowerMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = 0.1

        # Settings button
        self.add_widget(Button(text="Settings", size_hint_x=0.33))

        # Home button
        self.add_widget(Button(text="Home", size_hint_x=0.33))

        # Profile button
        self.add_widget(Button(text="Profile", size_hint_x=0.33))
