powershell .\venv\Scripts\activate

python .\backend\http_server\app.py &
python .\websocket_server\app.py &
