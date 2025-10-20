import pyttsx3
import pyautogui
import speech_recognition as sr
import os
import webbrowser
import time
from datetime import datetime

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 175)
TODO_FILE = "todo_list.txt"

# ---------------- Voice + Speech Functions ----------------
def speak(text):
    print("DeskBot:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for voice command and return as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)
        return query.lower()
    except:
        return ""

# ---------------- Helper Functions ----------------
def get_time():
    return datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.now().strftime("%A, %d %B %Y")

def add_todo(task):
    with open(TODO_FILE, "a") as f:
        f.write(task + "\n")
    speak("Task added to your to-do list.")

def read_todo():
    if not os.path.exists(TODO_FILE):
        speak("Your to-do list is empty.")
        return
    with open(TODO_FILE, "r") as f:
        tasks = f.readlines()
    if tasks:
        speak("Here’s your to-do list:")
        for t in tasks:
            speak(t.strip())
    else:
        speak("Your to-do list is empty.")

def clear_todo():
    if os.path.exists(TODO_FILE):
        os.remove(TODO_FILE)
    speak("All tasks cleared.")

# ---------------- Core Assistant ----------------
def deskbot():
    speak("DeskBot is running. Say 'Hey DeskBot' to wake me up.")

    while True:
        command = take_command()

        if "hey deskbot" in command:
            speak("Hello Monika, how can I help you?")
            
            while True:
                query = take_command()
                if query == "":
                    continue

                # Open Applications
                if "open notepad" in query:
                    os.system("notepad")
                    speak("Opening Notepad")

                elif "open chrome" in query:
                    os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
                    speak("Opening Chrome")

                elif "open youtube" in query:
                    webbrowser.open("https://www.youtube.com")
                    speak("Opening YouTube")

                # Date & Time
                elif "time" in query:
                    speak(f"The current time is {get_time()}")

                elif "date" in query:
                    speak(f"Today is {get_date()}")

                # Screenshot
                elif "screenshot" in query:
                    img = pyautogui.screenshot()
                    img.save("deskbot_screenshot.png")
                    speak("Screenshot taken and saved.")

                # To-Do List
                elif "add task" in query or "add to do" in query:
                    speak("What task should I add?")
                    task = take_command()
                    add_todo(task)

                elif "show tasks" in query or "read to do" in query:
                    read_todo()

                elif "clear tasks" in query:
                    clear_todo()

                # Exit
                elif "sleep" in query or "exit" in query or "stop" in query:
                    speak("Okay, going back to sleep.")
                    break

                time.sleep(1)

# ---------------- Run ----------------
if __name__ == "__main__":
    deskbot()
