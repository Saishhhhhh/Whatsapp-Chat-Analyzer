import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from collections import Counter

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

#Hourly Timeline
def hourly_timeline(df):
  timeline = df.groupby('period')['messages'].count().reset_index()
  time_period_order = [
      '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10',
      '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
      '18-19', '19-20', '20-21', '21-22', '22-23', '23-00'
    ]
  timeline = timeline.set_index('period').reindex(time_period_order).reset_index()
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

# Wordcloud

def create_wordcloud(df):

  wc = WordCloud(width=500, height = 500, min_font_size = 10, background_color = "white")
  df2 = df[df['messages'] != "<Media omitted>"]
  df_wc = wc.generate(df2['messages'].str.cat(sep=" "))
  return df_wc

#Most common emojis
def most_common_emojis_dataframe(df):
  emojis = []
  for message in df['messages']:
      emojis.extend([char for char in message if char in emoji.EMOJI_DATA])

  emoji_df = pd.DataFrame(Counter(emojis).most_common(10), columns=['emoji', 'count'])
  return emoji_df


#Most busy users barplot
def busy_user_bar(df):
  return df.groupby('user')['messages'].count().reset_index()

#Most busy users dataframe
def busy_user_dataframe(df):
  df2 = df.groupby('user')['messages'].count().reset_index()
  total_messages = df2['messages'].sum()
  df2['percentage'] = round((df2['messages']/ total_messages)*100,2)
  df2 = df2.sort_values('percentage', ascending=False)
  df2 = df2.drop(columns='messages', axis=1)
  
  return df2

def chatterbox(df):
  df2 = df.groupby('user')['messages'].count().reset_index()
  df2 = df2.sort_values('messages', ascending=False)

  df2 = df2[df2['user'] != 'Meta AI']

  return df2.loc[df2['messages'].idxmax()]

def keyboard_warrior(df):
  df2 = df.groupby('user')['word_count'].sum().reset_index()
  df2 = df2.sort_values('word_count', ascending=False)

  df2 = df2[df2['user'] != 'Meta AI']

  return df2.loc[df2['word_count'].idxmax()]

def media_Paglu(df):
  df2 = df.query('messages == "<Media omitted>"')
  df2 = df2.groupby('user')['messages'].count().reset_index().sort_values('messages', ascending=False)

  df2 = df2[df2['user'] != 'Meta AI']

  return df2.loc[df2['messages'].idxmax()]

def linkMaster(df):
  extractor = URLExtract()

  # Count number of links for each message
  df['link_count'] = df['messages'].apply(lambda msg: len(extractor.find_urls(msg)))

  # Group by user and sum link counts
  df2 = df.groupby('user', as_index=False)['link_count'].sum()

  df2 = df2[df2['user'] != 'Meta AI']

  # Find the user with the maximum number of links
  return df2.loc[df2['link_count'].idxmax()]
  
#A person who messages from 5am - 9am
def early_bird(df):
    # Early bird: messages sent between 5 AM and 8 AM (inclusive)
    df_early = df[(df['hour'] >= 5) & (df['hour'] <= 8)]
    if df_early.empty:
        return None
    df2 = df_early.groupby('user')['messages'].count().reset_index()
    df2 = df2.sort_values('messages', ascending=False)

    df2 = df2[df2['user'] != 'Meta AI']

    return df2.loc[df2['messages'].idxmax()]

def nightowl(df):
    # Night owl: messages sent between 10 PM and 2 AM
    df_night = df[(df['hour'] >= 22) | (df['hour'] <= 2)]
    if df_night.empty:
        return None
    df2 = df_night.groupby('user')['messages'].count().reset_index()
    df2 = df2.sort_values('messages', ascending=False)

    df2 = df2[df2['user'] != 'Meta AI']

    return df2.loc[df2['messages'].idxmax()]


# Least average words per message
def dryReplier(df):
    df['word_count'] = df['messages'].apply(lambda x: len(x.split()))
    df2 = df.groupby('user')['word_count'].mean().reset_index()
    df2['word_count'] = df2['word_count'].round(2)
    
    # Remove Meta AI
    df2 = df2[df2['user'] != 'Meta AI']
    
    return df2.loc[df2['word_count'].idxmin()]

# Highest average words per message
def eassyWriter(df):
    df['word_count'] = df['messages'].apply(lambda x: len(x.split()))
    df2 = df.groupby('user')['word_count'].mean().reset_index()
    df2['word_count'] = df2['word_count'].round(2)
    
    # Remove Meta AI
    df2 = df2[df2['user'] != 'Meta AI']
    
    return df2.loc[df2['word_count'].idxmax()]


#Least Message in the group
def ghost(df):
    df2 = df.groupby('user')['messages'].count().reset_index()
    df2 = df2.sort_values('messages', ascending=False)
    
    ghost_user = df2.loc[df2['messages'].idxmin()]
    
    if ghost_user['user'] == 'Meta AI':
        df2 = df2[df2['user'] != 'Meta AI']
        ghost_user = df2.loc[df2['messages'].idxmin()]
    
    return ghost_user

#Person Doing the most first Messages of the day
def conversationStarter(df):
  df = df[df['hour'] >= 6]

  df = df.sort_values(by=['date', 'hour', 'minute'])

  first_senders = df.groupby('date').first().reset_index()

  starter_counts = first_senders['user'].value_counts().reset_index()
  starter_counts.columns = ['user', 'count']

  starter_counts = starter_counts[starter_counts['user'] != 'Meta AI']
  
  return starter_counts.iloc[0]