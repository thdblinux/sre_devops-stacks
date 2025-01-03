## O que iremos ver hoje?

Hoje é dia de falar sobre duas coisas super importantes no mundo do Kubernetes, hoje nós vamos falar sobre` Secrets` e `ConfigMaps`.

Sim, essas duas peças fundamentais para que você possa ter a sua aplicação rodando no Kubernetes da melhor forma possível, pois elas são responsáveis por armazenar as informações sensíveis da sua aplicação, como por exemplo, senhas, tokens, chaves de acesso, configurações, etc.

Depois do dia de hoje você vai entender como funciona o armazenamento de informações sensíveis no Kubernetes e como você pode fazer para que a sua aplicação possa consumir essas informações da melhor forma possível.

Bora lá?

## O que são Secrets?

Os Secrets fornecem uma maneira segura e flexível de gerenciar informações sensíveis, como senhas, tokens OAuth, chaves SSH e outros dados que você não quer expor nas configurações de seus aplicaçãos.

Um Secret é um objeto que contém um pequeno volume de informações sensíveis, como uma senha, um token ou uma chave. Essas informações podem ser consumidas por Pods ou usadas pelo sistema para realizar ações em nome de um Pod.

 

### Como os Secrets funcionam

Os Secrets são armazenados no Etcd, o armazenamento de dados distribuído do Kubernetes. Por padrão, eles são armazenados sem criptografia, embora o Etcd suporte criptografia para proteger os dados armazenados nele. Além disso, o acesso aos Secrets é restrito por meio de Role-Based Access Control (RBAC), o que permite controlar quais usuários e Pods podem acessar quais Secrets.

Os Secrets podem ser montados em Pods como arquivos em volumes ou podem ser usados para preencher variáveis de ambiente para um container dentro de um Pod. Quando um Secret é atualizado, o Kubernetes não atualiza automaticamente os volumes montados ou as variáveis de ambiente que se referem a ele.

 

### Tipos de Secrets
Existem vários tipos de Secrets que você pode usar, dependendo de suas necessidades específicas. Abaixo estão alguns dos tipos mais comuns de Secrets:

- **Opaque Secrets** - são os Secrets mais simples e mais comuns. Eles armazenam dados arbitrários, como chaves de API, senhas e tokens. Os Opaque Secrets são codificados em base64 quando são armazenados no Kubernetes, mas não são criptografados. Eles podem ser usados para armazenar dados confidenciais, mas não são seguros o suficiente para armazenar informações altamente sensíveis, como senhas de banco de dados.

- **kubernetes.io/service-account-token** - são usados para armazenar tokens de acesso de conta de serviço. Esses tokens são usados para autenticar Pods com o Kubernetes API. Eles são montados automaticamente em Pods que usam contas de serviço.

- **kubernetes.io/dockercfg e kubernetes.io/dockerconfigjson** - são usados para armazenar credenciais de registro do Docker. Eles são usados para autenticar Pods com um registro do Docker. Eles são montados em Pods que usam imagens de container privadas.

- **kubernetes.io/tls, kubernetes.io/ssh-auth** e **kubernetes.io/basic-auth** - são usados para armazenar certificados TLS, chaves SSH e credenciais de autenticação básica, respectivamente. Eles são usados para autenticar Pods com outros serviços.

- **bootstrap.kubernetes.io/token** - são usados para armazenar tokens de inicialização de cluster. Eles são usados para autenticar nós com o plano de controle do Kubernetes.

Tem mais alguns tipos de Secrets, mas esses são os mais comuns. Você pode encontrar uma lista completa de tipos de Secrets na documentação do Kubernetes.

Cada tipo de Secret tem um formato diferente. Por exemplo, os Secrets Opaque são armazenados como um mapa de strings, enquanto os Secrets TLS são armazenados como um mapa de strings com chaves adicionais para armazenar certificados e chaves, por isso é importante saber qual tipo de Secret você está usando para que você possa armazenar os dados corretamente.

### Antes de criar um Secret, o Base64
Antes de começarmos a criar os nossos Secrets, precisamos entender o que é o Base64, pois esse é um assunto que sempre gera muitas dúvidas e sempre está presente quando falamos de Secrets.

Primeira coisa, Base64 é criptografia? Não, Base64 não é criptografia, Base64 é um esquema de codificação binária para texto que visa garantir que os dados binários possam ser enviados por canais que são projetados para lidar apenas com texto. Esta codificação ajuda a garantir que os dados permaneçam intactos sem modificação durante o transporte.

Base64 está comumente usado em várias aplicações, incluindo e-mail via MIME, armazenamento de senhas complexas, e muito mais.

A codificação Base64 converte os dados binários em uma string de texto ASCII. Essa string contém apenas caracteres que são considerados seguros para uso em URLs, o que torna a codificação Base64 útil para codificar dados que estão sendo enviados pela Internet.

No entanto, a codificação Base64 não é uma forma de criptografia e não deve ser usada como tal. Em particular, ela não fornece nenhuma confidencialidade. Qualquer um que tenha acesso à string codificada pode facilmente decodificá-la e recuperar os dados originais. Entender isso é importante para que você não armazene informações sensíveis em um formato codificado em Base64, pois isso não é seguro.

Agora que você já sabe o que é o Base64, vamos ver como podemos codificar e decodificar uma string usando o Base64.

Para codificar uma string em Base64, você pode usar o comando base64 no Linux. Por exemplo, para codificar a string matrix em Base64, você pode executar o seguinte comando:

```bash
echo -n 'matrix' | base64
```
 

O comando acima irá retornar a string Z2lyb3BvcHM=.

Para decodificar uma string em Base64, você pode usar o comando base64 novamente, mas desta vez com a opção -d. Por exemplo, para decodificar a string Z2lyb3BvcHM= em Base64, você 
pode executar o seguinte comando:

```bash
echo -n 'Z2lyb3BvcHM=' | base64 -d
``` 

O comando acima irá retornar a string matrix, simples como voar!

Estou usando o parâmetro -n no comando echo para que ele não adicione uma nova linha ao final da string, pois isso pode causar problemas ao codificar e decodificar a string.

Pronto, acho que você já está pronto para criar os seus Secrets, então é hora de começar a brincar!


### Criando nosso primeiro Secret
Agora que você já sabe o que são os Secrets, já entender que Base64 não é criptografia e já sabe como codificar e decodificar uma string usando o Base64, vamos criar o nosso primeiro Secret.

Primeiro, vamos criar um Secret do tipo Opaque. Este é o tipo de Secret mais comum, usado para armazenar informações arbitrárias.

Para criar um Secret do tipo Opaque, você precisa criar um arquivo YAML que defina o Secret. Por exemplo, você pode criar um arquivo chamado matrix-secret.yaml com o seguinte conteúdo:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: matrix-secret
type: Opaque
data: # Inicio dos dados
    username: SmVmZXJzb25fbGluZG8=
    password: Z2lyb3BvcHM=
```

O arquivo acima define um Secret chamado matrix-secret com dois campos de dados chamados username e password. O campo password contém a string matrix codificada em Base64. A minha pergunta é: qual é o valor do campo username?

Caso você descubra, eu desafio você a fazer um Tweet ou um post em outra rede social com o valor do campo username e as hashtags #desafioDay8 e #DescomplicandoKubernetes. Se você fizer isso, eu vou te dar um prêmio, mas não vou falar qual é o prêmio, pois isso é um segredo! :D

Outra informação importante que passamos para esse Secret foi o seu tipo, que é Opaque. Você pode ver que o tipo do Secret é definido no campo type do arquivo YAML.

Agora que você já criou o arquivo YAML, você pode criar o Secret usando o comando kubectl create ou kubectl apply. Por exemplo, para criar o Secret usando o comando kubectl create, vá com o seguinte comando:

```bash
kubectl create -f matrix-secret.yaml
```

```
secret/matrix-secret created
```
 

Pronto, o nosso primeiro Secret foi criado! Agora você pode ver o Secret usando o comando kubectl get:

```bash
kubectl get secret matrix-secret
```

```
NAME              TYPE     DATA   AGE
matrix-secret   Opaque   2      10s
```
 

A saída traz o nome do Secret, o seu tipo, a quantidade de dados que ele armazena e a quanto tempo ele foi criado.

Caso você queira ver os dados armazenados no Secret, você pode usar o comando kubectl get com a opção -o yaml:

kubectl get secret matrix-secret -o yaml
```yaml
apiVersion: v1
data:
  password: Z2lyb3BvcHM=
  username: SmVmZXJzb25fbGluZG8=
kind: Secret
metadata:
  creationTimestamp: "2023-05-21T10:38:39Z"
  name: matrix-secret
  namespace: default
  resourceVersion: "466"
  uid: ac816e95-8896-4ad4-9e64-4ee8258a8cda
type: Opaque
```
 

Simples assim! Portanto, mais uma vez, os dados armazenados no Secret não são criptografados e podem ser facilmente decodificados por qualquer pessoa que tenha acesso ao Secret, portanto, é fundamental controlar o acesso aos Secrets e não armazenar informações sensíveis neles.

Você também pode ver os detalhes do Secret usando o comando kubectl describe:

```bash
kubectl describe secret matrix-secret

```
```
Name:         matrix-secret
Namespace:    default
Labels:       <none>
Annotations:  <none

Type:  Opaque

Data
====
password:  8 bytes
username:  15 bytes
```
 

A saída do comando kubectl describe é muito parecido com o conteúdo do arquivo YAML que você criou para definir o Secret, mas com algumas informações adicionais, como o namespace do Secret, os labels e as annotations, coisas que você também pode definir no arquivo YAML.

Caso você queira criar esse mesmo Secret usando o comando kubectl create secret, você pode executar o seguinte comando:

```bash
kubectl create secret generic matrix-secret --from-literal=username=
```

## Usando o nosso primeiro Secret

Agora que já temos o nosso primeiro Secret criado, é hora de saber como usa-lo em um Pod.

Nesse nosso primeiro exemplo, somente irei mostrar como usar o Secret em um Pod, mas ainda sem nenhuma "função" especial, apenas para mostrar como usar o Secret.

Para usar o Secret em um Pod, você precisa definir o campo spec.containers[].env[].valueFrom.secretKeyRef no arquivo YAML do Pod. Eu estou trazendo o campo nesse formato, para que você possa começar a se familiarizar com esse formato, pois você irá usa-lo bastante para buscar alguma informação mais especifica na linha de comando, usando o comando kubectl get, por exemplo.

Voltando ao assunto principal, precisamos criar o nosso Pod, então vamos lá! Crie um arquivo chamado matrix-pod.yaml com o seguinte conteúdo:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: matrix-pod
spec:
  containers:
  - name: matrix-container
    image: nginx
    env: # Inicio da definição das variáveis de ambiente
    - name: USERNAME # Nome da variável de ambiente que será usada no Pod
      valueFrom: # Inicio da definição de onde o valor da variável de ambiente será buscado
        secretKeyRef: # Inicio da definição de que o valor da variável de ambiente será buscado em um Secret, através de uma chave
          name: matrix-secret # Nome do Secret que contém o valor da variável de ambiente que será usada no Pod
          key: username # Nome da chave do campo do Secret que contém o valor da variável de ambiente que será usada no Pod
    - name: PASSWORD # Nome da variável de ambiente que será usada no Pod
      valueFrom: # Inicio da definição de onde o valor da variável de ambiente será buscado
        secretKeyRef: # Inicio da definição de que o valor da variável de ambiente será buscado em um Secret, através de uma chave
          name: matrix-secret # Nome do Secret que contém o valor da variável de ambiente que será usada no Pod
          key: password # Nome da chave do campo do Secret que contém o valor da variável de ambiente que será usada no Pod
```
 

Eu adicionei comentários nas linhas que são novas para você, para que você possa entender o que cada linha faz.

Mas vou trazer aqui uma explicação mais detalhada sobre o campo **spec.containers[].env[].valueFrom.secretKeyRef:**

- **spec.containers[].env[].valueFrom.secretKeyRef.name:** o nome do Secret que contém o valor da variável de ambiente que será usada no Pod;

- **spec.containers[].env[].valueFrom.secretKeyRef.key:** a chave do campo do Secret que contém o valor da variável de ambiente que será usada no Pod;

Com isso teremos um Pod, que terá um container chamado matrix-container, que terá duas variáveis de ambiente, USERNAME e PASSWORD, que terão os valores que estão definidos no Secret matrix-secret.

Agora vamos criar o Pod usando o comando kubectl apply:
```bash
kubectl apply -f matrix-pod.yaml
```

```
pod/matrix-pod created
```
 

Agora vamos verificar se o Pod foi criado e se os Secrets foram injetados no Pod:

```bash
kubectl get pods
```


```
NAME           READY   STATUS    RESTARTS   AGE
matrix-pod   1/1     Running   0          2m
```

Para verificar se os Secrets foram injetados no Pod, você pode usar o comando kubectl exec para executar o comando env dentro do container do Pod:

```bash
kubectl exec matrix-pod -- env
```

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=matrix-pod
NGINX_VERSION=1.23.4
NJS_VERSION=0.7.11
PKG_RELEASE=1~bullseye
PASSWORD=matrix
USERNAME=CENSURADO
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
HOME=/root
```

Olha lá os nosso Secrets como variáveis de ambiente dentro do container do Pod!

Pronto! Tarefa executada com sucesso! \o/

Agora eu acho que já podemos partir para os próximos tipos de Secrets!

