import pika
import json

# Configurações de conexão
rabbitmq_host = 'localhost'  # Substitua pelo IP do seu servidor RabbitMQ
vhost = 'magaluloja1'         # O vhost correto
username = 'accessadmin'
password = '35lkK69gwoF0hGBb'

# Estabelecendo conexão com RabbitMQ
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=rabbitmq_host, virtual_host=vhost, credentials=credentials)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Callback para processar as mensagens recebidas
    def callback(ch, method, properties, body):
        message = json.loads(body)
        print("Mensagem recebida:", message)

    # Consumir mensagens da fila q.magalo.order.create
    channel.basic_consume(queue='q.magalo.order.create', on_message_callback=callback, auto_ack=True)

    print('Aguardando mensagens. Pressione CTRL+C para sair.')
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError:
    print("Erro de conexão com o RabbitMQ. Verifique o endereço do host e as credenciais.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    # Fechar a conexão se ela estiver aberta
    if 'connection' in locals() and connection.is_open:
        connection.close()
