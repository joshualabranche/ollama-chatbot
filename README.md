# ollama-chatbot

 ## **requirements**

  **ollama** https://ollama.com/download
  - used to maintain LLM libraries
    
  **conda** https://github.com/conda-forge/miniforge
  - python package management system using conda & conda-forge
  
  **nicegui** https://nicegui.io/
  - python library for generating GUIs
  
  **ollama-python** https://github.com/ollama/ollama-python
  - python ollama API for using ollama in python programs

## ** getting started **

1. install ollama as needed
   - ``` ollama serve # start the server ```
   - ``` ollama -v # print server version ```
3. install miniforge (any conda will do)
4. setup conda enviroment for ollama:
   - ``` $ conda env -n ollama-env ```
5. activate the environment:
   - ``` $ conda activate ollama-env ```
7. add pip:
   - ``` $ conda install -c conda-forge pip ``` (add any other python dependencies here)
9. install python ollama API:
    - ``` $ pip install ollama # $ conda install -c conda-forge ollama ```
11. install nicegui:
    - ``` $ pip install nicegui ```
