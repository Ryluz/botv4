
#Defines import system
import requests
import json
import discord
import os
from discord.ext.commands import Bot
from discord import Intents
from keep_alive import keep_alive

#Gets key and token from environmental file
KEY = os.environ['KEY']
TOKEN = os.environ['TOKEN']

#Defines bot command prefix
bot = Bot("!") # or whatever prefix you choose(!,%,?)
bot.remove_command('help')

#Connects to discord bot and sets status
#Prints in console log when ready
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "the air"))
    print("ready!")

#Defines "a" as prefix follower to run command
@bot.command(name="a")
#Gets text put after command
async def who(context, arg):
  #Tries to run command, error results in different code running
  try:
    channel = context.channel
    #Defines API from which the information is gotten
    data = requests.get("https://api.weatherbit.io/v2.0/current/airquality?postal_code="+ str(arg)+"&country=US&key=" + str(KEY)).json()

    #Defines variables containing data from API list
    airQuality = str(data["data"][0]["aqi"])
    Pm10 = round(data["data"][0]["pm10"], 3)
    O3 = round(data["data"][0]["o3"], 3)
    So2 = round(data["data"][0]["so2"], 3)
    No2 = round(data["data"][0]["no2"], 3)
    Pm25 = round(data["data"][0]["pm25"], 3)
    Co = round(data["data"][0]["co"], 3)
    cityName = data["city_name"]
    preDominant = data["data"][0]["predominant_pollen_type"]
    stateCode = data["state_code"]

    #Conditions to determine air quality
    #Ex: Good air quality (from 0-50 AQI) --> good air quality and a green color for the vertical sidebar
    if int(airQuality) >= 0 and int(airQuality) <= 50:
      aqi = str(airQuality) + " (Good)"
      colorz = 0x9cffa1
    elif int(airQuality) >= 51 and int(airQuality) <= 100:
      aqi = str(airQuality) + " (Moderate)"
      colorz = 0xFCF91E
    elif int(airQuality) >= 101 and int(airQuality) <= 150:
      aqi = str(airQuality) + " (Unhealthy for Sensitive Groups)"
      colorz = 0xFF5733
    elif int(airQuality) >= 151 and int(airQuality) <= 200:
      aqi = str(airQuality) + " (Unhealthy)"
      colorz = 0xEF1F07
    else:
      aqi = str(airQuality) + " (Very Unhealthy)"
      colorz = 0x581845
    

    #Defines discord embed --> formatting of information
    embed=discord.Embed(title= "Air Quality", url="https://www.weatherbit.io/", description="Check your city's air quality!" + "\n\u200b", color=colorz)
    embed.set_author(name="AirmonitorBot", icon_url="https://cdn.discordapp.com/attachments/935658413692682243/936301907343978496/Weather-No-Background_1.png")
    embed.set_thumbnail(url="https://aqicn.org/air/experiments/images/aqi-transparent.png")
    embed.add_field(name = "`>>" + str(cityName) + ", " + str(stateCode) + " " + str(arg) + "`", value= "------------------------------------------------------------------")
    embed.add_field(name="__AQI__", value=str(aqi) + "\n------------------------------------------------------------------", inline=False)
    
    embed.add_field(name="__Ozone__", value=str(O3) + " µg/m³" + "\n\u200b", inline=True)
    embed.add_field(name="__Carbon Monoxide__", value=str(Co) + " µg/m³" + "\n\u200b", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)


    embed.add_field(name="__Sulfur Dioxide__", value=str(So2) + " µg/m³" + "\n\u200b", inline=True)
    embed.add_field(name="__Nitrogen Dioxide__", value=str(No2) + " µg/m³" + "\n\u200b", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name="__PM < 2.5 μm__", value=str(Pm25) + " µg/m³" + "\n\u200b", inline=True)
    embed.add_field(name="__PM < 10 μm__", value=str(Pm10) + "  µg/m³" + "\n\u200b", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name="__Predominant Pollen Type__", value=str(preDominant) + "\n\u200b", inline=False)
    
    embed.set_footer(text="Made by ry#3306 and Wot#6821  •  01/27/2022")

    #Bot returns message after initial command
    await channel.send(embed=embed)
  except:
    #If no API list for requested zip code, return this message
    await channel.send("Please enter a valid zip code")

#Type !meme for a random meme (easteregg)
@bot.command(name="meme")
async def meme(ctx):
    request = requests.get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(request,)
    meme = discord.Embed(title=f"{data['title']}" , Color=discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)

#Runs function to keep bot running
keep_alive()

#Uses token from environmental file to run bot
bot.run(TOKEN)
