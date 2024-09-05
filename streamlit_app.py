import streamlit as st
import os
import replicate
import webbrowser
import requests
import json
from youtubesearchpython import VideosSearch

# Set your OpenAI API key

# Function to display assistant messages
def say(text):
    st.write(f"Assistant: {text}")
# Chatbot function using Replicate LLM
def chatbot(prompt_input):
    pre_prompt = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
    
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
   
    # Generate LLM response
    output = replicate.run(
        'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
        input={"prompt": f"{pre_prompt} {prompt_input} Assistant: ", "temperature": 0.1, "top_p": 0.9, "max_length": 128, "repetition_penalty": 1}
    )
    
    # Combine output into a full response
    full_response = ""
    for item in output:
        full_response += item
    say(full_response)
    return full_response

# Open Website Function
def open_website(site_name, site_url):
    say(f"Opening {site_name}...")
    webbrowser.open(site_url)

# Play Music Function
def open_music(music_name):
    say(f"Playing {music_name} song...")
    results = VideosSearch(music_name, limit=1).result()
    try:
        if results and len(results) > 0:
            video_url = f"https://www.youtube.com/results?search_query={music_name}" 
            webbrowser.open(video_url)
        else:
            st.write("No search results found for the given music name.")
    except Exception as e:
        st.write(f"Error: {e}")

# Search Function
def search(search_query):
    say("Searching Google...")
    search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    webbrowser.open(search_url)

# Weather Function
def weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key=43fb152c1e584163b64162705231507&q={city}"
    try:
        response = requests.get(url)
        weather_data = json.loads(response.text)
        temp_c = weather_data["current"]["temp_c"]
        temp_f = weather_data["current"]["temp_f"]
        condition = weather_data["current"]["condition"]["text"]
        last_updated = weather_data["current"]["last_updated"]
        say(f"In {city}, the temperature is {temp_c}°C ({temp_f}°F), and the weather condition is {condition}. Last updated: {last_updated}.")
    except Exception as e:
        say(f"Couldn't retrieve weather information: {e}")

# Process command function
def process_command(command):
    if "play" in command:
        music_name = command.split("play", 1)[1].strip()
        open_music(music_name)
    elif "open" in command:
        site_name = command.split("open", 1)[1].strip()
        if site_name.lower() == "youtube":
            open_website("YouTube", "https://www.youtube.com/")
        elif site_name.lower() == "linkedin":
            open_website("LinkedIn", "https://www.linkedin.com/")
        # Add more sites as needed
    elif "search" in command:
        search_query = command.split("search", 1)[1].strip()
        search(search_query)
    elif "the weather of" in command:
        city = command.split("weather of", 1)[1].strip()
        weather(city)
    else:
        chatbot(command)

# Main Streamlit logic
def main():
    st.title("AI Assistant with Command Features")
    
    # Add a sidebar for navigation and information
    with st.sidebar:
        st.header("Available Commands")
        st.markdown("""
        - **Play music**: Type `play [song name]` to play a song from YouTube.
        - **Open websites**: Type `open [website]` (YouTube, LinkedIn, etc.).
        - **Search Google**: Type `search [query]` to perform a Google search.
        - **Check the weather**: Type `the weather of [city]` to get the current weather.
        - **Chat with Assistant**: Type any question or statement to interact with the assistant.
        """)
        st.write("Try one of the commands in the input box below!")

    # Command input
    user_input = st.text_input("Enter your command here:")

    if user_input:
        process_command(user_input)




if __name__ == "__main__":
    main()

