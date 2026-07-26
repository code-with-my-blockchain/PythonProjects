import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

while 1:
    print("Enter the word you want to speak it out")
    s = input()
    speaker.Speak(s)
import win32com.client

l = ["Rahul", "Nishant", "Ali", "Awais"]

speaker = win32com.client.Dispatch("SAPI.SpVoice")

for name in l:
    speaker.Speak(f"Shoutout to {name}")  
    import os

l = ["Rahul", "Nishant", "Ali", "AwaisAli"]

for name in l:
    os.system(f"say Shoutout to {name}") 