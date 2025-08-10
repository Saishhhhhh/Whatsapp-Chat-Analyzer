import pandas as pd
import streamlit as st

st.title("Whatsapp Chat Analyzer")

uploaded_file = st.file_uploader("Choose your file", type = 'txt')

content = 'empty file'

if uploaded_file is not None:
  file = open('Whatsapp_Chat.txt', "r", encoding='utf-8')
  content = file.read()
  
