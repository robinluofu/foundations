
# coding: utf-8

# In[ ]:

import pandas as pd
from pandas import read_csv
crimes = read_csv('Chicago_Crimes_2012_to_2017.csv')


# In[ ]:

print(type(crimes))


# In[20]:

crimes.head()


# In[ ]:

crimes = crimes.iloc[:, 3: ]
crimes.head()


# In[ ]:

crimes.index = pd.to_datetime(crimes.index)


# In[23]:

print(crimes.shape)
print(crimes.head())


# In[ ]:

s = crimes[['Primary Type']]


# In[25]:

s.head()


# In[ ]:

crime_count = pd.DataFrame(s.groupby('Primary Type').size().sort_values(ascending=False).rename('counts').reset_index())


# In[9]:

crime_count.head()


# In[14]:

crime_count.shape


# In[ ]:

import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
sns.set(style="whitegrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(6, 15))


# Plot the total crashes
sns.set_color_codes("pastel")
sns.barplot(x="counts", y="Primary Type", data=crime_count.iloc[:10, :],
            label="Total", color="b")

ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(ylabel="Type",
       xlabel="Crimes")
sns.despine(left=True, bottom=True)

# Add a legend and informative axis label
plt.show()


# In[ ]:

crimes_2012 = crimes.loc['2012']
crimes_2013 = crimes.loc['2013']
crimes_2014 = crimes.loc['2014']
crimes_2015 = crimes.loc['2015']
crimes_2016 = crimes.loc['2016']
crimes_2017 = crimes.loc['2017']

## Yearly crimes
arrest_yearly = crimes[crimes['Arrest'] == True]['Arrest']


# In[ ]:

print(arrest_yearly.head())


# In[ ]:

plt.subplot()
arrest_yearly.resample('A').sum().plot()
plt.title('Yearly arrests')
plt.show()

arrest_yearly.resample('M').sum().plot()
plt.title('Monthly arrests')
plt.show()

arrest_yearly.resample('W').sum().plot()
plt.title('Monthly arrests')
plt.show()


# In[ ]:

y2012 = pd.DataFrame(crimes_2012[crimes_2012['Primary Type'].isin(['THEFT', 'BATTERY', 'CRIMINAL DAMAGE', 'NARCOTICS', 'ASSAULT'])]['Primary Type'])
y2013 = pd.DataFrame(crimes_2013[crimes_2013['Primary Type'].isin(['THEFT', 'BATTERY', 'CRIMINAL DAMAGE', 'NARCOTICS', 'ASSAULT'])]['Primary Type'])
y2014 = pd.DataFrame(crimes_2014[crimes_2014['Primary Type'].isin(['THEFT', 'BATTERY', 'CRIMINAL DAMAGE', 'NARCOTICS', 'ASSAULT'])]['Primary Type'])
y2015 = pd.DataFrame(crimes_2015[crimes_2015['Primary Type'].isin(['THEFT', 'BATTERY', 'CRIMINAL DAMAGE', 'NARCOTICS', 'ASSAULT'])]['Primary Type'])
y2016 = pd.DataFrame(crimes_2016[crimes_2016['Primary Type'].isin(['THEFT', 'BATTERY', 'CRIMINAL DAMAGE', 'NARCOTICS', 'ASSAULT'])]['Primary Type'])


# In[ ]:

grouper = y2012.groupby([pd.TimeGrouper('M'), 'Primary Type'])
grouper13 = y2013.groupby([pd.TimeGrouper('M'), 'Primary Type'])
grouper14 = y2014.groupby([pd.TimeGrouper('M'), 'Primary Type'])
grouper15 = y2015.groupby([pd.TimeGrouper('M'), 'Primary Type'])
grouper16 = y2016.groupby([pd.TimeGrouper('M'), 'Primary Type'])


# In[ ]:




# In[ ]:

data12 = grouper['Primary Type'].count().unstack()
data13 = grouper13['Primary Type'].count().unstack()
data14 = grouper14['Primary Type'].count().unstack()
data15 = grouper15['Primary Type'].count().unstack()
data16 = grouper16['Primary Type'].count().unstack()


# In[ ]:

data12.plot()
plt.title('Top 5 Monthly Crimes in 2012')
plt.show()


# In[ ]:

pd.set_option('precision', 0)
crimes.head()


# In[ ]:

comm = pd.read_csv('Census_Data.csv')


# In[ ]:

comm.head()


# In[ ]:

list(comm)


# In[163]:

comm.columns = ['community_area',
 'COMMUNITY AREA NAME',
 'PERCENT OF HOUSING CROWDED',
 'PERCENT HOUSEHOLDS BELOW POVERTY',
 'PERCENT AGED 16+ UNEMPLOYED',
 'PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA',
 'PERCENT AGED UNDER 18 OR OVER 64',
 'PER CAPITA INCOME ',
 'HARDSHIP INDEX']


# In[ ]:

crimes = pd.DataFrame(crimes)
list(crimes)


# In[ ]:

df = crimes.merge(comm[['community_area', 'COMMUNITY AREA NAME',
 'PERCENT OF HOUSING CROWDED',
 'PERCENT HOUSEHOLDS BELOW POVERTY',
 'PERCENT AGED 16+ UNEMPLOYED',
 'PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA',
 'PERCENT AGED UNDER 18 OR OVER 64',
 'PER CAPITA INCOME ',
 'HARDSHIP INDEX']], on = 'community_area', how='left')
df.head()


# In[ ]:




# In[ ]:

df_new = df[['community_area', 'COMMUNITY AREA NAME',
 'PERCENT OF HOUSING CROWDED', 'Primary Type',
 'PERCENT HOUSEHOLDS BELOW POVERTY',
 'PERCENT AGED 16+ UNEMPLOYED',
 'PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA',
 'PERCENT AGED UNDER 18 OR OVER 64',
 'PER CAPITA INCOME ',
 'HARDSHIP INDEX']]


# In[ ]:

df_new.head()


# In[ ]:

df_new['Primary Type'].unique()


# In[171]:

poverty = df['PERCENT HOUSEHOLDS BELOW POVERTY']
unemployed = df['PERCENT AGED 16+ UNEMPLOYED']
education = df['PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA']
dependent = df['PERCENT AGED UNDER 18 OR OVER 64']
income = df['PER CAPITA INCOME ']
hardship = df['HARDSHIP INDEX']
area = df['COMMUNITY AREA NAME']


# In[ ]:

df.groupby(poverty).count()


# In[ ]:




# In[ ]:

crimes['Primary Type'].unique()


# In[128]:

violent = ['HOMOCIDE', 'BATTERY', 'CRIM SEXUAL ASSAULT', 'ASSAULT', 'ROBBERY']


# In[131]:

def violence(row):
    if row['Primary Type'] in violent:
        value = True
    else:
        value = False
    return value


# In[137]:

df['violent'] = df.apply(lambda x: violence(x), 1)


# In[142]:

arrests_community = df[['Arrest', 'community_area_name', 'violent']]
crimes_community = arrests_community.groupby(arrests_community['community_area_name']).count().reset_index()
crimes_community.head()


# In[146]:

del crimes_community['violent']
crimes_community.columns = ['community_area_name', 'crimes']


# In[148]:

arrests_per = arrests_community.groupby(arrests_community['community_area_name']).sum().reset_index()
arrests_per.columns = ['community_area_name', 'arrests', 'violent_crimes']


# In[149]:

arrest_percent = crimes_community.merge(arrests_per[['arrests', 'violent_crimes']], left_index = True, right_index = True, how= 'left')


# In[150]:

arrest_percent.head()


# In[152]:

list(comm)


# In[ ]:



