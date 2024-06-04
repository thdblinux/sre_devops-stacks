## O que é o Helm?
O Helm é um gerenciador de pacotes para Kubernetes que facilita a definição, instalação e atualização de aplicações complexas no Kubernetes. Com ele você pode definir no detalhe como a sua aplicação será instalada, quais configurações serão utilizadas e como será feita a atualização da aplicação.

Mas para que você possa utilizar o Helm, a primeira coisa é fazer a sua instalação. Vamos ver como realizar a instalação do Helm na sua máquina Linux.

Lembrando que o Helm é um projeto da CNCF e é mantido pela comunidade, ele funciona em máquinas Linux, Windows e MacOS.

Para realizar a instalação no Linux, podemos utilizar diferentes formas, como baixar o binário e instalar manualmente, utilizar o gerenciador de pacotes da sua distribuição ou utilizar o script de instalação preparado pela comunidade.

Vamos ver como realizar a instalação do Helm no Linux utilizando o script de instalação, mas fique a vontade de utilizar a forma que você achar mais confortável, e tire todas as suas dúvidas no site da documentação oficial do Helm.

Para fazer a instalação, vamos fazer o seguinte:
```sh
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
Com o comando acima, você irá baixar o script de instalação utilizando o curl, dar permissão de execução para o script e executar o script para realizar a instalação do Helm na sua máquina.

A saída será algo assim:
```sh
Downloading https://get.helm.sh/helm-v3.14.0-linux-amd64.tar.gz
Verifying checksum... Done.
Preparing to install helm into /usr/local/bin
helm installed into /usr/local/bin/helm
```
Vamos ver se a instalação foi realizada com sucesso, executando o comando helm version:
```sh
helm version
```
No meu caso, no momento de criação desse material eu tenho a seguinte saída:
```sh
version.BuildInfo{Version:"v3.14.0", GitCommit:"3fc9f4b2638e76f26739cd77c7017139be81d0ea", GitTreeState:"clean", GoVersion:"go1.21.5"}
```
Pronto, agora que já temos o Helm instalado, já podemos começar a nossa brincadeira.

Durante o dia de hoje, eu quero ensinar o Helm de uma maneira diferente do que estamos acostumados a ver por aí. Vamos focar inicialmente na criação de Charts, e depois vamos ver como instalar e atualizar aplicações utilizando o Helm, de uma maneira mais natural e prática.

## O que é um Chart?
Um Chart é um pacote que contém informações necessárias para criar instâncias de aplicações Kubernetes. É com ele que iremos definir como a nossa aplicação será instalada, quais configurações serão utilizadas e como será feita a atualização da aplicação.

Um Chart, normalmente é composto por um conjunto de arquivos que definem a aplicação, e um conjunto de templates que definem como a aplicação será instalada no Kubernetes.

Vamos parar de falar e vamos criar o nosso primeiro Chart, acho que ficará mais fácil de entender.

## Criando o nosso primeiro Chart
Para o nosso exemplo, vamos usar novamente a aplicação de exemplo chamada Giropops-Senhas, que é uma aplicação que gera senhas aleatórias que criamos durante uma live no canal da LINUXtips.

Ela é uma aplicação simples, é uma aplicação em Python, mas especificamente uma aplicação Flask, que gera senhas aleatórias e exibe na tela. Ela utiliza um Redis para armazenar temporariamente as senhas geradas.

Simples como voar!

A primeira coisa que temos que fazer é clonar o repositório da aplicação, para isso, execute o comando abaixo:
```sh
git clone git@github.com:badtuxx/giropops-senhas.git
```
Com isso temos um diretório chamado giropops-senhas com o código da aplicação, vamos acessa-lo:
```sh
cd giropops-senhas
```
O conteúdo do diretório é o seguinte:

app.py  LICENSE  requirements.txt  static  tailwind.config.js  templates
Pronto, o nosso repo já está clonado, agora vamos começar com o nosso Chart.

A primeira coisa que iremos fazer, somente para facilitar o nosso entendimento, é criar os manifestos do Kubernetes para a nossa aplicação. Vamos criar um Deployment e um Service para o Giropops-Senhas e para o Redis.

Vamos começar com o Deployment do Redis, para isso, crie um arquivo chamado `redis-deployment.yaml` com o seguinte conteúdo:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: redis
  name: redis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - image: redis
        name: redis
        ports:
          - containerPort: 6379
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "250m"
```
Agora vamos criar o Service do Redis, para isso, crie um arquivo chamado `redis-service.yaml` com o seguinte conteúdo:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
  type: ClusterIP
```
Agora vamos criar o Deployment do Giropops-Senhas, para isso, crie um arquivo chamado `giropops-senhas-deployment.yaml` com o seguinte conteúdo:
```sh
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: giropops-senhas
  name: giropops-senhas
spec:
  replicas: 2
  selector:
    matchLabels:
      app: giropops-senhas
  template:
    metadata:
      labels:
        app: giropops-senhas
    spec:
      containers:
      - image: linuxtips/giropops-senhas:1.0
        name: giropops-senhas
        ports:
        - containerPort: 5000
        imagePullPolicy: Always
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "250m"
```
E finalmente, vamos criar o Service do Giropops-Senhas, para isso, crie um arquivo chamado `giropops-senhas-service.yaml` com o seguinte conteúdo:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: giropops-senhas
  labels:
    app: giropops-senhas
spec:
  selector:
    app: giropops-senhas
  ports:
    - protocol: TCP
      port: 5000
      nodePort: 32500
      targetPort: 5000
      name: tcp-app
  type: NodePort
```
Manifesos criados! Perceba que não temos nada de novo até agora, somente criamos os manifestos do Kubernetes para a nossa aplicação como já fizemos anteriormente.

Mas o pq eu fiz isso? Simples, para que você possa entender que um Chart é basicamente isso, um conjunto de manifestos do Kubernetes que definem como a sua aplicação será instalada no Kubernetes.

E você deve estar falando: Esse Jeferson está de brincadeira, pois eu já sei como fazer isso, cadê a novidade? Cadê o Helm? Calma calabrezo! 😄

Bem, a ideia de criar os manifestos é somente para nos guiar durante a criação do nosso Chart.

Com os arquivos para nos ajudar, vamos criar o nosso Chart.

Para criar o nosso Chart, poderiamos utilizar o comando helm create, mas eu quero fazer de uma maneira diferente, quero criar o nosso Chart na mão, para que você possa entender como ele é composto, e depois voltamos para o helm create para criar os nossos próximos Charts.

Bem, a primeira coisa que temos que fazer é criar um diretório para o nosso Chart, vamos criar um diretório chamado `giropops-senhas-chart`:
```sh
mkdir giropops-senhas-chart
```
Agora vamos acessar o diretório:
```sh
cd giropops-senhas-chart
```
Bem, agora vamos começar a criar a nossa estrutura de diretórios para o nosso Chart, e o primeiro cara que iremos criar é o Chart.yaml, que é o arquivo que contém as informações sobre o nosso Chart, como o nome, a versão, a descrição, etc.

Vamos criar o arquivo Chart.yaml com o seguinte conteúdo:
```yaml
apiVersion: v2
name: giropops-senhas
description: Esse é o chart do Giropops-Senhas, utilizados nos laboratórios de Kubernetes.
version: 0.1.0
appVersion: 0.1.0
sources:
  - https://github.com/badtuxx/giropops-senhas
```
Nada de novo até aqui, somente criamos o arquivo Chart.yaml com as informações sobre o nosso Chart. Agora vamos para o nosso próximo passo, criar o diretório templates que é onde ficarão os nossos manifestos do Kubernetes.

Vamos criar o diretório `templates:`
```sh
mkdir templates
```
Vamos mover os manifestos que criamos anteriormente para o diretório `templates:`
```sh
mv ../redis-deployment.yaml templates/
mv ../redis-service.yaml templates/
mv ../giropops-senhas-deployment.yaml templates/
mv ../giropops-senhas-service.yaml templates/
```
Vamos deixar eles quietinhos lá por enquanto, e vamos criar o próximo arquivo que é o `values.yaml`. Esse é uma peça super importante do nosso Chart, pois é nele que iremos definir as variáveis que serão utilizadas nos nossos manifestos do Kubernetes, é nele que o Helm irá se basear para criar os manifestos do Kubernetes, ou melhor, para renderizar os manifestos do Kubernetes.

Quando criamos os manifestos para a nossa App, nós deixamos ele da mesma forma como usamos para criar os manifestos do Kubernetes, mas agora, com o Helm, nós podemos utilizar variáveis para definir os valores que serão utilizados nos manifestos, e é isso que iremos fazer, e é isso que é uma das mágicas do Helm.

Vamos criar o arquivo `values.yaml` com o seguinte conteúdo:
```yaml
giropops-senhas:
  name: "giropops-senhas"
  image: "linuxtips/giropops-senhas:1.0"
  replicas: "3"
  port: 5000
  labels:
    app: "giropops-senhas"
    env: "labs"
    live: "true"
  service:
    type: "NodePort"
    port: 5000
    targetPort: 5000
    name: "giropops-senhas-port"
  resources:
    requests:
      memory: "128Mi"
      cpu: "250m"
    limits:
      memory: "256Mi"
      cpu: "500m"

redis:
  image: "redis"
  replicas: 1
  port: 6379
  labels:
    app: "redis"
    env: "labs"
    live: "true"
  service:
    type: "ClusterIP"
    port: 6379
    targetPort: 6379
    name: "redis-port"
  resources:
    requests:
      memory: "128Mi"
      cpu: "250m"
    limits:
      memory: "256Mi"
      cpu: "500m"
```
Não confunda o arquivo acima com os manifestos do Kubernetes, o arquivo acima é apenas algumas definições que iremos usar no lugar das variáveis que defineremos nos manifestos do Kubernetes.

Precisamos entender como ler o arquivo acima, e é bem simples, o arquivo acima é um arquivo YAML, e nele temos duas chaves, giropops-senhas e redis, e dentro de cada chave temos as definições que iremos utilizar, por exemplo:

- `giropops-senhas:`
   - `image:` A imagem que iremos utilizar para o nosso Deployment
   - `replicas:` A quantidade de réplicas que iremos utilizar para o nosso Deployment
   - `port:` A porta que iremos utilizar para o nosso Service
   - `labels:` As labels que iremos utilizar para o nosso Deployment
   - `service:` As definições que iremos utilizar para o nosso Service
   - `resources:` As definições de recursos que iremos utilizar para o nosso Deployment
- `redis:`
   - `image:` A imagem que iremos utilizar para o nosso Deployment
   - `replicas:` A quantidade de réplicas que iremos utilizar para o nosso Deployment
   - `port:` A porta que iremos utilizar para o nosso Service
   - `labels:` As labels que iremos utilizar para o nosso Deployment
   - `service:` As definições que iremos utilizar para o nosso Service
   - `resources:` As definições de recursos que iremos utilizar para o nosso Deployment
E nesse caso, caso eu queira usar o valor que está definido para` image`, eu posso utilizar a variável  no meu manifesto do Kubernetes, onde:

- : É a variável que o `Helm` utiliza para acessar as variáveis que estão definidas no arquivo `values.yaml`, e o resto é a chave que estamos acessando.
Entendeu? Eu sei que é meu confuso no começo, mas treinando irá ficar mais fácil.

Vamos fazer um teste rápido, como eu vejo o valor da porta que está definida para o Service do Redis?

Pensou?

Já sabemos que temos que começar com .Values, para representar o arquivo `values.yaml`, e depois temos que acessar a chave redis, e depois a chave service, e depois a chave port, então, o valor que está definido para a porta que iremos utilizar para o Service do Redis é .

Sempre você tem que respeitar a indentação do arquivo `values.yaml`, pois é ela que define como você irá acessar as chaves, certo?

Dito isso, já podemos começar a substituir os valores do que está definido nos manifestos do Kubernetes pelos valores que estão definidos no arquivo values.yaml. Iremos sair da forma estática para a forma dinâmica, é o Helm em ação!

Vamos começar com o arquivo` redis-deployment.yaml`, e vamos substituir o que está definido por variáveis, e para isso, vamos utilizar o seguinte conteúdo:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels: 
    app: redis 
  name: redis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - image: {{ .Values.redis.image }}
        name: redis
        ports:
          - containerPort: {{ .Values.redis.port }}
        resources:
          limits:
            memory: {{ .Values.redis.resources.limits.memory }}
            cpu: {{ .Values.redis.resources.limits.cpu }}
          requests:
            memory: {{ .Values.redis.resources.requests.memory }}
            cpu: {{ .Values.redis.resources.requests.cpu }}
```
Veja que estamos usando e abusando das variáveis que estão definidas no arquivo `values.yaml`, agora vou explicar o que estamos fazendo:
```sh
- `image`: Estamos utilizando a variável `{{ .Values.redis.image }}` para definir a imagem que iremos utilizar para o nosso Deployment
- `name`: Estamos utilizando a variável `{{ .Values.redis.name }}` para definir o nome que iremos utilizar para o nosso Deployment
- `replicas`: Estamos utilizando a variável `{{ .Values.redis.replicas }}` para definir a quantidade de réplicas que iremos utilizar para o nosso Deployment
- `resources`: Estamos utilizando as variáveis `{{ .Values.redis.resources.limits.memory }}`, `{{ .Values.redis.resources.limits.cpu }}`, `{{ .Values.redis.resources.requests.memory }}` e `{{ .Values.redis.resources.requests.cpu }}` para definir as definições de recursos que iremos utilizar para o nosso Deployment.
```
Com isso, ele irá utilizar os valores que estão definidos no arquivo values.yaml para renderizar o nosso manifesto do Kubernetes, logo, quando precisar alterar alguma configuração, basta alterar o arquivo values.yaml, e o Helm irá renderizar os manifestos do Kubernetes com os valores definidos.

Vamos fazer o mesmo para os outros manifestos do Kubernetes, e depois vamos ver como instalar a nossa aplicação utilizando o Helm.

Vamos fazer o mesmo para o arquivo `redis-service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: {{ .Values.redis.service.port }}
      targetPort: {{ .Values.redis.service.port }}
  type: {{ .Values.redis.service.type }}
E para o arquivo giropops-senhas-deployment.yaml:

apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: giropops-senhas
  name: giropops-senhas
spec:
  replicas: {{ .Values.giropops-senhas.replicas }}
  selector:
    matchLabels:
      app: giropops-senhas
  template:
    metadata:
      labels:
        app: giropops-senhas
    spec:
      containers:
      - image: {{ .Values.giropops-senhas.image }}
        name: giropops-senhas
        ports:
        - containerPort: {{ .Values.giropops-senhas.service.port }}
        imagePullPolicy: Always
        resources:
          limits:
            memory: {{ .Values.giropops-senhas.resources.limits.memory }}
            cpu: {{ .Values.giropops-senhas.resources.limits.cpu }}
          requests:
            memory: {{ .Values.giropops-senhas.resources.requests.memory }}
            cpu: {{ .Values.giropops-senhas.resources.requests.cpu }}
```
E para o arquivo giropops-senhas-service.yaml:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: giropops-senhas
  labels:
    app: giropops-senhas
spec:
  selector:
    app: giropops-senhas
  ports:
    - protocol: TCP
      port: {{ .Values.giropops-senhas.service.port }}
      nodePort: {{ .Values.giropops-senhas.service.nodePort }}
      targetPort: {{ .Values.giropops-senhas.service.port }}
  type: {{ .Values.giropops-senhas.service.type }}
```
Agora já temos todos os nosso manifestos mais dinâmicos, e portanto já podemos chama-los de Templates, que é o nome que o Helm utiliza para os manifestos do Kubernetes que são renderizados utilizando as variáveis.

Ahhh, temos que criar um diretório chamado charts para que o Helm possa gerenciar as dependências do nosso Chart, mas como não temos dependências, podemos criar um diretório vazio, vamos fazer isso:
```sh
mkdir charts
```
Pronto, já temos o nosso Chart criado!

Agora vamos testa-lo para ver se tudo está funcionando como esperamos.

## Instalando o nosso Chart
Para que possamos utilizar o nosso Chart, precisamos utilizar o comando helm install, que é o comando que utilizamos para instalar um Chart no Kubernetes.

Vamos instalar o nosso Chart, para isso, execute o comando abaixo:
```sh
helm install giropops-senhas ./
```
Se tudo ocorrer bem, você verá a seguinte saída:
```sh
NAME: giropops-senhas
LAST DEPLOYED: Thu Feb  8 16:37:58 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```
O nosso Chart foi instalado com sucesso!

Vamos listar os Pods para ver se eles estão rodando, execute o comando abaixo:
```sh
kubectl get pods
```
A saída será algo assim:
```sh
NAME                                READY   STATUS    RESTARTS      AGE
giropops-senhas-7d4fddc49f-9zfj9    1/1     Running   0             42s
giropops-senhas-7d4fddc49f-dn996    1/1     Running   0             42s
giropops-senhas-7d4fddc49f-fpvh6    1/1     Running   0             42s
redis-deployment-76c5cdb57b-wf87q   1/1     Running   0             42s
```
Perceba que temos 3 Pods rodando para a nossa aplicação Giropops-Senhas, e 1 Pod rodando para o Redis, conforme definimos no arquivo `values.yaml`.

Agora vamos listar os Charts que estão instalados no nosso Kubernetes, para isso, execute o comando abaixo:
```sh
helm list
```
Se você quiser ver de alguma namespace específica, você pode utilizar o comando `helm list -n <namespace>`, mas no nosso caso, como estamos utilizando a namespace default, não precisamos especificar a namespace.

Para ver mais detalhes do Chart que instalamos, você pode utilizar o comando `helm get`, para isso, execute o comando abaixo:
```sh
helm get all giropops-senhas
```
A saída será os detalhes do Chart e os manifestos que foram renderizados pelo Helm.

Vamos fazer uma alteração no nosso Chart, e vamos ver como atualizar a nossa aplicação utilizando o Helm.

## Atualizando o nosso Chart
Vamos fazer uma alteração no nosso Chart, e vamos ver como atualizar a nossa aplicação utilizando o Helm.

Vamos editar o `values.yaml` e alterar a quantidade de réplicas que estamos utilizando para a nossa aplicação Giropops-Senhas, para isso, edite o arquivo values.yaml e altere a quantidade de réplicas para 5:
```yaml
giropops-senhas:
  name: "giropops-senhas"
  image: "linuxtips/giropops-senhas:1.0"
  replicas: "5"
  port: 5000
  labels:
    app: "giropops-senhas"
    env: "labs"
    live: "true"
  service:
    type: "NodePort"
    port: 5000
    targetPort: 5000
    name: "giropops-senhas-port"
  resources:
    requests:
      memory: "128Mi"
      cpu: "250m"
    limits:
      memory: "256Mi"
      cpu: "500m"
redis:
  image: "redis"
  replicas: 1
  port: 6379
  labels:
    app: "redis"
    env: "labs"
    live: "true"
  service:
    type: "ClusterIP"
    port: 6379
    targetPort: 6379
    name: "redis-port"
  resources:
    requests:
      memory: "128Mi"
      cpu: "250m"
    limits:
      memory: "256Mi"
      cpu: "500m"
```
A única coisa que alteramos foi a quantidade de réplicas que estamos utilizando para a nossa aplicação Giropops-Senhas, de 3 para 5.

Vamos agora pedir para o Helm atualizar a nossa aplicação, para isso, execute o comando abaixo:
```sh
helm upgrade giropops-senhas ./
```
Se tudo ocorrer bem, você verá a seguinte saída:
```sh
Release "giropops-senhas" has been upgraded. Happy Helming!
NAME: giropops-senhas
LAST DEPLOYED: Thu Feb  8 16:46:26 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
```
Agora vamos ver se o número de réplicas foi alterado, para isso, execute o comando abaixo:
````sh
giropops-senhas-7d4fddc49f-9zfj9    1/1     Running   0             82s
giropops-senhas-7d4fddc49f-dn996    1/1     Running   0             82s
giropops-senhas-7d4fddc49f-fpvh6    1/1     Running   0             82s
redis-deployment-76c5cdb57b-wf87q   1/1     Running   0             82s
giropops-senhas-7d4fddc49f-ll25z    1/1     Running   0             18s
giropops-senhas-7d4fddc49f-w8p7r    1/1     Running   0             18s
````
Agora temos mais dois Pods em execução, da mesma forma que definimos no arquivo `values.yaml`.

Agora vamos remover a nossa aplicação:
```sh
helm uninstall giropops-senhas
```
A saída será algo assim:
```sh
release "giropops-senhas" uninstalled
```
Já era, a nossa aplicação foi removida com sucesso!

Como eu falei, nesse caso criamos tudo na mão, mas eu poderia ter usado o comando helm create para criar o nosso Chart, e ele teria criado a estrutura de diretórios e os arquivos que precisamos para o nosso Chart, e depois teríamos que fazer as alterações que fizemos manualmente.

A estrutura de diretórios que o `helm create` cria é a seguinte:
````sh
giropops-senhas-chart/
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml
````
Eu não criei dessa forma, pois acho que iria complicar um pouco o nosso entendimento inicial, pois ele iria criar mais coisas que iriamos utilizar, mas em contrapartida, podemos utiliza-lo para nos basear para os nossos próximos Charts.
Ele é o nosso amigo, e sim, ele pode nos ajudar! hahaha

Agora eu preciso que você pratique o máximo possível, brincando com as diversas opções que temos disponíveis no Helm, e o mais importante, use e abuse da documentação oficial do Helm, ela é muito rica e tem muitos exemplos que podem te ajudar.

Bora deixar o nosso Chart ainda mais legal?

## Utilizando range e o if no Helm
O Helm tem uma funcionalidade muito legal que é o range, que é uma estrutura de controle que nos permite iterar sobre uma lista de itens, e isso é muito útil quando estamos trabalhando com listas de itens, como por exemplo, quando estamos trabalhando com os manifestos do Kubernetes.

Para que você consiga utilizar o range, precisamos antes entender sua estrutura básica, por exemplo, temos um arquivo com 4 frutas, e queremos listar todas elas, como eu faria isso?

Primeiro, vamos criar um arquivo chamado frutas.yaml com o seguinte conteúdo:
```yaml
frutas:
  - banana
  - maçã
  - uva
  - morango
```
Agora vamos pegar fruta por fruta, e colocando a seguinte frase antes de cada uma delas: "Eu gosto de".

Para isso, vamos criar um arquivo chamado eu-gosto-frutas.yaml com o seguinte conteúdo:
```yaml
{{- range .Values.frutas }}
Eu gosto de {{ . }}
{{- end }}
```
O resultado será:
```sh
Eu gosto de banana
Eu gosto de maçã
Eu gosto de uva
Eu gosto de morango
```

Ficou fácil, certo? O `range` percorreu toda a lista e ainda adicionou a frase que queríamos.

Vamos imaginar que eu tenho uma lista de portas que eu quero expor para a minha aplicação, e eu quero criar um Service para cada porta que eu tenho na minha lista, como eu faria isso?

Por exemplo, a nossa aplicação Giropops-Senhas, ela tem 2 portas que ela expõe, a porta 5000 e a porta 8088. A porta 5000 é a porta que a aplicação escuta, e a porta 8088 é a porta que a aplicação expõe as métricas para o Prometheus.

Outra função super interessante e que é muito útil é o if, que é uma estrutura de controle que nos permite fazer uma verificação se uma condição é verdadeira ou falsa, e baseado nisso, podemos fazer alguma coisa ou não.

a Estrutura básica do if é a seguinte:
```sh
{{- if eq .Values.giropopsSenhas.service.type "NodePort" }}
  nodePort: {{ .Values.giropopsSenhas.service.nodePort }}
  targetPort: {{ .Values.giropopsSenhas.service.targetPort }}
{{- else }}
  targetPort: {{ .Values.giropopsSenhas.service.targetPort }}
{{- end }}
```
Onde:
```sh
- `{{- if eq .Values.giropopsSenhas.service.type "NodePort" }}`: Verifica se o valor que está definido para a chave `type` é igual a `NodePort`
- `nodePort: {{ .Values.giropopsSenhas.service.nodePort }}`: Se a condição for verdadeira, ele irá renderizar o valor que está definido para a chave `nodePort`
- `targetPort: {{ .Values.giropopsSenhas.service.targetPort }}`: Se a condição for verdadeira, ele irá renderizar o valor que está definido para a chave `targetPort`
- `{{- else }}`: Se a condição for falsa, ele irá renderizar o valor que está definido para a chave `targetPort`
- `{{- end }}`: Finaliza a estrutura de controle
```
Simples como voar! Bora lá utilizar essas duas fun´ções para deixar o nosso Chart ainda mais legal.

Vamos começar criando um arquivo chamado giropops-senhas-service.yaml com o seguinte conteúdo:
```yaml
{{- range .Values.giropops-senhas.ports }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .name }}
  labels:
    app: {{ .name }}
spec:
  type: {{ .serviceType }}
  ports:
  - name: {{ .name }}
    port: {{ .port }}
{{- if eq .serviceType "NodePort" }}
    nodePort: {{ .NodePort }}
{{- end }}
    targetPort: {{ .targetPort }}
  selector:
    app: giropops-senhas
---
{{- end }}
```
No arquivo acima, estamos utilizando a função `range` para iterar sobre a lista de portas que queremos expor para a nossa aplicação, e estamos utilizando a função `if` para verificar se a porta que estamos expondo é do tipo `NodePort`, e baseado nisso, estamos renderizando o valor que está definido para a chave `nodePort`.

Agora vamos alterar o arquivo `values.yaml` e adicionar a lista de portas que queremos expor para a nossa aplicação, para isso, edite o arquivo `values.yaml` e adicione a lista de portas que queremos expor para a nossa aplicação:
```yaml
giropops-senhas:
  name: "giropops-senhas"
  image: "linuxtips/giropops-senhas:1.0"
  replicas: "3"
  ports:
    - port: 5000
      targetPort: 5000
      name: "giropops-senhas-port"
      serviceType: NodePort
      NodePort: 32500
    - port: 8088
      targetPort: 8088
      name: "giropops-senhas-metrics"
      serviceType: ClusterIP
  labels:
    app: "giropops-senhas"
    env: "labs"
    live: "true"
  resources:
    requests:
      memory: "128Mi"
      cpu: "250m"
    limits:
      memory: "256Mi"
      cpu: "500m"
redis:
  image: "redis"
  replicas: 1
  port: 6379
  labels:
    app: "redis"
    env: "labs"
    live: "true"
  service:
    type: "ClusterIP"
    port: 6379
    targetPort: 6379
    name: "redis-port"
  resources:
    requests:
      memory: "128Mi"
      cpu: "250m"
    limits:
      memory: "256Mi"
      cpu: "500m"
```
Temos algumas coisas novas no arquivo `values.yaml.` O objetivo da mudança é deixar o arquivo ainda mais dinâmico, e para isso, adicionamos adicionamos mais informações sobre as portas que iremos utilizar. Deixamos as informações mais organizadas para facilitar a dinâmica criada no arquivo `giropops-senhas-service.yaml`.

Poderiamos ainda criar um único template para realizar o deploy do Redis e do Giropops-Senhas, somente para que possamos gastar um pouquinho mais do nosso conhecimento, ou seja, isso aqui é muito mais para fins didáticos do que para a vida real, mas vamos lá, vamos criar um arquivo chamado `giropops-senhas-deployment.yaml` com o seguinte conteúdo:
```yaml
{{- range $component, $config := .Values.deployments }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ $component }}
  labels:
    app: {{ $config.labels.app }}
spec:
  replicas: {{ $config.replicas }}
  selector:
    matchLabels:
      app: {{ $config.labels.app }}
  template:
    metadata:
      labels:
        app: {{ $config.labels.app }}
    spec:
      containers:
      - name: {{ $component }}
        image: {{ $config.image }}
        ports:
        {{- range $config.ports }}
        - containerPort: {{ .port }}
        {{- end }}
        resources:
          requests:
            memory: {{ $config.resources.requests.memory }}
            cpu: {{ $config.resources.requests.cpu }}
          limits:
            memory: {{ $config.resources.limits.memory }}
            cpu: {{ $config.resources.limits.cpu }}
{{- if $config.env }}
        env:
        {{- range $config.env }}
        - name: {{ .name }}
          value: {{ .value }}
        {{- end }}
{{- end }}
---
{{- end }}
```
Estamos utilizando a função range logo no inicio do arquivo, e com ele estamos interando sobre a lista de componentes que temos no nosso arquivo `values.yaml`, ou seja, o Redis e o Giropops-Senhas. Mas também estamos utilizando o range para interar sobre a lista de outras configurações que temos no nosso arquivo` values.yaml`, como por exemplo, as portas que queremos expor para a nossa aplicação e o limite de recursos que queremos utilizar. Ele definiu duas variáveis, `$component` e` $config`, onde `$component` é o nome do componente que estamos interando, e $config é a configuração que estamos interando, fácil!

Agora vamos instalar a nossa aplicação com o comando abaixo:
```sh
helm install giropops-senhas ./
```
A saída será algo assim:
```sh
Error: INSTALLATION FAILED: parse error at (giropops-senhas/templates/services.yaml:1): bad character U+002D '-'
```
Parece que alguma coisa de errado não está certo, certo? hahaha

O que aconteceu foi o seguinte:

Quando estamos utilizando o nome do componente com um hífen, e tentamos passar na utilização do range, o Helm não entende que aquele é o nome do recurso que estamos utilizando, e retorna o erro de `bad character U+002D '-'`.

Para resolver isso, vamos utilizar mais uma função do Helm, que é a função index.

A função `index`nos permite acessar um valor de um mapa baseado na chave que estamos passando, nesse caso seria o `.Values`, e ainda buscar um valor baseado na chave que estamos passando, que é o nome do componente que estamos interando. Vamos ver como ficaria o nosso `services.yaml` com a utilização da função `index:`
```yaml
{{- range (index .Values "giropops-senhas").ports }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .name }}
  labels:
    app: {{ .name }}
spec:
  type: {{ .serviceType }}
  ports:
  - name: {{ .name }}
    port: {{ .port }}
{{- if eq .serviceType "NodePort" }}
    nodePort: {{ .NodePort }}
{{- end }}
    targetPort: {{ .targetPort }}
  selector:
    app: giropops-senhas
---
{{- end }}
```
Pronto, agora acredito que tudo terá um final feliz, para ter certeza, vamos instalar a nossa aplicação com o comando abaixo:
```sh
helm install giropops-senhas ./
```
Se tudo ocorrer bem, você verá a seguinte saída:
```sh
NAME: giropops-senhas
LAST DEPLOYED: Sat Feb 10 12:19:27 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```
Vamos ver se deu bom!
```sh
kubectl get deployment
```
Temos a saída abaixo:
```sh
NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
giropops-senhas-deployment   3/3     3            3           4m1s
redis-deployment             1/1     1            1           4m1s
Agora os Pods:
```
```sh
kubectl get pods
```
A saída:
```sh
NAME                                         READY   STATUS    RESTARTS   AGE
giropops-senhas-deployment-5c547c9cf-979vp   1/1     Running   0          4m40s
giropops-senhas-deployment-5c547c9cf-s5k9x   1/1     Running   0          4m39s
giropops-senhas-deployment-5c547c9cf-zp4s4   1/1     Running   0          4m39s
redis-deployment-69c5869684-cxslb            1/1     Running   0          4m40s
```
Vamos ver os Services:
```sh
kubectl get svc
```
Se a sua saída trouxe os dois serviços, com os nomes `giropops-senhas-port` e `giropops-senhas-metrics`, e com os tipos `NodePort` e `ClusterIP`, `respectivamente`, é um sinal de que deu super bom!
```sh
NAME                      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
giropops-senhas-app       NodePort    10.96.185.6    <none>        5000:32500/TCP   5m1s
giropops-senhas-metrics   ClusterIP   10.96.107.37   <none>        8088/TCP         5m1s
kubernetes                ClusterIP   10.96.0.1      <none>        443/TCP          3d21h
```
Parece que deu ruim, certo?

Ficou faltando o Service do Redis. :/

Vamos resolver, mas antes, vamos mudar um pouco a organização em nosso values.yaml.
```yaml
deployments:
  giropops-senhas:
    name: "giropops-senhas"
    image: "linuxtips/giropops-senhas:1.0"
    replicas: "3"
    labels:
      app: "giropops-senhas"
      env: "labs"
      live: "true"
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "256Mi"
        cpu: "500m"
  redis:
    image: "redis"
    replicas: 1
    port: 6379
    labels:
      app: "redis"
      env: "labs"
      live: "true"
    service:
      type: "ClusterIP"
      port: 6379
      targetPort: 6379
      name: "redis-port"
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "256Mi"
        cpu: "500m"
services:
  giropops-senhas:
    ports:
      - port: 5000
        targetPort: 5000
        name: "giropops-senhas-app"
        serviceType: NodePort
        NodePort: 32500
      - port: 8088
        targetPort: 8088
        name: "giropops-senhas-metrics"
        serviceType: ClusterIP
    labels:
      app: "giropops-senhas"
      env: "labs"
      live: "true"
  redis:
    ports:
      - port: 6379
        targetPort: 6378
        name: "redis-port"
        serviceType: ClusterIP
    labels:
      app: "redis"
      env: "labs"
      live: "true"
```
Precisamos agora atualizar os nossos templates para que eles possam utilizar as novas chaves que criamos no arquivo `values.yaml`.

Vamos atualizar o services.yaml para que ele possa utilizar as novas chaves que criamos no arquivo `values.yaml`:
```yaml
{{- range $component, $config := .Values.services }}
  {{ range $port := $config.ports }}
apiVersion: v1
kind: Service
metadata:
  name: {{ $component }}-{{ $port.name }}
  labels:
    app: {{ $config.labels.app }}
spec:
  type: {{ $port.serviceType }}
  ports:
  - port: {{ $port.port }}
    targetPort: {{ $port.targetPort }}
    protocol: TCP
    name: {{ $port.name }}
    {{ if eq $port.serviceType "NodePort" }}
    nodePort: {{ $port.NodePort }}
    {{ end }}
  selector:
    app: {{ $config.labels.app }}
---
  {{ end }}
{{- end }}
```
Adicionamos um novo `range` para interar sobre a lista de portas que queremos expor para a nossa aplicação, e utilizamos a função index para acessar o valor que está definido para a chave services no arquivo `values.yaml`.

Como o nosso `deployments.yaml` já está atualizado, não precisamos fazer nenhuma alteração nele, o que precisamos é deployar o nosso `Chart` novamente e ver se as nossas mondificações funcionaram.

Temos duas opções, ou realizamos o` uninstall` e o `install` novamente, ou realizamos o upgrade da nossa aplicação.

Vou realizar o` uninstall` e o `install` novamente, para isso, execute os comandos abaixo:
```sh
helm uninstall giropops-senhas
```
E agora:
```sh
helm install giropops-senhas ./
```
Caso eu queira fazer o `upgrade`, eu poderia utilizar o comando abaixo:
```sh
helm upgrade giropops-senhas ./
```
Pronto, se tudo estiver certinho, temos uma saída parecida com a seguinte:
```sh
NAME: giropops-senhas
LAST DEPLOYED: Sat Feb 10 14:05:37 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```
Vamos listar os recursos:
```sh
kubectl get deployments,pods,svc
```
Assim ele trará todos os nossos recursos utilizados pela nossa aplicação.
```sh
NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/giropops-senhas   3/3     3            3           69s
deployment.apps/redis             1/1     1            1           69s

NAME                                   READY   STATUS    RESTARTS   AGE
pod/giropops-senhas-8598bc5699-68sn6   1/1     Running   0          69s
pod/giropops-senhas-8598bc5699-wgnxj   1/1     Running   0          69s
pod/giropops-senhas-8598bc5699-xqssx   1/1     Running   0          69s
pod/redis-69c5869684-62d2h             1/1     Running   0          69s

NAME                              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
service/giropops-senhas-app       NodePort    10.96.119.23   <none>        5000:30032/TCP   69s
service/giropops-senhas-metrics   ClusterIP   10.96.110.83   <none>        8088/TCP         69s
service/kubernetes                ClusterIP   10.96.0.1      <none>        443/TCP          3d22h
service/redis-service             ClusterIP   10.96.77.187   <none>        6379/TCP         69s
Pronto! Tudo criado com sucesso!
```

Agora você já sabe como utilizar o range, index e o if no Helm, e já sabe como criar um Chart do zero, e já sabe como instalar, atualizar e remover a sua aplicação utilizando o Helm