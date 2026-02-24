import sqlite3
from kivymd.uix.list import IRightBodyTouch, MDList, ThreeLineRightIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


# Just TB2 40 degrees data for now, currently capped at one 50 item page
def get_climb_list(db_path, filters):
    # Get the data from database file
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT 
                    c.name,
                    c.setter_username,
                    c.uuid,
                    s.ascensionist_count,
                    s.display_difficulty
                FROM climbs c
                JOIN climb_stats s
                    ON c.uuid = s.climb_uuid
                WHERE c.layout_id = ?
                  AND c.angle = ?
                  AND s.angle = ?
                LIMIT 50
            """,
                ("11", "40", "40"),
            )

            climb_data = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")

    climb_list = MDList()

    # Populate the climb list with climbs
    for climb in climb_data:
        item = ThreeLineRightIconListItem(
            text=climb[0],  # Climb name
            secondary_text=f"Set by {climb[1]}",  # Setter name
            tertiary_text=f"{climb[3]} repeats",  # Repeat count
        )
        # Add the custom right container to each list item
        item.add_widget(GradeContainer().getGrade(climb[4]))  # Climb grade
        climb_list.add_widget(item)

    return climb_list


# Custom container for the right side of each climb list item, which includes the climb's grade and a placeholder for more info icons (has instagram beta, benchmark/classic)
class GradeContainer(IRightBodyTouch, MDBoxLayout):
    def getGrade(self, grade):
        self.orientation = "vertical"
        self.size_hint_x = None

        self.add_widget(MDLabel(text=str(grade), halign="left"))

        return self
