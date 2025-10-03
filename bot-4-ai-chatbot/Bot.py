import discord
from discord.ext import commands
import openai
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")

@bot.event
async def on_ready():
    print(f"🤖 AI Bot logged in as {bot.user}")

@bot.command()
async def ask(ctx, *, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}]
    )
    await ctx.send(response['choices'][0]['message']['content'])

bot.run(os.getenv("DISCORD_TOKEN"))
