import sqlite3
import matplotlib

matplotlib.use('Agg')  # Installing the Matplotlib backend to save files in memory without displaying a window
import matplotlib.pyplot as plt
import cartopy.crs as ccrs  # Importing the module that will allow us to work with map projections

class DB_Map():
    def __init__(self, database):
        self.database = database  # Initializing the database path

    def create_user_table(self):
        conn = sqlite3.connect(self.database)  # Connecting to the database
        with conn:
            # Creating a table, if it does not exist, for storing user cities
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()  # Confirming the changes

    def add_city(self, user_id, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            # Querying the database for the city by name
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]
                # Adding the city to the user's list of cities
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1  # Indicating that the operation was a success
            else:
                return 0  # Indicating that the city wasn't found

    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            # Selecting all of the user's cities
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))
            cities = [row[0] for row in cursor.fetchall()]
            return cities  # Returning the user's list of cities

    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            # Getting the coordinates of the city by its name
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates  # Returning the city's coordinates

    def create_graph(self, path, cities):
        pass

    def draw_distance(self, city1, city2):
        # Drawing a line between two cities to display the distance
        pass


if __name__ == "__main__":
    m = DB_Map("database.db")  # Creating an that will interact with the database
    m.create_user_table()   # Creating the table with user's cities, if it does not already exist
