# Projeto - Aplicação de Chat Cliente-Servidor

# DEPENDENCIAS:

- urllib3
- requests
- pycryptodome
- python-dotenv

# Como rodar:

1 - instalar as dependencias
2 - Iniciar o servidor http:
  2.1 dentro do diretório backend/http_server usar python app.py
3 - Iniciar o servidor websocket 
  3.1 dentro do diretório backend/websocket_server usar python app.py
4 - Iniciar o client cmd:
  4.1 dentro do diretório clients/cmd_client usar python app.py

# Atenção:

No momento só conseguimos implementar envio de arquivos txt, por conta de um problema de codificação de dados binaários ao transformar os chunks recebidos no backend em caractres utf-8