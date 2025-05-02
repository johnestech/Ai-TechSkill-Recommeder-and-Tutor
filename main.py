import os
import google.generativeai as genai
from dotenv import load_dotenv
import urllib.request

def check_internet_connection():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=3)
        return True
    except:
        return False

if check_internet_connection():
    load_dotenv()

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Model configuration
    model_config = {
        "temperature":0.13,
        "top_k": 63,
        "top_p": 0.64,
        "max_output_tokens": 8500,
        "response_mime_type": "text/plain",
    }

    # Initiate model
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=model_config
    )

    chat_model = model.start_chat()

    # First message as system instruction 
    chat_model.send_message(
        "Your name is Meyi built and trained by John'es."
        "John'es is a Machine learning and AI engineer/tutor."
        "You're a tech expert and tutor."
        "You're to help people begin thier tech journey, most of which are completely beginners and have no technical knowledge."
        "Never refer to questions you havent actually asked in the current conversation."
        "Always start fresh with each user interaction."
        "You're to use very simple terms to help them understand."
        "If they are not sure what tech skill to learn, ask them several questions (at least 8) to get to understand thier realworld interest and recommed the best tech skill to them."
        "If they have a tech skill or pick one, you're to begin from the very basic with step by step instructions and guide on it."
        "You're an expert teach them like they only depend on you."
        "Do not answer any non-tech related questions."
        "When asked about John'es, do not say anything more than what you know about him."
        "Be very professional and simple."
    )

    def recommender_and_tutor():
        """Recommeder and tutor function"""
        
        print("Hi dear, i am Meyi your Tech skill tutor and recommender, do you want to learn a tech skill or you're confused about which tech skill to begin? I am here to help. (Type 'exit' to close end chat)")
        while True:
            user_input = input('\nYou:')
            if user_input.lower() == "exit":
                print("Exiting chat... Goodbye!")
                break
            try:
                model_response = chat_model.send_message(user_input)
                print(f"Meyi: {model_response.text}")
            
            except Exception as e:
                print(f"Unfortunately an error occured: {e}")

if __name__ == "__main__":
    if check_internet_connection():
        try:
            recommender_and_tutor()
        except KeyboardInterrupt:
            print("!Exiting chat... Goodbye!")
    else:
        print("No internet connection! Please check your connection and try again.")