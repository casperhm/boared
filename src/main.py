from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from menus import LowerMenu
from pages import HomeLayout

Window.size = (540, 960)


# Main application layout
# This layout contains the upper menu, the main content area, and the lower menu.
class BoaredLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create the main content area
        self.add_widget(HomeLayout(), index=1)

        # Create the lower menu
        self.add_widget(LowerMenu(), index=0)

    # Function to switch between different pages in the main content area
    def show_page(self, page):
        # Remove the current page if it exists
        if len(self.children) > 0:
            self.remove_widget(self.children[1])
        # Add the new page to the layout
        self.add_widget(page, index=1)


class BoaredApp(MDApp):
    def build(self):
        return BoaredLayout()


if __name__ == "__main__":
    BoaredApp().run()
