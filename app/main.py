from app.database import SessionLocal, sec_man
from app import crud
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import json


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Config:
    def __init__(self):
        load_dotenv()
        #self.TOKEN = sec_man.env["DISCORD_TOKEN"]
        self.TOKEN = os.getenv("DISCORD_TOKEN")


conf = Config()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if not message.author.bot:

        if crud.get_honeypot_channel(message):
            if crud.check_protected(message):
                return
            await message.delete()
            if crud.global_bans_enabled(message):
                crud.add_global_ban(message.author)
                await message.author.ban(reason="Global ban")
                print(f"{message.author.name} was banned from {message.guild} for triggering the honeypot")
                print(f"{message.author.name} was globally banned")
            else:
                await message.author.ban(reason="Honeypot ban")
                print(f"{message.author.name} was banned from {message.guild} for triggering the honeypot")

        prefix = crud.read_prefix(message)
        if message.content.startswith(prefix):
            await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    global_banned = crud.check_global_bans(member)
    if global_banned:
        await member.ban(reason="Global ban")
        print(f"{member.name} was banned from {member.guild} being globally banned")
        return


@bot.command()
async def protect_user(ctx):
    success = await crud.set_protected(ctx)
    if success:
        await ctx.send("User protected")
    else:
        await ctx.send("An error occurred")


@bot.command()
async def set_prefix(ctx):
    prefix = ctx.message.content.split(" ")[1]
    if len(prefix) > 1:
        await ctx.send("Prefix must be one character")
        return
    success = crud.set_prefix(ctx, prefix)
    if success:
        await ctx.send(f"Prefix set to {prefix}")
    else:
        await ctx.send("An error occurred")


bot.run(conf.TOKEN)