import sqlite3
from kivymd.uix.list import IRightBodyTouch, MDList, ThreeLineRightIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image


# Just TB2 40 degrees data for now, currently capped at one 50 item page
# one arg for each filter
def get_climb_list(db_path, filters):
    # Base query (temporary fixed params for TB2 @40)
    query_base = """
        SELECT c.name, 
            c.setter_username, 
            c.uuid, 
            s.ascensionist_count, 
            s.display_difficulty, 
            s.benchmark_difficulty,
            (SELECT 1 FROM beta_links b WHERE b.climb_uuid = c.uuid LIMIT 1) AS has_beta,
            c.is_nomatch
        FROM climbs c
        JOIN climb_stats s ON c.uuid = s.climb_uuid
        WHERE c.layout_id = ? AND c.angle = ? AND s.angle = ?
    """
    params = ["11", "40", "40"]
    query_addons = []

    # Add additional filters
    if "Benchmark" in filters:
        query_addons.append("AND s.benchmark_difficulty NOTNULL")
    if "Beta video" in filters:
        # This checks if the climb's UUID exists in the beta_links table
        query_addons.append("""
            AND EXISTS (
                SELECT 1 FROM beta_links b WHERE b.climb_uuid = c.uuid
            )
        """)

    # final query
    final_query = f"{query_base} {' '.join(query_addons)} LIMIT 50"

    # Get the data from database file
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(final_query, params)

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
        item.add_widget(ListRightContainer(climb))
        climb_list.add_widget(item)

    return climb_list


# Custom container for the right side of each climb list item, which includes the climb's grade and a placeholder for more info icons (has instagram beta, benchmark/classic)
class ListRightContainer(IRightBodyTouch, MDBoxLayout):
    def __init__(self, climb, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_x = None

        # Grade label
        self.add_widget(MDLabel(text=get_grade_string(climb[4]), halign="left"))

        # Icon container (for benchmark/classic, nomatch, and instagram beta)
        icon_container = MDBoxLayout(orientation="horizontal", padding=0, spacing=0)
        # Benchmark/Classic icon
        if climb[5] is not None:
            icon_container.add_widget(
                Image(
                    source="./data/icons/classic.png",
                    size_hint=(None, None),
                    size=("20dp", "20dp"),
                )
            )

        # Instagram beta
        if climb[6] == 1:  # uuid found in beta_links
            icon_container.add_widget(
                Image(
                    source="./data/icons/instagram.png",
                    size_hint=(None, None),
                    size=("20dp", "20dp"),
                )
            )

        # Match / No match
        if climb[7] == 1:
            icon_container.add_widget(
                Image(
                    source="./data/icons/no_match.png",
                    size_hint=(None, None),
                    size=("20dp", "20dp"),
                )
            )
        self.add_widget(icon_container)


GRADE_MAP = {
    1: "1a/V0",
    2: "1b/V0",
    3: "1c/V0",
    4: "2a/V0",
    5: "2b/V0",
    6: "2c/V0",
    7: "3a/V0",
    8: "3b/V0",
    9: "3c/V0",
    10: "4a/V0",
    11: "4b/V0",
    12: "4c/V0",
    13: "5a/V1",
    14: "5b/V1",
    15: "5c/V2",
    16: "6a/V3",
    17: "6a+/V3",
    18: "6b/V4",
    19: "6b+/V4",
    20: "6c/V5",
    21: "6c+/V5",
    22: "7a/V6",
    23: "7a+/V7",
    24: "7b/V8",
    25: "7b+/V8",
    26: "7c/V9",
    27: "7c+/V10",
    28: "8a/V11",
    29: "8a+/V12",
    30: "8b/V13",
    31: "8b+/V14",
    32: "8c/V15",
    33: "8c+/V16",
    34: "9a/V17",
    35: "9a+/V18",
    36: "9b/V19",
    37: "9b+/V20",
    38: "9c/V21",
    39: "9c+/V22",
}


# Returns the Font/V-scale string for a given difficulty integer
def get_grade_string(difficulty_int):
    return GRADE_MAP.get(int(difficulty_int), "Unknown")
