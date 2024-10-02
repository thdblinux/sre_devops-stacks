import pika

# Conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Não declare a exchange, use a existente
# channel.exchange_declare(exchange='amq.topic', exchange_type='topic')

# Enviar uma mensagem
routing_key = 'sigma.pedido.create'
message = {
    "pedidoId": "12345",
    "codigoRastreio": "ABC123456",
    "quantidade": 10,
    "insumo": "Insumo A",
    "dataPedido": "2024-10-01T12:00:00Z"
}

channel.basic_publish(
    exchange='amq.topic',
    routing_key=routing_key,
    body=str(message)
)

print(f"Mensagem enviada: {message}")
connection.close()
