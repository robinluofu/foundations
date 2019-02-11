
# coding: utf-8

# In[1]:

import requests


# In[2]:

page = requests.get("https://www.childrenshospitals.org/Directories/Hospital-Directory")


# In[3]:

page


# In[4]:

page.content


# In[5]:

from bs4 import BeautifulSoup


# In[6]:

soup = BeautifulSoup(page.content, 'html.parser')


# In[7]:

print(soup.prettify())


# In[8]:

list(soup.children)


# In[10]:

center = soup.find_all("div", {"class": "contact-info"})


# In[11]:

len(center)


# In[12]:

center[0]


# In[13]:

center[0].find_all("span", {"class":"title"})[0]


# In[14]:

l = []
for item in center:
    d = {}
    d["Hospital"] = item.find_all("span", {"class": "title"})[0].text
    d["Address"] = item.find_all("span", {"class": "contact-address"})[0].text.replace("United States of America", "")
    print(" ")
    l.append(d)


# In[93]:

len(l)


# In[94]:

import pandas as pd


# In[95]:

df = pd.DataFrame(l)


# In[96]:

df


# In[97]:

df.to_csv("Output.csv")


# In[98]:

from sqlalchemy import create_engine


# In[99]:

engine = create_engine('sqlite://', echo=False)


# In[100]:

df.to_sql('users', con=engine)


# In[101]:

engine.execute('SELECT * FROM users').fetchall()


# In[17]:

import sqlite3


# In[18]:

conn = sqlite3.connect('users')
c = conn.cursor()

results = c.execute("SELECT * from users")
for row in results:
    print(row)
conn.close()
# In[108]:




# In[ ]:



