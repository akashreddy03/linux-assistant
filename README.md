# Linux Assistant

This project provides a Linux assistant that understands natural language. It can execute shell commands, manage files, search the internet, monitor system resources, and launch applications. Built with LangGraph for flexible workflows and it also integrates Whisper for speech-to-text input.

## ✨ Key Features

* Natural language command execution.
* File system operations (read, write, delete, etc.).
* Web searching capabilities.
* System resource monitoring.
* Application launching.
* Speech-to-text via Whisper.

## 📂 File Structure
```bash
linux-assistant
├── main.py
├── prompt.py
├── requirements.txt
├── .env.example
├── .gitignore
└── utils
    ├── __init__.py
    ├── command_executor.py
    └── speech_to_text.py
```
## 🚀 Getting Started
This project uses python 3.11. So make sure to install it before following the steps below. 
### 1. Clone:
```bash 
git clone <repository_url> 
cd linux_assistant 
```
### 2. Create a Virtual Environment (Recommended):
```bash 
python -m venv .venv
source ./.venv/bin/activate
``` 
### 3. Install:
```bash 
pip install -r requirements.txt 
``` 
### 4. Configure LLM: 

#### Google Gen AI 
1. Create a `.env` file.
	```bash
	cp .env.example .env
	```
2. Set up a Google Cloud project and obtain an API key. Configure the API key as an environment variable in `.env` file
	```
	GOOGLE_API_KEY=your-api-key
	``` 
#### Ollama
1. Ensure Ollama is installed and running. 
2. Adjust model name/endpoint in `main.py`.
### 5. Run:
```bash 
python main.py 
``` 

## 🤝 Contributing 
Contributions are welcome. Feel free to open issues or submit pull requests. 

## 📜 License 
This project is licensed under the  [MIT License](https://opensource.org/licenses/MIT)  — see the  [`LICENSE`](https://github.com/akashreddy03/linux-assistant/blob/main/LICENSE)  file for details.
