import json
import time
import pika

# Configurações de conexão com RabbitMQ
rabbitmq_host = '10.2.13.71'  # IP do servidor RabbitMQ
vhost = 'eco_dev'
username = 'accessadmin'
password = '35lkK69gwoF0hGBb'

# Credenciais de conexão
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, virtual_host=vhost, credentials=credentials)

# Estabelecendo conexão
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declarar o exchange do tipo direct e garantir que ele é durável
exchange_name = 'e.sigma.stok.pedido.create'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

# Declarar a fila e bindar ao exchange com uma routing key
queue_name = 'q.sigma.stok.pedido.create'  # Nome da fila
routing_key = 'pedido_create'  # Defina a routing key
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

# Mensagem a ser enviada
mensagem = {
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

# Loop para enviar a mensagem a cada 5 segundos
while True:
    mensagem_json = json.dumps(mensagem)  # Converte o dicionário para JSON
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=mensagem_json)
    print(f"Mensagem enviada: {mensagem_json}")
    
    # Espera 2 segundos antes de enviar a próxima mensagem
    time.sleep(2)

# Fechar a conexão (essa linha nunca será atingida no loop infinito, mas está aqui por boas práticas)
connection.close()