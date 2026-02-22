from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from menus import UpperMenu, LowerMenu
from pages import HomeLayout

Window.size = (540, 960)


# Main application layout
# This layout contains the upper menu, the main content area, and the lower menu.
class BoaredLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create the upper menu
        self.add_widget(UpperMenu())

        # Create the main content area
        self.add_widget(HomeLayout())

        # Create the lower menu
        self.add_widget(LowerMenu())


class BoaredApp(MDApp):
    def build(self):
        return BoaredLayout()


if __name__ == "__main__":
    BoaredApp().run()


# ideas:
# average user grade
