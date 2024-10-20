import pika
import json
import time

# Configurações de conexão
rabbitmq_host = 'localhost'
vhost = 'magaluloja1'
username = 'accessadmin'
password = '35lkK69gwoF0hGBb'

# Mensagem a ser enviada
message = {
    "dataHoraOperacao": "2024-09-14T00:00:00",
    "codigoRastreio": "a1sd24ew-s221ds74-a21sd1f-asd1",
    "pedidoTransferencia": {
        "depositoRequistante": "207030",
        "codigoRastreio": "a1sd24ew-s221ds74-a21sd1f-asd1",
        "itens": [
            {"codigo": "00000001", "qtdSolicitada": 1},
            {"codigo": "00000002", "qtdSolicitada": 120}
        ],
        "qtdTotalItens": 2
    }
}

# Estabelecendo conexão com RabbitMQ
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, virtual_host=vhost, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

try:
    while True:
        # Enviar a mensagem
        channel.basic_publish(exchange='e.magalo.order.create', routing_key='', body=json.dumps(message))
        print("Mensagem enviada:", message)

        # Aguardar 2 segundos antes de enviar a próxima mensagem
        time.sleep(2)
except KeyboardInterrupt:
    print("Envio de mensagens interrompido.")

# Fechar a conexão ao final do envio
connection.close()