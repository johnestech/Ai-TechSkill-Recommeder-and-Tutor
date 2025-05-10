import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model congiguration
model_config = {
    "temperature": 1.2,
    "top_k": 64,
    "top_p":0.84,
    "max_output_tokens": 9600
}

# Model initialization
meyi_model = genai.GenerativeModel(
    model_name= "gemini-2.0-flash",
    generation_config=model_config
)

def chat_with_model():
    """Initialize the chat on streamlit"""

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat" not in st.session_state:
        system_prompt = """Your name is Meyi built and trained by John'es.
        John'es is a Machine learning and AI engineer/tutor.
        You're a tech expert and tutor.
        You're to help people begin thier tech journey, most of which are completely beginners and have no technical knowledge.
        Never refer to questions you havent actually asked in the current conversation.
        Always start fresh with each user interaction.
        You're to use very simple terms to help them understand.
        If they are not sure what tech skill to learn, ask them several questions (at least 8) to get to understand thier realworld interest and recommed the best tech skill to them.
        If they have a tech skill or pick one, you're to begin from the very basic with step by step instructions and guide on it.
        You're an expert teach them like they only depend on you.
        Do not answer any non-tech related questions.
        Do not say anything about who built and trained you except you are asked.
        When asked about John'es, do not say anything more than what you know about him.
        Be very professional and educative."""

        st.session_state.chat = meyi_model.start_chat(history=[
            {
                "role": "user",
                "parts": [system_prompt]
            }
        ])


def clean_response(text):
    """Clean HTML text such as div tags etc."""
    clean_text = re.sub(r'</?div>|<[^>]*>', '', text)
    clean_text = clean_text.replace('</div>', '')
    clean_text = clean_text.replace('<div>', '')

    clean_text = clean_text.strip()
    return clean_text


def app_run():
    """main function to run streamlit app"""

    st.set_page_config()

    st.markdown("""
        <style>
        /* Main container */
        .main {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        /* Chat flow container */
        div[data-testid="stChatFlow"] {
            max-width: 1000px !important;
            margin: 0 auto !important;
            padding: 1.5rem !important;
        }
        /* Column layout */
        div[data-testid="column"] {
            padding: 0.5rem 1rem !important;
        }
        /* Chat message base styling */
        div.stChatMessage {
            width: fit-content !important;
            min-width: 120px !important;
            max-width: 80% !important;
            margin: 0.75rem 0 !important;
            padding: 0 !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
        }
        /* Message content container */
        div[data-testid="stChatMessageContent"] {
            padding: 0.875rem 1.25rem !important;
            margin: 0 !important;
            line-height: 1.5 !important;
        }
        /* User message specific styling (dark grey like WhatsApp) */
        .stChatMessage.user-message {
            background-color: #23272a !important;
            color: #fff !important;
            border-radius: 10px 10px 10px 10px !important;
            margin-left: auto !important;
            padding: 10px !important;
            margin-right: 20px !important;
        }
        /* Assistant message specific styling (blue like Messenger) */
        .stChatMessage.assistant-message {
            background-color: #0084ff !important;
            color: #fff !important;
            border-radius: 10px 10px 10px 10px !important;
            margin-right: auto !important;
            padding: 10px !important;
            margin-left: 10px !important;
        }
        /* Message text */
        div[data-testid="stMarkdownContainer"] p {
            color: white !important;
            margin: 0 !important;
        }
        /* Avatar customization */
        .stChatMessage [data-testid="stImage"] {
            width: 12px !important;
            height: 12px !important;
            margin: 0 0.75rem !important;
            border-radius: 20% !important;
        }
        /* Title and description styling */
        h1 {
            margin-bottom: 1rem !important;
            padding: 1rem !important;
        }
        .stMarkdown p {
            padding: 0 1rem !important;
            margin-bottom: 2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("'MEYI' Your AI powered tech tutor/skill recommender")
    st.write('Want to begin your tech journey, advance on your current knowledge or unsure on what tech skill to learn. Meyi got you covered, ask any question you have.')

    chat_with_model()
    for message in st.session_state.messages:
        role, content = message
        if role == "user":
            st.markdown(
                f'<div style="display:flex;flex-direction:row-reverse;align-items:flex-start;width:100%;">'
                f'<div style="min-width:36px;text-align:center;">'
                f'<span style="font-size:1.5rem;">👨🏾‍💻</span>'
                f'</div>'
                f'<div class="stChatMessage user-message" style="background:#23272a;color:#fff;border-radius:18px 18px 0 18px;margin-left:auto;margin-right:0;">'
                f'{content}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div style="display:flex;align-items:flex-start;gap:0;width:100%;">'
                f'<div style="min-width:36px;text-align:center;">'
                f'<span style="font-size:1.5em;">🤖</span>'
                f'</div>'
                f'<div class="stChatMessage assistant-message" style="background:#0084ff;color:#fff;border-radius:18px 18px 18px 0;padding:0.875rem 1.25rem;max-width:80%;margin-right:auto;margin-left:0;">'
                f'{content}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # Chat input
    user_input = st.chat_input("Ask anything tech...")
    
    if user_input:
        st.session_state.messages.append(("user", user_input))
        try:
            with st.spinner("Thinking..."):
                response = st.session_state.chat.send_message(user_input)
                if response and response.text:
                    cleaned_response = clean_response(response.text)
                    st.session_state.messages.append(("assistant", cleaned_response))
                    st.rerun()
        except Exception as e:
            st.error(f"An Error occurred: {str(e)}")

if __name__ == "__main__":
    app_run()