import discord
import asyncio
from discord.ext import commands
import random
import mysql.connector
import datetime
import logging
import sys

#Variable pour connexion à la base T4C
mysql_host = ""
mysql_user = ""
mysql_password = ""
mysql_base = ""

#Variable pour le bot Discord
channelCimetiere = ""
channelCC = ""
botKey = ""



class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''

   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())

logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   filename="out.log",
   filemode='a'
)

stdout_logger = logging.getLogger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('STDERR')
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl


description = '''An example bot to for T4C'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Commands T4C

# Boucle toutes les 5 minutes et annonce les morts depuis les 5 derniéres minutes
async def send_message_to_channel(channel, message):
     await bot.wait_until_ready()
     await bot.send_message(channel,'{0} : {1}'.format(channel,message))

# Commande cimetiere, annonce le top 10 XP
@bot.command()
async def top10XP():
        conn = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password, database=mysql_base)
        cursor = conn.cursor()
        cursor.execute("""SELECT PlayerName,CurrentLevel FROM playingcharacters ORDER BY CurrentLevel DESC LIMIT 10""")
        rows = cursor.fetchall()
        for row in rows:
                await bot.say('{0} - lvl {1}'.format(row[0],row[1]))
        conn.close()

bot.run(botKey)
