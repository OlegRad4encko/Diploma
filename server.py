import json
import asyncio
from SettingsManager import SettingsManager
from flask import Flask, send_file, render_template, url_for, request
import webbrowser
import threading
import re



# configs of VA assistant
settings_manager = SettingsManager()
settings_manager.load_settings()
assistant_stt = settings_manager.get_setting('ASSISTANT_STT', {})
assistant_tts = settings_manager.get_setting('ASSISTANT_TTS', {})
assistant_tra = settings_manager.get_setting('ASSISTANT_TRA', {})
current_settings = settings_manager.get_setting('CURRENT_SETTINGS', {})
assistant_cmd_list = settings_manager.get_setting('ASSISTANT_CMD_LIST', {})
assistant_alias = settings_manager.get_setting('ASSISTANT_ALIAS', {})



# config for local web server
web_config = ''
with open('web_config.json', 'r') as file:
    web_config = json.load(file)


# functions
def is_latin_only(input_string):
    return bool(re.match("^[a-zA-Z]+$", input_string))



# web Server
app = Flask(__name__, template_folder='web')



# home page
@app.route('/', methods=['GET', 'POST'])
def serve_html():
    # handler
    if request.method == 'POST':
        current_settings['ASSISTANT_TTS'] = request.form.get('ttsLang')
        current_settings['ASSISTANT_STT'] = request.form.get('sttLang')
        current_settings['ASSISTANT_TRA'] = request.form.get('transLang')

        settings_manager.set_setting('CURRENT_SETTINGS', current_settings)
        settings_manager.save_settings()

    return render_template('index.html', assistant_stt=assistant_stt,
        assistant_tts=assistant_tts,
        assistant_tra=assistant_tra,
        current_settings=current_settings)



# other settings page
@app.route('/other_settings', methods=['GET', 'POST'])
def other_settings():
    # handler
    if request.method == 'POST':
        if request.form.get('SpeakTheAnswer') == None:
            current_settings['SPEAK_THE_ANSWER'] = False
        else:
            current_settings['SPEAK_THE_ANSWER'] = True
        if request.form.get('IsQuickAnswer') == None:
            current_settings['IS_QUICK_ANSWER'] = False
        else:
            current_settings['IS_QUICK_ANSWER'] = True

        settings_manager.set_setting('CURRENT_SETTINGS', current_settings)
        settings_manager.save_settings()

    return render_template('otherSettings.html', current_settings=current_settings)



# add languages page
@app.route('/add_languages')
def add_languages():
    return render_template('addLanguages.html')



# add speech to text language page
@app.route('/add_stt_language', methods=['GET', 'POST'])
def add_stt_language():
    # handler
    if request.method == 'POST':
        if request.form.get('label') != '' and request.form.get('key') != '' and request.form.get('model') != '':
            key = request.form.get('key')
            model = request.form.get('model')
            label = request.form.get('label')

            assistant_stt[key] = {
                "model": model,
                "label": label
            }

            settings_manager.set_setting('ASSISTANT_STT', assistant_stt)
            settings_manager.save_settings()

    return render_template('addSTTLanguage.html')



# add text to speach language page
@app.route('/add_tts_language', methods=['GET', 'POST'])
def add_tss_language():
    # handler
    if request.method == 'POST':
        if request.form.get('label') != '' and request.form.get('key') != '' and request.form.get('id_model') != '' and request.form.get('speaker') != '':
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

    return render_template('addTTSLanguage.html')



# add translate language page
@app.route('/add_translate_language', methods=['GET', 'POST'])
def add_translate_language():
    # handler
    if request.method == 'POST':
        if request.form.get('label') != '' and request.form.get('key') != '':
            key = request.form.get('key')
            label = request.form.get('label')

            assistant_tra[key] = {
                "label": label,
                "lang": key
            }
            settings_manager.set_setting('ASSISTANT_TRA', assistant_tra)
            settings_manager.save_settings()

    return render_template('addTranslateLanguage.html')



# commands list page
@app.route('/commands_list', methods=['GET', 'POST'])
def commands_list():
    # handler
    if request.method == 'POST':

        # edit command render
        if request.form.get('command_edit') != None:
            word_list = [word.strip() for word in assistant_cmd_list[request.form.get('command_edit')]['word_list']]
            word_list_str = ', '.join(word_list)

            return render_template('commandEdit.html', command_edit=request.form.get('command_edit'), assistant_cmd_list=assistant_cmd_list, word_list_str=word_list_str)

        # edit command handler
        if request.form.get('edit') == 'pass':
            if request.form.get('key') != None and request.form.get('word_list') != None:
                key = request.form.get('key')
                words_string = request.form.get('word_list')
                word_list = [word.strip() for word in words_string.split(',')]

                if assistant_cmd_list[key]['can_delete'] == "False":
                    assistant_cmd_list[key] = {
                        "word_list": word_list,
                        "can_delete": "False"
                    }
                else:
                    assistant_cmd_list[key] = {
                        "word_list": word_list,
                        "can_delete": "True"
                    }

                settings_manager.set_setting('ASSISTANT_CMD_LIST', assistant_cmd_list)
                settings_manager.save_settings()


        # delete command handler
        if request.form.get('command_delete') != None:
               settings_manager.delete_setting_from_key('ASSISTANT_CMD_LIST', request.form.get('command_delete'))


    return render_template('commandsList.html', assistant_cmd_list=assistant_cmd_list)



# edit command page
@app.route('/command_edit', methods=['GET', 'POST'])
def command_edit():
    return render_template('commandsList.html', assistant_cmd_list=assistant_cmd_list)



# add command page
@app.route('/add_command', methods=['GET', 'POST'])
def add_command():
    # handler
    if request.method == 'POST':
        if request.form.get('key') != '' and request.form.get('word_list') != '':
            if is_latin_only(request.form.get('key')):
                key = request.form.get('key')
                word_list = [word.strip() for word in request.form.get('word_list').split(',')]
                assistant_cmd_list[key] = {
                    "word_list": word_list,
                    "can_delete": "True"
                }

                settings_manager.set_setting('ASSISTANT_CMD_LIST', assistant_cmd_list)
                settings_manager.save_settings()

            else:
                message_type = 'latin_error'
                message_text = 'Будь-ласка, введіть назву команди англійською без пробілів!'
                return render_template('addCommand.html', message_type=message_type, message_text=message_text)

        else:
            message_type = 'fields_error'
            message_text = 'Будь-ласка, заповніть всі поля!'
            return render_template('addCommand.html', message_type=message_type, message_text=message_text)

    return render_template('addCommand.html')



# VA names page
@app.route('/voice_assistant_names', methods=['GET', 'POST'])
def voice_assistant_names():
    # handler
    if request.method == 'POST':

        # deleting name
        if request.form.get('delete_name') != None:
            if request.form.get('delete_name') in assistant_alias:
                settings_manager.delete_value_from_key('ASSISTANT_ALIAS', request.form.get('delete_name'))
            else:
                message_type = 'delete_error'
                message_text = 'Помилка при видаленні. <br> Спробуйте ще раз!'
                return render_template('VANames.html', message_type=message_type, message_text=message_text, assistant_alias=assistant_alias)

        # adding new name
        if request.form.get('add_name') == 'add_name':
            if request.form.get('new_name') == '':
                message_type = 'empty_field'
                message_text = "Введіть нове ім'я!"
                return render_template('VANames.html', message_type=message_type, message_text=message_text, assistant_alias=assistant_alias)
            else:
                if request.form.get('new_name') in assistant_alias:
                    message_type = 'name_exists'
                    message_text = "Таке і'мя вже присутнє! <br> Придумайте нове."
                    return render_template('VANames.html', message_type=message_type, message_text=message_text, assistant_alias=assistant_alias)
                else:
                    assistant_alias.append(request.form.get('new_name'))
                    print
                    settings_manager.set_setting('ASSISTANT_ALIAS', assistant_alias)
                    settings_manager.save_settings()


    return render_template('VANames.html', assistant_alias=assistant_alias)



# load styles to page
@app.route('/src/styles.css')
def serve_css():
    return send_file('src/styles.css', mimetype='text/css')



# open browser with home page
def open_browser():
    webbrowser.open('http://'+str(web_config['host'])+':'+str(web_config['port'])+'/')
