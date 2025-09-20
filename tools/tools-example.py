#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 19:19:32 2025

@author: jlab
"""

from typing import Iterator
from ollama import ChatResponse, Client

import requests
from bs4 import BeautifulSoup
import csv
import re


def exec_code(code: str) -> None:
    exec(code)


available_functions = {
  'exec_code': exec_code,
}

code = open('nyt_scraper.py').read()
messages = [{'role': 'system', 'content': 'You are a python interpreter, you one and ONLY task is use the given python tool to execute python code. Assume the given code is correct ALWAYS. Do *NOT* attempt to analyze, check, verify, test, debug, etc any of the code!'}]
messages.append({'role': 'user', 'content': f"Run the followig code as is: {code}"})
print('----- Prompt:', messages[0]['content'], '\n')

model = 'qwen3:latest'
client = Client()
response: Iterator[ChatResponse] = client.chat(model, stream=True, messages=messages, tools=[exec_code], think=True)

for chunk in response:
  if chunk.message.thinking:
    print(chunk.message.thinking, end='', flush=True)
  if chunk.message.content:
    print(chunk.message.content, end='', flush=True)
  if chunk.message.tool_calls:
    for tool in chunk.message.tool_calls:
      if function_to_call := available_functions.get(tool.function.name):
        print('\nCalling function:', tool.function.name, 'with arguments:', tool.function.arguments)
        output = function_to_call(**tool.function.arguments)
        print('> Function output:', output, '\n')

        # Add the assistant message and tool call result to the messages
        messages.append(chunk.message)
        messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})
      else:
        print('Function', tool.function.name, 'not found')

print('----- Sending result back to model \n')
if any(msg.get('role') == 'tool' for msg in messages):
  res = client.chat(model, stream=True, tools=[exec_code], messages=messages, think=True)
  done_thinking = False
  for chunk in res:
    if chunk.message.thinking:
      print(chunk.message.thinking, end='', flush=True)
    if chunk.message.content:
      if not done_thinking:
        print('\n----- Final result:')
        done_thinking = True
      print(chunk.message.content, end='', flush=True)
    if chunk.message.tool_calls:
      # Model should be explaining the tool calls and the results in this output
      print('Model returned tool calls:')
      print(chunk.message.tool_calls)
else:
  print('No tool calls returned')