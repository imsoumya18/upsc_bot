from datetime import datetime, date, time, timedelta

TOKEN = 'TOKEN(str)'  # Bot Token
DEVELOPER_ID = 'DEVELOPER_ID(int)'  # Your Own ID
DEVELOPER_PRIVATE_CHANNEL = 'DEVELOPER_PRIVATE_CHANNEL_ID(int)'  # Developer's Private Channel ID
DEVELOPER_SEND_CHANNEL = 'DEVELOPER_SEND_CHANNEL_ID(int)'  # Developer's Send Channel ID
REQUEST_CHANNEL = 'ADD_REQUESTS_CHANNEL_ID(int)'  # Add Requests Channel
COUNTDOWN_CHANNEL = 'COUNTDOWN_CHANNEL_ID(int)'  # Countdown Channel ID
THE_HINDU_CHANNELS = ['LIST OF THE HINDU CHANNEL IDS(int)']  # The Hindu Channel IDs
VISION_IAS_CHANNELS = ['LIST OF VISION IAS CHANNEL IDS(int)']  # Vision IAS Channel IDs
NEXT_IAS_CHANNELS = ['LIST OF NEXT IAS CHANNEL IDS(int)']  # Next IAS Channel IDs
INSIGHTS_IAS_CHANNELS = ['LIST OF INSIGHTS IAS CHANNEL IDS(int)']  # Insights IAS Channel IDs
WHEN = (datetime.combine(date.today(), time(8, 00, 00)) + timedelta(hours=-5, minutes=-30)).time()  # IST Time
