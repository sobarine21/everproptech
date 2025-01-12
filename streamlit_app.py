import streamlit as st
import requests
import google.generativeai as genai

# Configure the AI API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Weather and AQI API keys
WEATHER_API_KEY = 'your_openweathermap_api_key'
AQI_API_KEY = 'your_aqicn_api_key'
GEMINI_API_KEY = 'your_gemini_api_key'

# Function to fetch weather data
def get_weather(location):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data['weather'][0]['description'], data['main']['temp']
    else:
        return None, None

# Function to fetch AQI data
def get_aqi(location):
    url = f'http://api.waqi.info/feed/{location}/?token={AQI_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data['status'] == 'ok':
        return data['data']['aqi']
    else:
        return None

# Function to fetch property data from Gemini AI (simplified)
def get_properties_from_gemini():
    url = 'https://api.gemini.com/v1/properties'  # Replace with the real endpoint
    headers = {'Authorization': f'Bearer {GEMINI_API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Example response: list of properties
    else:
        return []

# Streamlit App UI
st.title("Real Estate Assistant with AI, Weather, and AQI")
st.write("Get real estate recommendations along with environmental insights.")

# Input for location
location = st.text_input("Enter a location for property search:")

# Fetch weather and AQI data
if location:
    weather_desc, weather_temp = get_weather(location)
    aqi = get_aqi(location)

    # Display weather and AQI data
    if weather_desc and weather_temp:
        st.write(f"Weather in {location}: {weather_desc}, Temperature: {weather_temp}°C")
    else:
        st.write("Could not fetch weather data for the location.")

    if aqi:
        st.write(f"AQI (Air Quality Index) in {location}: {aqi}")
    else:
        st.write("Could not fetch AQI data for the location.")

# Fetch and display real estate properties
properties = get_properties_from_gemini()

if properties:
    st.write(f"Found {len(properties)} properties matching your criteria:")
    for prop in properties:
        st.write(f"Property Name: {prop['name']}")
        st.write(f"Price: {prop['price']}")
        st.write(f"Location: {prop['location']}")
        st.write("---")
else:
    st.write("No properties found.")

# AI Section: Input and Generate Response
st.write("### Ask AI for Real Estate Advice or Other Information")
prompt = st.text_input("Enter your prompt:", "What are the best places to invest in real estate?")

if st.button("Generate Response"):
    try:
        # Load and configure the AI model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model
        response = model.generate_content(prompt)
        
        # Display the AI response
        st.write("AI Response:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")

# Optionally, you can integrate a map here using streamlit-folium or other visualization tools
