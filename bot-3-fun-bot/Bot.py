import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and now it won’t stop sending me KitKat ads."
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def joke(ctx):
    await ctx.send(random.choice(jokes))

@bot.command()
async def roast(ctx, user: discord.Member):
    roasts = ["You're as useless as the 'ueue' in 'queue'.", "You're the reason the gene pool needs a lifeguard."]
    await ctx.send(f"{user.mention}, {random.choice(roasts)}")

@bot.command()
async def eightball(ctx, *, question):
    responses = ["Yes", "No", "Maybe", "Definitely", "Ask again later"]
    await ctx.send(f"🎱 {random.choice(responses)}")

bot.run(os.getenv("DISCORD_TOKEN"))
