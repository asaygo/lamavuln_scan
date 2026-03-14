import ollama
import sys
import os
import json
import subprocess
import re
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

# --- Remote Server Configuration ---
OLLAMA_SERVER_IP = ""
client = ollama.Client(host=f"http://{OLLAMA_SERVER_IP}:11434")

MODEL_NAME = 'qwen2.5-coder:3b'
# MODEL_NAME = 'codestral:latest'

# --- Eye-Friendly Color Palette (Nord/Slate Inspired) ---
USER_PROMPT_COLOR = Fore.LIGHTYELLOW_EX  # Softer Gold
AI_HEADER_COLOR = Fore.LIGHTBLUE_EX      # Calm Sky Blue
AI_TEXT_COLOR = Fore.WHITE               # Clean White
SYSTEM_MSG_COLOR = Fore.CYAN             # Teal/Slate
ERROR_COLOR = Fore.LIGHTRED_EX           # Muted Red
TOOL_COLOR = Fore.LIGHTCYAN_EX           # Frost Blue
SEPARATOR_LINE = Fore.BLACK + Style.BRIGHT + "-" * 60 + Style.RESET_ALL

def log(msg):
    """Log AI responses to scan_results.log."""
    try:
        with open("scan_results.log", "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

    return
    
def read_file(fname):
    s = ""
    try:
        with open(fname, "r") as f:
            s = f.read()
            f.close()
    except:
        pass
    return s

def scan_file(fname):
    # Initial system message
    system_prompt = (
        "You are a Software Security Engineer.\n"
        "You analyze code for software vulnerabilities. Do not explain what the code does.\n"
        "When a vulnerability is found, you say [VULN_FOUND], assign a severity for the identified vulnerability and show the vulnerable code. Do not provide additional details.\n"
        "If a vulnerability isn't found, just print [NOT_VULN]\n"
        "Example: Let's say we have this golang code: resp, err := http.Get(user_input_url)\ndefer resp.Body.Close()\nout, err := os.Create(output)\ndefer out.Close()\n"
        "Your answer: [VULN_FOUND] [Severity:Important] The code is vulnerable to SSRF. Here is the vulnerable code: resp, err := http.Get(user_input_url)\n"
        "Example: Let's say we have this golang code: x := 1\n"
        "Your answer: [NOT_VULN]"
    )

    messages = [
        {
            'role': 'system',
            'content': system_prompt
        }
    ]

    print(SEPARATOR_LINE)

    data = read_file(fname)
    if len(OLLAMA_SERVER_IP) > 5 and len(MODEL_NAME) > 2 and len(data) > 5:
        try:
            user_input = f"[FILE CONTENT]:\n{data}"
            messages.append({'role': 'user', 'content': data})

            print(AI_HEADER_COLOR + ">>> ANALYZE " + fname)
            response = client.chat(
                model=MODEL_NAME,
                messages=messages,
                stream=False
            )

            content = response['message']['content']
            if "[VULN_FOUND]" in content:
                print(AI_TEXT_COLOR + content, end="", flush=True)
                log("[File:" + fname + "]\n-----")
                log(content)
                log("-----")

        except KeyboardInterrupt:
            print(SYSTEM_MSG_COLOR + "\nInterrupt received. Exiting...")
            return
        except Exception as e:
            print(ERROR_COLOR + f"\n[CRITICAL]: {e}")
            return
    return

def check_file(fname):
    try:
        scan_file(fname)
    except:
        return
    return
