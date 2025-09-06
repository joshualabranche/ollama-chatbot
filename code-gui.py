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

# generate a list of message information to keep a chat history with the bot
message = []

@ui.page('/')
def main():
    global message
    
    # generate a bot icon from user ID and human icon from 'human' string
    user_id = str(uuid4())
    robot_avatar = f'https://robohash.org/{user_id}?bgset=bg2'
    user_avatar = 'https://robohash.org/human?bgset=bg2'
    
    # async function to clear messages such that the chat history is wiped
    async def clear() -> None:
        message.clear()
        ui.notify('History Cleared!')
    
    
    async def send() -> None:           
        # text is a ui.input used to get user input
        question = text.value
        text.value = ''

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
            log.push(question)

        # append current prompt to chat history
        message.append({'role': 'user', 'content': question + ". make sure any python code has proper linebreak characters for proper format when using the python function print"})
        # retrieve the response async as a streamed output
        part = await AsyncClient().chat(model='gemma3:latest', messages=message, format=code_response.model_json_schema(), stream=False)
        output = code_response.model_validate_json(part['message']['content'])
        #response += part['message']['content']
        response_message.clear()
        with response_message:
            ui.label(output.information)
            ui.code(output.snippet)
            ui.html("OVERVIEW: <br> "+ output.overview + "<br><br> *** <br><br> EXECUTION: <br>" + output.execution)
        # js function to auto scroll as chat develops
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

        # once responded no more "thinking" dots
        message_container.remove(spinner)
        # save bot response to chat history and log tab
        message.append({'role': 'assistant', 'content' : part['message']['content']})
        log.push(part['message']['content'])
        
    # CSS style options
    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full bg-black')

    # create two tabs in the window
    with ui.tabs().classes('bg-grey') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    
    # create message container for the chat tab and log for the log tab
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full bg-black mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full bg-black')

    # this is where the user input box and clear history button are constructed
    with ui.footer().classes('bg-black'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message'
            text = ui.input(placeholder=placeholder).props('input-class=mx-3') \
                .classes('w-full bg-grey self-center').on('keydown.enter', send)
            ui.button('Reset History', on_click=clear) #lambda message: (message := [], ui.notify('Chat History Cleared!')))

# lastly we run the GUI
ui.run(title='LLM Chat', favicon='https://robohash.org/friend?bgset=bg2')
