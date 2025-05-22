## CMDGPT
generate cli commands using Gemini models.


### Installation
- clone the repository and cd into the directory
- run the following commands
```commandline
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
```

### Using the script
```commandline
GEMINI_API_KEY=<> bin/python3 withsdk.py
```

or start script with previous run's history
```commandline
GEMINI_API_KEY=<> bin/python3 withsdk.py -H
```
