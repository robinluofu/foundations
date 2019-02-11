
# coding: utf-8

# In[4]:

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
plt.style.use('ggplot')
pd.options.display.float_format = "{:.2f}".format


# In[5]:

data = pd.read_csv('survey_public.csv')


# In[6]:

data.head()


# In[7]:

ds = "Data scientist or machine learning specialist"
data['DevType'].value_counts()


# In[5]:

type = pd.DataFrame(data.groupby('DevType').size().sort_values(ascending=False).rename('counts').reset_index())
type


# In[ ]:




# In[8]:




# In[8]:

data.loc[(data['DevType'] == 'Data scientist or machine learning specialist'), 'type'] = 'Data Science'
data.loc[(data['DevType'] =='Data or business analyst'), 'type'] = 'Data analyst'
data.type.value_counts()


# In[ ]:




# In[24]:

job_type = data['DevType']


# In[28]:

data.columns


# In[ ]:




# In[ ]:




# In[11]:

df = data[["DevType", "ConvertedSalary"]]
df.head()


# In[13]:

list(data['DevType'])


# In[ ]:




# In[37]:

list(df)


# In[78]:

data['ConvertedSalary'].value_counts()


# In[25]:

def salary(value):
    if value == range (0, 50000):
        return "< $50000"
    elif value == range(50001, 75000):
        return "$50,000 - $75,000"


# In[26]:

salary(45000)


# In[ ]:



