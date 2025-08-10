import pandas as pd
import streamlit as st
import re
import preprocess
import datetime
import helper

# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

# Main header
st.markdown("## 💬 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose your file", type='txt')

if uploaded_file is not None:
    df = preprocess.create_dataframe_from_file(uploaded_file)
    
    options = ['all']
    
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
        format="YYYY-MM-DD",
        step=datetime.timedelta(days=1) 
    )
    
    start_date, end_date = selected_dates
    
    st.sidebar.write(f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
    
    # Show Analysis Button Clicked
    if st.sidebar.button("Show Analysis"):
        # Dataframe Conversion as per data range
        df = helper.date_range_dataframe(df, start_date, end_date)
        
        # For single user
        if(choice != 'all'):
            df = df[df['user'] == choice].reset_index(drop=True)
        
        st.dataframe(df)
        
        # Basic Stats
        total_messages, total_media, total_words, total_links = helper.basic_stats(df)
        
        st.text(f"Total Messages: {total_messages}")    
        st.text(f"Total Media Shared: {total_media}")
        st.text(f"Total Words Written: {total_words}")
        st.text(f"Total Links Shared: {total_links}")

# Welcome message when no file is uploaded
elif uploaded_file is None:
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>🚀 Welcome to WhatsApp Chat Analyzer</h2>
        <p style="font-size: 1.1rem; color: #666;">
            Upload your WhatsApp chat export file to get started with the analysis.
        </p>
        <div style="margin-top: 1rem;">
            <p><strong>📋 Supported format:</strong> .txt files</p>
            <p><strong>📱 How to export:</strong> WhatsApp → Chat → Export Chat → Without Media</p>
        </div>
    </div>
    """, unsafe_allow_html=True)