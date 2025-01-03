import pika
import json

# Configurações de conexão
rabbitmq_host = '10.2.13.71'  # Substitua pelo IP do seu servidor RabbitMQ
vhost = 'eco_dev'
username = 'accessadmin'
password = '35lkK69gwoF0hGBb'

# Estabelecendo conexão com RabbitMQ
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, virtual_host=vhost, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Callback para processar as mensagens recebidas
def callback(ch, method, properties, body):
    message = json.loads(body)
    print("Mensagem recebida:", message)

# Consumir mensagens da fila
channel.basic_consume(queue='q.sigma.stok.pedido.create', on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens. Pressione CTRL+C para sair.')
channel.start_consuming()