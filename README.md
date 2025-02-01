# The Mapping Bot

This project is a bot that allows users to display specified cities on the map and to save cities for further display.

## Key Features

- **Display cities on a map**: The bot can display selected cities on a map using Cartopy and Matplotlib libraries.
- **Save cities**: Users can save cities they are interested in to their personal list.
- **View saved cities**: Upon request, the bot can output a list of all cities saved by the user.

## Technologies

- **Python 3**: Programming language.
- **SQLite**: Database for storing user and city information.
- **Matplotlib and Cartopy**: Libraries for creating graphical data representations.
- **Discord.py**: Library for creating and managing bots.

## Installation and Setup

1. **Clone the repository:**
    ```bash
    git clone <url_to_repository>
    cd <repository_name>
    ```
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure environment variables:**
Open the `config.py` file in the root directory of the project and set the necessary variables:
    ```bash
    TOKEN=<your_bot_token>
    ```
4. **Run the bot:**
    ```bash
    python bot.py
    ```

## List of bot's commands

- `!start` - start working with the bot and receive a welcome message.\n"
- `!help_me` - receive the list of available commands\n"
- `!show_city <city_name>` - display the given city on the map.\n"
- `!remember_city <city_name>` - remember the given city.\n"
- `!show_my_cities` - display all the rememberd cities."
        
