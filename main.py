from trayMenu import startTray
from multiprocessing import Process


# creating tray icon to control voice assistant
if __name__ == '__main__':
     tray_process = Process(target=startTray)
     tray_process.start()

