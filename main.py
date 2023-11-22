from trayMenu import startTray
from multiprocessing import Process
from multiprocessing import Process, freeze_support
import time

freeze_support()

# creating tray icon to control voice assistant
if __name__ == '__main__':
     tray_process = Process(target=startTray)
     tray_process.start()
     tray_process.join()



# pyinstaller --onefile --add-data ".\venv\Lib\site-packages\vosk;./vosk" --add-data "web;web" --hidden-import tkinter --hidden-import plyer.platforms.win.notification  main.py
# pyinstaller --onefile --add-data ".\venv\Lib\site-packages\vosk;./vosk" --add-data "web;web" --hidden-import tkinter --hidden-import plyer.platforms.win.notification --noconsole  main.py



