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

    # st.markdown(
    #     """
    #     <script>
    #         document.addEventListener('keydown', function(e) {
    #             if (e.key === 'Enter' && e.shiftKey) {
    #                 e.preventDefault();
    #                 return false;
    #             }
    #         });
    #     </script>
    #     """,
    #     unsafe_allow_html=True
    # )
    
    st.markdown(
        """
        <style>
        [data-testid="stChatInput"] {
            bottom: 0 !important;
            padding: 1rem !important;
            z-index: 999 !important;
        }
        
        section[data-testid="stChatFlow"] > div:last-child {
            margin-bottom: 0px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("'MEYI' Your AI powered tech tutor/skill recommender")
    st.write('Want to begin your tech journey, advance on your current knowledge or unsure on what tech skill to learn. Meyi got you covered, ask any question you have.')

    
    chat_with_model()
    
    
    for message in st.session_state.messages:
        role, content = message
        if role == "user":
            st.chat_message("user", avatar="👨🏾‍💻").write(content)
        else:
            st.chat_message("assistant", avatar="🤖").write(content)

    
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