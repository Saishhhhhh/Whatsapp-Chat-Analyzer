import pandas as pd
from urlextract import URLExtract

extract = URLExtract()

# Creating New DataFrame based on Date Range For Processing Further
def date_range_dataframe(df, min_date, max_date):

  new_df = df.query('date >= @min_date and date <= @max_date').reset_index(drop=True)

  return new_df

#Basic Stats 
def basic_stats(df):
  total_messages = df.shape[0]

  media_messages = df[df['messages'] == "<Media omitted>"].shape[0]

  #Deleting the media messages words ("Media ommitted")
  total_words = (df['word_count'].sum()) - media_messages*2

  links = []
  for message in df['messages']:
    links.extend(extract.find_urls(message))

  return total_messages, media_messages, total_words, len(links)

#Monthly Timeline
def monthly_timeline(df):
  timeline = df.groupby(['year', 'month_num', 'month'])['messages'].count().reset_index()
  time = []

  for i in range(timeline.shape[0]):
      time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

  timeline['time'] = time
  return timeline;

#Datewise Timeline
def datewise_timeline(df):
  timeline = df.groupby('date')['messages'].count().reset_index()

  return timeline

#Weekly Timeline

def weekly_timeline(df):
  timeline = df.groupby(['day_name'])['messages'].count().reset_index()

  day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

  # Convert 'day_name' to a categorical type with that order
  timeline['day_name'] = pd.Categorical(timeline['day_name'], categories=day_order, ordered=True)

  # Sort by the categorical order
  timeline = timeline.sort_values('day_name').reset_index(drop=True)

  return timeline

#Month Wise Timeline
def monthwise_timeline(df):
  timeline = df.groupby(['month'])['messages'].count().reset_index()

  month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

  # Convert 'month' to a categorical type with that order
  timeline['month'] = pd.Categorical(timeline['month'], categories=month_order, ordered=True)

  # Sort by the categorical order
  timeline = timeline.sort_values('month').reset_index(drop=True)

  return timeline

# Weekly Activity
def weekly_heatmap(df):
  user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

  time_period_order = [
    '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10',
    '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
    '18-19', '19-20', '20-21', '21-22', '22-23', '23-00'
  ]

  day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

  user_heatmap = user_heatmap.reindex(day_order)

  existing_columns = [col for col in time_period_order if col in user_heatmap.columns]
  user_heatmap = user_heatmap[existing_columns]

  return user_heatmap