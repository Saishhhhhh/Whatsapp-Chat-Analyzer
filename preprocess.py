import pandas as pd
import re

def create_dataframe_from_file(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    content = bytes_data.decode("utf-8")
    # Normalize narrow/non-breaking spaces that may precede am/pm
    content = content.replace('\u202f', ' ').replace('\xa0', ' ')
    
    # Support optional AM/PM (e.g., "11:40 am - ")
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s*[apAP][mM])?\s-\s'
    messages = re.split(pattern, content)[1:]

    dates = re.findall(pattern, content)

    df = pd.DataFrame({'user_message': messages, 'date': dates})
    
    # Robust parser: try 24h and 12h formats (2- or 4-digit years), fallback to inference
    def parse_date_str(date_str: str):
        s = date_str.replace('\u202f', ' ').replace('\xa0', ' ')
        s = re.sub(r'(\d{1,2}:\d{2})\s*([ap]m)\b',
                   lambda m: f"{m.group(1)} {m.group(2).upper()}", s, flags=re.IGNORECASE)
        for fmt in (
            '%d/%m/%Y, %H:%M - ',
            '%d/%m/%y, %H:%M - ',
            '%d/%m/%Y, %I:%M %p - ',
            '%d/%m/%y, %I:%M %p - ',
        ):
            try:
                return pd.to_datetime(s, format=fmt)
            except ValueError:
                continue
        return pd.to_datetime(s, dayfirst=True, errors='coerce')

    df['date'] = df['date'].apply(parse_date_str)

    users = []
    messages = []

    for msg in df['user_message']:
        if ":" in msg:
            users.append(msg.split(":", 1)[0])     # username
            messages.append(msg.split(":", 1)[1].strip())  # message text
        else:
            users.append(None)      # or "System"
            messages.append(msg.strip())

    df['user'] = users
    df['messages'] = messages
    df.drop(columns = ['user_message'], inplace = True)

    df.dropna(inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    df['word_count'] = df['messages'].str.split().str.len()

    df.drop(columns = ['date'], inplace=True)
    df.rename(columns={'only_date':'date'}, inplace=True)

    df.reset_index(drop = True, inplace = True)

    return df