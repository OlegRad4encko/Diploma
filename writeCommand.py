from multiprocessing import Process
import vosk
import sys
import sounddevice as sd
import queue
import json
import tkinter as tk
import time
import pygetwindow as gw
import pyautogui
import keyboard


# the queue
q = queue.Queue()


# getting active window title
def get_active_window_title():
    active_window = gw.getActiveWindow()
    return active_window.title if active_window else None


# pasting text to active window
def paste_to_active_window(text:str):
    active_window_title = get_active_window_title()
    keyboard.write(text)


# stop callback to tkinder window
def stop_callback(root: tk):
    root.result = "stop"
    root.destroy()


# run tkinder window
def run_window():
    root = tk.Tk()
    root.title("Зупинити")
    root.geometry("200x100")
    root.resizable(width=False, height=False)
    root.protocol("WM_DELETE_WINDOW", lambda: stop_callback(root))
    stop_button = tk.Button(root, text="Stop", command=lambda: stop_callback(root), width=10, height=2)
    stop_button.pack(pady=20)
    root.mainloop()
    final_result = root.result
    return final_result


# the function processes the input string and returns the result without or with a space
def write(voice: str, result: str):
    if voice != '':
        if result == '':
            result = voice
            return result
        else:
            result = " "+voice
            return result
    return ''


# This callback function when recording audio
def query_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    q.put(bytes(indata))


# function data flow handler from the "vosk" model
def listen_write(stt_model):
    model = vosk.Model('models_stt/' + stt_model)
    sample_rate = 16000
    block_size = 8000
    device = 1
    d_type = 'int16'
    channels = 1
    result = ''

    try:
        with sd.RawInputStream(samplerate=sample_rate, blocksize=block_size, device=device, dtype=d_type, channels=channels,
                           callback=query_callback):
            rec = vosk.KaldiRecognizer(model, sample_rate)

            window_process = Process(target=run_window)
            window_process.start()

            while window_process.is_alive():
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = write(json.loads(rec.Result())["text"], result)
                    paste_to_active_window(result)

    except(KeyboardInterrupt):
        sys.exit(0)


