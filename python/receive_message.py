import pika

def callback(ch, method, properties, body):
    print(f"Recebido {body}")

# Conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar a fila (caso ainda não tenha sido declarada)
channel.queue_declare(queue='q.stok.pedido.create')

# Vínculo da fila à exchange
channel.queue_bind(exchange='amq.topic', queue='q.stok.pedido.create', routing_key='sigma.pedido.*')

# Configurar o consumidor
channel.basic_consume(queue='q.stok.pedido.create', on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens. Para sair, pressione CTRL+C')
channel.start_consuming()