from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import menus
import pages

Window.size = (540, 960)


# Main application layout
# This layout contains the upper menu, the main content area, and the lower menu.
class BoaredLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Search filters
        self.filters = []

        # Store last visited page
        self.last_page = None
        self.orientation = "vertical"

        # Create the main content area
        self.add_widget(pages.HomePage(), index=1)

        # Create the lower menu
        self.add_widget(menus.LowerMenu(), index=0)

    # Function to switch between different pages in the main content area
    def show_page(self, page):
        # Remove the current page if it exists
        if len(self.children) > 0:
            # Save current page to last_page
            self.last_page = self.children[1]
            self.remove_widget(self.children[1])
        # Add the new page to the layout
        self.add_widget(page, index=1)


class BoaredApp(MDApp):
    def build(self):
        return BoaredLayout()


if __name__ == "__main__":
    BoaredApp().run()
