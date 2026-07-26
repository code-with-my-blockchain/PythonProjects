import os
import time
from plyer import notification

if __name__ == "__main__":
    while True:
        notification.notify(
            title = "Please Drink Water Now!!",
            message = "The National Academies of Sciences, Engineering, and Medicine determines that an adequate daily fluid intake is: About 15.5 cups (3.7 liters) of fluids for men. About 11.5 cups (2.7 liters) of fluids a day for women.",
            app_icon = None,
            timeout = 10
        )
        # time.sleep(60*60) # Remind every hour
        time.sleep(10) # Testing for every 10 seconds