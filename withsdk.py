import os
import pickle

from google import genai
from google.genai import types
import pyperclip
import sys


api_key = os.environ.get("GEMINI_API_KEY")
SYSTEM_PROMPT = """
You are an expert command-line assistant. Your sole purpose is to translate a user's natural language description of a task into a precise and runnable shell command.

- Analyze the user's request carefully.
- Generate the most appropriate and efficient command(s) to achieve the described task.
- **Output ONLY the command(s).** Do not include any conversational text, greetings, or explanations before or after the command unless specifically requested by the user in their prompt.
- If multiple commands are needed (e.g., a pipeline or sequence), provide them one per line or chained appropriately.
- Assume a Bash shell environment (for Linux/macOS) unless otherwise specified or strongly implied by the request.
- If a request is ambiguous or lacks critical details for command generation, you MUST ask for clarification by responding with "CLARIFY:" followed by your question.
- If a command is inherently dangerous (e.g., involves `rm -rf`, `dd`, or modifying system files without confirmation), provide the command but also add a concise warning on a new line immediately after the command, starting with "WARNING:".
"""
PICKLE_HISTORY_FILE = "/tmp/cmd_gpt_chat_history.pkl"


def save_history_pickle(chat_session, filename=PICKLE_HISTORY_FILE):
    try:
        with open(filename, 'wb') as f: # 'wb' for write binary
            pickle.dump(chat_session.get_history(), f)
        print(f"Chat history saved to {filename} using pickle.")
    except (IOError, pickle.PicklingError) as e:
        print(f"Error saving history with pickle: {e}")


def load_history_pickle(filename=PICKLE_HISTORY_FILE):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'rb') as f: # 'rb' for read binary
            history = pickle.load(f)
        print(f"Chat history loaded from {filename} using pickle.")
        return history
    except (IOError, pickle.UnpicklingError, EOFError) as e: # EOFError if file is empty/corrupt
        print(f"Error loading history with pickle: {e}. Starting new session.")
        return []


arguments = sys.argv[1:]
history = []
if "-H" in arguments:
    history = load_history_pickle()
client = genai.Client(api_key=api_key)
chat = client.chats.create(
    # model="gemini-2.0-flash",
    model="gemini-2.5-flash-preview-05-20",
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    history=history
)
# chat.record_history()
text = input("Enter prompt:")
response = None
while text != "":
    response = chat.send_message(text)
    print(response.text)
    text = input("Enter prompt:")

if response.text is not None:
    pyperclip.copy(response.text)
if len(chat.get_history()) >= 2:
    save_history_pickle(chat)

print("End of user input")