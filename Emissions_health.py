
# coding: utf-8

# In[2]:

import pandas as pd
from pandas import read_csv


# In[3]:

data = pd.read_csv('CarbonDioxide.csv', encoding = 'cp1252')
data


# In[4]:

data.columns


# In[5]:

data.columns = ['Region', 'Country', 'Year', 'Series', 'Value','Footnotes', 'Source']


# In[6]:

data


# In[10]:

data['Year'].unique()


# In[42]:

data['Value'] = data['Value'].fillna((data['Value'].mean())) 


# In[11]:

emis = data[['Country', 'Year', 'Value']].where(data['Year']== '2014').sort_values(by='Country')
emis.head()


# In[40]:

data['Value'] = data['Value'].fillna((data['Value'].mean()))


# In[38]:

import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
sns.set(style="whitegrid") 

f, ax = plt.subplots(figsize = (6,15))

sns.set_color_codes("pastel")
sns.barplot(x="Country", y = "Value", data=emis, label = "Country", color="b")


# In[19]:

emissions


# In[ ]:




# In[13]:

Health = pd.read_csv('SOWCtable.csv', encoding = 'cp1252', header=None)
Health = Health[3:]


# In[14]:

data = Health.rename(columns=Health.iloc[0])


# In[15]:

new_df = data.iloc[1:]
new_df.columns


# In[16]:

new_df.columns = ['nan', 
                  'Countries', 
                  'Under 5 mortality rank', 
                  'Under 5 mortality rate M', 
                  'Under 5 mortality rate F'
                  'Under 5 mortality sex M', 
                  'Under 5 mortality sex F'
                  'Infant mortality rate M', 
                  'Infant mortality rate F',
                  'Neonatal mortality rate', 
                  'Total pop (1000s)', 
                 'Total num of births', 
                  'Annual number of under 5 deaths', 
                  'Life expectancy at birth', 
                  'Adult Literacy rate', 
                  'nan'
                  'primary school enrollment',
                 'nan',
                 'nan',
                 'nan',
                 'nan',
                 'nan',
                 'nan',
                 'nan',
                 'nan',
                 'nan',
                 'nan',]


# In[17]:

new_df


# In[ ]:



