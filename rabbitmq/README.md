# Explicação Simples do Fluxo de Mensageria entre a NASA e Startrek

## Analogia
Imagine o fluxo de mensageria entre a NASA e Startrek como a comunicação interestelar entre duas estações espaciais, com cada parte desempenhando um papel específico no envio e recebimento de mensagens.

- **Estação Espacial Exchange**: É como um centro de distribuição de cartas. Recebe as cartas (mensagens) e decide para onde elas devem ir. No nosso exemplo, estamos usando o exchange `amq.topic`, que direciona as mensagens baseadas em tipos específicos. Entre NASA e Startrek, há uma Exchange, que pode ser vista como um centro de distribuição espacial. Ela recebe as mensagens da NASA e as direciona corretamente para Startrek, de acordo com o tipo de comunicação (ex. dados de coordenação de voo ou atualizações de status).

- **Fila (Queue)**: São as gavetas de cartas. Cada gaveta recebe cartas de acordo com o endereço (routing key). Neste caso, temos filas que armazenam as mensagens até que um consumidor esteja pronto para lê-las.

- **NASA Produtor (Producer)**: A NASA é o responsável por criar e enviar as mensagens para Startrek. Em termos de um sistema de mensageria, a NASA atua como o Produtor, gerando dados sobre missões espaciais, coordenadas e comandos que são transmitidos. É quem escreve e envia cartas. No nosso caso, é o script `send_message.py`. Ele cria a mensagem e a publica na exchange.

- **Startrek Consumidor (Consumer)**: É quem recebe e lê as cartas. Neste caso, é o script `receive_message.py`. Ele se conecta à fila e espera por mensagens. Startrek é a nave estelar que recebe essas mensagens e executa as ações necessárias. Aqui, Startrek funciona como o Consumidor, processando as mensagens que chegam e aplicando-as às suas operações, como manobras e atualizações de status.

- **Conexões (Connections)**: É como o caminho entre o produtor e o consumidor. Quando o produtor envia uma mensagem ou o consumidor lê uma mensagem, uma conexão é estabelecida entre eles através do RabbitMQ.

- **Canais (Channels)**: Dentro de uma conexão, temos canais que funcionam como tubos para enviar e receber mensagens. Um canal é uma forma de multiplexar várias mensagens e comandos em uma única conexão, permitindo que o sistema seja mais eficiente.

## Informações do Sistema
Na console do RabbitMQ, você pode observar informações úteis sobre o estado atual do sistema:

- **Connections**: 1: Indica que há uma conexão ativa entre o produtor ou consumidor e o RabbitMQ.
- **Channels**: 1: Indica que há um canal aberto na conexão, permitindo a comunicação entre o produtor e o consumidor.
- **Exchanges**: 7: Mostra que existem sete exchanges configuradas no RabbitMQ. Essas exchanges são responsáveis por rotear mensagens para as filas apropriadas.
- **Queues**: 1: Indica que há uma fila configurada, onde as mensagens estão sendo armazenadas até serem consumidas.
- **Consumers**: 1: Mostra que há um consumidor ativo ouvindo a fila e pronto para processar as mensagens.

## Fluxo do Sistema

### Passo 1: Enviando Mensagens
O script `send_message.py` é o responsável por criar e enviar uma mensagem para o RabbitMQ.

Por exemplo, ele envia uma mensagem que contém detalhes de um pedido, como `pedidoId`, `codigoRastreio`, `quantidade`, `insumo`, e informações específicas para o `Stok` e `Sigma`.

```bash
python3 send_message.py
```
```bash
Mensagem enviada: {
    "dataHoraOperacao": "2024-09-14T00:00:00",
    "codigoRastreio": "a1sd24ew-s221ds74-a21sd1f-asd1",
    "pedidoTransferencia": {
        "depositoRequistante": "207030",
        "codigoRastreio": "a1sd24ew-s221ds74-a21sd1f-asd1",
        "itens": [
            {
                "codigo": "00000001",
                "qtdSolicitada": 1
            },
            {
                "codigo": "00000002",
                "qtdSolicitada": 120
            }
        ],
        "qtdTotalItens": 2
    }
}
```
**Passo 2: Aguardando Mensagens**

O script receive_message.py é responsável por ouvir as mensagens que chegam à fila. Ele está em um loop, esperando por novas mensagens.
```bash
python3 receive_message.py
```
Quando uma mensagem chega, você verá:

```bash
Aguardando mensagens. Para sair, pressione CTRL+C
Recebido b"{
    \"dataHoraOperacao\": \"2024-09-14T00:00:00\",
    \"codigoRastreio\": \"a1sd24ew-s221ds74-a21sd1f-asd1\",
    \"pedidoTransferencia\": {
        \"depositoRequistante\": \"207030\",
        \"codigoRastreio\": \"a1sd24ew-s221ds74-a21sd1f-asd1\",
        \"itens\": [
            {
                \"codigo\": \"00000001\",
                \"qtdSolicitada\": 1
            },
            {
                \"codigo\": \"00000002\",
                \"qtdSolicitada\": 120
            }
        ],
        \"qtdTotalItens\": 2
    }
}"
```
## Destaques do Processo

- **Durabilidade:** As mensagens enviadas são armazenadas de forma durável, o que significa que mesmo que o sistema falhe, as mensagens não serão perdidas.
- **Desacoplamento:** O produtor e o consumidor estão desacoplados. Isso significa que eles não precisam estar ativos ao mesmo tempo, permitindo maior flexibilidade e escalabilidade no sistema.
- **Roteamento:** O uso de routing keys permite que as mensagens sejam direcionadas para as filas corretas. Neste caso, estamos usando uma chave de roteamento para que a mensagem do pedido seja enviada para a fila apropriada.
- **Conexões e Canais:** A comunicação entre o produtor, o consumidor e o RabbitMQ ocorre através de conexões e canais. As conexões estabelecem um caminho entre os componentes, e os canais permitem a troca de várias mensagens de forma eficiente.

## Conclusão
Esse fluxo de mensageria facilita a comunicação entre diferentes partes do sistema, permitindo que a aplicação envie e receba dados de forma eficiente e confiável. É uma maneira eficaz de garantir que informações importantes sejam entregues e processadas, mesmo que as partes que enviam e recebem não estejam sempre disponíveis.