import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import pyttsx3

chatStr = ""

engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Anant: {query}\nJarvis: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["text"]
        say(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        error_message = "Sorry, I couldn't process the request."
        say(error_message)
        return error_message

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["text"]
        text += response_text
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print("Error during OpenAI API call:", e)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Error during speech recognition:", e)
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [
            ["youtube", "https://www.youtube.com"], 
            ["wikipedia", "https://www.wikipedia.com"], 
            ["google", "https://www.google.com"]
        ]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "open music" in query.lower():
            musicPath = "C:/Users/Anant Lad/Downloads/downfall-21371.mp3"
            os.system(f"start {musicPath}")
        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes")
        elif "open facetime" in query.lower():
            os.system("start /System/Applications/FaceTime.app")
        elif "open pass" in query.lower():
            os.system("start /Applications/Passky.app")
        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)
        elif "jarvis" in query.lower():
            say("Goodbye sir.")
            break
        elif "reset chat" in query.lower():
            chatStr = ""
        else:
            print("Chatting...")
            chat(query)

