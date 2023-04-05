# api-bluetooth-server

API that gets data, starts bluetooth service (as a device) on RPi which handles the data until an Android device connects and reads it.

Tested on Raspberry Pi OS and Android.

## Installation

For Raspberry Pi OS, Python and pip come pre-installed. Run the requirements with:

```bash
pip install -r requirements.txt
```

or just run setup_env.sh

## Usage

To start the API run:

```bash
gunicorn3 api:app -b 0.0.0.0:PORT --timeout SECONDS
```

where:

- `api:app` -> are the file/service
- `-b 0.0.0.0:PORT` -> 0.0.0.0 enables external access and PORT specifies the port to listen
- `--timeout SECONDS` -> SECONDS is the time for the worker to timeout (it restarts after that, use 0 for no timeout)

To enable the API, send a POST request:

```bash
curl.exe -X POST -H 'Content-Type: application/json' -d '{"""field""":value,"""field""":value,"""field""":value,"""field""":value,"""field""":value}' http://IP.ADD.RE.SS:PORT/ROUTE
```
