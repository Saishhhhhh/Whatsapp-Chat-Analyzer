import pandas as pd
import streamlit as st
import re
import preprocess
import datetime

st.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose your file", type = 'txt')

if uploaded_file is not None:
  df = preprocess.create_dataframe_from_file(uploaded_file)
  st.dataframe(df)

  options = ['all'];

  for users in df['user'].unique():
    options.append(users)
  
  choice = st.sidebar.selectbox("Choose a user:", options)
  st.sidebar.write(f"You selected {choice}.")

  min_date = df.loc[0,'date']
  max_date = df.iloc[-1]['date']

  default_start_date = min_date
  default_end_date = max_date

  selected_dates = st.sidebar.slider(
    "Select a date range",
    value=(default_start_date, default_end_date),
    min_value=min_date,
    max_value=max_date,
    format="YYYY-MM-DD" 
  )

  start_date, end_date = selected_dates

  st.sidebar.write(f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")

  if st.sidebar.button("Show Analysis"):
    pass