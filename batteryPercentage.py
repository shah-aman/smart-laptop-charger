import psutil
import time
import pyttsx3
from win10toast import ToastNotifier # also need to install win32api
import threading

toaster = ToastNotifier()
jarvis=pyttsx3.init()
jarvis.setProperty('rate',130)
jarvis.setProperty('volume',8)
count = 0

def show_notification(show_text):
   toaster.show_toast(show_text,
                       icon_path='battery_indicator.ico',
                       duration=10)
   # loop the toaster over some period of time
   while toaster.notification_active():
      time.sleep(0.1)

def monitor():
   while (True):
      time.sleep(10)
      battery = psutil.sensors_battery()
      plugged = battery.power_plugged
      percent = int(battery.percent)
      
      if percent < 40:
         if plugged == False:
            processThread = threading.Thread(target=show_notification, args=("Your Battery at "+str(percent)+"% Please plug the cable",))  # <- note extra ','
            processThread.start()
            jarvis.say("Your battery is getting low so charge it right now")
            jarvis.runAndWait()
            count = 0
      elif percent == 100:
         if plugged == True:
            processThread = threading.Thread(target=show_notification, args=("Charging is getting complete",))  # <- note extra ','
            processThread.start()
            jarvis.say("Charging is getting complete")
            jarvis.runAndWait()
      elif percent == 90:
         if plugged == True:
            if count == 0:
               processThread = threading.Thread(target=show_notification, args=("Your Battery at 90% Please plug out the cable",))  # <- note extra ','
               processThread.start()
               jarvis.say("Your battery at 90% ")
               jarvis.runAndWait()
               count = count + 1

if __name__ == "__main__":
   monitor()
