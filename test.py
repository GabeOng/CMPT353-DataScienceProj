import pandas as pd
import numpy as np

df=pd.read_csv('stop_times.txt')
df1=pd.read_csv('trips.txt')
startDay=False
day=0
df=df[['trip_id','arrival_time', 'stop_id']]
df1=df1[['trip_id', 'trip_headsign']]

df= df.join(df1.set_index('trip_id'), on='trip_id')
print(df)

sorted=df.groupby('trip_headsign').apply(lambda x: x.sort_values(['trip_id', 'arrival_time'], ascending=True)).reset_index(drop=True)
print(sorted)

sorted.to_csv('sorted.csv')

#part that doesnt work
def convert_to_timedelta(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)

# Function to label each day within each group
#arrival time 
def label_days(group):
    group['arrival_time'] = pd.to_timedelta(group['arrival_time'])
    group['time_diff'] = group['arrival_time'].diff()
    
    # Threshold for considering a time difference as indicating a new day
    time_threshold = pd.Timedelta(hours=20)
    
    # Identifying new day indices based on time difference and trip_id change
    new_day_indices = group[(group['trip_id'].diff() > 0) & 
                            ((group['time_diff'] < -time_threshold) | 
                             (group['time_diff'].isnull()))].index
    
    # Labeling days
    group['day_label'] = (group.index.isin(new_day_indices)).cumsum()
    return group

# Group by 'trip_headsign' and apply the operation within each group
df = sorted.groupby('trip_headsign').apply(label_days).reset_index(drop=True)

df.drop(columns=['Unnamed: 0'], inplace=True)
df['day_label']=df['day_label']%7
print(df)