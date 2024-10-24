import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use female voice, if available

def talk(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen_for_hotword():
    """Waits until it hears 'alexa'."""
    while True:
        try:
            with sr.Microphone(device_index=2) as source:
                listener.adjust_for_ambient_noise(source)
                print("Waiting for hotword 'Alexa'...")
                voice = listener.listen(source, timeout=5)
                command = listener.recognize_google(voice).lower()
                if 'alexa' in command:
                    talk("Yes?")
                    return  # Exit and proceed to next command
        except sr.UnknownValueError:
            pass  # Ignore unrecognized input
        except sr.RequestError:
            talk("Sorry, my speech service is down.")
        except Exception as e:
            print("Error")

def take_command():
    """Listens for and returns a command after hearing the hotword."""
    try:
        with sr.Microphone(device_index=2) as source:
            listener.adjust_for_ambient_noise(source)
            print("Listening for a command...")
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice).lower()
            print(f"Command: {command}")
            return command
    except sr.UnknownValueError:
        talk("Sorry, I did not catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

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
            print(info)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk("I couldn't find information on that person. Please try again.")
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"That name is too ambiguous. Please be more specific. Some options are: {e.options[:3]}")
        except Exception as e:
            talk(f"An error occurred:")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'search for' in command:
        search_term = command.replace('search for', '')
        talk(f'Searching for {search_term}')
        pywhatkit.search(search_term)

    else:
        talk("I'm not sure about that. Please try again.")

# Main loop to wait for hotword and execute commands
while True:
    listen_for_hotword()
    run_robo()
