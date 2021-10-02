# smart-shell
State of the art AI available right inside of the terminal.

## Compatibility
Smart shell is currently available for Unix machines.

## Installing the executable
smart-shell is currently bundled as an executable that can be downloaded and run as a command. To use the executable version:
- Clone the repo to your home directory `git clone https://github.com/joseph-mcallister/smart-shell.git ~/.smart-shell`
- Run `chmod +x ~/.smart-shell/downloads/latest/smart-shell`
- Add the executable to your path. Ex. `sudo ln -s ~/.smart-shell/downloads/latest/smart-shell /usr/local/bin/smart-shell`
- Run `smart-shell setup` to provide your API key. Note: since smart-shell is not yet available through package managers, you may need to tell your OS it is a safe application before running.

## Getting an API key
smart-shell is currently in a private beta as the language model is fine-tuned on a growing dataset and the client is improved. To request access, please create a GitHub issue. 

Beta access is provisioned through RapidAPI. If you already have been granted access to the private plan API, search "smart shell" on [RapidAPI](https://rapidapi.com/hub) and join the private plan. Copy your `x-rapidapi-key` (this can be seen under the sample in endpoints) and provide it once the executable is installed. 

## Setup
After an API key has been provisioned and the download is ready, run:
- `smart-shell setup` and provide the API key
- `smart-shell "What directory am I in?"`

## Examples
### Creating a node project and installing packages
![Sample node usage](https://raw.githubusercontent.com/joseph-mcallister/smart-shell/main/images/node_sample.png)

### What's the weather like 
![Sample weather usage](https://raw.githubusercontent.com/joseph-mcallister/smart-shell/main/images/weather_in_seattle.png)