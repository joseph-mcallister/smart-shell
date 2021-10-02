## Setup + Example
`pip install -r requirements.txt`
`python3 ai.py setup`
`python3 ai.py "Print files in current directory"`

## Building bundle
`pyinstaller --onefile --distpath ../downloads/latest --name smart-shell client.py`

## TODO
- Show good error if no internet connect
- Run `which <first-command>` and prompt to download if not available
- Add anonymized telemetry for successful commands