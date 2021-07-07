import os, discord, csv, asyncio
from random import randint
from discord.ext import commands, tasks

#Variables
my_id = "<@255879838987059201>"
her_id = "<@342466814728470532>"
channel_id = 862138233189040168
hours = 4#Interval between message resending

client = discord.Client()
bot = commands.Bot("!")

@client.event
async def on_ready():
  print(f"{client.user} logged in now!")
  client.loop.create_task(lovemessage())

#Open file with phrases and put all phrases in the list
phrases = []
with open("phrases.csv") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=",")
  for row in csv_reader:
    phrases.append(row[1])

#Send love messages every 4 hours
async def lovemessage():
  await client.wait_until_ready()
  while not client.is_closed():
    channel = client.get_channel(id=channel_id)
    response = phrases[randint(0, len(phrases)-1)]
    await channel.send(response)#Send message

    await asyncio.sleep(60*60*hours)#Wait

#Respond to messages
@client.event
async def on_message(message):
  #print(message.content)
  #print(dir(message))#Print all atributes of the bot
  #await message.delete() #Delete messages obviously
  if message.content.startswith("$greet"):
    await message.channel.send(f"Hello my comrade {message.author}")
  elif "$message" in message.content:
    response = phrases[randint(0, len(phrases)-1)]
    await message.channel.send(response)
  elif "$mentionme" in message.content:
    mention = "<@" + str(message.author.id) + ">"
    await message.channel.send(' %s hello you ' % mention)

#Run Bot
my_secret = os.environ['TOKEN']
client.run(my_secret)
