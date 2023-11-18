from pystray import Icon, Menu, MenuItem
from PIL import Image
from server import *
from multiprocessing import Process

class TrayMenu:
    def __init__(self):
        self.VAstate = "Start"
        self.image = Image.open("src/images/icon.png")
        self.menu = Menu(MenuItem('Settings', self.openSettings),
                         MenuItem('Start \ Stop', self.start_stopVA),
                         MenuItem('Quit', self.on_quit))

        self.icon = Icon("name", self.image, menu=self.menu)


    def start_stopVA(self, icon, item):
        self.changeState()
        print('VA ' + self.VAstate + 'ed')

    def changeState(self):
        if self.VAstate == "Start":
            self.VAstate == "Stop"
        else:
            self.VAstate == "Start"

    def openSettings(self, icon, item):
        print(f'Start server')
        server_process = Process(target=run_server)
        server_process.start()
        open_browser()
        time.sleep(300)
        server_process.terminate()
        server_process.join()

        print("Server Stoped")

    def on_quit(self, icon, item):
        icon.stop()

    def run(self):
        self.icon.run()

tray_menu = TrayMenu()


def startTray():
    trayProcess = Process(target=tray_menu.run())
    process.start()
    process.join()






