#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 13:24:12 2025

@author: jlab

This code creates a new Nicegui window with a chat area and a prompt area, 
and sets up a button to send messages to an Ollama model. 
When the user clicks the button, the message in the prompt area is sent 
to the Ollama model using the `ollama_client.prompt()` method, 
and the response from the model is displayed in the chat area.

You will need to replace the `ollama_client` variable with your own 
instance of an Ollama client object, which you can create by calling 
the `OllamaClient()` constructor and passing in your API key and 
secret as arguments. You will also need to modify the `on_send_message()` 
function to handle the response from the Ollama model in a way that makes sense
for your application.


"""

from nicegui import ui
from ollama import AsyncClient
from uuid import uuid4
from datetime import datetime

message = []

@ui.page('/')
def main():
    global message
    
    user_id = str(uuid4())
    robot_avatar = f'https://robohash.org/{user_id}?bgset=bg2'
    user_avatar = 'https://robohash.org/human?bgset=bg2'
    
    async def clear() -> None:
        message.clear()
        ui.notify('History Cleared!')
    
    message = []
    async def send() -> None:
               
        question = text.value
        text.value = ''

        with message_container:
            stamp = datetime.now().strftime('%X')
            ui.chat_message(text=question, stamp=stamp, avatar=user_avatar, name='User', sent=True)
            response_message = ui.chat_message(name='Mr. Robot', stamp=stamp, avatar=robot_avatar, sent=False)
            spinner = ui.spinner(type='dots')
            log.push(question)

        message.append({'role': 'user', 'content': question})
        response = ''
        async for part in await AsyncClient().chat(model='codellama:latest', messages=message, stream=True):
            response += part['message']['content']
            response_message.clear()
            with response_message:
                ui.html(response)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)
        message.append({'role': 'assistant', 'content' : response})
        log.push(response)
        
    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
            ui.button('Reset History', on_click=clear) #lambda message: (message := [], ui.notify('Chat History Cleared!')))

ui.run(title='LLM Chat', favicon='😊')
