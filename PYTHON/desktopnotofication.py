from plyer import notification
import pyttsx3
import time

def drink_water_notification():
 
    engine = pyttsx3.init()
    
   
    msg = "Hey Ali, please drink water now!"

    while True:
       
        notification.notify(
            title="Drink Water",
            message=msg,
            app_name="Water Reminder",
            timeout=10
        )
        
       
        engine.say(msg)
        engine.runAndWait()
        
    
        time.sleep(3600)

if __name__ == "__main__":
    drink_water_notification()