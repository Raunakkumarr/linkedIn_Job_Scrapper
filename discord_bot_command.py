import os
import discord
from bs4 import BeautifulSoup
import requests

my_secret = os.environ['BotKey']

botCmd = discord.Client()

@botCmd.event
async def on_ready():
  print("Carrer Bot has logged in. Bot Name is {0.user}".format(botCmd))

@botCmd.event
async def on_message(message):
  if message.author == botCmd.user:
    return

  initial_url = 'https://www.linkedin.com/jobs/search?'

  msg = message.content
  if msg.lower().startswith('&findjob'):
    location = msg.split(":")[1]
    keyword = msg.split(":")[2]
    if " " in location:
        location = location.replace(" ","%20")
    if "," in location:
        location = location.replace(",","%2C")
    if " " in keyword:
        keyword = keyword.replace(" ","%20")
    if "," in keyword:
        keyword = keyword.replace(",","%2C")
    final_url = initial_url+"keywords="+keyword+"&location="+location+"&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"
    address = requests.get(final_url)
    src = address.content
    soup = BeautifulSoup(src, 'lxml')
    jobs = soup.find_all('a', class_="base-card__full-link")
    for i in range(0,10):
      job = jobs[i]
      link=job['href']
      parent = job.find_parent()
      title = parent.find('h3').text
      company = parent.find('h4').text
      location = parent.find('span',class_="job-search-card__location").text
      posted_on=parent.find('time')['datetime']
      job_msg = discord.Embed(title="Job Search Result", description="Check out some results to your query for prefferred job type. If the results didn't satisfy you, please try providing some other location or keywords.", color=0x00ff00)
      job_msg.add_field(name="S.N.",value=str(i+1), inline=True)
      job_msg.add_field(name="Job: ",value=title, inline=True)
      job_msg.add_field(name="Company: ",value=company, inline=True)
      job_msg.add_field(name="Location: ",value=location, inline=True)
      job_msg.add_field(name="Date Posted: ",value=posted_on, inline=True)
      job_msg.add_field(name="Get more Info: ",value=link, inline=True)
      job_msg.set_author(name="Linkdev Community", url="https://linkdev-sabin.herokuapp.com/login", icon_url="https://raw.githubusercontent.com/Raunakkumarr/linkedIn_Job_Scrapper/main/linkdev.jpg")
      job_msg.set_thumbnail(url="https://raw.githubusercontent.com/Raunakkumarr/linkedIn_Job_Scrapper/main/linkdev.jpg")
      job_msg.set_footer(text="Information requested by: {}".format(message.author.display_name))
      await message.channel.send(embed=job_msg)

  if msg.lower().startswith('&help'):
    help_msg = discord.Embed(title="Career Bot User Guide", description="In order to use the bot, please go through the instructions first.", color=0x00ff00)
    help_msg.add_field(name="Instructions to User Manual",value="Please use the command format '&findjob:Location:Keyword' to search for a job at particular location with a particular keyword.", inline=False)
    help_msg.add_field(name="Note:",value="Please do not use space before or after ':' for optimized results.", inline=False)
    help_msg.add_field(name="Remember:",value="'Location' in above instructions means where do you want the job to be and 'Keyword' means what kind or speciality of job do you want.", inline=False)
    help_msg.set_author(name="Raunak Kumar", url="https://www.raunakmishra.com.np/#Contact", icon_url="https://www.raunakmishra.com.np/signature.png")
    help_msg.set_thumbnail(url="https://raw.githubusercontent.com/Raunakkumarr/linkedIn_Job_Scrapper/main/linkdev.jpg")
    help_msg.set_footer(text="Information requested by: {}".format(message.author.display_name))
    await message.channel.send(embed=help_msg)
botCmd.run(my_secret)
