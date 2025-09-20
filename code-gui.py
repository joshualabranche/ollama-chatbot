#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 13:24:12 2025

@author: jlab

"""

from nicegui import ui
from ollama import AsyncClient
from uuid import uuid4
from datetime import datetime
from response_formats import code_response

import torch
from TTS.api import TTS
from playsound import playsound
import os


class tts():
    def __init__(self):
        self.fname = "tmp_audio.wav"
        self.output_path = os.getcwd() + "/" + self.fname
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.speaker_wav = "/home/jlab/Music/voice_pack_v2/ana_florence/misceallaneous_new_personal_best.wav"
        self.audio_processor = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=False).to(self.device)


    async def speak(self, text_input):
        for sentence in text_input:
            if sentence == '':
                pass
            else:
                self.audio_processor.tts_to_file(text=sentence, file_path=self.output_path)
        
            # Play audio
            playsound(self.output_path)


class conversation():
    """conversation class"""

    def __init__(self):
        """Initializes the conversation object."""
        self.messages = []
        self.pyformat = """
            You are PyCode, a highly specialized Large Language Model dedicated to generating high-quality, functional Python code. 
            Your primary goal is to understand the user's request precisely and deliver a solution that meets their needs reliably. 
            You operate with a structured, iterative approach to ensure optimal code quality. 
            You are designed to be a helpful and collaborative coding partner.
            Include a brief summary that is maximally 2-5 sentences in length.
            **Core Principles:** 
            1. **Library Restriction:** 
            You *must* adhere to the following list of libraries. 
            You are *not* permitted to use any other libraries unless explicitly instructed to do so. 
            This ensures consistency and allows for optimized performance. 
            * `requests` (for making HTTP requests) 
            * `beautifulsoup4` (for HTML parsing) 
            * `numpy` (for data manipulation and analysis) 
            * `datetime` (for working with dates and times) 
            * `re` (for regular expression matching) 
            * `os` (for interacting with the operating system) 
            * `json` (for working with JSON data)
            * `scipy` (for signal processing and advanced scientific coding)
            * `nicegui` (for generating GUIs and GUI related tasks)
            2. **Self-Checking & Verification:** 
            After generating a code block, you *must* execute it locally (simulated execution) to test its functionality. 
            You will then report the output and any errors encountered. 
            You will then ask the user if the output is what they intended, and if not, iterate. 
            3. **Documentation & Comments:** 
            Include comments within the generated code to explain its purpose and logic. 
            This enhances readability and maintainability. 
            4. **Error Handling:** 
            Implement robust error handling to prevent unexpected crashes. 
            Include `try...except` blocks to catch potential exceptions. 
            **Workflow & Interaction Sequence:** 
            1. **Sub-Task Decomposition:** 
            Based on the user’s request, identify the essential sub-tasks needed to achieve the goal. 
            Example: "To accomplish this, I propose the following steps: 
                1) [Sub-task 1], 2) [Sub-task 2], 3) [Sub-task 3]... Does this breakdown seem appropriate?” 
            2. **Prompt Generation for Sub-Tasks:** 
            For each sub-task, create a specific prompt tailored to that task. 
            Example: "Now, let’s focus on Sub-task 1: [State sub-task]. 
            I will generate code to accomplish this. 
            Please let me know if you have any additional constraints or specifications for this sub-task." 
            3. **Code Generation:** 
            Generate Python code for the sub-task, utilizing only the approved libraries. 
            4. **Local Execution & Verification:** 
            Execute the generated code (simulated execution). 
            Report the output, any errors encountered, and a brief assessment of the code’s functionality. 
            Example: “I’ve executed the code. The output was: [Output]. I detected [Error, if any]. 
            Does this output align with your expectations? 
            Should I modify the code based on this result?" 
            5. **User Feedback & Iteration:** 
            Based on the user’s response, either refine the code or proceed to the next sub-task. 
            Repeat steps 3, 4, and 5 until the final solution is achieved. 
            **Important Notes to the Model:** 
            * **Be Explicit:** Don't assume anything. Always ask clarifying questions. 
            * **Prioritize Clarity:** Write clear, concise code. 
            * **Handle Edge Cases:** Consider potential edge cases and include appropriate error handling. 
            * **Maintain Conversation History:** Retain context from previous interactions to ensure consistent behavior. 
            * **Formatting:** Use consistent code formatting by following PEP 8 guidelines.
            **Example Initial Prompt (This is what the model would *start* with - you'd provide the actual user prompt):** 
            “Write a Python script that scrapes the titles of all articles from the New York Times website and saves them to a CSV file.” 
            **Now, waiting for the user's response to the initial confirmation prompt.**
        """
        # self.append_message('system',self.pyformat)
        self.options = {
            #'num_keep': 1,
            #'seed': 42,
            #'num_predict': -1,
            #'top_k': 20,
            #'top_p': 0.9,
            #'min_p': 0.0,
            #'typical_p': 0.7,
            #'repeat_last_n': 64,
            #'temperature': 0.1,
            #'repeat_penalty': 1.1,
            #'presence_penalty': 1.5,
            #'frequency_penalty': 1.1,
            #'penalize_newline': False,
            #'stop': ["user:"],
            #'numa': False,
            #'num_ctx': 32768,
            #'num_batch': 2,
            #'num_gpu': 1,
            #'main_gpu': 0,
            #'use_mmap': True,
            #'num_thread': 8
          }
        
    def set_option(self, opt_name, value):
        if opt_name in self.options:
            self.options[opt_name] = value
            
    def list_options(self):
        for option in self.options:
            print(option)
    
    def append_message(self, role, content):
        self.messages.append({'role': role, 'content': content})

    def clear_messages(self):
        self.messages.clear()
        
    def clear_history(self):
        self.clear_messages()
        ui.notify('Chat History Cleared!')
        self.append_message('system',self.pyformat)


@ui.page('/')
def main():
    # initialize the web GUI in dark mode
    dark = ui.dark_mode()
    dark.enable()
    
    """ 
    NAME                    ID              SIZE      MODIFIED       
    gpt-oss:latest          aa4295ac10c3    13 GB     2 minutes ago     
    qwen2.5-coder:latest    dae161e27b0e    4.7 GB    48 minutes ago    
    gemma3:latest           a2af6cc3eb7f    3.3 GB    5 days ago      
    """
    model_name = 'gemma3:latest'
    
    # initialize the conversation
    convo = conversation()
    
    # generate a bot icon from user ID and human icon from 'human' string
    user_id = str(uuid4())
    robot_avatar = f'https://robohash.org/{user_id}?bgset=bg2'
    user_avatar = 'https://robohash.org/human?bgset=bg2'
    
    async def send() -> None:
        # initialize tts object
        voice = tts()
        
        # text is a ui.input used to get user input
        question = text.value
        text.value = ''
        
        # append style guidelines to log file
        # log.push(convo.pyformat)

        with message_container:
            # timestamp each message
            stamp = datetime.now().strftime('%X')
            # create user message input
            ui.chat_message(text=question, stamp=stamp, avatar=user_avatar, name='User', sent=True)
            # create bot response message
            response_message = ui.chat_message(name='Mr. Robot', stamp=stamp, avatar=robot_avatar, sent=False)
            # "thinking" dots for output
            spinner = ui.spinner(type='dots')
            # append chat history to log file
            log.push("python code request: " + question)

        # append current prompt to chat history
        convo.append_message('user', "python code request: " + question)
        # retrieve the response async as a streamed output
        part = await AsyncClient().chat(model=model_name, messages=convo.messages, options=convo.options, format=code_response.model_json_schema(), stream=False)
        output = code_response.model_validate_json(part['message']['content'])
        #response += part['message']['content']
        response_message.clear()
        
        with response_message:
            ui.label(output.information)
            code = output.generated_code
            code = code[9:-3]
            ui.code(code).style('color: black;')
            # ui.html("OVERVIEW: <br> "+ output.overview + "<br><br> *** <br><br> EXECUTION: <br>" + output.execution)
            
        # synthesize voice
        sentences = output.information.split('.')
        sentences = [x for x in sentences if x]
        await voice.speak(sentences)
        
        # js function to auto scroll as chat develops
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

        # once responded no more "thinking" dots
        message_container.remove(spinner)
        
        # remove speech function from the message container
        # message_container.remove(speech)
        
        # save bot response to chat history and log tab
        convo.append_message('assistant', part['message']['content'])
        log.push(part['message']['content'])
        
    # CSS style options
    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500; font-size: 18}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    # create two tabs in the window
    with ui.tabs().classes('bg-grey') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    
    # create message container for the chat tab and log for the log tab
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')

    # this is where the user input box and clear history button are constructed
    with ui.footer().classes('bg-black'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message'
            text = ui.input(placeholder=placeholder).props('input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
            ui.button('Reset History', on_click=convo.clear_history)

# lastly we run the GUI
ui.run(title='LLM Code',
       dark=True,
       favicon='https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg',
       binding_refresh_interval=1,
       reconnect_timeout=60)