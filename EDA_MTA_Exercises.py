
# coding: utf-8

# ### Exploratory Data Analysis with Python
# 
# We will explore the NYC MTA turnstile data set. These data files are from the New York Subway. It tracks the hourly entries and exits to turnstiles (UNIT) by day in the subway system.
# 
# Here is an [example of what you could do with the data](https://jameskao.me/analyzing-the-nyc-subway-dataset/). James Kao investigates how subway ridership is affected by incidence of rain.

# ## Exercise 1
# 
# - Download at least 2 weeks worth of [MTA turnstile data](http://web.mta.info/developers/turnstile.html) (You can do this manually or via Python)
# - Open up a file, use csv reader to read it, make a python dict where there is a key for each (C/A, UNIT, SCP, STATION). These are the first four columns. The value for this key should be a list of lists. Each list in the list is the rest of the columns in a row. For example, one key-value pair should look like
# 
# 
#         {    ('A002','R051','02-00-00','LEXINGTON AVE'):    
#              [
#                ['NQR456', 'BMT', '01/03/2015', '03:00:00', 'REGULAR', '0004945474', '0001675324'],          
#                  ['NQR456', 'BMT', '01/03/2015', '07:00:00', 'REGULAR', '0004945478', '0001675333'],  
#                 ['NQR456', 'BMT', '01/03/2015', '11:00:00', 'REGULAR', '0004945515', '0001675364'],
#               ...   
#          ] 
#         }
# 
# *Store all the weeks in a data structure of your choosing*

# In[1]:

import wget

url_template = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_180609.txt'


# In[2]:

import csv, glob
from collections import defaultdict

def read_csv(file):
    turnstile_reading = defaultdict(list)
    
    with open(file, 'r') as csv_file:
        mta_reader = csv.reader(csv_file)
        
        for i, row in enumerate(mta_reader):
            if i == 0:
                continue
            
            turnstile_info = tuple(row[:4])
            count_reading = row[4:]
            turnstile_reading[turnstile_info].append(count_reading)
            
        return turnstile_reading


# In[3]:

weekly_data_dicts = [read_csv(csvfile) for csvfile in glob.glob('turnstile_*.txt')]


# In[5]:

sample_dict = list(weekly_data_dicts[0].items())[:1]
print(sample_dict)


# In[6]:

from pprint import pprint
pprint(sample_dict)


# In[ ]:




# In[ ]:




# ## Exercise 2
# - Let's turn this into a time series.
# 
#  For each key (basically the control area, unit, device address and station of a specific turnstile), have a list again, but let the list be comprised of just the point in time and the cumulative count of entries.
# 
# This basically means keeping only the date, time, and entries fields in each list. You can convert the date and time into datetime objects -- That is a python class that represents a point in time. You can combine the date and time fields into a string and use the [dateutil](https://dateutil.readthedocs.io/en/stable/) module to convert it into a datetime object.
# 
# Your new dict should look something like
#  
#     {    ('A002','R051','02-00-00','LEXINGTON AVE'):    
#              [
#                 [datetime.datetime(2013, 3, 2, 3, 0), 3788],
#                 [datetime.datetime(2013, 3, 2, 7, 0), 2585],
#                 [datetime.datetime(2013, 3, 2, 12, 0), 10653],
#                 [datetime.datetime(2013, 3, 2, 17, 0), 11016],
#                 [datetime.datetime(2013, 3, 2, 23, 0), 10666],
#                 [datetime.datetime(2013, 3, 3, 3, 0), 10814],
#                 [datetime.datetime(2013, 3, 3, 7, 0), 10229],
#                 ...
#               ],
#      ....
#      }
# 
# 

# In[7]:

from datetime import datetime
from dateutil.parser import parse

def convert_to_time_series(week_data_dict):
    time_series = defaultdict(list)
    
    for i, (turnstile, row_data) in enumerate(week_data_dict.items()):
        if i % 100 == 0:
            print('Processing turnstile ' , turnstile)
            
        for lines, division, datestr, timestr, event, cum_entries, cum_exits in row_data:
            timestamp = parse('%sT%s' %(datestr, timestr))
            time_series[turnstile].append([timestamp, int(cum_entries)])
            
        return time_series


# In[8]:

from datetime import datetime
from dateutil.parser import parse

def convert_week_data_to_time_series(week_data_dict):
    turnstile_to_time_series = defaultdict(list)
    for i, (turnstile, row_data) in enumerate(week_data_dict.items()):
        if i % 200 == 0:
            print('Processing turnstile', turnstile)
        for lines, division, datestr, timestr, event, cum_entries, cum_exits in row_data:
            timestamp = parse('%sT%s' % (datestr, timestr))
            turnstile_to_time_series[turnstile].append([timestamp, int(cum_entries)])
            
    return turnstile_to_time_series


# In[9]:

weekly_time_series = list(map(convert_to_time_series, weekly_data_dicts))


# ## Exercise 3
# - These counts are cumulative every n hours. We want total daily entries. 
# 
# Now make it that we again have the same keys, but now we have a single value for a single day, which is not cumulative counts but the total number of passengers that entered through this turnstile on this day.
# 

# In[10]:

def combine_weeks(weekly_time_series):
    combined = defaultdict(list)
    
    for week in weekly_time_series:
        for turnstile, time_series in week.items():
            combined[turnstile] += time_series
            
    return combined


# In[11]:

combined_time_series = combine_weeks(weekly_time_series)


# In[12]:

list(combined_time_series.items())[:5]


# In[20]:

def convert_to_daily_time_series(combined_time_series):
    turnstile_daily_time_series = {}
    
    for i, (turnstile, time_series) in enumerate(combined_time_series.items()):
        print('Processing turnstile', turnstile)
        turnstile_daily_time_series[turnstile] = daily_calculation(time_series)
        
    return turnstile_daily_time_series


# In[26]:

from itertools import groupby

def count_within_normal_bounds(count):
    if count is None:
        return True
    else: 
        return 10000 > count >= 0

def daily_calculation(time_series):
    daily_time_series = []
    
    def day_of_timestamp(entry):
        timestamp, tot_entries = entry
        return timestamp.date()
    
    count_on_previous_day = None
    for day, entries_on_this_day in groupby(time_series, key=day_of_timestamp):
        cum_entry_count_on_day = max([count for time, count in entries_on_this_day])

        if count_on_previous_day is None:
            daily_entries = None
        else: daily_entries = cum_entry_count_on_day - count_on_previous_day
            
        count_on_previous_day = cum_entry_count_on_day
        
        if count_within_normal_bounds(daily_entries):
            daily_time_series.append((day, daily_entries))
        else: 
            print('Warning: Abnormal entry count found on day %s: %s' % (day, daily_entries))
            daily_time_series.append((day, None))
            
    return daily_time_series
        
    daily_time_series.append((day, daily_entries))
    


# In[27]:

daily_time_series = convert_to_daily_time_series(combined_time_series)


# In[32]:

pprint(daily_time_series[('A002', 'R051', '02-00-00', '59 ST')])


# ## Exercise 4
# - We will plot the daily time series for a turnstile.
# 
# In ipython notebook, add this to the beginning of your next cell:    
# 
#     %matplotlib inline
# 
# This will make your matplotlib graphs integrate nicely with the notebook.
# To plot the time series, import matplotlib with 
# 
#     import matplotlib.pyplot as plt
# 
# Take the list of [(date1, count1), (date2, count2), ...], for the turnstile and turn it into two lists:
# dates and counts. This should plot it:
# 
#     plt.figure(figsize=(10,3))
#     plt.plot(dates,counts)
# 

# In[34]:

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt

time_series = daily_time_series[('A002', 'R051', '02-00-00', '59 ST')]
days,counts = zip(*time_series)
plt.figure(figsize=(15,5))
plt.plot(days,counts)
plt.show()


# ## Exercise 5
# - So far we've been operating on a single turnstile level, let's combine turnstiles in the same ControlArea/Unit/Station combo. There are some ControlArea/Unit/Station groups that have a single turnstile, but most have multiple turnstilea-- same value for the C/A, UNIT and STATION columns, different values for the SCP column.
# 
# We want to combine the numbers together -- for each ControlArea/UNIT/STATION combo, for each day, add the counts from each turnstile belonging to that combo.
# 

# In[36]:

from collections import Counter

def booth_of_item(item):
    turnstile, time_series = item
    control_area, unit, device_id, station = turnstile
    return (control_area, unit, station)

def reduce_to_booths(daily_time_series):
    turnstile_time_series_items = sorted(daily_time_series.items())
    booth_to_time_series = {}
    
    for booth, item_list_of_booth in groupby(turnstile_time_series_items, key=booth_of_item):
        daily_counter = Counter()
        
    for turnstile, time_series in item_list_of_booth:
        for day, count in time_series:
            if count is not None:
                daily_counter[day] += count
                
        booth_to_time_series[booth] = sorted(daily_counter.items())
        
    return booth_to_time_series


# In[39]:

booth_series = reduce_to_booths(daily_time_series)
pprint(booth_series[('A002', 'R051', '59 ST')])


# ## Exercise 6
# - Similarly, combine everything in each station, and come up with a time series of `[(date1, count1),(date2,count2),...]` type of time series for each STATION, by adding up all the turnstiles in a station.

# In[47]:

def station_of_item(item):
    booth, time_series = item
    control_area, unit, station = booth
    return station
    
def reduce_to_station(booth_series):
    booth_time_series_items = sorted(booth_series.items())
    station_to_time_series = {}
    
    for station, item_list_of_station in groupby(booth_time_series_items, key=station_of_item):
        daily_counter = Counter()
        
        for turnstile, time_series in item_list_of_station:
            for day, count in time_series:
                daily_counter[day] += count
                
        station_to_time_series[station] = sorted(daily_counter.items())
        
    return station_to_time_series


# In[48]:

station_series = reduce_to_station(booth_series)
pprint(station_series[('59 ST')])


# ## Exercise 7
# - Plot the time series for a station

# In[49]:

def plot_station(station_name, station_series):
    time_series - station_series[station_name]
    days, counts = zip(*time_series)
    plt.figure(figsize=(15,5))
    plt.plot(days, counts)
    plt.xlabel('Date')
    plt.ylabel('Number of turnstile entries')
    plt.title('Daily entries for station %s' % station_name)


# In[51]:

plot_station('59 ST', station_series)


# ## Exercise 8
# - Make one list of counts for **one** week for one station. Monday's count, Tuesday's count, etc. so it's a list of 7 counts.
# Make the same list for another week, and another week, and another week.
# `plt.plot(week_count_list)` for every `week_count_list` you created this way. You should get a rainbow plot of weekly commute numbers on top of each other.
# 
# 

# In[53]:

import numpy as np

def separate_weeks(time_series):
    time_series_for_each_week = []
    week = []
    
    for i, (day, count) in enumerate(time_series):
        week.append[(day,count)]
        
        if i % 7 == 6:
            time_series_for_each_week.append(week)
            return time_series_for_each_week

def rainbow_plot(station_name, station_series):
    time_series = station_series(station_name)
    time_series_for_each_week = separate_weeks(time_series)
    
    plt.figure(figsize=(15,5))
    for week, in time_series_for_each_week:
        days, counts = zip(*week)
        days = range(len(counts))
        plt.plot(days, counts)
        
        plt.xlabel('Day of Week')
        plt.ylable('Number of Turnstile Entries')
        plt.xticks(np.arrange(7), ['St', 'Sn', 'Mo', 'Tu', 'We', 'Th', 'Fr'])
        plt.title('Ridership per day for station %s' % station_name)
    


# In[54]:

rainbow_plot('59 ST', station_series)


# ## Exercise 9
# - Over multiple weeks, sum total ridership for each station and sort them, so you can find out the stations with the highest traffic during the time you investigate

# In[ ]:




# ## Exercise 10
# - Make a single list of these total ridership values and plot it with `plt.hist(total_ridership_counts)` to get an idea about the distribution of total ridership among different stations.   
# This should show you that most stations have a small traffic, and the histogram bins for large traffic volumes have small bars.
# 
# *Additional Hint*:    
# If you want to see which stations take the meat of the traffic, you can sort the total ridership counts and make a `plt.bar` graph. For this, you want to have two lists: the indices of each bar, and the values. The indices can just be `0,1,2,3,...`, so you can do 
# 
#     indices = range(len(total_ridership_values))
#     plt.bar(indices, total_ridership_values)
# 
#     

# In[ ]:



