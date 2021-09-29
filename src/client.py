import os
from posixpath import split
import sys
import requests
import json
from requests.api import options
import subprocess
import time
import csv
from subprocess import check_output

home = os.environ.get("XDG_CONFIG_HOME") or os.environ.get("HOME")
logs_path = "{0}/.config/smart_shell_context.json".format(home)
base_api_url = os.environ.get("API_URL") or "https://smart-shell-function-app.azurewebsites.net/api"

def get_config_data(is_setup_mode):
    config_path = "{0}/.config/smart_shell.json".format(home)
    config_data = {}
    if not os.path.exists(config_path) or is_setup_mode:
        api_key = input("Please enter an API key: ")
        with open(config_path, "w") as config_file:
            config_data = { "api_key": api_key }
            json.dump(config_data, config_file)
            config_file.close()
    else: 
        with open(config_path, "r") as config_file:
            config_data = json.load(config_file)
            config_file.close()
    return config_data

def write_context(prompt, command):
    context_data = get_context()
    with open(logs_path, "w+") as logs_file:
        context_data["context"].insert(0, { "prompt": prompt, "command": command, "timestamp": time.time()})
        if len(context_data["context"]) >= 3:
            context_data["context"].pop()
        json.dump(context_data, logs_file)

def get_context():
    context_data = None
    if os.path.exists(logs_path):
        with open(logs_path, "r") as logs_file:
            context_data = json.load(logs_file)
    return context_data or { "context": [] } 

# Remove current prompt from context if found to prevent overfitting prompt
def get_context_data_without_prompt(context_data, prompt):
    context_data_deduplicated = { "context": [] } 
    for context_sample in context_data["context"]:
        if context_sample["prompt"] != prompt:
            context_data_deduplicated["context"].append(context_sample)
    return context_data_deduplicated

# Returns an array of strings split on spaces but ignoring quotes
# Ex. 'echo "hey there test" > test.txt' -> ['echo', 'hey there test', '>', 'test.txt']
def split_command(str):
    arr = []
    last_seq = ""
    is_single_quote_delim = is_double_quote_delim = False
    for char in command.strip():
        if char == ' ' and not is_single_quote_delim and not is_double_quote_delim:
            arr.append(last_seq)
            last_seq = ""
        elif char == "'":
            last_seq += char
            is_single_quote_delim = not is_single_quote_delim
        elif char == "\"":
            last_seq += char
            is_double_quote_delim = not is_double_quote_delim 
        else:
            last_seq += char
    arr.append(last_seq)
    return arr

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 0 else None
    config_data = get_config_data(arg == "setup")
    if arg != "setup":
        context_data = get_context()
        context_data = get_context_data_without_prompt(context_data, arg)
        r = requests.post("{0}/Command".format(base_api_url), 
            json={
                "prompt": arg, 
                "tags": ["mac","python"],
                "context": context_data["context"] 
            },
            headers={
                "Content-Type": "application/json",
                "X-RapidAPI-Proxy-Secret": config_data["api_key"]
            }
        )
        
        if r.status_code >= 200 and r.status_code < 300:   
            response = r.json()
            command = response["choices"][0]["text"].strip()
            print("Suggested command: '{0}'".format(command))
            if input("Run command above? (y/n): ") in ["Y", "y"]:
                command_arr = split_command(command)
                try:
                    output = subprocess.check_output(command, shell=True)
                    if output is not None and output != "":
                        print(output.decode("utf-8"), end='')
                    write_context(arg, command)
                except:
                    print("Oops, looks like we still have some work to do!")

        elif r.status_code == 401:
            print("API key not valid.")
            get_config_data(True)

        else:
            print("Error fetching command from API")