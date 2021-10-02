# smart-shell
State of the art AI available right inside of the terminal

## Download
smart-shell is currently bundled as an executable that can be downloaded and run as a command. Eventually, smart-shell will be released on package managers like homebrew. To use the executable version:
- Clone the repo to your home directory `git clone https://github.com/joseph-mcallister/smart-shell.git ~/.smart-shell`
- Run `chmod +x ~/.smart-shell/downloads/latest/smart-shell`
- Add the executable to your path. Ex. `sudo ln -s ~/.smart-shell/downloads/latest/smart-shell /usr/local/bin/smart-shell`
- Run `smart-shell setup` to provide your API key. Note: since smart-shell is not yet available through package managers, you may need to tell your OS it is a safe application before running.

## Setup
Smart shell is currently in private beta and an API key is needed. Feel free to reach out to me (Joe) if you are interested. After an API key has been provisioned and the download is ready run
- Run `smart-shell setup` and provide the API key
- Run `smart-shell "What directory am I in?"`

## Example
![Sample usage](https://raw.githubusercontent.com/joseph-mcallister/smart-shell/main/images/node_sample.png)

## Compatibality
Smart shell is currently available for Unix machines.
