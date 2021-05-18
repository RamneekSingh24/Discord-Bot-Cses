import requests
import os
import json
from bs4 import BeautifulSoup
import pandas as pd

headers = (eval(os.getenv('headers').strip()))
cookies = (eval(os.getenv('cookies').strip()))
response = requests.get('https://cses.fi/problemset/', headers=headers, cookies=cookies)

soup = BeautifulSoup(response.text, 'html.parser')


#cats = soup.find_all('h2')

content = soup.find_all("ul", class_="task-list")
content = content[1:]
prob_cats = []
probs_info = []

for cat in content:
  prob_cats.append(str(cat.previous_element))
  lst = []
  probs = cat.find_all('li')
  #print(len(probs))
  for p in probs:
    p = p.find('a')
    #print(p)
    lst.append([p.text, p['href']])
  probs_info.append(lst)

#print(probs_info)
for i in range(len(prob_cats)):
  df = pd.DataFrame(probs_info[i])
  df.columns = ['name','link']
  #df = df[['name','link']]
  print(df.head(3))
  path = 'problems/' + prob_cats[i]
  df.to_csv(path,index=False)


all_probs = sum(probs_info,[])
df = pd.DataFrame(all_probs)
df.columns = ['name','link']
df.to_csv('problems/all',index=False)
