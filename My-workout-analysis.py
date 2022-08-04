#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import urllib3
from matplotlib import pyplot as plt
import seaborn as sns
import datetime as dt

activities = 'https://www.strava.com/api/v3/athlete/activities'
auth_url = "https://www.strava.com/oauth/token"


# In[2]:


payload = {
    'client_id': "90629",
    'client_secret': 'dac647219a4e276d758fe38ffb52906e4d5144d8', 
    'refresh_token': '04119dc851c6419a8fbc4f0c205f672cbc1a1bc0',
    'grant_type': "refresh_token",
    'f': 'json'}

res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

print(res)


# In[3]:


my_dataset = pd.DataFrame()
empty_page = True
page = 1
while empty_page:
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': page}
    page_dataset = requests.get(activities, headers=header, params=param).json()
    my_dataset = pd.concat([my_dataset,pd.DataFrame(page_dataset)], ignore_index = True)
    empty_page = bool(page_dataset)
    if bool(page_dataset):
        print('\n Página:',page)
    else:
        print("\n Parando")
    page += 1
print("\n {} recordes carregados!".format(len(my_dataset)))


# In[4]:


my_dataset['start_date'] = pd.to_datetime(my_dataset['start_date'],infer_datetime_format = True)
my_dataset


# In[5]:


my_dataset.head(20)


# In[6]:


runs = my_dataset[my_dataset['type'] == 'Run']


# In[7]:


my_dataset.columns


# In[46]:


my_dataset[['average_speed', 'distance',"max_speed", 'moving_time']][my_dataset['type'] == 'Run']


# In[66]:


def plotador(coluna):
    r = runs[["start_date", coluna]].groupby(runs['start_date'].dt.to_period('M')).mean()
    fig, ax = plt.subplots(figsize=(20, 10), facecolor='white')
    ax.set_facecolor("xkcd:white")
    #ax.set_xticklabels(ax.get_xticklabels(),rotation=60)
    ax.tick_params(axis='x', labelsize=12, labelrotation = 45)
    ax = sns.barplot(data = r, x = r.index , y = coluna)
    plt.ylabel("MÉDIA DE " + str(coluna).upper())
    
    return ax


# In[67]:


plotador('distance')


# In[10]:


#my_dataset = my_dataset.groupby(my_dataset['start_date'].dt.to_period('M')).sum('distance')


    

ax = sns.barplot(x = runs['start_date'].dt.to_period('M'), y = my_dataset['distance'])
ax = ax.set_xticklabels(ax.get_xticklabels(),rotation=60)


# In[ ]:




