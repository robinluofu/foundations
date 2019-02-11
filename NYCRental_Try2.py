
# coding: utf-8

# In[8]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math
get_ipython().magic('matplotlib inline')
import subprocess
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import seaborn as sns


# In[5]:

geolocator = Nominatim()

df_entire = pd.read_json('train.json')
df_entire['created'] = pd.to_datetime(df_entire['created'])
df_entire['month'] = df_entire['created'].dt.month
df_entire['date'] = df_entire['created'].dt.day
df_entire['price_scaled_bath'] = df_entire['price']/df_entire['bathrooms']
df_shuffled = df_entire.sample(frac=1)
df_train = df_shuffled[:int(0.6*len(df_shuffled))]
df_test = df_shuffled[int(0.6*len(df_shuffled)):int(len(df_shuffled))]
print(df_train.shape)
print(df_test.shape)
df_entire['date'].value_counts()
print(df_entire.shape)
percent_low = 100*df_train['interest_level'].value_counts()['low']/df_train['interest_level'].value_counts().sum()
percent_medium = 100*df_train['interest_level'].value_counts()['medium']/df_train['interest_level'].value_counts().sum()
percent_high = 100*df_train['interest_level'].value_counts()['high']/df_train['interest_level'].value_counts().sum()
print('low-->', percent_low, '%')
print('medium-->', percent_medium, '%')
print('high-->', percent_high, '%')
df_entire.dtypes


# In[15]:

sns.set_style('white')
sns.set(style="ticks")
df_entire_ss=df_entire[(df_entire['price']>0)&(df_entire['price']<20000)&(df_entire['latitude']<40.9)&
(df_entire['latitude']>40.55)&(df_entire['longitude']>-74.05)]
g=sns.pairplot(df_entire_ss, palette="muted", markers=['o', 'x', '+'],vars=['price', 'latitude', 'longitude'],
              size=4,hue='interest_level', hue_order=['low', 'medium', 'high'])
g=g.map_offdiag(plt.scatter, s=20)
sns.despine()
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Pair plot for rental listing dataset', fontsize=34, color='k',alpha=1)
g.savefig('pairplot_price_latitude_longitude.png')


# In[17]:

sns.set_style('white')
df_entire2=df_entire[df_entire['bathrooms']>0]
ax=sns.boxplot(y=df_entire['price'], x=df_entire['interest_level'], order=['low', 'medium', 'high'], showfliers=False)
fig=ax.get_figure()
fig.suptitle('Distribution of Rental Prices for different interest level categories')
fig.savefig('price_boxplot.png')
df_entire[df_entire['price']>7000]['interest_level'].value_counts().sum()


# In[21]:

bedbathmat=pd.crosstab(df_train.bedrooms, df_train.bathrooms, margins = True)
bedbathmat_low=pd.crosstab(df_train[df_train['interest_level']=='low'].bedrooms, 
                           df_train[df_train['interest_level']=='low'].bathrooms, margins=True)
bedbathmat_medium=pd.crosstab(df_train[df_train['interest_level']=='medium'].bedrooms, 
                           df_train[df_train['interest_level']=='medium'].bathrooms, margins=True)
bedbathmat_high=pd.crosstab(df_train[df_train['interest_level']=='high'].bedrooms, 
                           df_train[df_train['interest_level']=='high'].bathrooms, margins=True)


# In[19]:

pd.crosstab(df_entire.bathrooms, df_entire.interest_level, margins=True)


# In[22]:

bedbathmat_low


# In[23]:

bedbathmat_medium


# In[24]:

bedbathmat_high


# In[25]:

baths = pd.crosstab(df_entire.bathrooms, df_entire.interest_level, margins=True)
baths['low interest (%)']=100*baths['low']/baths['All']
baths['medium interest (%)']=100*baths['medium']/baths['All']
baths['high interest (%)']=100*baths['high']/baths['All']
baths


# In[28]:

df_entire_1bath=df_entire[df_entire['bathrooms']==1]
beds1bth=pd.crosstab(df_entire_1bath.bedrooms, df_entire.interest_level, margins=True)
beds1bth['low interest (%)']=100*beds1bth['low']/beds1bth['All']
beds1bth['medium interest (%)']=100*beds1bth['medium']/beds1bth['All']
beds1bth['high interest (%)']=100*beds1bth['high']/beds1bth['All']
beds1bth


# In[29]:

df_entire_2bath=df_entire[df_entire['bathrooms']==2]
beds2bth=pd.crosstab(df_entire_2bath.bedrooms, df_entire.interest_level, margins=True)
beds2bth['low interest (%)']=100*beds2bth['low']/beds2bth['All']
beds2bth['medium interest (%)']=100*beds2bth['medium']/beds2bth['All']
beds2bth['high interest (%)']=100*beds2bth['high']/beds2bth['All']
beds2bth


# In[31]:

def interest_predict_bb(train, numbed, numbath, price, level, iprice):
    count_total=len(train[(train['bathrooms']==numbath)&(train['bedrooms']==numbed)])
    count_low=len(train[(train['bathrooms']==numbath)&(train['bedrooms']==numbed)&(train['interest_level']=='low')])
    count_medium=len(train[(train['bathrooms']==numbath)&(train['bedrooms']==numbed)&(train['interest_level']=='medium')])
    count_high=len(train[(train['bathrooms']==numbath)&(train['bedrooms']==numbed)&(train['interest_level']=='high')])
    if count_total == 0:
        return 0.33
    if count_total >= 5:
        price_low_50=train[(train['bathrooms']==numbath)&(train['bedrooms']==numbed)&(train['interest_level']=='low')]['price'].quantile(0.5)
        price_low_25=train[(train['bathrooms']==numbath)&(train['bedrooms']==numbed)&(train['interest_level']=='low')]['price'].quantile(0.25)
        price_low_75=train[(train['bathrooms']==numbath)&(train['bedrooms']==numbed)&(train['interest_level']=='low')]['price'].quantile(0.75)
        if price == price_low_50:
            lowp=1
        elif price>price_low_50:
            lowp=(count_low/count_total)*(price_low_75-price_low_50)/(price-price_low_50)
        else:
            lowp=(count_low/count_total)*(price_low_50-price_low_25)/(-price+price_low_50)
    else:
        lowp=count_low/count_total
    if count_medium>=5:
        price_medium_50=train[(train['bathroom']==numbath) & (train['bedrooms']==numbed)&(train['interest_level']=='medium')]['price'].quantile(0.5)
        price_medium_25=train[(train['bathroom']==numbath) & (train['bedrooms']==numbed)&(train['interest_level']=='medium')]['price'].quantile(0.25)
        price_medium_75=train[(train['bathroom']==numbath) & (train['bedrooms']==numbed)&(train['interest_level']=='medium')]['price'].quantile(0.75)
        if price==price_high_50:
            highp=1
        elif price>price_medium_50:
            highp=(count_high/count_total)*(price_high_75-price_high_50)/(price-price_high_50)
        else:
            highp=(count_high/count_total)*(price_high_50-price_high_25)/(-price+price_high_50)
    else:
        highp=count_high/count_total
    if iprice==1:
        if level=='low':
            return lowp/(lowp+mediump+highp)
        if level=='medium':
            return mediump/(lowp+mediump+highp)
        if level == 'high':
            return highp/(lowp+mediump+highp)
    else:
        if level == 'low':
            return count_low/count_total
        if level == 'medium':
            return count_medium/count_total
        if level == 'high':
            return count_high/count_total


# In[32]:

def interest_predict_bbpll_lp(train, nbed, nbath, price, lat, long):
    if (nbath!=1) & (nbath!=2):
        lowp=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='low')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        mediump=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='medium')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        highp=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='high')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        return lowp
    else:
        nlist=train[(train['bedrooms']==nbed)&(train['bathrooms']==nbath)]['interest_level'].value_counts().sum()
        if nlist==0:
            return 1.0
        else:
            latl=lat-0.1
            lath=lat+0.1
            longl=long-0.05
            longh=long+0.05
            pricel=price-1000
            priceh=price+1000
            train_slice=train[(train['price']>=price1)&(train['price']<=priceh)&(train['latitude']>=latl)&(train['latitude']<=lath)*(train['longitude']>=longl)&(train['longitude']<=longh)]
            nlist=train_slice['interest_level'].value_counts().sum()
            if nlist==0:
                return 1.0
            else:
                lowp=len(train_slice[train_slice['interest_level']=='low'])/nlist
                mediump=len(train_slice[train_slice['interest_level']=='medium'])/nlist
                highp=len(train_slice[train_slice['interest_level']=='high'])/nlist
                return lowp


# In[36]:

def interest_predict_bbpll_mp(train, nbed, nbath, price, lat, long):
    if (nbath!=1) & (nbath!=2):
        lowp=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='low')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        mediump=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='medium')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        highp=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='high')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        return mediump
    else:
        nlist=train[(train['bedrooms']==nbed)&(train['bathrooms']==nbath)]['interest_level'].value_counts().sum()
        if nlist==0:
            return 0.0
        else:
            latl=lat-0.1
            lath=lat+0.1
            longl=long-0.05
            longh=long+0.05
            pricel=price-1000
            priceh=price+1000
            train_slice=train[(train['price']>=price1)&(train['price']<=priceh)&(train['latitude']>=latl)&(train['latitude']<=lath)*(train['longitude']>=longl)&(train['longitude']<=longh)]
            nlist=train_slice['interest_level'].value_counts().sum()
            if nlist==0:
                return 0.0
            else:
                lowp=len(train_slice[train_slice['interest_level']=='low'])/nlist
                mediump=len(train_slice[train_slice['interest_level']=='medium'])/nlist
                highp=len(train_slice[train_slice['interest_level']=='high'])/nlist
                return mediump


# In[37]:

def interest_predict_bbpll_hp(train, nbed, nbath, price, lat, long):
    if (nbath!=1) & (nbath!=2):
        lowp=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='low')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        mediump=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='medium')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        highp=len(train[(train['bathrooms']!=1)&(train['bathrooms']!=2)&(train['interest_level']=='high')])/train[(train['bathrooms']!=1)&
                                                                    (train['bathrooms']!=2)]['interest_level'].value_counts().sum*()
        return highp
    else:
        nlist=train[(train['bedrooms']==nbed)&(train['bathrooms']==nbath)]['interest_level'].value_counts().sum()
        if nlist==0:
            return 0.0
        else:
            latl=lat-0.1
            lath=lat+0.1
            longl=long-0.05
            longh=long+0.05
            pricel=price-1000
            priceh=price+1000
            train_slice=train[(train['price']>=price1)&(train['price']<=priceh)&(train['latitude']>=latl)&(train['latitude']<=lath)*(train['longitude']>=longl)&(train['longitude']<=longh)]
            nlist=train_slice['interest_level'].value_counts().sum()
            if nlist==0:
                return 0.0
            else:
                lowp=len(train_slice[train_slice['interest_level']=='low'])/nlist
                mediump=len(train_slice[train_slice['interest_level']=='medium'])/nlist
                highp=len(train_slice[train_slice['interest_level']=='high'])/nlist
                return highp


# In[39]:

df_test_s=df_test.sample(frac=1.0)
df_test_s['prob_low_1']=df_test_s.apply(lambda x: interest_predict_bb(df_train,x['bedrooms'],x['bathrooms'],x['price'],'low',0),axis=1)
df_test_s['prob_medium_1']=df_test_s.apply(lambda x: interest_predict_bb(df_train,x['bedrooms'],x['bathrooms'],x['price'],'medium',0),axis=1)
df_test_s['prob_high_1']=df_test_s.apply(lambda x: interest_predict_bb(df_train,x['bedrooms'],x['bathrooms'],x['price'],'high',0),axis=1)


# In[40]:

df_test_s['prob_low']=df_test_s.apply(lambda x: interest_predict_bbpll_lp(df_train,x['bedrooms'],x['bathrooms'],x['price'],x['latitude'],x['longitude']),axis=1)
df_test_s['prob_medium']=df_test_s.apply(lambda x: interest_predict_bbpll_mp(df_train,x['bedrooms'],x['bathrooms'],x['price'],x['latitude'],x['longitude']),axis=1)
df_test_s['prob_high']=df_test_s.apply(lambda x: interest_predict_bbpll_hp(df_train,x['bedrooms'],x['bathrooms'],x['price'],x['latitude'],x['longitude']),axis=1)


# In[ ]:



