import speech_recognition as sr
import openai
import pyttsx3
from openai import OpenAI

client = #YOUR API KEY

def get_ai_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            store=True
        )

        print("Response from OpenAI:")
        response = completion.choices[0].message.content
        return response.strip()

    except Exception as e:
        return f"Error during API call: {e}"


def listen_to():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        recognizer.energy_threshold = 100

        print("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing audio...")

            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            print("No speech detected. Try again.")
        except sr.UnknownValueError:
            print("Sorry, couldn't understand.")
        except sr.RequestError:
            print("Could not connect to Google API. Check your internet.")


def speak_response(response):
    """
    Use pyttsx3 to convert text response to speech and play it.
    """
    engine = pyttsx3.init()  # Correct initialization
    engine.say(response)
    engine.runAndWait()
    engine.setProperty('rate', 150)

if __name__ == "__main__":
    print("Please provide the code.>")

    code_input = ""
    print("Type your code here:")

    while True:
        line=input()
        if not line:
                break
        code_input += line + "\n"

    print("Your code is:")
    print(code_input)

    print("\nListening for your command...")
    voice_command = listen_to()

    if voice_command:
        if "fix" in voice_command or "debug" in voice_command or "correct" in voice_command:

            prompt = f"The following code might have issues: \n{code_input}\nPlease fix it and return the corrected version."

            openai_response = get_ai_response(prompt)

            print(f"OpenAI response: {openai_response}")

            speak_response(openai_response)

        elif "analyze" in voice_command or "check" in voice_command:
            prompt = f"Please analyze the following code: \n{code_input}\nWhat are the possible issues?"

            openai_response = get_ai_response(prompt)

            print(f"AI analysis: {openai_response}")

            speak_response(openai_response)


        else:

         print("Sorry, I didn't understand that command. Please try again.")

         speak_response("I didn't understand the command. Please try again.")

    else:

     print("No valid voice input detected, continuing to listen...")

     