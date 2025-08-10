import pandas as pd
import streamlit as st
import re
import preprocess
import datetime
import helper
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",  # Browser tab title
    page_icon="💬",                       # Emoji icon
    layout="wide"                         # Wide page layout
)

# Main header
st.markdown("## 💬 WhatsApp Chat Analyzer")

# Sidebar: File Uploader
uploaded_file = st.sidebar.file_uploader("Choose your file", type='txt')

#If file is uploaded
if uploaded_file is not None:

    # Convert uploaded file into DataFrame using custom preprocess function
    df = preprocess.create_dataframe_from_file(uploaded_file)
    
    # Initialize options list for user selection
    options = ['all']
    
    # Add all unique users from chat to the dropdown options
    for users in df['user'].unique():
        options.append(users)
    
    # Sidebar dropdown for selecting a specific user or "all"
    choice = st.sidebar.selectbox("Choose a user:", options)
    st.sidebar.write(f"You selected {choice}.")
    
    # Get minimum and maximum dates from chat for date range filter
    min_date = df.loc[0,'date']
    max_date = df.iloc[-1]['date']
    
    # Default date range (entire chat)
    default_start_date = min_date
    default_end_date = max_date
    
    # Sidebar date range slider
    selected_dates = st.sidebar.slider(
        "Select a date range",
        value=(default_start_date, default_end_date),
        min_value=min_date,
        max_value=max_date,
        format="YYYY-MM-DD",
        step=datetime.timedelta(days=1) 
    )
    
    start_date, end_date = selected_dates
    
     # Display selected date range in sidebar
    st.sidebar.write(f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
    
    # Show Analysis Button Clicked
    if st.sidebar.button("Show Analysis"):

        # Filter DataFrame as per selected date range
        df = helper.date_range_dataframe(df, start_date, end_date)
        
        # If specific user is selected, filter chat only for that user
        if(choice != 'all'):
            df = df[df['user'] == choice].reset_index(drop=True)
        
        st.dataframe(df)
        
        # Calculate basic statistics using helper function
        total_messages, total_media, total_words, total_links = helper.basic_stats(df)
        
        st.text(f"Total Messages: {total_messages}")    
        st.text(f"Total Media Shared: {total_media}")
        st.text(f"Total Words Written: {total_words}")
        st.text(f"Total Links Shared: {total_links}")

        # Monthly Timeline
        timeline = helper.monthly_timeline(df)

        fig, ax = plt.subplots()
        sns.lineplot(x=timeline['time'], y=timeline['messages'], ax=ax)

        ax.set_title("Messages Per Month")
        ax.set_ylabel("No. Of Messages")
        ax.set_xlabel("")

        # Show fewer ticks (e.g., max 10 labels)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))

        plt.xticks(rotation=45, ha='right')  # Rotate and align labels
        st.pyplot(fig)

        #Datewise Timeline
        timeline = helper.datewise_timeline(df)
        fig,ax = plt.subplots() # Create a Matplotlib figure and axes
        sns.lineplot(x = timeline['date'], y = timeline['messages'])

        ax.set_title("Messages Per Day") # Customize with Matplotlib
        ax.set_ylabel("No. Of Messages")
        ax.set_xlabel("")

        plt.xticks(rotation='vertical') 
        st.pyplot(fig)

        #Hourly Timeline
        timeline = helper.hourly_timeline(df)
        fig,ax = plt.subplots() # Create a Matplotlib figure and axes
        sns.barplot(x = timeline['period'], y = timeline['messages'])

        ax.set_title("Messages Per Hour") # Customize with Matplotlib
        ax.set_ylabel("No. Of Messages")
        ax.set_xlabel("")

        plt.xticks(rotation='vertical') 
        st.pyplot(fig)

        #Activity Map

        #Weekly Timeline
        timeline = helper.weekly_timeline(df)
        fig,ax = plt.subplots() # Create a Matplotlib figure and axes
        sns.barplot(x = timeline['day_name'], y = timeline['messages'])

        ax.set_title("Messages Per Day") # Customize with Matplotlib
        ax.set_ylabel("No. Of Messages")
        ax.set_xlabel("")

        plt.xticks(rotation='vertical') 
        st.pyplot(fig)

        #Month wise Timeline
        timeline = helper.monthwise_timeline(df)
        fig,ax = plt.subplots() # Create a Matplotlib figure and axes
        sns.barplot(x = timeline['month'], y = timeline['messages'])

        ax.set_title("Messages Per Month") # Customize with Matplotlib
        ax.set_ylabel("No. Of Messages")
        ax.set_xlabel("")

        plt.xticks(rotation='vertical') 
        st.pyplot(fig)

        #Weekly Heatmap
        table = helper.weekly_heatmap(df)
        fig,ax = plt.subplots() # Create a Matplotlib figure and axes
        sns.heatmap(table, cmap='rocket_r')

        ax.set_title("Day-Time Heatmap") # Customize with Matplotlib
        ax.set_ylabel("Day")
        ax.set_xlabel("Hour Of The Day")

        st.pyplot(fig)

        #Wordcloud
        df_wc = helper.create_wordcloud(df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Only All Features
        if(choice == 'all'):

            #Most busy users barplot
            timeline = helper.busy_user_bar(df)
            fig,ax = plt.subplots() # Create a Matplotlib figure and axes
            sns.barplot(x = timeline['user'], y = timeline['messages'])

            ax.set_title("Most Busy Users") # Customize with Matplotlib
            ax.set_ylabel("")
            ax.set_xlabel("")

            plt.xticks(rotation='vertical') 
            st.pyplot(fig)

            #Most busy users dataframe

            percent_df = helper.busy_user_dataframe(df)

            st.dataframe(percent_df)

           
        emoji_frame = helper.most_common_emojis_dataframe(df)

        st.dataframe(emoji_frame)

        fig,ax = plt.subplots()
        ax.pie(
            emoji_frame['count'].head(),
            labels=emoji_frame['emoji'].head(),
            autopct="%0.2f%%"  # Added % to make it show percentages
        )
        st.pyplot(fig)

        if(choice == 'all'):

            #Awards Section

            frame = helper.chatterbox(df)
            if frame is not None:
                st.text(f"Highest Messages: {frame['user']}")
                st.text(frame['messages'])
            else:
                st.text("No messages found.")

            frame = helper.keyboard_warrior(df)
            if frame is not None:
                st.text(f"Highest Word Count: {frame['user']}")
                st.text(frame['word_count'])
            else:
                st.text("No messages found.")

            frame = helper.media_Paglu(df)
            if frame is not None:
                st.text(f"Most Media Messages: {frame['user']}")
                st.text(frame['messages'])
            else:
                st.text("No messages found.")

            frame = helper.linkMaster(df)
            if frame is not None:
                st.text(f"Most Links Shared: {frame['user']}")
                st.text(frame['link_count'])
            else:
                st.text("No messages found.")

            frame = helper.early_bird(df)
            if frame is not None:
                st.text(f"Early Bird: {frame['user']}")
                st.text(frame['messages'])
            else:
                st.text("No messages found.")

            frame = helper.nightowl(df)
            if frame is not None:
                st.text(f"Night Owl: {frame['user']}")
                st.text(frame['messages'])
            else:
                st.text("No messages found.")

            frame = helper.dryReplier(df)
            if frame is not None:
                st.text(f"Dry Replier: {frame['user']}")
                st.text(frame['word_count'])
            else:
                st.text("No messages found.")

            frame = helper.eassyWriter(df)
            if frame is not None:
                st.text(f"Eassy Writer: {frame['user']}")
                st.text(frame['word_count'])
            else:
                st.text("No messages found.")

            frame = helper.ghost(df)
            if frame is not None:
                st.text(f"Ghost: {frame['user']}")
                st.text(frame['messages'])
            else:
                st.text("No messages found.")

            frame = helper.conversationStarter(df)
            if frame is not None:
                st.text(f"Conversation Starter: {frame['user']}")
                st.text(frame['count'])
            else:
                st.text("No messages found.")

# If no file is uploaded (welcome screen)
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