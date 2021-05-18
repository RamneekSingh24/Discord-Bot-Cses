import discord
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import threading
import time
import pprint
from keep_alive import keep_alive


users = {}
all_probs = pd.read_csv('problems/all.csv')
prob_ids = [p[-4:] for p in list(all_probs['link'])]
prob_names = list(all_probs['name'])
headers = (eval(os.getenv('headers').strip()))
cookies = (eval(os.getenv('cookies').strip()))
topics = {
'Introductory Problems':[0,18], 
'Sorting and Searching':[19,53],
'Dynamic Programming':[54,72],
'Graph Algorithms':[73,108],
'Range Queries': [109,127],
'Tree Algorithms':[128,143],
'Mathematics':[144,174],
'String Algorithms':[175,191],
'Geometry':[192,198],
'Advanced Techniques':[199,222],
'Additional Problems':[223,299]
}







#https://colab.research.google.com/drive/1aR8PU0Avbl5JXrtbS4MiK-_Chq3PrUXs#scrollTo=mTBrOKHucXMy
#https://cses.fi/problemset/user/61694/ dr_pp
#https://cses.fi/problemset/user/24029/ dbhupi12
#https://cses.fi/user/17331 chill_coder


def update(username, p_no, l_no = 1):
  p_id = prob_ids[p_no]
  l_no = str(l_no)
  url = 'https://cses.fi/problemset/hack/1093/list/12/'+l_no
  url = url.replace("1093", str(p_id))
  #print(url)
  response = requests.get(url, headers=headers, cookies=cookies)
  #print(response)
  soup = BeautifulSoup(response.text, 'html.parser')
  found = 0
  table = soup.find_all('table')
  submissions = table[0].find_all('tr')
  for sub in submissions:
    info = sub.find_all('td')
    if(len(info) < 6):
      continue
    if username == info[1].text:
      rc = update_h(info,username,p_no)
      return rc
  return 0


def update_h(info,unsername,p_no):
  print(info)
  return 1



def thread_function(username='dr_pp', userid = 61694):
  #userid = 61694
  #username = 'dr_pp'
  ns = threading.local()
  users[username] = userid
  
  ns.URL = 'https://cses.fi/problemset/user/'+str(userid)+'/'

  ns.df = pd.read_csv('users/'+username+'.csv')
  ns.prev_solved = ns.df['time']
  
  ns.prev_solved = [0 if str(p) == 'nan' else 1 for p in ns.prev_solved]


  while True:
    ns.page = requests.get(ns.URL)
    ns.soup = BeautifulSoup(ns.page.content, 'html.parser')
    ns.data = ns.soup.find_all('td')
    ns.data = [ns.d.find('a')['class'] for ns.d in ns.data]
    ns.solved = [0 if len(ns.d) <= 2 else (1 if ns.d[2] =='full'\
    else 0) for ns.d in ns.data]
    
    ns.new_solved = []

    for i in range(len(ns.solved)):
      if ns.solved[i] != ns.prev_solved[i]:
        ns.new_solved.append(i)
      
    for p_no in ns.new_solved:
      #p_pid = prob_ids[p_no]
      print("SOLVED: " , p_no)
      ns.info = []
      ns.rc = 0
      ns.l_no = 0
      while ns.rc == 0:
        ns.l_no += 1
        if ns.l_no == 3:
          break
        ns.rc = update(username, p_no, ns.l_no)
      

      ns.prev_solved =  ns.solved





# while True:
#   rc = update('dr_pp',0)
#   if rc == 1:
#     break

#thread_function()





client = discord.Client()



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  params = message.content.split(' ')
  if params[0] == '!file':
    att = message.attachments[0]
    f = open('users/'+att.filename, "wb")
    await att.save(f)
    userid = params[1]
    username = att.filename[:-4]
    print("Adding user: ", userid, username)
    x = threading.Thread(target=thread_function,\
     args=(username,userid), daemon=True)
    x.start()


  if params[0] == '!add':
    user = params[1]
    if user in users.keys():
      await message.channel.send("User already added!")
    else:
      msg = "Hey " + user + " please go the the fowlloing notebook:" +  \
      "[ https://colab.research.google.com/drive/1aR8PU0Avbl5JXrtbS4MiK-_Chq3PrUXs?usp=sharing ]"\
      + ", clone the notebook in your account and run it with your"+\
      "CSES username and password and attach the .csv" +\
      " with the a comment:\n !file userID. Your userID will be shown in" + \
      "the output when you run the code."
      e = discord.Embed(
            title="",
            description=msg,
            color=0xFF5733)
      await message.channel.send(embed=e)
  

  if params[0] == '!topics':
    await message.channel.send(list(topics.keys()))
  
  if params[0] == '!stats':
    pr = ' '.join(params[1:])

    if pr == 'all':
      stats = {}
      for user in users.keys():
        df = pd.read_csv('users/'+user+'.csv')
        cnt = df.shape[0] - df.dropna().shape[0]
        stats[user] = len(prob_names) - cnt
      msg = "Name: Number of problems solved \n"
      for w in sorted(stats, key=stats.get, reverse=True):
        msg += w + ": " +  str(stats[w]) + "\n"
      #msg = pprint.pformat(msg)
      e = discord.Embed(
              title="",
              description=msg,
              color=0xFF5733)
      await message.channel.send(embed=e)

    elif pr in topics.keys():
      stats = {}
      st = topics[pr][0]
      ed = topics[pr][1]+1
      for user in users:
        df = pd.read_csv('users/'+user+'.csv')
        dfc = df[st:ed]
        cnt = dfc.shape[0] - dfc.dropna().shape[0]
        stats[user] = ed-st - cnt

      msg = "Name: Number of problems solved \n"
      for w in sorted(stats, key=stats.get, reverse=True):
        msg += w + ": " +  str(stats[w]) + "\n"

      #msg = pprint.pformat(msg)
      e = discord.Embed(
            title="",
            description=msg,
            color=0xFF5733)
      await message.channel.send(embed=e)
    
    elif pr in prob_names:
      idx = prob_names.index(pr)
      stats = {}
      for user in users:
        df = pd.read_csv('users/'+user+'.csv')
        sol_time = df.iloc[[idx]]['code-time'].values[0]
        sol_time = 'N/A' if str(sol_time) == 'nan' else str(sol_time) + " s"
        stats[user] = str(sol_time)

      msg = "Name: Solution time\n"
      for w in users:
        msg += w + ": " +  stats[w] + "\n"

      #msg = pprint.pformat(msg)
      e = discord.Embed(
            title="",
            description=msg,
            color=0xFF5733)
      await message.channel.send(embed=e)
    
    else:
      await message.channel.send("No such problem!")


  if params[0] == '!sol':
    user = params[1]
    pr_name = ' '.join(params[2:])

    if user not in users.keys():
      await message.channel.send('User not added')

    elif pr_name not in prob_names:
      await message.channel.send('Please enter a valid problem name')
    
    else:
      pr_id = prob_names.index(pr_name)
      df = pd.read_csv('users/'+user+'.csv')
      subm_id = df.iloc[[pr_id]]['submission-id'].values[0]

      if str(subm_id) == 'nan':
        await message.channel.send("User has not solved the problem!")
      else:
        url = 'https://cses.fi/problemset/hack/1068/entry/1942673/'
        response = requests.get(url, headers=headers, cookies=cookies)
        print(response)
        soup = BeautifulSoup(response.text, 'html.parser')

        code = soup.find_all('script')[2].next_element.next_element
        
        text_file = open("solution.cpp", "wt")
        n = text_file.write(code)
        text_file.close()
        await message.channel.send(file=discord.File('solution.cpp'))


  if params[0] == '!users':
    await message.channel.send(list(users.keys()))


  


keep_alive()
client.run(os.getenv('TOKEN'))


