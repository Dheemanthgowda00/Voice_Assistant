import tkinter as tk
from tkinter import messagebox
import threading
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use female voice, if available

def talk(text):
    """Convert text to speech, display animated text, and apply color vibration effect."""
    add_message(text, animate=True, vibrate=True)
    engine.say(text)
    engine.runAndWait()

def add_message(text, animate=False, vibrate=False):
    """Add message to the GUI output box with optional animation and vibration effects."""
    if animate:
        typewriter_effect(text, vibrate)
    else:
        output_box.insert(tk.END, text + '\n')
        output_box.see(tk.END)

def typewriter_effect(text, vibrate=False):
    """Display text with a typewriter effect and optional color vibration."""
    for char in text:
        output_box.insert(tk.END, char)
        output_box.update()
        if vibrate:
            output_box.tag_configure("vibrate", foreground="red")
            output_box.tag_add("vibrate", "end-1c", "end")
            main_window.after(100, lambda: output_box.tag_configure("vibrate", foreground="blue"))
        time.sleep(0.05)  # Adjust speed for typing effect
    output_box.insert(tk.END, '\n')
    output_box.see(tk.END)

def listen_for_hotword():
    """Wait until it hears 'alexa' and show a listening animation."""
    add_message("Waiting for hotword 'Alexa'...", animate=True)
    show_listening_animation(True)
    while True:
        try:
            with sr.Microphone(device_index=2) as source:
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source, timeout=5)
                command = listener.recognize_google(voice).lower()
                if 'alexa' in command:
                    show_listening_animation(False)
                    talk("Yes?")
                    return
        except sr.UnknownValueError:
            pass  # Ignore unrecognized input
        except sr.RequestError:
            talk("Sorry, my speech service is down.")
        except Exception as e:
            add_message(f"Error: {e}")

def take_command():
    """Listens for and returns a command after hearing the hotword."""
    try:
        show_listening_animation(True)
        with sr.Microphone(device_index=2) as source:
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice).lower()
            add_message(f"Command: {command}", animate=True)
            return command
    except sr.UnknownValueError:
        talk("Sorry, I did not catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        return ""
    except Exception as e:
        add_message(f"Error: {e}")
        return ""
    finally:
        show_listening_animation(False)

def run_robo():
    """Process commands after hotword activation."""
    command = take_command()

    if 'play' in command:
        song = command.replace('play', '')
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'The current time is {current_time}')

    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        try:
            info = wikipedia.summary(person, sentences=1)
            add_message(info, animate=True)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk("I couldn't find information on that person. Please try again.")
        except wikipedia.exceptions.DisambiguationError as e:
            talk("That name is too ambiguous. Please be more specific.")
        except Exception as e:
            add_message(f"Error: {e}")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        add_message(joke, animate=True)
        talk(joke)

    elif 'search for' in command:
        search_term = command.replace('search for', '')
        talk(f'Searching for {search_term}')
        pywhatkit.search(search_term)

    else:
        talk("I'm not sure about that. Please try again.")

def start_assistant_thread():
    """Starts the assistant in a separate thread."""
    threading.Thread(target=start_assistant, daemon=True).start()

def start_assistant():
    """Listen for hotword and run the assistant continuously."""
    while True:
        listen_for_hotword()
        run_robo()

def show_listening_animation(active):
    """Show or hide the listening animation (pulsing circle)."""
    if active:
        pulse_circle.pack(pady=10)
        pulse_circle.after(100, lambda: pulse_circle.config(bg="green"))
        pulse_circle.after(200, lambda: pulse_circle.config(bg="lightgreen"))
    else:
        pulse_circle.pack_forget()

# GUI for the login page
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "password":  # Replace with your desired credentials
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Incorrect Username or Password")

def open_main_window():
    global main_window, output_box, pulse_circle

    # Main Window
    main_window = tk.Tk()
    main_window.title("Voice Assistant")
    main_window.geometry("800x600")  # Increased window size for better visibility

    output_box = tk.Text(main_window, wrap=tk.WORD, height=25, width=70, font=("Helvetica", 12))
    output_box.pack(pady=20)

    pulse_circle = tk.Label(main_window, text="Listening...", font=("Helvetica", 16), bg="lightgreen", width=10, height=5)
    pulse_circle.pack_forget()  # Initially hidden

    start_button = tk.Button(main_window, text="Start Assistant", command=start_assistant_thread, font=("Helvetica", 14))
    start_button.pack(pady=10)

    main_window.mainloop()

# Login Window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username", font=("Helvetica", 12)).pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password", font=("Helvetica", 12)).pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=login, font=("Helvetica", 12))
login_button.pack(pady=20)

login_window.mainloop()
