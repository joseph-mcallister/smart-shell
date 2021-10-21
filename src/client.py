import os
from posixpath import split
import sys
import requests
import json
from requests.api import options
import subprocess
import time
from subprocess import check_output
import logging 
from psutil import Process

home = os.environ.get("XDG_CONFIG_HOME") or os.environ.get("HOME")
logs_path = "{0}/.config/smart_shell_context.json".format(home)
base_api_url = "https://smart-shell.p.rapidapi.com"

def get_os():
    # TODO: dynamically detect OS
    return "mac"

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
    for char in str.strip():
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


## Return True if command is found 
def command_exists(command):
    which_check = "which {0}".format(command)
    try:    
        subprocess.check_output(which_check, shell=True)
        return True
    except:
        return False

def post_command(prompt):
    config_data = get_config_data(prompt == "setup")
    context_data = get_context()
    context_data = get_context_data_without_prompt(context_data, prompt)
    r = requests.post("{0}/Command".format(base_api_url), 
        json={
            "prompt": prompt, 
            "tags": ["mac","python"],
            "context": context_data["context"] 
        },
        headers={
            "Content-Type": "application/json",
            "X-RapidApi-Key": config_data["api_key"]
        }
    )
    if r.status_code >= 200 and r.status_code < 300:
        return r
    elif r.status_code == 401:
        print("API key not valid.")
        get_config_data(True)
    else:
        print("Error fetching command from API")
    return None

def post_telemetry(prompt, command):
    config_data = get_config_data(False)
    try:
        requests.post("{0}/Telemetry".format(base_api_url), 
            json={
                "prompt": prompt, 
                "command": command,
                "os": get_os()
            },
            headers={
                "Content-Type": "application/json",
                "X-RapidApi-Key": config_data["api_key"]
            },
            timeout=0.1 # hack to avoid blocking script
        )
    except requests.exceptions.ReadTimeout:
        pass

def get_shell_from_proc():
    proc = Process(os.getpid())
    while proc is not None and proc.pid > 0:
        try:
            name = proc.name()
        except TypeError:
            name = proc.name

        name = os.path.splitext(name)[0]
        if "zsh" in name:
            return "zsh"
        elif "bash" in name:
            return "bash"

        try:
            proc = proc.parent()
        except TypeError:
            proc = proc.parent

def get_history_file_name(shell):
    if shell == "zsh":
        return os.path.expanduser('~/.zsh_history')
    elif shell == "bash":
        return os.environ.get(os.path.expanduser('~/.bash_history'))

def main():
    if len(sys.argv) == 1:
        print("No arguments provided. See below for sample commands")
        print("> plz setup")
        print('> plz "Tell me my curent directory"')
        return
    arg = sys.argv[1] if len(sys.argv) > 0 else None
    get_config_data(arg == "setup")
    if arg == "fix":
        shell = get_shell_from_proc()
        last_command = None
        if shell:
            with open(get_history_file_name(shell)) as f:
                print(f)
                last_command = f.readlines() [-2:]
            print(last_command)

        else:
            print("Shell not supported. Currently only zsh and bash are supported")

    elif arg != "setup":
        r = post_command(arg)

        if r.status_code >= 200 and r.status_code < 300:   
            response = r.json()
            command = response["choices"][0]["text"].strip()
            first_command = command.split(" ")[0]
            print("Suggested command: '{0}'".format(command))
            # TODO: prompt to install if command not found !command_exists
            if input("Run command above? (y/n): ") in ["Y", "y"]:
                try:
                    output = subprocess.check_output(command, shell=True)
                    if output is not None and output != "":
                        print(output.decode("utf-8"), end='')
                        try:
                            write_context(arg, command)
                            post_telemetry(arg, command) 
                        except:
                            ## TODO: update to only log if dev environment
                            logging.exception('')
                except:
                    print("Oops, looks like we still have some work to do!")

        elif r.status_code == 401:
            print("API key not valid.")
            get_config_data(True)

        else:
            print("Error fetching command from API")

if __name__ == "__main__":
    main()