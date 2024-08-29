import requests
import playsound
import os
import random
from rich import Union

def generate_audio(message: str, voice: str = "Matthew"):
    url = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except:
        return None

def Speak(message: str, voice: str = "Brian", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    try:
        result_content = generate_audio(message, voice)
        file_path = os.path.join(folder, f"{voice}{extension}")
        with open(file_path, "wb") as file:
            file.write(result_content)
        playsound.playsound(file_path)
        os.remove(file_path)
        return None
    except Exception as e:
        return "Error playing TTS: " + str(e)

def TTS(Text):
    Data = str(Text).split(".")
    responses = ["The rest of the result has been printed to the chat screen, kindly check it out sir.",
                 "The rest of the text is now on the chat screen, sir, please check it.",
                 "You can see the rest of the text on the chat screen, sir.",
                 "The remaining part of the text is now on the chat screen, sir.",
                 "Sir, you'll find more text on the chat screen for you to see.",
                 "The rest of the answer is now on the chat screen, sir.",
                 "Sir, please look at the chat screen, the rest of the answer is there.",
                 "You'll find the complete answer on the chat screen, sir.",
                 "The next part of the text is on the chat screen, sir.",
                 "Sir, please check the chat screen for more information.",
                 "There's more text on the chat screen for you, sir.",
                 "Sir, take a look at the chat screen for additional text.",
                 "You'll find more to read on the chat screen, sir.",
                 "Sir, check the chat screen for the rest of the text.",
                 "The chat screen has the rest of the text, sir.",
                 "There's more to see on the chat screen, sir, please look.",
                 "Sir, the chat screen holds the continuation of the text.",
                 "You'll find the complete answer on the chat screen, kindly check it out sir.",
                 "Please review the chat screen for the rest of the text, sir.",
                 "Sir, look at the chat screen for the complete answer."]
    
    if len(Data) > 4 and len(Text) >= 250:
        Speak(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses))
    else:
        Speak(Text)

if __name__ == "__main__":
    TTS("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.")
