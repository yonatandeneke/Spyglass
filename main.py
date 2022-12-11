import discord
from mcstatus import JavaServer
from discord.ext import commands, tasks

TOKEN = 'YOUR_TOKEN'

SERVER_IP = "hypixel.net"
SERVER_PORT = 25565

bot = commands.Bot(command_prefix='$', intents=discord.Intents.default())

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.tree.sync()
    print('Spyglass online.')
    updateStatus.start()

@bot.tree.command(name='changeserver', description='Change the server to watch.')
async def changeServer(interaction: discord.Interaction, serverip: str, serverport: int):
    global SERVER_IP
    global SERVER_PORT
    SERVER_IP = serverip
    SERVER_PORT = serverport
    await interaction.response.send_message("Server changed to " + SERVER_IP + ":" + str(SERVER_PORT))

@tasks.loop(seconds=5.0)
async def updateStatus():
    status = JavaServer.lookup(SERVER_IP, SERVER_PORT).status()
    count = str(status.players.online) + "/" + str(status.players.max)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(count + " on " + SERVER_IP)))


bot.run(TOKEN)