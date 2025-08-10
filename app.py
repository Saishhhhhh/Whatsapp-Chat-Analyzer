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

# Add custom styling for the app
st.markdown("""
<style>
/* Data Overview Section Styling */
.data-overview-header {
    background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    border: 1px solid #404040;
}

.data-overview-title {
    color: #ffffff;
    font-size: 1.8em;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}

.metric-container {
    background: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    transition: transform 0.2s ease;
}

.metric-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}

.metric-label {
    color: #cccccc;
    font-size: 0.9em;
    font-weight: 500;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    color: #00bfff;
    font-size: 2.2em;
    font-weight: bold;
    margin-bottom: 5px;
}

.metric-unit {
    color: #888888;
    font-size: 0.8em;
    font-weight: normal;
}

/* Award Section Styling */
.award-container {
    background: #1a1a1a;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid #404040;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

.award-title {
    font-size: 1.3em;
    font-weight: bold;
    color: #ffd700;
    margin-bottom: 8px;
}

.award-value {
    font-size: 1.2em;
    color: #ffffff;
    font-weight: 600;
    margin-bottom: 8px;
}

.award-data {
    font-size: 0.9em;
    color: #cccccc;
    font-weight: normal;
    margin-bottom: 10px;
}

.award-description {
    font-size: 0.95em;
    color: #cccccc;
    font-style: italic;
    margin-top: 8px;
    padding: 8px 0;
    border-top: 1px solid #404040;
}

/* Timeline Analysis Section Styling */
.timeline-header {
    background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    border: 1px solid #404040;
}

.timeline-title {
    color: #ffffff;
    font-size: 1.8em;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}

.timeline-subheader {
    background: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 12px;
    padding: 15px 20px;
    margin: 15px 0;
    text-align: center;
}

.timeline-subtitle {
    color: #00bfff;
    font-size: 1.4em;
    font-weight: bold;
    margin: 0;
}

.chart-container {
    background: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* Content Analysis Section Styling */
.content-header {
    background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    border: 1px solid #404040;
}

.content-title {
    color: #ffffff;
    font-size: 1.8em;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}

.content-subheader {
    background: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 12px;
    padding: 15px 20px;
    margin: 15px 0;
    text-align: center;
}

.content-subtitle {
    color: #00bfff;
    font-size: 1.4em;
    font-weight: bold;
    margin: 0;
}

.dataframe-container {
    background: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* User Analysis Section Styling */
.user-header {
    background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    border: 1px solid #404040;
}

.user-title {
    color: #ffffff;
    font-size: 1.8em;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}

.user-subheader {
    background: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 12px;
    padding: 15px 20px;
    margin: 15px 0;
    text-align: center;
}

.user-subtitle {
    color: #00bfff;
    font-size: 1.4em;
    font-weight: bold;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("## 💬 WhatsApp Chat Analyzer")

# Sidebar: File Uploader
uploaded_file = st.sidebar.file_uploader("Choose your file", type='txt')

# If file is uploaded
if uploaded_file is not None:
    # Convert uploaded file into DataFrame
    df = preprocess.create_dataframe_from_file(uploaded_file)
    
    # Initialize options list for user selection
    options = ['all']
    
    # Add all unique users from chat to options
    for users in df['user'].unique():
        options.append(users)
    
    # User selection dropdown
    choice = st.sidebar.selectbox("Choose a user:", options)
    st.sidebar.write(f"You selected {choice}.")
    
    # Get min/max dates for date range filter
    min_date = df.loc[0,'date']
    max_date = df.iloc[-1]['date']
    
    # Default date range (entire chat)
    default_start_date = min_date
    default_end_date = max_date
    
    # Date range slider
    selected_dates = st.sidebar.slider(
        "Select a date range",
        value=(default_start_date, default_end_date),
        min_value=min_date,
        max_value=max_date,
        format="YYYY-MM-DD",
        step=datetime.timedelta(days=1) 
    )
    
    start_date, end_date = selected_dates
    
    # Display selected date range
    st.sidebar.write(f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
    
    # Analysis button clicked
    if st.sidebar.button("Show Analysis"):
        # Filter DataFrame by date range
        df = helper.date_range_dataframe(df, start_date, end_date)
        
        # Filter by specific user if selected
        if(choice != 'all'):
            df = df[df['user'] == choice].reset_index(drop=True)
        
        # ===== DATA OVERVIEW SECTION =====
        st.markdown("""
        <div class="data-overview-header">
            <div class="data-overview-title">📊 Data Overview</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display filtered data
        with st.expander("View Chat Data", expanded=False):
            st.dataframe(df)
        
        # Calculate and display basic stats
        total_messages, total_media, total_words, total_links = helper.basic_stats(df)
        
        # Stats in columns with custom styling
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Total Messages</div>
                <div class="metric-value">{total_messages}</div>
                <div class="metric-unit">messages</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Media Shared</div>
                <div class="metric-value">{total_media}</div>
                <div class="metric-unit">files</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Words Written</div>
                <div class="metric-value">{total_words}</div>
                <div class="metric-unit">words</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Links Shared</div>
                <div class="metric-value">{total_links}</div>
                <div class="metric-unit">links</div>
            </div>
            """, unsafe_allow_html=True)

        # ===== TIMELINE ANALYSIS SECTION =====
        st.markdown("""
        <div class="timeline-header">
            <div class="timeline-title">📈 Timeline Analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Monthly Timeline Chart
        st.markdown("""
        <div class="timeline-subheader">
            <div class="timeline-subtitle">📅 Monthly Activity</div>
        </div>
        """, unsafe_allow_html=True)
        
        timeline = helper.monthly_timeline(df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=timeline['time'], y=timeline['messages'], ax=ax, color='#00d4ff', linewidth=3, marker='o', markersize=6)
        
        ax.set_title("Messages Per Month", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("No. Of Messages", color='#cccccc', fontsize=12)
        ax.set_xlabel("", color='#cccccc')
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#1a1a1a')
        ax.tick_params(colors='#cccccc')
        ax.spines['bottom'].set_color('#404040')
        ax.spines['top'].set_color('#404040')
        ax.spines['left'].set_color('#404040')
        ax.spines['right'].set_color('#404040')
        
        # Limit x-axis ticks for readability
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
        plt.xticks(rotation=45, ha='right')
        
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Daily Timeline Chart
        st.markdown("""
        <div class="timeline-subheader">
            <div class="timeline-subtitle">📊 Daily Activity</div>
        </div>
        """, unsafe_allow_html=True)
        
        timeline = helper.datewise_timeline(df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=timeline['date'], y=timeline['messages'], color='#ff6b6b', linewidth=2, alpha=0.8)
        
        ax.set_title("Messages Per Day", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("No. Of Messages", color='#cccccc', fontsize=12)
        ax.set_xlabel("", color='#cccccc')
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#1a1a1a')
        ax.tick_params(colors='#cccccc')
        ax.spines['bottom'].set_color('#404040')
        ax.spines['top'].set_color('#404040')
        ax.spines['left'].set_color('#404040')
        ax.spines['right'].set_color('#404040')
        
        plt.xticks(rotation='vertical')
        
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== TIME PATTERNS SECTION =====
        st.markdown("""
        <div class="timeline-header">
            <div class="timeline-title">⏰ Time Patterns</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hourly Timeline Chart
        st.markdown("""
        <div class="timeline-subheader">
            <div class="timeline-subtitle">🕐 Hourly Activity</div>
        </div>
        """, unsafe_allow_html=True)
        
        timeline = helper.hourly_timeline(df)
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43', '#10ac84', '#ee5a24', '#2e86de', '#a55eea', '#26de81', '#778ca3', '#fd79a8', '#fdcb6e', '#6c5ce7', '#00b894', '#e84393', '#6c5ce7', '#00cec9', '#fd79a8']
        sns.barplot(x=timeline['period'], y=timeline['messages'], ax=ax, palette=colors[:len(timeline)])
        
        ax.set_title("Messages Per Hour", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("No. Of Messages", color='#cccccc', fontsize=12)
        ax.set_xlabel("", color='#cccccc')
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#1a1a1a')
        ax.tick_params(colors='#cccccc')
        ax.spines['bottom'].set_color('#404040')
        ax.spines['top'].set_color('#404040')
        ax.spines['left'].set_color('#404040')
        ax.spines['right'].set_color('#404040')
        
        plt.xticks(rotation='vertical')
        
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Weekly Timeline Chart
        st.markdown("""
        <div class="timeline-subheader">
            <div class="timeline-subtitle">📅 Weekly Activity</div>
        </div>
        """, unsafe_allow_html=True)
        
        timeline = helper.weekly_timeline(df)
        fig, ax = plt.subplots(figsize=(10, 6))
        weekly_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff']
        sns.barplot(x=timeline['day_name'], y=timeline['messages'], ax=ax, palette=weekly_colors)
        
        ax.set_title("Messages Per Day", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("No. Of Messages", color='#cccccc', fontsize=12)
        ax.set_xlabel("", color='#cccccc')
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#1a1a1a')
        ax.tick_params(colors='#cccccc')
        ax.spines['bottom'].set_color('#404040')
        ax.spines['top'].set_color('#404040')
        ax.spines['left'].set_color('#404040')
        ax.spines['right'].set_color('#404040')
        
        plt.xticks(rotation='vertical')
        
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Monthly Timeline Chart
        st.markdown("""
        <div class="timeline-subheader">
            <div class="timeline-subtitle">📊 Monthly Activity</div>
        </div>
        """, unsafe_allow_html=True)
        
        timeline = helper.monthwise_timeline(df)
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43', '#10ac84', '#ee5a24']
        sns.barplot(x=timeline['month'], y=timeline['messages'], ax=ax, palette=monthly_colors[:len(timeline)])
        
        ax.set_title("Messages Per Month", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("No. Of Messages", color='#cccccc', fontsize=12)
        ax.set_xlabel("", color='#cccccc')
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#1a1a1a')
        ax.tick_params(colors='#cccccc')
        ax.spines['bottom'].set_color('#404040')
        ax.spines['top'].set_color('#404040')
        ax.spines['left'].set_color('#404040')
        ax.spines['right'].set_color('#404040')
        
        plt.xticks(rotation='vertical')
        
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Weekly Heatmap
        st.markdown("""
        <div class="timeline-subheader">
            <div class="timeline-subtitle">🔥 Weekly Heatmap</div>
        </div>
        """, unsafe_allow_html=True)
        
        table = helper.weekly_heatmap(df)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(table, cmap='viridis', ax=ax, cbar_kws={'label': 'Messages'}, annot=True, fmt='.0f', linewidths=0.5)
        
        ax.set_title("Day-Time Heatmap", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("Day", color='#cccccc', fontsize=12)
        ax.set_xlabel("Hour Of The Day", color='#cccccc', fontsize=12)
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#1a1a1a')
        ax.tick_params(colors='#cccccc')
        
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # ===== CONTENT ANALYSIS SECTION =====
        st.markdown("""
        <div class="content-header">
            <div class="content-title">📝 Content Analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Wordcloud
        st.markdown("""
        <div class="content-subheader">
            <div class="content-subtitle">☁️ Word Cloud</div>
        </div>
        """, unsafe_allow_html=True)
        
        df_wc = helper.create_wordcloud(df)
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(df_wc)
        ax.axis('off')
        ax.set_title("Most Common Words in Chat", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
        
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Emoji analysis
        st.markdown("""
        <div class="content-subheader">
            <div class="content-subtitle">😊 Emoji Usage</div>
        </div>
        """, unsafe_allow_html=True)
        
        emoji_frame = helper.most_common_emojis_dataframe(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="dataframe-container">
            """, unsafe_allow_html=True)
            st.dataframe(emoji_frame)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Emoji pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43']
            wedges, texts, autotexts = ax.pie(
                emoji_frame['count'].head(10),
                labels=emoji_frame['emoji'].head(10),
                autopct="%0.1f%%",
                colors=colors[:len(emoji_frame.head(10))],
                startangle=90
            )
            
            # Style the pie chart
            ax.set_title("Top 10 Emojis", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
            ax.set_facecolor('#1a1a1a')
            fig.patch.set_facecolor('#1a1a1a')
            
            # Style the text elements
            for autotext in autotexts:
                autotext.set_color('#ffffff')
                autotext.set_fontweight('bold')
            
            for text in texts:
                text.set_color('#cccccc')
                text.set_fontsize(12)
            
            st.markdown("""
            <div class="chart-container">
            """, unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        # ===== USER ANALYSIS SECTION =====
        if(choice == 'all'):
            # Hide empty wrapper boxes created by HTML containers around charts/dataframes
            st.markdown("""
            <style>
            .chart-container, .dataframe-container {
                display: none !important;
                padding: 0 !important;
                margin: 0 !important;
                border: none !important;
                box-shadow: none !important;
                background: transparent !important;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="content-header">
                <div class="content-title">👥 User Analysis</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Top 10 most active users
            st.markdown("""
            <div class="content-subheader">
                <div class="content-subtitle">📊 Most Active Users</div>
            </div>
            """, unsafe_allow_html=True)
            timeline = helper.busy_user_bar(df).head(10)
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Use better colors for the bar plot
            colors = ['#00d4ff', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3']
            sns.barplot(x=timeline['user'], y=timeline['messages'], palette=colors[:len(timeline)])
            
            # Style the chart
            ax.set_title("Most Busy Users", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel("Messages", color='#ffffff', fontsize=12)
            ax.set_xlabel("Users", color='#ffffff', fontsize=12)
            ax.set_facecolor('#1a1a1a')
            fig.patch.set_facecolor('#1a1a1a')
            ax.tick_params(colors='#cccccc')
            
            # Style the spines
            for spine in ax.spines.values():
                spine.set_color('#404040')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            st.markdown("""
            <div class="chart-container">
            """, unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

            # User message percentages
            st.markdown("""
            <div class="content-subheader">
                <div class="content-subtitle">📈 User Message Distribution</div>
            </div>
            """, unsafe_allow_html=True)
            percent_df = helper.busy_user_dataframe(df)
            
            st.markdown("""
            <div class="dataframe-container">
            """, unsafe_allow_html=True)
            st.dataframe(percent_df)
            st.markdown("</div>", unsafe_allow_html=True)

            # ===== AWARDS SECTION =====
            st.markdown("""
            <div class="content-header">
                <div class="content-title">🏆 Chat Awards</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create columns for awards
            col1, col2 = st.columns(2)
            
            with col1:
                # Chatterbox award
                frame = helper.chatterbox(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Chatterbox</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">📊 {int(frame['messages'])} messages</div>
                        <div class="award-description">User with the most total messages in the chat</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

                # Keyboard warrior award
                frame = helper.keyboard_warrior(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Keyboard Warrior</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">📝 {int(frame['word_count'])} words</div>
                        <div class="award-description">User who wrote the most total words</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

                # Media sharer award
                frame = helper.media_Paglu(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Media Master</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">📱 {int(frame['messages'])} media files</div>
                        <div class="award-description">User who shared the most media files (images, videos, etc.)</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

                # Link master award
                frame = helper.linkMaster(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Link Master</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">🔗 {int(frame['link_count'])} links</div>
                        <div class="award-description">User who shared the most links/URLs</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

            with col2:
                # Early bird award
                frame = helper.early_bird(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Early Bird</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">🌅 {int(frame['messages'])} early messages</div>
                        <div class="award-description">User who sent most messages between 5 AM - 8 AM</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

                # Night owl award
                frame = helper.nightowl(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Night Owl</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">🦉 {int(frame['messages'])} late night messages</div>
                        <div class="award-description">User who sent most messages between 10 PM - 2 AM</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

                # Dry replier award
                frame = helper.dryReplier(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Dry Replier</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">💬 {float(frame['word_count']):.1f} avg words</div>
                        <div class="award-description">User with lowest average words per message</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

                # Essay writer award
                frame = helper.eassyWriter(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Essay Writer</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">📚 {float(frame['word_count']):.1f} avg words</div>
                        <div class="award-description">User with highest average words per message</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

            # Ghost and Conversation Starter in full width
            col1, col2 = st.columns(2)
            
            with col1:
                # Ghost award
                frame = helper.ghost(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Ghost</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">👻 {int(frame['messages'])} messages</div>
                        <div class="award-description">User with the least messages in the group</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

            with col2:
                # Conversation starter award
                frame = helper.conversationStarter(df)
                if frame is not None:
                    st.markdown(f"""
                    <div class="award-container">
                        <div class="award-title">🏆 Conversation Starter</div>
                        <div class="award-value">{str(frame['user'])}</div>
                        <div class="award-data">🚀 {int(frame['count'])} times</div>
                        <div class="award-description">User who started most conversations (first message of the day)</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.text("No messages found.")

# Welcome screen when no file uploaded
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