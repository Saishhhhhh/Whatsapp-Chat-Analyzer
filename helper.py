import pandas as pd
from urlextract import URLExtract

extract = URLExtract()

# Creating New DataFrame based on Date Range For Processing Further
def date_range_dataframe(df, min_date, max_date):

  new_df = df.query('date >= @min_date and date <= @max_date').reset_index(drop=True)

  return new_df



def basic_stats(df):
  total_messages = df.shape[0]

  media_messages = df[df['messages'] == "<Media omitted>"].shape[0]

  #Deleting the media messages words ("Media ommitted")
  total_words = (df['word_count'].sum()) - media_messages*2

  links = []
  for message in df['messages']:
    links.extend(extract.find_urls(message))

  return total_messages, media_messages, total_words, len(links)
