import streamlit as st
import requests
import base64

# ----------------------------
# 🌤️ Weather App — Custom Backgrounds (PNG)
# ----------------------------

# Set page title and layout
st.set_page_config(page_title="Weather App", layout="centered")
st.title("🌤️ Weather App")

# ----------------------------
# User input
# ----------------------------
city = st.text_input("Enter a city name:")

# Dictionary linking main weather conditions to local PNG images
weather_backgrounds = {
    "Clear": "images/clear.png",
    "Clouds": "images/clouds.png",
    "Rain": "images/rain.png",
    "Drizzle": "images/drizzle.png",
    "Thunderstorm": "images/thunderstorm.png",
    "Snow": "images/snow.png",
    "Mist": "images/mist.png"
}

# ----------------------------
# Helper function to set local background
# ----------------------------
def set_bg_local(image_file):
    # Open image and encode in base64
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    # Inject CSS to set background
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# Button triggers the API request
# ----------------------------
if st.button("Get Weather"):

    # Build the API URL
    api_key = st.secrets["api_key"]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

    try:
        # API request
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract weather info
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description'].capitalize()
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        # ----------------------------
        # Set background image based on main weather
        # ----------------------------
        main_weather = data['weather'][0]['main']
        background_file = weather_backgrounds.get(main_weather, None)
        if background_file:
            set_bg_local(background_file)

        # ----------------------------
        # Display weather information in columns
        # ----------------------------
        st.subheader(f"Weather in {city}")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(icon_url)
        with col2:
            st.write(f"**Temperature:** {temp}°F")
            st.write(f"**Feels like:** {feels_like}°F")
            st.write(f"**Description:** {description}")

    # ----------------------------
    # Error handling
    # ----------------------------
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            st.error("City not found. Try again!")
        elif response.status_code == 401:
            st.error("API key error. Check your key!")
        else:
            st.error(f"HTTP error: {response.status_code}")
    except requests.exceptions.RequestException as err:
        st.error(f"Network error occurred: {err}")
    except KeyError as err:
        st.error(f"Unexpected response format: missing key {err}")
