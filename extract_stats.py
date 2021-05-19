#!pip install mechanicalsoup
# USER_NAME = 'chill_coder'
# PASSWORD = 'RamneekS24IITDPepsiMan"
# https://www.youtube.com/watch?v=dQw4w9WgXcQ

USER_NAME = 'username'
PASSWORD = 'password'

import mechanicalsoup
import json
import pandas as pd

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
    user_agent='MyBot/0.1: mysite.example.com/bot_info',
)

browser.open("https://cses.fi/login")
browser.select_form('form')
#browser.get_current_form().print_summary()
browser['nick'] = USER_NAME
browser['pass'] = PASSWORD

resp = browser.submit_selected()


browser.open("https://cses.fi/login")
browser.select_form('form')
#browser.get_current_form().print_summary()
browser['nick'] = USER_NAME
browser['pass'] = PASSWORD

resp = browser.submit_selected()
browser.open('https://cses.fi/problemset/list')
page = browser.get_current_page()
acc_no = page.find('a',class_='account')['href']
#print("USER ID:", acc_no)

#data = {'user_no':acc_no}

all_data = []

print(browser.open('https://cses.fi/problemset/list/'))
page = browser.get_current_page()
probs = page.find_all('li')
probs = probs[6:]
#print(probs[0].find('a')['href'])
#/problemset/task/1068
url = 'https://cses.fi/problemset/view/'
stats = [100.00 for i in range(len(probs))]
data = []
for i in range(len(probs)):
  #print(i)
  p_no = probs[i].find('a')['href'][len('/problemset/task/'):]
  browser.open(url + str(p_no) + '/')
  page = browser.get_current_page()
  acs = page.find_all('td',class_='task-score icon full')
  data = ['NaN' for i in range(5)]
  for ac in acs:
    d = ac.parent.find_all('td')
    time = float(d[2].text.split(' ')[0])
    #stats[i] = min(stats[i], time)
    if time < stats[i]:
      stats[i] = time
      data = [d[i].text for i in range(4)]
      data.append(d[-1].find('a')['href'])
  data[2] = stats[i]
  if data[-1] != 'NaN':
    data[-1] = data[-1][len('/problemset/result/'):-1]
  #print(data)
  all_data.append(data)


for i in range(len(stats)):
  all_data[i][2] = 'NaN' if stats[i] > 50.00 else str(stats[i])

df = pd.DataFrame(all_data)
df.columns = ['time', 'lang', 'code-time', 'code-len','submission-id']
df.to_csv(USER_NAME  +'.csv',index=False)
print('YOUR USERID: ',  acc_no[len('/user/'):])
