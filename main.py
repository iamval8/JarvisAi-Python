import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Set up OpenAI and speech modules
import openai
openai.api_key = OPENAI_KEY
r = sr.Recognizer()

def SpeakText(command):
   """Converts text to speech."""
   engine = pyttsx3.init()
   engine.say(command)
   engine.runAndWait()

def record_text():
   """Records spoken input from the microphone."""
   try:
       with sr.Microphone() as source:
           r.adjust_for_ambient_noise(source, duration=0.2)
           print("I'm Listening...")
           audio = r.listen(source)
           text = r.recognize_google(audio)
           print(f"Recognized: {text}")
           return text
   except sr.RequestError as e:
       print(f"Could not request results; {e}")
   except sr.UnknownValueError:
       print("I did not understand that.")
   except Exception as e:
       print(f"An error occurred: {e}")
   return None


def send_to_chatGPT(messages):
   """Sends messages to ChatGPT and returns the response."""
   try:
       # Limiting the number of messages to avoid exceeding token limits
       if len(messages) > 10:  # You can adjust this number based on your needs
           messages = messages[-10:]  # Keep only the last 10 interactions

       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=messages,
           max_tokens=1500  # Reduced max_tokens
       )
       content = response['choices'][0]['message']['content']
       messages.append({"role": "system", "content": content})
       return content
   except Exception as e:
       print(f"Failed to send message to ChatGPT: {e}")
       return "Error connecting to AI."
# Main loop
messages = [{"role": "system", "content": "Hello! I am your assistant. How can I help you today?"}]
SpeakText(messages[-1]["content"])  # Speak the initial message

while True:
   try:
       text = record_text()
       if text is None or text.lower() == 'exit':  # Adding a simple exit command
           print("Exiting...")
           break

       if text:
           messages.append({"role": "user", "content": text})
           response = send_to_chatGPT(messages)
           SpeakText(response)
           print(response)
       else:
           SpeakText("Please say that again.")
   except KeyboardInterrupt:
       print("Interrupted by user, exiting...")
       break
