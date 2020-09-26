import pyttsx3
import datetime
import speech_recognition as sr
import random
import wikipedia
from gtts import gTTS
import os
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello I am Cookie. How may I assist you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said : {query}\n")
    except Exception as e:
        print("Pardon me, please say that again")
        return "None"
    return query


def wakeWord(text):
    WAKE_WORDS = ['hey cookie', 'cookie']
    text = text.lower()
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    return False


def greeting(text):
    # Greeting Inputs
    GREETING_INPUTS = ['hi', 'hey', 'hola', 'greetings', 'wassup', 'hello']

    # Greeting Response back to the user
    GREETING_RESPONSES = ['whats good', 'hello',
                          'hey there', 'hi', 'hey', 'hola']

    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    return ''


def assistantResponse(text):
    print(text)
    # Convert the text to speech
    speak(text)


if __name__ == "__main__":

    while True:
        # Checking for the wake word/phrase
        query = takeCommand()
        response = ''
        if (wakeWord(query) == True):
            # Check for greetings by the user
            response = response + greeting(query)
            assistantResponse(response)
            response = greeting(query)
            assistantResponse(response)
