import sqlite3


def getClimbList(db_path):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name, setter_username FROM climbs")
            climb_data0 = cursor.fetchall()
            cursor.execute(
                "SELECT ascensionist_count, display_difficulty FROM climb_stats"
            )
            climb_data1 = cursor.fetchall()
            # Combine the two sets o1f data into a single list of tuples
            climb_data = []
            for i, j in zip(climb_data0, climb_data1):
                climb_data.append(i + j)

            return climb_data
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
