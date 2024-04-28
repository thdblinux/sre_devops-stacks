## Os ServiceMonitors
Um dos principais recursos que o Kube-Prometheus utiliza é o ServiceMonitor. O ServiceMonitor é um recurso do Prometheus Operator que permite que você configure o Prometheus para monitorar um serviço. Para isso, você precisa criar um ServiceMonitor para cada serviço que você deseja monitorar.

O ServiceMonitor define o conjunto de endpoints a serem monitorados pelo Prometheus e também fornece informações adicionais, como o caminho e a porta de um endpoint, além de permitir a definição de rótulos personalizados. Ele pode ser usado para monitorar os endpoints de um aplicativo ou de um serviço específico em um cluster Kubernetes.

Você consegue criar algumas regras com o objetivo de filtrar quais serão os targets que o Prometheus irá monitorar. Por exemplo, você pode criar uma regra para monitorar apenas os pods que estão com o label `app=nginx` ou ainda capturar as métricas somente de endpoints que estejam com alguma label que você definiu.

O Kube-Prometheus já vem com vários ServiceMonitors configurados, como por exemplo o ServiceMonitor do API Server, do Node Exporter, do Blackbox Exporter, etc.

```sh
kubectl get servicemonitors -n monitoring
```

```sh
NAME                      AGE
alertmanager              17m
blackbox-exporter         17m
coredns                   17m
grafana                   17m
kube-apiserver            17m
kube-controller-manager   17m
kube-scheduler            17m
kube-state-metrics        17m
kubelet                   17m
node-exporter             17m
prometheus-adapter        17m
prometheus-k8s            17m
prometheus-operator       17m
```
Para ver o conteúdo de um ServiceMonitor, basta executar o seguinte comando:
```sh
kubectl get servicemonitor prometheus-k8s -n monitoring -o yaml
```
Nesse caso estamos pegando o ServiceMonitor do Prometheus, mas você pode pegar o ServiceMonitor de qualquer outro serviço.
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"monitoring.coreos.com/v1","kind":"ServiceMonitor","metadata":{"annotations":{},"labels":{"app.kubernetes.io/component":"prometheus","app.kubernetes.io/instance":"k8s","app.kubernetes.io/name":"prometheus","app.kubernetes.io/part-of":"kube-prometheus","app.kubernetes.io/version":"2.41.0"},"name":"prometheus-k8s","namespace":"monitoring"},"spec":{"endpoints":[{"interval":"30s","port":"web"},{"interval":"30s","port":"reloader-web"}],"selector":{"matchLabels":{"app.kubernetes.io/component":"prometheus","app.kubernetes.io/instance":"k8s","app.kubernetes.io/name":"prometheus","app.kubernetes.io/part-of":"kube-prometheus"}}}}
  creationTimestamp: "2023-01-23T19:08:26Z"
  generation: 1
  labels:
    app.kubernetes.io/component: prometheus
    app.kubernetes.io/instance: k8s
    app.kubernetes.io/name: prometheus
    app.kubernetes.io/part-of: kube-prometheus
    app.kubernetes.io/version: 2.41.0
  name: prometheus-k8s
  namespace: monitoring
  resourceVersion: "4100"
  uid: 6042e08c-cf18-4622-9860-3ff43e696f7c
spec:
  endpoints:
  - interval: 30s
    port: web
  - interval: 30s
    port: reloader-web
  selector:
    matchLabels:
      app.kubernetes.io/component: prometheus
      app.kubernetes.io/instance: k8s
      app.kubernetes.io/name: prometheus
      app.kubernetes.io/part-of: kube-prometheus
```
Eu vou dar uma limpada nessa saída para ficar mais fácil de entender:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  annotations:
  labels:
    app.kubernetes.io/component: prometheus
    app.kubernetes.io/instance: k8s
    app.kubernetes.io/name: prometheus
    app.kubernetes.io/part-of: kube-prometheus
    app.kubernetes.io/version: 2.41.0
  name: prometheus-k8s
  namespace: monitoring
spec:
  endpoints:
  - interval: 30s
    port: web
  - interval: 30s
    port: reloader-web
  selector:
    matchLabels:s
      app.kubernetes.io/component: prometheus
      app.kubernetes.io/instance: k8s
      app.kubernetes.io/name: prometheus
      app.kubernetes.io/part-of: kube-prometheus
```
Pronto, eu tirei algumas informações que não são importantes para a criação do ServiceMonitor, elas apenas trazer as informações do service monitor que foi criado e que pegamos a saída.

Com o arquivo limpo, podemos entender melhor o que está acontecendo.

- `apiVersion:` Versão da API do Kubernetes que estamos utilizando.
- `kind:` Tipo de objeto que estamos criando.
- `metadata:` Informações sobre o objeto que estamos criando.
- `metadata.annotations: `Anotações que podemos adicionar ao nosso objeto.
- `metadata.labels:` Labels que podemos adicionar ao nosso objeto.
- `metadata.name:` Nome do nosso objeto.
- `metadata.namespace:` Namespace onde o nosso objeto será criado.
- `spec:`Especificações do nosso objeto.
- `spec.endpoints:` Endpoints que o nosso ServiceMonitor irá monitorar.
- `spec.endpoints.interval:` Intervalo de tempo que o Prometheus irá fazer a coleta de métricas.
- `spec.endpoints.port:` Porta que o Prometheus irá utilizar para coletar as métricas.
- `spec.selector:` Selector que o ServiceMonitor irá utilizar para encontrar os serviços que ele irá monitorar.
Com isso, sabemos que o ServiceMonitor do Prometheus irá monitorar os serviços que possuem as labels `app.kubernetes.io/component: prometheus`, `app.kubernetes.io/instance: k8s`,` app.kubernetes.io/name: prometheus` e `app.kubernetes.io/part-of: kube-prometheus`, e que ele irá monitorar as portas `web` e` reloader-web` com um intervalo de 30 segundos. É fácil ou não é?

Então sempre que precisarmos criar um ServiceMonitor para monitorar algum serviço, basta criarmos um arquivo YAML com as informações que precisamos e aplicarmos em nosso cluster.

### Vamos criar o nosso ServiceMonitor com o seguinte arquivo YAML:
```sh
apiVersion: monitoring.coreos.com/v1 # versão da API
kind: ServiceMonitor # tipo de recurso, no caso, um ServiceMonitor do Prometheus Operator
metadata: # metadados do recurso
  name: nginx-servicemonitor # nome do recurso
  labels: # labels do recurso
    app: nginx # label que identifica o app
spec: # especificação do recurso
  selector: # seletor para identificar os pods que serão monitorados
    matchLabels: # labels que identificam os pods que serão monitorados
      app: nginx # label que identifica o app que será monitorado
  endpoints: # endpoints que serão monitorados
    - interval: 10s # intervalo de tempo entre as requisições
      path: /metrics # caminho para a requisição
      targetPort: 9113 # porta do target
```
### Agora vamos entender o que está acontecendo no nosso arquivo YAML.

- `apiVersion:` Versão da API do Kubernetes que estamos utilizando.
- `kind:` Tipo de objeto que estamos criando, no nosso caso, um ServiceMonitor.
- `metadata:` Informações sobre o objeto que estamos criando.
- `metadata.name:` Nome do nosso objeto.
- `metadata.labels:` Labels que serão utilizadas para identificar o nosso objeto.
- `spec:` Especificações do nosso objeto.
- `spec.selector:` Seletor que será utilizado para identificar o nosso Service.
- `spec.selector.matchLabels:` Labels que serão utilizadas para identificar o nosso Service, no nosso caso, o Service que tema - label` app: nginx.`
- `spec.endpoints:` Endpoints que serão monitorados pelo Prometheus.
- `spec.endpoints.interval:` Intervalo de tempo que o Prometheus irá capturar as métricas, no nosso caso, 15 segundos.
- `spec.endpoints.path:` Caminho que o Prometheus irá fazer a requisição para capturar as métricas, no nosso caso, /metrics.
- `spec.endpoints.targetPort:` Porta que o Prometheus irá fazer a requisição para capturar as métricas, no nosso caso, `9113.`

### Vamos criar o nosso ServiceMonitor com o seguinte comando:
```sh
kubectl apply -f nginx-service-monitor.yaml
```
Maravilha! Agora que já temos o nosso Nginx rodando e as métricas sendo expostas, vamos verificar se o Prometheus está capturando as métricas do Nginx e do Nginx Exporter.

Vamos fazer o port-forward do Prometheus para acessar o Prometheus localmente:
```sh
kubectl port-forward -n monitoring svc/prometheus-k8s 39090:9090
```
E agora vamos usar o curl para verificar se o Prometheus está capturando as métricas do Nginx e do Nginx Exporter:
```sh
curl http://localhost:39090/api/v1/targets
```
Pronto, agora você já sabe como que faz para criar um Service no Kubernetes, expor as métricas do Nginx e do Nginx Exporter e ainda criar um ServiceMonitor para o seu Service ficar monitorado pelo Prometheus. \o/

É muito importante que você saiba que o Prometheus não captura as métricas automaticamente, ele precisa de um ServiceMonitor para capturar as métricas.

### Os PodMonitors
E quando o nosso workload não é um Service? E quando o nosso workload é um Pod? Como que faz para monitorar o Pod?
Tem situações que não temos um service na frente de nossos pods, por exemplo, quando temos CronJobs, Jobs, DaemonSets, etc. Eu já vi situações onde o pessoal estavam utilizando o PodMonitor para monitorar pods não HTTP, por exemplo, pods que expõem métricas do RabbitMQ, do Redis, Kafka, etc.

### Criando um PodMonitor
Para criar um PodMonitor, quase não teremos muitas mudanças do que aprendemos para criar um ServiceMonitor. Vamos criar o nosso PodMonitor com o seguinte arquivo YAML chamado nginx-pod-monitor.yaml:

```sh
apiVersion: monitoring.coreos.com/v1 # versão da API
kind: PodMonitor # tipo de recurso, no caso, um PodMonitor do Prometheus Operator
metadata: # metadados do recurso
  name: nginx-podmonitor # nome do recurso
  labels: # labels do recurso
    app: nginx # label que identifica o app
spec:
  namespaceSelector: # seletor de namespaces
    matchNames: # namespaces que serão monitorados
      - default # namespace que será monitorado
  selector: # seletor para identificar os pods que serão monitorados
    matchLabels: # labels que identificam os pods que serão monitorados
      app: nginx # label que identifica o app que será monitorado
  podMetricsEndpoints: # endpoints que serão monitorados
    - interval: 10s # intervalo de tempo entre as requisições
      path: /metrics # caminho para a requisição
      targetPort: 9113 # porta do target
```
Veja que usamos quase que as mesmas opções do ServiceMonitor, a única diferença é que usamos o podMetricsEndpoints para definir os endpoints que serão monitorados.
Outra novidade para nós é o namespaceSelector, que é utilizado para selecionar os namespaces que serão monitorados. No nosso caso, estamos monitorando o namespace default, onde estará em execução o nosso Pod do Nginx.

Antes de deployar o nosso PodMonitor, vamos criar o nosso Pod do Nginx com o seguinte arquivo YAML chamado `nginx-pod.yaml:`

```sh
apiVersion: v1 # versão da API
kind: Pod # tipo de recurso, no caso, um Pod
metadata: # metadados do recurso
  name: nginx-pod # nome do recurso
  labels: # labels do recurso
    app: nginx # label que identifica o app
spec: # especificações do recursos
  containers: # containers do template 
    - name: nginx-container # nome do container
      image: nginx # imagem do container do Nginx
      ports: # portas do container
        - containerPort: 80 # porta do container
          name: http # nome da porta
      volumeMounts: # volumes que serão montados no container
        - name: nginx-config # nome do volume
          mountPath: /etc/nginx/conf.d/default.conf # caminho de montagem do volume
          subPath: nginx.conf # subpath do volume
    - name: nginx-exporter # nome do container que será o exporter
      image: 'nginx/nginx-prometheus-exporter:0.11.0' # imagem do container do exporter
      args: # argumentos do container
        - '-nginx.scrape-uri=http://localhost/metrics' # argumento para definir a URI de scraping
      resources: # recursos do container
        limits: # limites de recursos
          memory: 128Mi # limite de memória
          cpu: 0.3 # limite de CPU
      ports: # portas do container
        - containerPort: 9113 # porta do container que será exposta
          name: metrics # nome da porta
  volumes: # volumes do template
    - configMap: # configmap do volume, nós iremos criar esse volume através de um configmap
        defaultMode: 420 # modo padrão do volume
        name: nginx-config # nome do configmap
      name: nginx-config # nome do volume
```
Pronto, com o nosso Pod criado, vamos criar o nosso PodMonitor utilizando o arquivo YAML chamado `nginx-pod-monitor.yaml`, que criamos anteriormente:
```sh
kubectl apply -f nginx-pod-monitor.yaml
```
Vamos verificar os PodMonitors que estão criados em nosso cluster:
```sh
kubectl get podmonitors
```
Caso você queira ver os PodMonitors em detalhes, basta executar o seguinte comando:
```sh
kubectl describe podmonitors nginx-podmonitor
```
E claro, você pode fazer o mesmo com o ServiceMonitor, basta executar o seguinte comando:
```sh
kubectl describe servicemonitors nginx-servicemonitor
```
Vamos ver a saida do describe para o nosso PodMonitor:
```sh
Name:         nginx-podmonitor
Namespace:    default
Labels:       app=nginx
Annotations:  <none>
API Version:  monitoring.coreos.com/v1
Kind:         PodMonitor
Metadata:
  Creation Timestamp:  2023-03-01T17:17:13Z
  Generation:          1
  Managed Fields:
    API Version:  monitoring.coreos.com/v1
    Fields Type:  FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .:
          f:kubectl.kubernetes.io/last-applied-configuration:
        f:labels:
          .:
          f:app:
      f:spec:
        .:
        f:namespaceSelector:
          .:
          f:matchNames:
        f:podMetricsEndpoints:
        f:selector:
    Manager:         kubectl-client-side-apply
    Operation:       Update
    Time:            2023-03-01T17:17:13Z
  Resource Version:  9473
  UID:               8c1bb91c-7285-4184-90e7-dcffcb143b92
Spec:
  Namespace Selector:
    Match Names:
      default
  Pod Metrics Endpoints:
    Interval:  10s
    Path:      /metrics
    Port:      9113
  Selector:
    Match Labels:
      App:  nginx
Events:     <none>
```
Como podemos ver, o nosso PodMonitor foi criado com sucesso. 😄

Agora vamos ver se ele está aparecendo como um target no Prometheus. Para isso, vamos acessar o Prometheus localmente através do` kubectl port-forward:`
```sh
kubectl port-forward -n monitoring svc/prometheus-k8s 39090:9090
```
Pronto, corre lá conferir o seu mais novo target e as métricas que estão sendo coletadas. 😄

Uma coisa que vale a pena lembrar, é que você pode acessar o container com o kubectl exec e verificar se o seu exporter está funcionando corretamente ou somente para conferir quais são as métricas que ele está expondo para o Prometheus. Para isso, basta executar o seguinte comando:
```sh
kubectl exec -it nginx-pod -c nginx-exporter -- bash
```
Agora vamos utilizar o curl para verificar se o nosso exporter está funcionando corretamente:
```sh
curl localhost:9113/metrics
```
Se tudo está funcionando corretamente, você deve ver uma saída parecida com a seguinte:
```sh
# HELP nginx_connections_accepted Accepted client connections
# TYPE nginx_connections_accepted counter
nginx_connections_accepted 1
# HELP nginx_connections_active Active client connections
# TYPE nginx_connections_active gauge
nginx_connections_active 1
# HELP nginx_connections_handled Handled client connections
# TYPE nginx_connections_handled counter
nginx_connections_handled 1
# HELP nginx_connections_reading Connections where NGINX is reading the request header
# TYPE nginx_connections_reading gauge
nginx_connections_reading 0
# HELP nginx_connections_waiting Idle client connections
# TYPE nginx_connections_waiting gauge
nginx_connections_waiting 0
# HELP nginx_connections_writing Connections where NGINX is writing the response back to the client
# TYPE nginx_connections_writing gauge
nginx_connections_writing 1
# HELP nginx_http_requests_total Total http requests
# TYPE nginx_http_requests_total counter
nginx_http_requests_total 61
# HELP nginx_up Status of the last metric scrape
# TYPE nginx_up gauge
nginx_up 1
# HELP nginxexporter_build_info Exporter build information
# TYPE nginxexporter_build_info gauge
nginxexporter_build_info{arch="linux/amd64",commit="e4a6810d4f0b776f7fde37fea1d84e4c7284b72a",date="2022-09-07T21:09:51Z",dirty="false",go="go1.19",version="0.11.0"} 1
```
Lembrando que você pode consultar todas essas métricas lá no seu Prometheus. 😄

### Bora mudar um pouco de assunto? Vamos falar sobre alertas!

Criando nosso primeiro alerta
Agora que já temos o nosso Kube-Prometheus instalado, vamos configurar o Prometheus para monitorar o nosso cluster `EKS`. Para isso, vamos utilizar o kubectl port-forward para acessar o Prometheus localmente. Para isso, basta executar o seguinte comando:
```sh
kubectl port-forward -n monitoring svc/prometheus-k8s 39090:9090
```
Se você quiser acessar o Alertmanager, basta executar o seguinte comando:
```sh
kubectl port-forward -n monitoring svc/alertmanager-main 39093:9093
```
Pronto, agora você já sabe como que faz para acessar o `Prometheus`, `AlertManager` e o `Grafana` localmente. 😄

Lembrando que você pode acessar o Prometheus e o AlertManager através do seu navegador, basta acessar as seguintes URLs:

`Prometheus: http://localhost:39090`
`AlertManager: http://localhost:39093`
Simples assim!

Evidentemente, você pode expor esses serviços para a internet ou para um VPC privado, mas isso é assunto para você discutir com seu time.

Antes sair definindo um novo alerta, precisamos entender como faze-lo, uma vez que nós não temos mais o arquivo de alertas, igual tínhamos quando instalamos o Prometheus em nosso servidor Linux.

Agora, precisamos entender que boa parte da configuração do Prometheus está dentro de configmaps, que são recursos do Kubernetes que armazenam dados em formato de chave e valor e são muito utilizados para armazenar configurações de aplicações.

Para listar os `configmaps` do nosso cluster, basta executar o seguinte comando:
```sh
kubectl get configmaps -n monitoring
```
O resultado do comando acima deverá ser parecido com o seguinte:
```sh
NAME                                                  DATA   AGE
adapter-config                                        1      7m20s
blackbox-exporter-configuration                       1      7m49s
grafana-dashboard-alertmanager-overview               1      7m46s
grafana-dashboard-apiserver                           1      7m46s
grafana-dashboard-cluster-total                       1      7m46s
grafana-dashboard-controller-manager                  1      7m45s
grafana-dashboard-grafana-overview                    1      7m44s
grafana-dashboard-k8s-resources-cluster               1      7m44s
grafana-dashboard-k8s-resources-namespace             1      7m44s
grafana-dashboard-k8s-resources-node                  1      7m43s
grafana-dashboard-k8s-resources-pod                   1      7m42s
grafana-dashboard-k8s-resources-workload              1      7m42s
grafana-dashboard-k8s-resources-workloads-namespace   1      7m41s
grafana-dashboard-kubelet                             1      7m41s
grafana-dashboard-namespace-by-pod                    1      7m41s
grafana-dashboard-namespace-by-workload               1      7m40s
grafana-dashboard-node-cluster-rsrc-use               1      7m40s
grafana-dashboard-node-rsrc-use                       1      7m39s
grafana-dashboard-nodes                               1      7m39s
grafana-dashboard-nodes-darwin                        1      7m39s
grafana-dashboard-persistentvolumesusage              1      7m38s
grafana-dashboard-pod-total                           1      7m38s
grafana-dashboard-prometheus                          1      7m37s
grafana-dashboard-prometheus-remote-write             1      7m37s
grafana-dashboard-proxy                               1      7m37s
grafana-dashboard-scheduler                           1      7m36s
grafana-dashboard-workload-total                      1      7m36s
grafana-dashboards                                    1      7m35s
kube-root-ca.crt                                      1      11m
prometheus-k8s-rulefiles-0                            8      7m10s
```
Como você pode ver, temos diversos configmaps que contém configurações do Prometheus, AlertManager e do Grafana. Vamos focar no configm`ap prometheus-k8s-rulefiles-0`, que é o configmap que contém os alertas do Prometheus.

Para visualizar o conteúdo do configmap, basta executar o seguinte comando:
```sh
kubectl get configmap prometheus-k8s-rulefiles-0 -n monitoring -o yaml
```
Eu não vou colar a saída inteira aqui porque ela é enorme, mas vou colar um pedaço com um exemplo de alerta:
```yaml
- alert: KubeMemoryOvercommit
    annotations:
        description: Cluster has overcommitted memory resource requests for Pods by
        {{ $value | humanize }} bytes and cannot tolerate node failure.
        runbook_url: https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubememoryovercommit
        summary: Cluster has overcommitted memory resource requests.
    expr: |
        sum(namespace_memory:kube_pod_container_resource_requests:sum{}) - (sum(kube_node_status_allocatable{resource="memory"}) - max(kube_node_status_allocatable{resource="memory"})) > 0
        and
        (sum(kube_node_status_allocatable{resource="memory"}) - max(kube_node_status_allocatable{resource="memory"})) > 0
    for: 10m
    labels:
        severity: warning
```
Como você pode ver, o alerta acima é chamado de `KubeMemoryOvercommit` e ele é disparado quando o cluster tem mais memória alocada para os pods do que a memória disponível nos nós. A sua definição é a mesma que usamos quando criamos o arquivo de alertas no nosso servidor Linux.

### Criando um novo alerta
Muito bom, já sabemos que temos algumas regras já definidas, e que elas estão dentro de um configmap. Agora, vamos criar um novo alerta para monitorar o nosso Nginx.

Mas antes, precisamos entender o que é um recurso chamado `PrometheusRule`.

### O que é um PrometheusRule?
O PrometheusRule é um recurso do Kubernetes que foi instalado no momento que realizamos a instalação dos CRDs do kube-prometheus. O PrometheusRule permite que você defina alertas para o Prometheus. Ele é muito parecido com o arquivo de alertas que criamos no nosso servidor Linux, porém nesse momento vamos fazer a mesma definição de alerta, mas usando o PrometheusRule.

### Criando um PrometheusRule
Vamos criar um arquivo chamado `nginx-prometheus-rule.yaml` e vamos colocar o seguinte conteúdo:
```yaml
apiVersion: monitoring.coreos.com/v1 # Versão da api do PrometheusRule
kind: PrometheusRule # Tipo do recurso
metadata: # Metadados do recurso (nome, namespace, labels)
  name: nginx-prometheus-rule
  namespace: monitoring
  labels: # Labels do recurso
    prometheus: k8s # Label que indica que o PrometheusRule será utilizado pelo Prometheus do Kubernetes
    role: alert-rules # Label que indica que o PrometheusRule contém regras de alerta
    app.kubernetes.io/name: kube-prometheus # Label que indica que o PrometheusRule faz parte do kube-prometheus
    app.kubernetes.io/part-of: kube-prometheus # Label que indica que o PrometheusRule faz parte do kube-prometheus
spec: # Especificação do recurso
  groups: # Lista de grupos de regras
  - name: nginx-prometheus-rule # Nome do grupo de regras
    rules: # Lista de regras
    - alert: NginxDown # Nome do alerta
      expr: up{job="nginx"} == 0 # Expressão que será utilizada para disparar o alerta
      for: 1m # Tempo que a expressão deve ser verdadeira para que o alerta seja disparado
      labels: # Labels do alerta
        severity: critical # Label que indica a severidade do alerta
      annotations: # Anotações do alerta
        summary: "Nginx is down" # Título do alerta
        description: "Nginx is down for more than 1 minute. Pod name: {{ $labels.pod }}" # Descrição do alerta
```
Agora, vamos criar o PrometheusRule no nosso cluster:
```sh
kubectl apply -f nginx-prometheus-rule.yaml
```
Agora, vamos verificar se o PrometheusRule foi criado com sucesso:
```sh
kubectl get prometheusrules -n monitoring
```
A saída deve ser parecida com essa:
```sh
NAME                              AGE
alertmanager-main-rules           92m
grafana-rules                     92m
kube-prometheus-rules             92m
kube-state-metrics-rules          92m
kubernetes-monitoring-rules       92m
nginx-prometheus-rule             20s
node-exporter-rules               91m
prometheus-k8s-prometheus-rules   91m
prometheus-operator-rules         91m
```
Agora nós já temos um novo alerta configurado em nosso Prometheus. Lembrando que temos a integração com o AlertManager, então, quando o alerta for disparado, ele será enviado para o` AlertManager` e o AlertManager vai enviar uma notificação, por exemplo, para o nosso `Slack`ou `e-mail`.

Você pode acessar o nosso alerta tanto no Prometheus quanto no AlertManager.

Vamos imaginar que você precisa criar um novo alerta para monitorar a quantidade de requisições simultâneas que o seu Nginx está recebendo. Para isso, você precisa criar uma nova regra no PrometheusRule. Podemos utilizar o mesmo arquivo` nginx-prometheus-rule.yaml` e adicionar a nova regra no final do arquivo:
```sh
apiVersion: monitoring.coreos.com/v1 # Versão da api do PrometheusRule
kind: PrometheusRule # Tipo do recurso
metadata: # Metadados do recurso (nome, namespace, labels)
  name: nginx-prometheus-rule
  namespace: monitoring
  labels: # Labels do recurso
    prometheus: k8s # Label que indica que o PrometheusRule será utilizado pelo Prometheus do Kubernetes
    role: alert-rules # Label que indica que o PrometheusRule contém regras de alerta
    app.kubernetes.io/name: kube-prometheus # Label que indica que o PrometheusRule faz parte do kube-prometheus
    app.kubernetes.io/part-of: kube-prometheus # Label que indica que o PrometheusRule faz parte do kube-prometheus
spec: # Especificação do recurso
  groups: # Lista de grupos de regras
  - name: nginx-prometheus-rule # Nome do grupo de regras
    rules: # Lista de regras
    - alert: NginxDown # Nome do alerta
      expr: up{job="nginx"} == 0 # Expressão que será utilizada para disparar o alerta
      for: 1m # Tempo que a expressão deve ser verdadeira para que o alerta seja disparado
      labels: # Labels do alerta
        severity: critical # Label que indica a severidade do alerta
      annotations: # Anotações do alerta
        summary: "Nginx is down" # Título do alerta
        description: "Nginx is down for more than 1 minute. Pod name: {{ $labels.pod }}" # Descrição do alerta

    - alert: NginxHighRequestRate # Nome do alerta
        expr: rate(nginx_http_requests_total{job="nginx"}[5m]) > 10 # Expressão que será utilizada para disparar o alerta
        for: 1m # Tempo que a expressão deve ser verdadeira para que o alerta seja disparado
        labels: # Labels do alerta
            severity: warning # Label que indica a severidade do alerta
        annotations: # Anotações do alerta
            summary: "Nginx is receiving high request rate" # Título do alerta
            description: "Nginx is receiving high request rate for more than 1 minute. Pod name: {{ $labels.pod }}" # Descrição do alerta
```
Pronto, adicionamos uma nova definição de alerta em nosso PrometheusRule. Agora vamos atualizar o nosso PrometheusRule:
```sh
kubectl apply -f nginx-prometheus-rule.yaml
```
Agora, vamos verificar se o PrometheusRule foi atualizado com sucesso:
```sh
kubectl get prometheusrules -n monitoring nginx-prometheus-rule -o yaml
```
A saída deve ser parecida com essa:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"monitoring.coreos.com/v1","kind":"PrometheusRule","metadata":{"annotations":{},"labels":{"app.kubernetes.io/name":"kube-prometheus","app.kubernetes.io/part-of":"kube-prometheus","prometheus":"k8s","role":"alert-rules"},"name":"nginx-prometheus-rule","namespace":"monitoring"},"spec":{"groups":[{"name":"nginx-prometheus-rule","rules":[{"alert":"NginxDown","annotations":{"description":"Nginx is down for more than 1 minute. Pod name: {{ $labels.pod }}","summary":"Nginx is down"},"expr":"up{job=\"nginx\"} == 0","for":"1m","labels":{"severity":"critical"}},{"alert":"NginxHighRequestRate","annotations":{"description":"Nginx is receiving high request rate for more than 1 minute. Pod name: {{ $labels.pod }}","summary":"Nginx is receiving high request rate"},"expr":"rate(nginx_http_requests_total{job=\"nginx\"}[5m]) \u003e 10","for":"1m","labels":{"severity":"warning"}}]}]}}
  creationTimestamp: "2023-03-01T14:14:00Z"
  generation: 2
  labels:
    app.kubernetes.io/name: kube-prometheus
    app.kubernetes.io/part-of: kube-prometheus
    prometheus: k8s
    role: alert-rules
  name: nginx-prometheus-rule
  namespace: monitoring
  resourceVersion: "24923"
  uid: c0a6914d-9a54-4083-bdf8-ebfb5c19077d
spec:
  groups:
  - name: nginx-prometheus-rule
    rules:
    - alert: NginxDown
      annotations:
        description: 'Nginx is down for more than 1 minute. Pod name: {{ $labels.pod
          }}'
        summary: Nginx is down
      expr: up{job="nginx"} == 0
      for: 1m
      labels:
        severity: critical
    - alert: NginxHighRequestRate
      annotations:
        description: 'Nginx is receiving high request rate for more than 1 minute.
          Pod name: {{ $labels.pod }}'
        summary: Nginx is receiving high request rate
      expr: rate(nginx_http_requests_total{job="nginx"}[5m]) > 10
      for: 1m
      labels:
        severity: warning
```
Pronto, o alerta foi criado com sucesso e você pode conferir no Prometheus ou no AlertManager.

Com o novo alerta, caso o Nginx esteja recebendo mais de 10 requisições por minuto, o alerta será disparado e você receberá uma notificação no Slack ou e-mail, claro, dependendo da configuração que você fez no AlertManager.

Acho que já podemos chamar o dia de hoje de sucesso absoluto, pois entendemos como funciona para criar um novo target para o Prometheus, bem como criar um novo alerta para o AlertManager/Prometheus.

Agora você precisa dar asas para a sua imaginação e sair criando tudo que é exemplo de de alerta que você bem entender, e claro, coloque mais serviços no seu cluster Kubernetes para que você possa monitorar tudo que é possível através do ServiceMonitor e PrometheusRule do Prometheus Operator, e claro, não esqueça de compartilhar com a gente o que você criou.