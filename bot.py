from config import *
from logic import *
import discord
from discord.ext import commands
from config import TOKEN

# Initializing the database manager
manager = DB_Map("database.db")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot started")

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f"Hi, {ctx.author.name}. Enter !help_me to explore the list of available commands")

@bot.command()
async def help_me(ctx: commands.Context):
    await ctx.send(
        # Implement the command that will display the list of available commands
    )

@bot.command()
async def show_city(ctx: commands.Context, *, city_name=""):
    # Implement the command that will display the map with the specified city

@bot.command()
async def show_my_cities(ctx: commands.Context):
    cities = manager.select_cities(ctx.author.id)  # Getting the list of cities remembered by the user

    # Implement the command that will display the map with the user's cities

@bot.command()
async def remember_city(ctx: commands.Context, *, city_name=""):
    if manager.add_city(ctx.author.id, city_name):  # Checking if the city exists in the database; if so, adding it to user's memory
        await ctx.send(f'The city of {city_name} has been saved successfully!')
    else:
        await ctx.send("Incorrect format. Please enter the name of the city in English, with a space after the command.")

if __name__ == "__main__":
    bot.run(TOKEN)