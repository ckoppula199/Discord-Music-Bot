import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from music import Player

intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is now online')
    bot.add_cog(Player(bot))

bot.run(TOKEN)