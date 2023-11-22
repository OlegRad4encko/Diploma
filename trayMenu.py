from pystray import Icon, Menu, MenuItem
from PIL import Image
from server import run_server, stop_server, open_browser
from multiprocessing import Process
from commandProcessor import run_command_processor
from notificationModule import show_notification
import time

class TrayMenu:
    # init object
    def __init__(self):
        self.VAstate = "Stop"
        self.image = Image.open("src/images/icon.png")
        self.menu = Menu(MenuItem('Settings', self.openSettings),
                         MenuItem('Start \ Stop', self.start_stopVA),
                         MenuItem('Quit', self.on_quit))

        self.icon = Icon("name", self.image, menu=self.menu)
        self.server_process = None
        self.server_stopper = None
        self.command_process = None

        show_notification("Голосовий помічник","Увімкніть прослуховування голосу")


    # start\stop action handler
    def start_stopVA(self):
        self.changeState()
        if self.VAstate == "Start":
            self.command_process = Process(target=run_command_processor)
            self.command_process.start()
        else:
            self.command_process.terminate()
            self.command_process.join()
            show_notification("Голосовий помічник","Ваш голос більше не слухається")


    #change state method
    def changeState(self):
        if self.VAstate == "Start":
            self.VAstate = "Stop"
        else:
            self.VAstate = "Start"


    # open setting action handler
    def openSettings(self):
        if self.server_process == None and self.server_stopper == None:
            self.server_process = Process(target=run_server)
            self.server_process.start()
            server_pid = self.server_process.pid
            self.server_stopper = Process(target=stop_server, kwargs = {"server_process":server_pid})
            self.server_stopper.start()
            return 1

        if self.server_process.is_alive() and self.server_stopper.is_alive():
            open_browser()
            return 1
        else:
            self.server_process = None
            self.server_stopper = None
            self.openSettings()


    # quit action handler
    def on_quit(self, icon):
        if self.server_process != None:
            if self.server_process.is_alive():
                self.server_process.terminate()
                self.server_process.join()
        if self.server_stopper != None:
            if self.server_stopper.is_alive():
                self.server_stopper.terminate()
                self.server_stopper.join()
        if self.command_process != None:
            if self.command_process.is_alive():
                self.command_process.terminate()
                self.command_process.join()

        icon.stop()


    # run icon
    def run(self):
        self.icon.run()



# creating Tray object and run it
def startTray():
    tray_menu = TrayMenu()
    tray_menu.run()



