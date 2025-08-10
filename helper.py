import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from collections import Counter

# Initialize URL extractor for finding links in messages
extract = URLExtract()

# Filter dataframe by date range for analysis
def date_range_dataframe(df, min_date, max_date):
  new_df = df.query('date >= @min_date and date <= @max_date').reset_index(drop=True)
  return new_df

# Calculate basic statistics: total messages, media, words, and links
def basic_stats(df):
  total_messages = df.shape[0]

  # Count media messages (images, videos, etc.)
  media_messages = df[df['messages'] == "<Media omitted>"].shape[0]

  # Calculate total words excluding media messages
  total_words = (df['word_count'].sum()) - media_messages*2

  # Extract and count all URLs from messages
  links = []
  for message in df['messages']:
    links.extend(extract.find_urls(message))

  return total_messages, media_messages, total_words, len(links)

# Group messages by month and year for timeline analysis
def monthly_timeline(df):
  timeline = df.groupby(['year', 'month_num', 'month'])['messages'].count().reset_index()
  time = []

  # Create formatted time labels (e.g., "January-2023")
  for i in range(timeline.shape[0]):
      time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

  timeline['time'] = time
  return timeline

# Count messages per date for daily timeline
def datewise_timeline(df):
  timeline = df.groupby('date')['messages'].count().reset_index()
  return timeline

# Count messages per day of week, ordered from Monday to Sunday
def weekly_timeline(df):
  timeline = df.groupby(['day_name'])['messages'].count().reset_index()

  # Define proper day order for sorting
  day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

  # Convert to categorical for proper sorting
  timeline['day_name'] = pd.Categorical(timeline['day_name'], categories=day_order, ordered=True)
  timeline = timeline.sort_values('day_name').reset_index(drop=True)

  return timeline

# Count messages per month, ordered from January to December
def monthwise_timeline(df):
  timeline = df.groupby(['month'])['messages'].count().reset_index()

  # Define proper month order for sorting
  month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

  # Convert to categorical for proper sorting
  timeline['month'] = pd.Categorical(timeline['month'], categories=month_order, ordered=True)
  timeline = timeline.sort_values('month').reset_index(drop=True)

  return timeline

# Count messages per hour period (24-hour format)
def hourly_timeline(df):
  timeline = df.groupby('period')['messages'].count().reset_index()
  
  # Define hour periods in order
  time_period_order = [
      '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10',
      '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
      '18-19', '19-20', '20-21', '21-22', '22-23', '23-00'
    ]
  
  # Reindex to maintain proper hour order
  timeline = timeline.set_index('period').reindex(time_period_order).reset_index()
  return timeline

# Create weekly activity heatmap (day vs hour)
def weekly_heatmap(df):
  # Pivot table: rows=days, columns=hours, values=message counts
  user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

  # Define proper ordering for time periods and days
  time_period_order = [
    '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10',
    '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
    '18-19', '19-20', '20-21', '21-22', '22-23', '23-00'
  ]

  day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

  # Reindex to maintain proper order
  user_heatmap = user_heatmap.reindex(day_order)
  existing_columns = [col for col in time_period_order if col in user_heatmap.columns]
  user_heatmap = user_heatmap[existing_columns]

  return user_heatmap

# Generate wordcloud from all text messages (excluding media)
def create_wordcloud(df):
  wc = WordCloud(width=500, height = 500, min_font_size = 10, background_color = "white")
  # Filter out media messages before generating wordcloud
  df2 = df[df['messages'] != "<Media omitted>"]
  df_wc = wc.generate(df2['messages'].str.cat(sep=" "))
  return df_wc

# Find top 10 most used emojis in messages
def most_common_emojis_dataframe(df):
  emojis = []
  # Extract all emojis from each message
  for message in df['messages']:
      emojis.extend([char for char in message if char in emoji.EMOJI_DATA])

  # Count emoji frequencies and return top 10
  emoji_df = pd.DataFrame(Counter(emojis).most_common(10), columns=['emoji', 'count'])
  return emoji_df

# Count messages per user for bar plot
def busy_user_bar(df):
  return df.groupby('user')['messages'].count().reset_index()

# Calculate message percentage per user (excluding Meta AI)
def busy_user_dataframe(df):
  df2 = df.groupby('user')['messages'].count().reset_index()
  total_messages = df2['messages'].sum()
  # Calculate percentage contribution of each user
  df2['percentage'] = round((df2['messages']/ total_messages)*100,2)
  df2 = df2.sort_values('percentage', ascending=False)
  df2 = df2.drop(columns='messages', axis=1)
  
  return df2

# Find user with most messages (excluding Meta AI)
def chatterbox(df):
  df2 = df.groupby('user')['messages'].count().reset_index()
  df2 = df2.sort_values('messages', ascending=False)

  # Filter out Meta AI from analysis
  df2 = df2[df2['user'] != 'Meta AI']

  return df2.loc[df2['messages'].idxmax()]

# Find user who wrote most words (excluding Meta AI)
def keyboard_warrior(df):
  df2 = df.groupby('user')['word_count'].sum().reset_index()
  df2 = df2.sort_values('word_count', ascending=False)

  # Filter out Meta AI from analysis
  df2 = df2[df2['user'] != 'Meta AI']

  return df2.loc[df2['word_count'].idxmax()]

# Find user who shared most media (excluding Meta AI)
def media_Paglu(df):
  df2 = df.query('messages == "<Media omitted>"')
  df2 = df2.groupby('user')['messages'].count().reset_index().sort_values('messages', ascending=False)

  # Filter out Meta AI from analysis
  df2 = df2[df2['user'] != 'Meta AI']

  return df2.loc[df2['messages'].idxmax()]

# Find user who shared most links (excluding Meta AI)
def linkMaster(df):
  extractor = URLExtract()

  # Count links in each message
  df['link_count'] = df['messages'].apply(lambda msg: len(extractor.find_urls(msg)))

  # Sum link counts per user
  df2 = df.groupby('user', as_index=False)['link_count'].sum()

  # Filter out Meta AI from analysis
  df2 = df2[df2['user'] != 'Meta AI']

  return df2.loc[df2['link_count'].idxmax()]
  
# Find user who messages most between 5 AM - 8 AM (early bird)
def early_bird(df):
    # Filter messages sent between 5 AM and 8 AM
    df_early = df[(df['hour'] >= 5) & (df['hour'] <= 8)]
    if df_early.empty:
        return None
    
    df2 = df_early.groupby('user')['messages'].count().reset_index()
    df2 = df2.sort_values('messages', ascending=False)

    # Filter out Meta AI from analysis
    df2 = df2[df2['user'] != 'Meta AI']

    return df2.loc[df2['messages'].idxmax()]

# Find user who messages most between 10 PM - 2 AM (night owl)
def nightowl(df):
    # Filter messages sent between 10 PM and 2 AM (crosses midnight)
    df_night = df[(df['hour'] >= 22) | (df['hour'] <= 2)]
    if df_night.empty:
        return None
    
    df2 = df_night.groupby('user')['messages'].count().reset_index()
    df2 = df2.sort_values('messages', ascending=False)

    # Filter out Meta AI from analysis
    df2 = df2[df2['user'] != 'Meta AI']

    return df2.loc[df2['messages'].idxmax()]

# Find user with lowest average words per message (dry replier)
def dryReplier(df):
    # Calculate word count for each message
    df['word_count'] = df['messages'].apply(lambda x: len(x.split()))
    df2 = df.groupby('user')['word_count'].mean().reset_index()
    df2['word_count'] = df2['word_count'].round(2)
    
    # Remove Meta AI from analysis
    df2 = df2[df2['user'] != 'Meta AI']
    
    return df2.loc[df2['word_count'].idxmin()]

# Find user with highest average words per message (essay writer)
def eassyWriter(df):
    # Calculate word count for each message
    df['word_count'] = df['messages'].apply(lambda x: len(x.split()))
    df2 = df.groupby('user')['word_count'].mean().reset_index()
    df2['word_count'] = df2['word_count'].round(2)
    
    # Remove Meta AI from analysis
    df2 = df2[df2['user'] != 'Meta AI']
    
    return df2.loc[df2['word_count'].idxmax()]

# Find user with least messages in the group (ghost)
def ghost(df):
    df2 = df.groupby('user')['messages'].count().reset_index()
    df2 = df2.sort_values('messages', ascending=False)
    
    ghost_user = df2.loc[df2['messages'].idxmin()]
    
    # If Meta AI has least messages, find the next user
    if ghost_user['user'] == 'Meta AI':
        df2 = df2[df2['user'] != 'Meta AI']
        ghost_user = df2.loc[df2['messages'].idxmin()]
    
    return ghost_user

# Find user who starts most conversations (first message of the day)
def conversationStarter(df):
  # Filter messages after 6 AM (reasonable start time)
  df = df[df['hour'] >= 6]

  # Sort by date, hour, minute to find first message of each day
  df = df.sort_values(by=['date', 'hour', 'minute'])

  # Get first message of each day
  first_senders = df.groupby('date').first().reset_index()

  # Count how many times each user sent first message
  starter_counts = first_senders['user'].value_counts().reset_index()
  starter_counts.columns = ['user', 'count']

  # Remove Meta AI from analysis
  starter_counts = starter_counts[starter_counts['user'] != 'Meta AI']
  
  return starter_counts.iloc[0]