import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random
import mysql.connector
import sys

#Variable pour connexion à la base T4C
mysql_host = ""
mysql_user = ""
mysql_password = ""
mysql_base = ""

#Variable pour le bot Discord
botKey = ""

description = '''A bot form T4C''' 
client = commands.Bot(command_prefix="?", description=description)

# Id des channels discord
channels = {
	"cc-main" : xxxxxxxxxxxxxxx,
	"cc-shop" : xxxxxxxxxxxxxxx,
	"cc-cimetiere" : xxxxxxxxxxxxxxx,
	"cc-francais" : xxxxxxxxxxxxxxx,
	"cc-english" : xxxxxxxxxxxxxxx,
	"cc-portugues" : xxxxxxxxxxxxxxx
}
		
@client.event
@asyncio.coroutine
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@asyncio.coroutine
def death_log():
	yield from client.wait_until_ready()
	while not client.is_closed:
		conn = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password,database=mysql_base)
		cursor = conn.cursor()
		cursor.execute("""select TIMESTAMP,VICTIME,ASSASSIN from discord_logdeath""")
		rows = cursor.fetchall()
		channel = discord.Object(id=channels['cc-cimetiere'])
		for row in rows:
			yield from client.send_message(channel,'```{0} à été tué par {1}```'.format(row[1],row[2]))
        
		cursor.execute("""TRUNCATE TABLE discord_logdeath""")
		conn.commit()
		cursor.close()
		conn.close()
		
		yield from  asyncio.sleep(5) # task runs every 60 seconds


client.loop.create_task(death_log())
client.run(botKey)

