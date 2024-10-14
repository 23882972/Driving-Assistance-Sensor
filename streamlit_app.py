import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# CSV file raw URL from GitHub
GITHUB_CSV_URL = 'https://raw.githubusercontent.com/23882972/Driving-Assistance-Sensor/refs/heads/main/sensor_data.csv'

def read_web_csv(url=GITHUB_CSV_URL):
    # Fetch the CSV file from the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the CSV file into a pandas DataFrame
        csv_data = StringIO(response.text)
        return pd.read_csv(csv_data)  # Return DataFrame directly
    else:
        raise Exception(f"Failed to retrieve CSV file. Status code: {response.status_code}")

# Load CSV
df = read_web_csv()

if df is not None:
    # Show the data in the app
    st.write("Data Overview:")
    # First 6 rows with headers
    st.write(df.head())
    # Select menu for image of the driver
    selected_image = st.selectbox('Select a time of an image:', df['Timestamp'])
    image_path = f'https://raw.githubusercontent.com/23882972/Driving-Assistance-Sensor/main/photos/{selected_image}.jpg'
    st.image(image_path, caption="Image of the driver during the buzzer", use_column_width=True)
    # First line graph of time against acceleration
    fig = px.line(df, x='Timestamp', y='Total_Acceleration', title='Line Graph of Time against Acceleration of buzzer')
    st.plotly_chart(fig)
    
