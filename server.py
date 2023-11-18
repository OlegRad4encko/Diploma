import json
import asyncio
from SettingsManager import SettingsManager, settings_manager
from flask import Flask, send_file, render_template, url_for, request
import webbrowser
from multiprocessing import Process, Value, Lock
import re
import os
import time
import sys
import signal
import logging
from default_config_assistant import last_request_time


# configs of VA assistant ==============================================================================================
settings_manager.load_settings()
current_settings = settings_manager.get_setting('CURRENT_SETTINGS', {})
assistant_cmd_list = settings_manager.get_setting('ASSISTANT_CMD_LIST', {})
assistant_alias = settings_manager.get_setting('ASSISTANT_ALIAS', {})
assistant_stt = settings_manager.get_setting('ASSISTANT_STT', {})
assistant_tts = settings_manager.get_setting('ASSISTANT_TTS', {})
assistant_tra = settings_manager.get_setting('ASSISTANT_TRA', {})



# config for local web server ==========================================================================================
web_config = ''
with open('web_config.json', 'r') as file:
    web_config = json.load(file)


last_request_time = time.time()

# web Server
app = Flask(__name__, template_folder='web')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# functions ============================================================================================================

# run server
def run_server():
    open_browser()
    app.run(host=web_config['host'], port=web_config['port'], threaded=True, processes=1, use_reloader=False)

def change_last_request_time():
    current_settings['LAST_REQUEST'] = time.time()
    settings_manager.set_setting('CURRENT_SETTINGS', current_settings)
    settings_manager.save_settings()

def get_last_request_time():
    settings_manager.load_settings()
    return settings_manager.get_setting('CURRENT_SETTINGS', {})['LAST_REQUEST']

def stop_server(**kwargs):
    server_inactive_live = web_config['server_inactive_live']
    server_last_answer = web_config['server_last_answer']
    server_process = kwargs.get("server_process")

    if server_inactive_live <= server_last_answer:
        server_inactive_live = 300
        server_last_answer = 100

    change_last_request_time()
    while True:
        elapsed_time = time.time() - get_last_request_time()
        if elapsed_time > server_inactive_live:
            os.kill(server_process, signal.SIGTERM)
            print("Server Stopped")
            break
        time.sleep(server_last_answer)



# check string on latin symbols only
def is_latin_only(input_string):
    return bool(re.match("^[a-zA-Z]+$", input_string))


# check string on the correct link path
def if_link(input_string):
    url_pattern = re.compile(r'(https?://|ftp://|file://|http://localhost:|http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?/)(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+(?::\d+)?(?:/[^\s]*)?')
    return bool(url_pattern.match(input_string))


# check string on the folder path
def if_folder_path(input_string):
    return bool(input_string and input_string[1:3] == ":\\" and not input_string.endswith('\\') and '.' not in input_string)


# check string on the executable file path
def if_executable(input_string):
    return bool(
        input_string and
        input_string[1:3] == ":\\" and
        not input_string.endswith('\\') and
        '.' in input_string and
        input_string.lower().endswith(('.exe', '.bat', '.cmd'))
    )

# open browser with home page
def open_browser(destination: str = ''):
    webbrowser.open('http://'+str(web_config['host'])+':'+str(web_config['port'])+'/'+destination)


# endpoints ============================================================================================================

# home page
@app.route('/', methods=['GET', 'POST'])
def serve_html():
    change_last_request_time()

    # handler
    if request.method == 'POST':
        current_settings['ASSISTANT_TTS'] = request.form.get('ttsLang')
        current_settings['ASSISTANT_STT'] = request.form.get('sttLang')
        current_settings['ASSISTANT_TRA'] = request.form.get('transLang')

        message_type = 'info'
        message_text = "Збережено"
        return render_template('index.html', assistant_stt=assistant_stt, assistant_tts=assistant_tts,
            assistant_tra=assistant_tra, current_settings=current_settings,
            message_type=message_type, message_text=message_text)


    return render_template('index.html', assistant_stt=assistant_stt, assistant_tts=assistant_tts,
        assistant_tra=assistant_tra, current_settings=current_settings)



# other settings page
@app.route('/other_settings', methods=['GET', 'POST'])
def other_settings():
    change_last_request_time()

    # handler
    if request.method == 'POST':
        if request.form.get('SpeakTheAnswer') == None:
            current_settings['SPEAK_THE_ANSWER'] = "False"
        else:
            current_settings['SPEAK_THE_ANSWER'] = "True"
        if request.form.get('IsQuickAnswer') == None:
            current_settings['IS_QUICK_ANSWER'] = "False"
        else:
            current_settings['IS_QUICK_ANSWER'] = "True"

        settings_manager.set_setting('CURRENT_SETTINGS', current_settings)
        settings_manager.save_settings()

        message_type = 'info'
        message_text = "Збережено"
        return render_template('otherSettings.html', current_settings=current_settings,
            message_type=message_type, message_text=message_text)

    return render_template('otherSettings.html', current_settings=current_settings)



# add languages page
@app.route('/add_languages')
def add_languages():
    change_last_request_time()
    return render_template('addLanguages.html')



# add speech to text language page
@app.route('/add_stt_language', methods=['GET', 'POST'])
def add_stt_language():
    change_last_request_time()

    # handler
    if request.method == 'POST':
        if request.form.get('label') == '' or request.form.get('key') == '' or request.form.get('model') == '':
            message_type = 'error'
            message_text = "Заповніть всі поля"
            return render_template('addSTTLanguage.html',
                message_type=message_type, message_text=message_text, label=request.form.get('label'),
                key=request.form.get('key'), model=request.form.get('model'))

        if request.form.get('key') not in default_config.ISO_639_1:
            message_type = 'error'
            message_text = "Двох символьний код мови невірний, ознайомтесь з стандартом"
            return render_template('addSTTLanguage.html',
                message_type=message_type, message_text=message_text, label=request.form.get('label'),
                key=request.form.get('key'), model=request.form.get('model'))

        if os.path.exists(os.path.join(os.getcwd(), "models_stt//"+request.form.get('model'))) == False:
            message_type = 'error'
            message_text = "Модель з ім'ям '"+request.form.get('model')+"' відсутня в теці 'models_stt' в корні проекту"
            return render_template('addSTTLanguage.html',
                message_type=message_type, message_text=message_text, label=request.form.get('label'),
                key=request.form.get('key'), model=request.form.get('model'))

        key = request.form.get('key')
        model = request.form.get('model')
        label = request.form.get('label')

        assistant_stt[key] = {
            "model": model,
            "label": label
        }


        settings_manager.set_setting('ASSISTANT_STT', assistant_stt)
        settings_manager.save_settings()

        message_type = 'info'
        message_text = "Додано мову розпізнавання тексту"
        return render_template('addSTTLanguage.html',
            message_type=message_type, message_text=message_text)

    return render_template('addSTTLanguage.html')



# add text to speach language page
@app.route('/add_tts_language', methods=['GET', 'POST'])
def add_tss_language():
    change_last_request_time()

    # handler
    if request.method == 'POST':
        if request.form.get('label') == '' or request.form.get('key') == '' or request.form.get('id_model') == '' or request.form.get('speaker') == '':
            message_type = 'error'
            message_text = "Заповніть всі поля"
            return render_template('addTTSLanguage.html',
                message_type=message_type, message_text=message_text,
                label=request.form.get('label'), key=request.form.get('key'),
                id_model=request.form.get('id_model'), speaker=request.form.get('speaker'))

        if request.form.get('key') not in default_config.ISO_639_1:
            message_type = 'error'
            message_text = "Двох символьний код мови невірний, ознайомтесь з стандартом"
            return render_template('addTTSLanguage.html',
                message_type=message_type, message_text=message_text,
                label=request.form.get('label'), key=request.form.get('key'),
                id_model=request.form.get('id_model'), speaker=request.form.get('speaker'))


        key = request.form.get('key')
        label = request.form.get('label')
        model_id = request.form.get('id_model')
        sample_rate = 48000
        speaker = request.form.get('speaker')

        assistant_tts[key] = {
            "label": label,
            "language": key,
            "model_id": model_id,
            "sample_rate": sample_rate,
            "speaker": speaker
        }

        settings_manager.set_setting('ASSISTANT_TTS', assistant_tts)
        settings_manager.save_settings()

        message_type = 'info'
        message_text = "Додано мову генерації голосу"
        return render_template('addSTTLanguage.html',
            message_type=message_type, message_text=message_text)

    return render_template('addTTSLanguage.html')



# add translate language page
@app.route('/add_translate_language', methods=['GET', 'POST'])
def add_translate_language():
    change_last_request_time()

    # handler
    if request.method == 'POST':
        if request.form.get('label') == '' or request.form.get('key') == '':
            message_type = 'error'
            message_text = "Заповніть всі поля"
            return render_template('addTranslateLanguage.html',
                message_type=message_type, message_text=message_text,
                label=request.form.get('label'), key=request.form.get('key'))

        if request.form.get('key') not in default_config.ISO_639_1:
            message_type = 'error'
            message_text = "Двох символьний код мови невірний, ознайомтесь з стандартом"
            return render_template('addTranslateLanguage.html',
                message_type=message_type, message_text=message_text,
                label=request.form.get('label'), key=request.form.get('key'))

        key = request.form.get('key')
        label = request.form.get('label')

        assistant_tra[key] = {
            "label": label,
            "lang": key
        }

        settings_manager.set_setting('ASSISTANT_TRA', assistant_tra)
        settings_manager.save_settings()

        message_type = 'info'
        message_text = "Додано мову перекладу тексту"
        return render_template('addSTTLanguage.html',
            message_type=message_type, message_text=message_text)

    return render_template('addTranslateLanguage.html')



# commands list page
@app.route('/commands_list', methods=['GET', 'POST'])
def commands_list():
    change_last_request_time()

    # handler
    if request.method == 'POST':

        # edit command render
        if request.form.get('command_edit') != None:
            word_list = [word.strip() for word in assistant_cmd_list[request.form.get('command_edit')]['word_list']]
            word_list_str = ', '.join(word_list)

            return render_template('commandEdit.html', command_edit=request.form.get('command_edit'),
                assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str,
                commandType=assistant_cmd_list[request.form.get('command_edit')]['commandType'],
                customCommand=assistant_cmd_list[request.form.get('command_edit')]['customCommand'])


        # edit command handler
        if request.form.get('edit') == 'pass':
            if request.form.get('key') == '' or request.form.get('word_list') == '' or request.form.get('customCommand') == '':
                message_type = 'error'
                message_text = 'Будь-ласка, заповніть всі поля!'
                word_list = [word.strip() for word in assistant_cmd_list[request.form.get('key')]['word_list']]
                word_list_str = ', '.join(word_list)


                return render_template('commandEdit.html', message_type=message_type, command_edit=request.form.get('key'),
                    message_text=message_text, assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str,
                    customCommand=request.form.get('customCommand'), commandType=request.form.get('commandType'))


            if is_latin_only(request.form.get('key')) == False:
                message_type = 'error'
                message_text = 'Будь-ласка, введіть назву команди англійською без пробілів!'
                word_list = [word.strip() for word in assistant_cmd_list[request.form.get('key')]['word_list']]
                word_list_str = ', '.join(word_list)

                return render_template('commandEdit.html', message_type=message_type, command_edit=request.form.get('key'),
                    message_text=message_text, assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str,
                    customCommand=request.form.get('customCommand'), commandType=request.form.get('commandType'))

            if assistant_cmd_list[request.form.get('key')]['isCustom'] == 'True':
                if request.form.get('commandType') == 'None':
                    message_type = 'error'
                    message_text = 'Будь-ласка, виберіть тип команди'
                    word_list = [word.strip() for word in assistant_cmd_list[request.form.get('key')]['word_list']]
                    word_list_str = ', '.join(word_list)

                    return render_template('commandEdit.html', message_type=message_type, command_edit=request.form.get('key'),
                        message_text=message_text, assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str,
                        customCommand=request.form.get('customCommand'), commandType=request.form.get('commandType'))


                if if_link(request.form.get('customCommand')) == False and request.form.get('commandType') == 'openWebPage':
                    message_type = 'error'
                    message_text = "Це не посилання"
                    word_list = [word.strip() for word in assistant_cmd_list[request.form.get('key')]['word_list']]
                    word_list_str = ', '.join(word_list)

                    return render_template('commandEdit.html', message_type=message_type, command_edit=request.form.get('key'),
                        message_text=message_text, assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str,
                        customCommand=request.form.get('customCommand'), commandType=request.form.get('commandType'))

                else:
                    if if_folder_path(request.form.get('customCommand')) == False and request.form.get('commandType') == 'explorer':
                        message_type = 'error'
                        message_text = "Не шлях до теки"
                        word_list = [word.strip() for word in assistant_cmd_list[request.form.get('key')]['word_list']]
                        word_list_str = ', '.join(word_list)

                        return render_template('commandEdit.html', message_type=message_type, command_edit=request.form.get('key'),
                            message_text=message_text, assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str,
                            customCommand=request.form.get('customCommand'), commandType=request.form.get('commandType'))
                    else:
                        if if_executable(request.form.get('customCommand')) == False and request.form.get('commandType') == 'execute':
                            message_type = 'error'
                            message_text = "Не шлях до виконавчого файлу"
                            word_list = [word.strip() for word in assistant_cmd_list[request.form.get('key')]['word_list']]
                            word_list_str = ', '.join(word_list)

                            return render_template('commandEdit.html', message_type=message_type, command_edit=request.form.get('key'),
                                message_text=message_text, assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str,
                                customCommand=request.form.get('customCommand'), commandType=request.form.get('commandType'))


            key = request.form.get('key')
            words_string = request.form.get('word_list')
            word_list = [word.strip() for word in words_string.split(',')]


            if assistant_cmd_list[key]['can_delete'] == "False" and assistant_cmd_list[key]['isCustom'] == "False":
                assistant_cmd_list[key] = {
                    "word_list": word_list,
                    "can_delete": "False",
                    "isCustom": "False",
                    "commandType": "None",
                    "customCommand": ""
                }
            else:
                commandType = request.form.get('commandType')
                customCommand = request.form.get('customCommand')
                assistant_cmd_list[key] = {
                    "word_list": word_list,
                    "can_delete": "True",
                    "isCustom": "True",
                    "commandType": commandType,
                    "customCommand": customCommand
                }

            settings_manager.set_setting('ASSISTANT_CMD_LIST', assistant_cmd_list)
            settings_manager.save_settings()

            message_type = 'info'
            message_text = "Данні збережено"
            return render_template('commandEdit.html', message_type=message_type, command_edit=request.form.get('key'),
                            message_text=message_text, assistant_cmd_list=assistant_cmd_list, word_list_str=words_string,
                            customCommand=assistant_cmd_list[key]['customCommand'],
                            commandType=assistant_cmd_list[key]['commandType'])


        # delete command handler
        if request.form.get('command_delete') != None:
            settings_manager.delete_setting_from_key('ASSISTANT_CMD_LIST', request.form.get('command_delete'))

            message_type = 'info'
            message_text = "Команду видалено"
            return render_template('commandsList.html', assistant_cmd_list=assistant_cmd_list,
                message_type=message_type, message_text=message_text)


    return render_template('commandsList.html', assistant_cmd_list=assistant_cmd_list)



# edit command page
@app.route('/command_edit', methods=['GET', 'POST'])
def command_edit():
    change_last_request_time()

    return render_template('commandsList.html', assistant_cmd_list=assistant_cmd_list)



# add command page
@app.route('/add_command', methods=['GET', 'POST'])
def add_command():
    global last_request_time
    last_request_time = time.time()

    # handler
    if request.method == 'POST':
        if request.form.get('key') == '' or request.form.get('word_list') == '' or request.form.get('customCommand') == '':
            message_type = 'error'
            message_text = 'Будь-ласка, заповніть всі поля!'
            return render_template('addCommand.html', message_type=message_type,
                message_text=message_text, key=request.form.get('key'), word_list=request.form.get('word_list'),
                commandType=request.form.get('commandType'), customCommand=request.form.get('customCommand'))


        if is_latin_only(request.form.get('key')) == False:
            message_type = 'error'
            message_text = 'Будь-ласка, введіть назву команди англійською без пробілів!'
            return render_template('addCommand.html', message_type=message_type,
                message_text=message_text, key=request.form.get('key'), word_list=request.form.get('word_list'),
                commandType=request.form.get('commandType'), customCommand=request.form.get('customCommand'))


        if request.form.get('commandType') == 'None':
            message_type = 'error'
            message_text = 'Будь-ласка, виберіть тип команди'
            return render_template('addCommand.html', message_type=message_type,
                message_text=message_text, key=request.form.get('key'), word_list=request.form.get('word_list'),
                commandType=request.form.get('commandType'), customCommand=request.form.get('customCommand'))


        if if_link(request.form.get('customCommand')) == False and request.form.get('commandType') == 'openWebPage':
            message_type = 'error'
            message_text = "Це не посилання"
            return render_template('addCommand.html', message_type=message_type,
                message_text=message_text, key=request.form.get('key'), word_list=request.form.get('word_list'),
                commandType=request.form.get('commandType'), customCommand=request.form.get('customCommand'))
        else:
            if if_folder_path(request.form.get('customCommand')) == False and request.form.get('commandType') == 'explorer':
                message_type = 'error'
                message_text = "Не шлях до теки"
                return render_template('addCommand.html', message_type=message_type,
                    message_text=message_text, key=request.form.get('key'), word_list=request.form.get('word_list'),
                    commandType=request.form.get('commandType'), customCommand=request.form.get('customCommand'))
            else:
                if if_executable(request.form.get('customCommand')) == False and request.form.get('commandType') == 'execute':
                    message_type = 'error'
                    message_text = "Не шлях до виконавчого файлу"
                    return render_template('addCommand.html', message_type=message_type,
                        message_text=message_text, key=request.form.get('key'), word_list=request.form.get('word_list'),
                        commandType=request.form.get('commandType'), customCommand=request.form.get('customCommand'))



        key = request.form.get('key')
        word_list = [word.strip() for word in request.form.get('word_list').split(',')]
        commandType = request.form.get('commandType')
        customCommand = request.form.get('customCommand')
        assistant_cmd_list[key] = {
            "word_list": word_list,
            "can_delete": "True",
            "isCustom": "True",
            "commandType": commandType,
            "customCommand": customCommand
        }

        settings_manager.set_setting('ASSISTANT_CMD_LIST', assistant_cmd_list)
        settings_manager.save_settings()

        message_type = 'info'
        message_text = "Команду додано!"
        return render_template('addCommand.html', message_type=message_type, message_text=message_text)

    return render_template('addCommand.html')



# VA names page
@app.route('/voice_assistant_names', methods=['GET', 'POST'])
def voice_assistant_names():
    change_last_request_time()

    # handler
    if request.method == 'POST':

        # deleting name
        if request.form.get('delete_name') != None:
            if request.form.get('delete_name') not in assistant_alias:
                message_type = 'error'
                message_text = 'Помилка при імені видаленні. <br> Спробуйте ще раз!'
                return render_template('VANames.html', message_type=message_type,
                    message_text=message_text, assistant_alias=assistant_alias, new_name=request.form.get('new_name'))


            settings_manager.delete_value_from_key('ASSISTANT_ALIAS', request.form.get('delete_name'))
            message_type = 'info'
            message_text = "Ім'я голосого асистента видалено"
            return render_template('VANames.html', message_type=message_type,
                message_text=message_text, assistant_alias=assistant_alias, new_name=request.form.get('new_name'))


        # adding new name
        if request.form.get('add_name') == 'add_name':
            if request.form.get('new_name') == '':
                message_type = 'error'
                message_text = "Введіть ім'я!"
                return render_template('VANames.html', message_type=message_type,
                    message_text=message_text, assistant_alias=assistant_alias, new_name=request.form.get('new_name'))

            if request.form.get('new_name') not in assistant_alias:
                assistant_alias.append(request.form.get('new_name'))
                settings_manager.set_setting('ASSISTANT_ALIAS', assistant_alias)
                settings_manager.save_settings()
                message_type = 'info'
                message_text = "Ім'я успішно додане"
                return render_template('VANames.html', message_type=message_type,
                    message_text=message_text, assistant_alias=assistant_alias)

            message_type = 'error'
            message_text = "Таке і'мя вже присутнє! <br> Придумайте нове."
            return render_template('VANames.html', message_type=message_type,
                message_text=message_text, assistant_alias=assistant_alias, new_name=request.form.get('new_name'))

    return render_template('VANames.html', assistant_alias=assistant_alias)



# load styles to page
@app.route('/src/styles.css')
def serve_css():
    change_last_request_time()

    return send_file('src/styles.css', mimetype='text/css')
