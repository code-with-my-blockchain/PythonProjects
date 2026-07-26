import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

l = ["Arslan", "Awais", "Ali"]

for name in l:
    speaker.Speak(f"Shoutout to {name}")