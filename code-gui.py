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


class conversation():
    """conversation class"""

    def __init__(self):
        """Initializes the MyClass object."""
        self.messages = []
        self.pyformat = """
           required: linebreak characters for proper format when using the python function print.
           required: 'PEP 8' official python style guide for all python code generation.
           required: PEP 484 type hint styling.
           required: lower_case_with_underscores naming conventions.
           required: do not use triple quotes at the beginning of the code snippet
           required: do use ``` python ``` to distinguish the code in text
        """
        self.append_message('user',self.pyformat)
        self.append_message('assistant','Yes sir, I will follow those rules!')
        self.options = {
            'num_keep': 5,
            'seed': 42,
            'num_predict': 2048,
            'top_k': 20,
            'top_p': 0.75,
            'min_p': 0.0,
            'typical_p': 0.7,
            'repeat_last_n': 64,
            'temperature': 0.2,
            'repeat_penalty': 1.1,
            'presence_penalty': 1.5,
            'frequency_penalty': 1.0,
            'penalize_newline': False,
            'stop': ["user:"],
            'numa': False,
            'num_ctx': 4096,
            'num_batch': 2,
            'num_gpu': 1,
            'main_gpu': 0,
            'use_mmap': True,
            'num_thread': 8
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
        self.append_message('user',self.pyformat)
        self.append_message('assistant','Yes sir, I will follow those rules!')


@ui.page('/')
def main():
    # initialize the web GUI in dark mode
    dark = ui.dark_mode()
    dark.enable()
    
    """ 
    NAME                        COMMIT          SIZE      UPDATED
    deepseek-coder-v2:latest    63fb193b3a9b    8.9 GB    21 seconds ago
    qwen2.5-coder:latest        dae161e27b0e    4.7 GB    6 minutes ago
    codellama:latest            8fdf8f752f6e    3.8 GB    5 days ago
    gemma3:latest               a2af6cc3eb7f    3.3 GB    5 days ago
    """
    model_name = 'deepseek-coder-v2:latest'
    
    # initialize the conversation
    convo = conversation()
    
    # generate a bot icon from user ID and human icon from 'human' string
    user_id = str(uuid4())
    robot_avatar = f'https://robohash.org/{user_id}?bgset=bg2'
    user_avatar = 'https://robohash.org/human?bgset=bg2'
    
    async def send() -> None:
        
        # text is a ui.input used to get user input
        question = text.value
        text.value = ''
        
        # append style guidelines to log file
        log.push(convo.pyformat)

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
            ui.code(output.generated_code).style('color: black;')
            # ui.html("OVERVIEW: <br> "+ output.overview + "<br><br> *** <br><br> EXECUTION: <br>" + output.execution)
        # js function to auto scroll as chat develops
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

        # once responded no more "thinking" dots
        message_container.remove(spinner)
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
ui.run(title='LLM Code', favicon='https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg')