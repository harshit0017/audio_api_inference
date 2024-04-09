import streamlit as st
import requests
from uuid import uuid4

# Function to fetch audio response from the API
def get_audio(text):
    url = 'http://34.42.153.11:5000/infer'
    try:
        response = requests.post(url, json={'text': text})
        data = response.json()
        return data.get('output_audio_url')
    except Exception as e:
        st.error(f'Error fetching audio response: {e}')
        return None

def main():
    st.title('Audio Test Room')

    # Initialize messages list
    messages = []

    # Text input for user's message
    text_input = st.text_input('Enter your message:')

    # Submit button to send message
    submit_button = st.button('Submit')

    # If submit button is clicked and text input is not empty
    if submit_button and text_input:
        # Add user's message to the messages list
        new_message = {'id': str(uuid4()), 'sender': 'Human', 'data': text_input}
        messages.append(new_message)

        # Fetch audio response from the API
        audio_url = get_audio(text_input)

        # If audio response is available, add it to the messages list
        if audio_url:
            new_message = {'id': str(uuid4()), 'sender': 'Bot', 'data': audio_url}
            messages.append(new_message)

    # Display the chat messages
    chat_container = st.empty()

    for message in messages:
        if message['sender'] == 'Human':
            # Display user's message
            chat_container.write(f'You: {message["data"]}', unsafe_allow_html=True)
        elif message['sender'] == 'Bot':
            # Display audio response from the bot
            st.audio(message['data'], format='audio/mp3')

    # Add some CSS styling to improve the visual appearance
    st.markdown(
        """
        <style>
            .stApp {
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }
            .stTextInput {
                width: calc(100% - 100px);
                margin-right: 10px;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    main()
