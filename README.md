## WhatsApp Chat Analyzer (EDA + Feature Engineering)

Analyze your WhatsApp chat exports with an elegant Streamlit dashboard. Explore activity timelines, content insights, user behavior, and automatically computed chat awards — all with a cohesive dark theme and polished visuals.

### 🔍 Highlights
- **Zero-setup UI**: Upload your exported WhatsApp `.txt` file and explore instantly
- **Robust parsing**: Supports both 24-hour and 12-hour (AM/PM) timestamps, including narrow spaces (e.g., 11:40 am)
- **Consistent dark theme**: Clean headers, subtle containers, and styled charts
- **Rich insights**: Timelines, heatmaps, word cloud, emoji usage, top users, and awards
- **Local-first**: Your data stays on your machine

---

## ✅ Features
- **Data Overview**: Clean metrics for total messages, media, links, etc.
- **Timeline Analysis**:
  - Monthly and daily timelines
  - Hourly/weekly/monthly activity breakdowns
  - Day–time heatmap (with annotations)
- **Content Analysis**:
  - Word Cloud
  - Emoji frequency table and pie chart (Top 10)
- **User Analysis**:
  - Most active users (Top 10 bar chart)
  - User message distribution table
- **Chat Awards** (with integrated descriptions and subtle numeric data):
  - Chatterbox: Most total messages
  - Keyboard Warrior: Most total words
  - Media Master: Most media files shared
  - Link Master: Most links shared
  - Early Bird: Most messages between 5 AM – 8 AM
  - Night Owl: Most messages between 10 PM – 2 AM
  - Dry Replier: Lowest average words per message
  - Essay Writer: Highest average words per message
  - Ghost: Least messages
  - Conversation Starter: Most days started the conversation

---

## 🧩 Tech Stack
- **Streamlit** for the app UI
- **Pandas** for data handling
- **Matplotlib + Seaborn** for charts
- **WordCloud** for word cloud generation
- **Emoji** for emoji handling

---

## 🚀 Setup

### 1) Clone
```bash
git clone https://github.com/Saishhhhhh/Whatsapp-Chat-Analyzer
cd Whatsapp_Chat_Analysis_EDA_Feature_Engineering
```

### 2) Create and activate a virtual environment (Windows PowerShell)
```bash
python -m venv .venv
.venv\Scripts\Activate
```

### 3) Install dependencies
Option A: Using a requirements file (recommended)
```bash
pip install -r requirements.txt
```

Option B: Install directly
```bash
pip install streamlit pandas matplotlib seaborn wordcloud emoji
```

### 4) Run the app
```bash
streamlit run app.py
```

---

## 📥 Input Data (WhatsApp Export)
- In WhatsApp: Chat → Export Chat → Without Media → Save `.txt`
- Supported date/time examples:
  - `28/12/2022, 11:40 am - Alice: Hello`
  - `28/12/2022, 23:40 - Bob: Hello`
- Preprocessing handles 2- or 4-digit years and both 24h/12h formats.

---

## 🔧 How It Works (Overview)
- `preprocess.py`
  - Reads uploaded `.txt` file
  - Robustly parses timestamps (handles AM/PM and narrow spaces)
  - Extracts `user` and `messages`
  - Derives fields: `date`, `year`, `month`, `day`, `day_name`, `hour`, `minute`, `period`, `word_count`
- `helper.py`
  - Aggregations for timelines and activity plots
  - Word cloud and emoji analysis
  - User stats and award determination
- `app.py`
  - Streamlit UI (sidebar upload + filters)
  - Sectioned layout with consistent dark styling
  - Plots with improved palettes and legibility

---

## 🖥️ Using the App
1. Start the app: `streamlit run app.py`
2. Upload your exported WhatsApp `.txt` file from the sidebar
3. Choose a user or select `all`
4. Explore sections:
   - Data Overview
   - Timeline Analysis (Monthly/Daily/Activity/Heatmap)
   - Content Analysis (Word Cloud, Emojis)
   - User Analysis (Top Users, Distribution)
   - Chat Awards (with per-award descriptions)

---

## 🎨 Visual & Styling Notes
- Consistent dark theme across sections
- Section headers: `.content-header` + `.content-title`
- Subsection headers: `.content-subheader` + `.content-subtitle`
- Chart/data containers use subtle borders and spacing for separation
- Charts:
  - Titles, axis labels, tick colors adapted for dark background
  - Thoughtful palettes for line and bar charts
  - Heatmap uses `viridis` and annotated counts

---

## 📄 Project Structure
```
Whatsapp_Chat_Analysis_EDA_Feature_Engineering/
├─ app.py                 # Streamlit app
├─ preprocess.py          # Input parsing & feature engineering
├─ helper.py              # Aggregations, plots, awards helpers
```

---

## 🔒 Privacy
- The app runs locally; your chat data never leaves your machine.
- You can delete the uploaded file from the sidebar at any time.

---

## 📜 License
Add your preferred license (e.g., MIT) to a `LICENSE` file.
