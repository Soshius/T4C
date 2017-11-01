import discord
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
botKey = "DISCORD_API_KEY"

description = '''A wonderfull bot that allow interaction with a T4C Server''' 
client = commands.Bot(command_prefix="?", description=description)

channels = {
	"Main" : 000000000000000,
	"Trade" : 000000000000000,
	"Death" : 000000000000000,
	"Francais" : 000000000000000,
	"English" : 000000000000000,
	"Portugues" : 000000000000000
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
		cursor.execute("""select date_format(TIMESTAMP,'%H:%i:%S') as formatted_date,VICTIME,ASSASSIN from discord_logdeath""")
		rows = cursor.fetchall()
		channel = discord.Object(id=channels['Death'])
		for row in rows:
			yield from client.send_message(channel,"""```Markdown
[{0}]({1})[ got killed by ]({2})
```""".format(row[0],row[1],row[2]))
        
		cursor.execute("""TRUNCATE TABLE discord_logdeath""")
		conn.commit()
		cursor.close()
		conn.close()
		
		yield from  asyncio.sleep(5) # task runs every 5 seconds

@asyncio.coroutine
def chat_log(chat):
	yield from client.wait_until_ready()
	while not client.is_closed:
		conn = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password,database=mysql_base)
		cursor = conn.cursor()
		cursor.execute("""select date_format(TIMESTAMP,'%H:%i:%S') as formatted_date,PLAYER,MESSAGE from discord_logchat where CHANNEL='""" + chat+ "'")
		rows = cursor.fetchall()
		channel = discord.Object(id=channels[chat])
		for row in rows:
			yield from client.send_message(channel,"""```Markdown
[{0}]({1})[{2}]
```""".format(row[0],row[1],row[2]))
        
		cursor.execute("""DELETE FROM discord_logchat WHERE CHANNEL='""" + chat + "'")
		conn.commit()
		cursor.close()
		conn.close()
		
		yield from  asyncio.sleep(5) # task runs every 5 seconds
		
@client.command()
@asyncio.coroutine
def playtime(player : str):
	""" Usage : ?playtime PlayerName   (This command show the total playtime of the player)"""
	conn = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password,database=mysql_base)
	cursor = conn.cursor()
	cursor.execute("""select PLAYTIME from playtime where PLAYER='""" + player+ "'")
	rows = cursor.fetchall()
	playtime = 0
	for row in rows:
		playtime += row[0]
	m, s = divmod(playtime, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	yield from client.say(player + " played %d day(s) and %d hour(s), %02d minute(s) et %02d second(s)" % (d, h, m, s))
	


client.loop.create_task(death_log())
client.loop.create_task(chat_log('Main'))
client.loop.create_task(chat_log('Trade'))
client.loop.create_task(chat_log('Francais'))
client.loop.create_task(chat_log('English'))
client.loop.create_task(chat_log('Portugues'))
client.run(botKey)

