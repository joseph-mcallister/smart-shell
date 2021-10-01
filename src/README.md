## Setup + Example
`pip install -r requirements.txt`
`python3 ai.py setup`
`python3 ai.py "Print files in current directory"`

## Building bundle
`pyinstaller --onefile --distpath ../downloads/latest --name smart-shell client.py`
`codesign --remove-signature smart-shell`
`codesign -o runtime --timestamp -s "Joseph McAllister"  smart-shell`
`ditto -c -k --keepParent <path>/downloads/latest <path>/downloads/smart-shell.zip