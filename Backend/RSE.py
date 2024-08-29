import os
from winotify import Notification, audio
from os import getcwd

def Alert(Text):
    icon_path = r"C:\Users\my pc\Downloads\Search\OneDrive\Desktop\CODEMAN--BD\JARVIS-RE-J4E\images.jpeg"

    toast = Notification(
        app_id="Jarvis",
        title=Text,
        duration="long",
        icon=icon_path
    )

    toast.set_audio(audio.SMS, loop=False)



    toast.show()
    
# Alert("SIR YOUR HORNY GIRL AI IS READY SIR!!")    