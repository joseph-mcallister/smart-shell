# smart-shell
State of the art AI available right inside of the terminal.

## Compatibility
Smart shell is available for all machines with Python3.4+ and pip installed. It currently works best on Linux and Unix machines.

## Examples
### Creating a node project and installing packages
![Sample node usage](https://raw.githubusercontent.com/joseph-mcallister/smart-shell/main/images/node_sample.png)

### What's the weather like 
![Sample weather usage](https://raw.githubusercontent.com/joseph-mcallister/smart-shell/main/images/weather_in_seattle.png)

## Getting an API key
smart-shell is currently in a private beta as the language model is fine-tuned on a growing dataset and the client is improved. To request access, please create a GitHub issue. 

Beta access is provisioned through RapidAPI. If you already have been granted access to the private plan API, search "smart shell" on [RapidAPI](https://rapidapi.com/hub) and join the private plan. Copy your `x-rapidapi-key` (this can be seen under the sample in endpoints) and provide it once the executable is installed. 

## Requirements
- python (3.4+)
- pip
- python-dev

## Installation
- `pip3 install smart-shell`

## Setup
After an API key has been provisioned and the download is ready, run:
- `plz setup` and provide the API key
- `plz "What directory am I in?"`