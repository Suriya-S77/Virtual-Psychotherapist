import speech_recognition as sr
import pyttsx3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

# Initialize models and services
analyzer = SentimentIntensityAnalyzer()

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the speaking rate
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Adjust for different voices if needed

# Doctor's info
doctor_name = "Dr. Jeevaa"
doctor_phone = "6380372501"

def speak(text):
    """
    Convert text to speech.
    """
    print(f"Speaking: {text}")  # Ensure you can see the output before speech
    engine.say(text)
    engine.runAndWait()

def listen():
    """
    Listen to user input via microphone and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"You: {user_input}")
            return user_input
        except sr.UnknownValueError:
            speak("I'm sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            speak("Sorry, there seems to be an issue with the speech recognition service.")
            return None

def analyze_sentiment(text):
    """
    Analyze the sentiment of the input text.
    Returns a sentiment score and emotion label (Positive, Negative, Neutral).
    """
    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        emotion = "Positive"
    elif sentiment['compound'] <= -0.05:
        emotion = "Negative"
    else:
        emotion = "Neutral"
    return sentiment['compound'], emotion

def predefined_response(emotion):
    """
    Return predefined responses based on the sentiment.
    """
    if emotion == "Positive":
        return "That's great to hear! I'm really happy you're feeling good."
    elif emotion == "Neutral":
        return "I hear you. Sometimes things are just okay, and that's perfectly fine."
    elif emotion == "Negative":
        return "It seems you are feeling sad. I can help you schedule a call with Dr. Jeevaa."
    
def schedule_call():
    """
    Schedule a call with the doctor if the user is sad.
    """
    speak(f"It seems you are feeling sad. I can help you schedule a call with a Doctor.")
    time.sleep(2)  # Pause to let the speech complete
    speak(f"Please call {doctor_name} at {doctor_phone}. Feel free to reach out for support.")

def virtual_psychotherapist_voice():
    """
    Main function to simulate a voice-enabled virtual psychotherapist conversation loop.
    """
    speak("Hi! I'm your virtual psychotherapist. How can I help you today?")
    while True:
        user_input = listen()
        if user_input is None:
            continue
        if user_input.lower() in ["exit", "quit", "bye"]:
            speak("It was nice talking to you. Take care!")
            break
        
        # Step 1: Analyze sentiment
        sentiment_score, emotion = analyze_sentiment(user_input)
        print(f"Sentiment Analysis: {emotion} (Score: {sentiment_score})")
        
        # Step 2: Respond based on the sentiment
        bot_response = predefined_response(emotion)
        
        # If sentiment is negative, schedule a call
        if emotion == "Negative":
            schedule_call()
        
        print(f"Virtual Psychotherapist: {bot_response}")
        speak(bot_response)

# Run the voice-enabled psychotherapist chatbot
virtual_psychotherapist_voice()
