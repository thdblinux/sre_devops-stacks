## O que iremos ver hoje

Durante o dia de hoje iremos aprender sobre todas as possibilidades que temos com a utilização do` Prometheus + Kubernetes`!
Hoje é dia de conhecer o sensacional` kube-prometheus`, projeto esse criado pelos mesmos criadores do `Prometheus Operator`, que nos permite monitorar o nosso cluster de Kubernetes de forma simples e eficiente. Além disso, iremos aprender como utilizar o `Prometheus Adapter` para que possamos utilizar o nosso querido e lindo Prometheus como fonte de dados para o `Horizontal Pod Autoscaler`, ou seja, iremos aprender como utilizar o nosso querido e lindo Prometheus para escalar nossos pods de forma automática!
E ainda de quebra você vai aprender como instalar o Kubernetes, mais do que isso, você vai aprender como instalar um cluster EKS! Sim, você vai aprender como instalar um cluster `EKS`, o cluster de Kubernetes da` AWS`, através da ferramenta eksctl, que é uma ferramenta de linha de comando que nos permite instalar um cluster `EKS` em minutos!

**O que é o kube-prometheus?**

O kube-prometheus é um conjunto de manifestos do Kubernetes que nos permite ter o `Prometheus Operator`, `Grafana`,` AlertManager`, `Node Exporter`, `Kube-State-Metrics`, `Prometheus-Adapter` instalados e configurados de forma tranquila e com alta disponibilidade. Além disso, ele nos permite ter uma visão completa do nosso cluster de Kubernetes. Ele nos permite monitorar todos os componentes do nosso cluster de Kubernetes, como por exemplo:` kube-scheduler`, k`ube-controller-manager`, `kubelet, kube-proxy`, etc.

**Instalando o nosso cluster Kubernetes**
Como dissemos, para esse nosso exemplo iremos utilizar o cluster de Kubernetes da` AWS`, o EKS. Para instalar o nosso cluster EKS, iremos utilizar a ferramenta `eksctl`, portanto precisamos instalá-la em nossa máquina. Para instalar a ferramenta, basta executar o seguinte comando:

```sh
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
```
```sh
sudo mv /tmp/eksctl /usr/local/bin
```
Precisamos ter o CLI da` aws` instalado em nossa máquina, para isso, basta executar o seguinte comando:

```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

```sh
unzip awscliv2.zip
```

```sh
sudo ./aws/install
```
Pronto, agora você já tem o eksctl e o aws instalados em sua máquina.

Para que possamos criar tudo o que precisamos na AWS, é importante que você tenha uma conta na AWS, e que tenha as credenciais de acesso configuradas em sua máquina. Para configurar as credenciais de acesso, basta executar o seguinte comando:
```sh
aws configure
```
O comando acima irá solicitar que você informe a sua` AWS Access Key ID`, a sua `AWS Secret Access Key`, a sua Default region name, e o seu Default output format. Para saber mais sobre como configurar as credenciais de acesso, basta acessar a documentação oficial da AWS.

No comando acima estamos baixando o binário do eksctl compactado e descompactando ele na pasta /tmp, e depois movendo o binário para a pasta` /usr/local/bin`.

Lembrando que estou instando em uma máquina Linux, caso que esteja utilizando uma máquina Mac ou Windows, basta acessar a página de releases do projeto e baixar a versão adequada para o seu sistema operacional.

E enquanto você faz a instalação, vale a pena mencionar que o `eksctl` é uma ferramenta criada pela `WeaveWorks`, empresa que criou o `Flux`, que é um projeto de `GitOps` para `Kubernetes`, além de ter o Weavenet, que é um `CNI` para `Kubernetes`, e o `Weave Scope`, que é uma ferramenta de visualização de clusters de Kubernetes e muito mais, recomendo que vocês dêem uma olhada nos projetos, é sensacional!

Bem, agora você já tem o eksctl instalado em sua máquina, então vamos criar o nosso `cluster EKS`! Para isso, basta executar o seguinte comando:

```sh
eksctl create cluster --name=eks-cluster --version=1.24 --region=us-east-1 --nodegroup-name=eks-cluster-nodegroup --node-type=t3.medium --nodes=2 --nodes-min=1 --nodes-max=3 --managed
```

O comando acima irá criar um cluster EKS com o nome eks-cluster, na região us-east-1, com 2 nós do tipo t3.medium, e com um mínimo de 1 nó e um máximo de 3 nós. Além disso, o comando acima irá criar um nodegroup chamado eks-cluster-nodegroup. O eksctl irá cuidar de toda a infraestrutura necessária para o funcionamento do nosso cluster EKS. A versão do Kubernetes que será instalada no nosso cluster será a 1.24.

Após a criação do nosso cluster EKS, precisamos instalar o kubectl em nossa máquina. Para instalar o kubectl, basta executar o seguinte comando:


```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
```sh
chmod +x ./kubectl
```
```sh
sudo mv ./kubectl /usr/local/bin/kubectl
```
O comando acima irá baixar o binário do kubectl e o colocar na pasta `/usr/local/bin`, e dar permissão de execução para o binário.

Agora que já temos o kubectl instalado em nossa máquina, precisamos configurar o kubectl para utilizar o nosso cluster EKS. Para isso, basta executar o seguinte comando:

```sh
aws eks --region us-east-1 update-kubeconfig --name eks-cluster
```
Aonde us-east-1 é a região do nosso cluster EKS, e eks-cluster é o nome do nosso cluster EKS. Esse comando é necessário para que o kubectl saiba qual cluster ele deve utilizar, ele irá pegar as credenciais do nosso cluster EKS e armazenar no arquivo` ~/.kube/config.`

LEMBRE-SE: Você não precisa ter o Kubernetes rodando no EKS, fique a vontade para escolher onde preferir para seguir o treinamento.

Vamos ver se o kubectl está funcionando corretamente? Para isso, basta executar o seguinte comando:
```sh
kubectl get nodes
```
Se tudo estiver funcionando corretamente, você deverá ver uma lista com os nós do seu cluster EKS. 😄

Antes de seguirmos em frente, vamos conhecer algums comandos do eksctl, para que possamos gerenciar o nosso cluster EKS. Para listar os clusters EKS que temos em nossa conta, basta executar o seguinte comando:
```sh
eksctl get cluster -A
```
O parametro -A é para listar os clusters EKS de todas as regiões. Para listar os clusters EKS de uma região específica, basta executar o seguinte comando:

```sh
eksctl get cluster -r us-east-1
```
Para aumentar o número de nós do nosso cluster EKS, basta executar o seguinte comando:
```sh
eksctl scale nodegroup --cluster=eks-cluster --nodes=3 --nodes-min=1 --nodes-max=3 --name=eks-cluster-nodegroup -r us-east-1
```
Para diminuir o número de nós do nosso cluster EKS, basta executar o seguinte comando:
```sh
eksctl scale nodegroup --cluster=eks-cluster --nodes=1 --nodes-min=1 --nodes-max=3 --name=eks-cluster-nodegroup -r us-east-1
```
Para deletar o nosso cluster EKS, basta executar o seguinte comando:
```sh
eksctl delete cluster --name=eks-cluster -r us-east-1
```
Mas não delete o nosso cluster EKS, vamos utilizar ele para os próximos passos! hahahah

Instalando o Kube-Prometheus
Agora que já temos o nosso cluster EKS criado, vamos instalar o Kube-Prometheus. Para isso, basta executar o seguinte comando:
```sh
git clone https://github.com/prometheus-operator/kube-prometheus
```
```sh
cd kube-prometheus
```
```sh
kubectl create -f manifests/setup
```
Com o comando acima nós estamos clonando o repositório oficial do projeto, e aplicando os manifests necessários para a instalação do Kube-Prometheus. Após a execução do comando acima, você deverá ver uma mensagem parecida com a seguinte:

```sh
customresourcedefinition.apiextensions.k8s.io/alertmanagerconfigs.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/alertmanagers.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/podmonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/probes.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/prometheuses.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/prometheusrules.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/servicemonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/thanosrulers.monitoring.coreos.com created
namespace/monitoring created
```
Basicamente o que fizemos foi a instalação de alguns` CRDs (Custom Resource Definitions)` que são como extensões do Kubernetes, e que são utilizados pelo `Kube-Prometheu`s e com isso o Kubernetes irá reconhecer esses novos recursos, como por exemplo o PrometheusRule e o ServiceMonitor que irei falar mais a frente.

O processo de instalação dos CRDs pode demorar alguns minutos, então vamos aguardar a instalação terminar. 😄

Para verificar se a instalação dos CRDs foi concluída, o comando abaixo deverá funcionar,se ainda não funcionar, aguarde alguns minutos e tente novamente.
```sh
kubectl get servicemonitors -A
```
Após a instalação dos` CRDs,` vamos instalar o Prometheus e o `Alertmanager`. Para isso, basta executar o seguinte comando:
```sh
kubectl apply -f manifests/
```
Com o comando acima nós estamos aplicando os manifests necessários para a instalação do Prometheus e do` Alertmanager`. Após a execução do comando acima, você deverá ver uma mensagem parecida com a seguinte:

```sh
alertmanager.monitoring.coreos.com/main created
networkpolicy.networking.k8s.io/alertmanager-main created
poddisruptionbudget.policy/alertmanager-main created
prometheusrule.monitoring.coreos.com/alertmanager-main-rules created
secret/alertmanager-main created
service/alertmanager-main created
serviceaccount/alertmanager-main created
servicemonitor.monitoring.coreos.com/alertmanager-main created
clusterrole.rbac.authorization.k8s.io/blackbox-exporter created
clusterrolebinding.rbac.authorization.k8s.io/blackbox-exporter created
configmap/blackbox-exporter-configuration created
deployment.apps/blackbox-exporter created
networkpolicy.networking.k8s.io/blackbox-exporter created
service/blackbox-exporter created
serviceaccount/blackbox-exporter created
servicemonitor.monitoring.coreos.com/blackbox-exporter created
secret/grafana-config created
secret/grafana-datasources created
configmap/grafana-dashboard-alertmanager-overview created
configmap/grafana-dashboard-apiserver created
configmap/grafana-dashboard-cluster-total created
configmap/grafana-dashboard-controller-manager created
configmap/grafana-dashboard-grafana-overview created
configmap/grafana-dashboard-k8s-resources-cluster created
configmap/grafana-dashboard-k8s-resources-namespace created
configmap/grafana-dashboard-k8s-resources-node created
configmap/grafana-dashboard-k8s-resources-pod created
configmap/grafana-dashboard-k8s-resources-workload created
configmap/grafana-dashboard-k8s-resources-workloads-namespace created
configmap/grafana-dashboard-kubelet created
configmap/grafana-dashboard-namespace-by-pod created
configmap/grafana-dashboard-namespace-by-workload created
configmap/grafana-dashboard-node-cluster-rsrc-use created
configmap/grafana-dashboard-node-rsrc-use created
configmap/grafana-dashboard-nodes-darwin created
configmap/grafana-dashboard-nodes created
configmap/grafana-dashboard-persistentvolumesusage created
configmap/grafana-dashboard-pod-total created
configmap/grafana-dashboard-prometheus-remote-write created
configmap/grafana-dashboard-prometheus created
configmap/grafana-dashboard-proxy created
configmap/grafana-dashboard-scheduler created
configmap/grafana-dashboard-workload-total created
configmap/grafana-dashboards created
deployment.apps/grafana created
networkpolicy.networking.k8s.io/grafana created
prometheusrule.monitoring.coreos.com/grafana-rules created
service/grafana created
serviceaccount/grafana created
servicemonitor.monitoring.coreos.com/grafana created
prometheusrule.monitoring.coreos.com/kube-prometheus-rules created
clusterrole.rbac.authorization.k8s.io/kube-state-metrics created
clusterrolebinding.rbac.authorization.k8s.io/kube-state-metrics created
deployment.apps/kube-state-metrics created
networkpolicy.networking.k8s.io/kube-state-metrics created
prometheusrule.monitoring.coreos.com/kube-state-metrics-rules created
service/kube-state-metrics created
serviceaccount/kube-state-metrics created
servicemonitor.monitoring.coreos.com/kube-state-metrics created
prometheusrule.monitoring.coreos.com/kubernetes-monitoring-rules created
servicemonitor.monitoring.coreos.com/kube-apiserver created
servicemonitor.monitoring.coreos.com/coredns created
servicemonitor.monitoring.coreos.com/kube-controller-manager created
servicemonitor.monitoring.coreos.com/kube-scheduler created
servicemonitor.monitoring.coreos.com/kubelet created
clusterrole.rbac.authorization.k8s.io/node-exporter created
clusterrolebinding.rbac.authorization.k8s.io/node-exporter created
daemonset.apps/node-exporter created
networkpolicy.networking.k8s.io/node-exporter created
prometheusrule.monitoring.coreos.com/node-exporter-rules created
service/node-exporter created
serviceaccount/node-exporter created
servicemonitor.monitoring.coreos.com/node-exporter created
clusterrole.rbac.authorization.k8s.io/prometheus-k8s created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-k8s created
networkpolicy.networking.k8s.io/prometheus-k8s created
poddisruptionbudget.policy/prometheus-k8s created
prometheus.monitoring.coreos.com/k8s created
prometheusrule.monitoring.coreos.com/prometheus-k8s-prometheus-rules created
rolebinding.rbac.authorization.k8s.io/prometheus-k8s-config created
rolebinding.rbac.authorization.k8s.io/prometheus-k8s created
rolebinding.rbac.authorization.k8s.io/prometheus-k8s created
rolebinding.rbac.authorization.k8s.io/prometheus-k8s created
role.rbac.authorization.k8s.io/prometheus-k8s-config created
role.rbac.authorization.k8s.io/prometheus-k8s created
role.rbac.authorization.k8s.io/prometheus-k8s created
role.rbac.authorization.k8s.io/prometheus-k8s created
service/prometheus-k8s created
serviceaccount/prometheus-k8s created
servicemonitor.monitoring.coreos.com/prometheus-k8s created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io created
clusterrole.rbac.authorization.k8s.io/prometheus-adapter created
clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-adapter created
clusterrolebinding.rbac.authorization.k8s.io/resource-metrics:system:auth-delegator created
clusterrole.rbac.authorization.k8s.io/resource-metrics-server-resources created
configmap/adapter-config created
deployment.apps/prometheus-adapter created
networkpolicy.networking.k8s.io/prometheus-adapter created
poddisruptionbudget.policy/prometheus-adapter created
rolebinding.rbac.authorization.k8s.io/resource-metrics-auth-reader created
service/prometheus-adapter created
serviceaccount/prometheus-adapter created
servicemonitor.monitoring.coreos.com/prometheus-adapter created
clusterrole.rbac.authorization.k8s.io/prometheus-operator created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-operator created
deployment.apps/prometheus-operator created
networkpolicy.networking.k8s.io/prometheus-operator created
prometheusrule.monitoring.coreos.com/prometheus-operator-rules created
service/prometheus-operator created
serviceaccount/prometheus-operator created
servicemonitor.monitoring.coreos.com/prometheus-operator created
```
Com isso fizemos a instalação da Stack do nosso `Kube-Prometheus`, que é composta pelo` Prometheus,` pelo` Alertmanager`, `Blackbox Exporter` e `Grafana`. 😄
Perceba que ele já está configurando um monte de outras coisas como os `ConfigMaps`, `Secrets,` `ServiceAccounts`, etc.

Para verificar se a instalação foi concluída, basta executar o seguinte comando:
```sh
kubectl get pods -n monitoring
```
O resultado esperado é o seguinte:
```sh
NAME                                  READY   STATUS    RESTARTS   AGE
alertmanager-main-0                   2/2     Running   0          57s
alertmanager-main-1                   2/2     Running   0          57s
alertmanager-main-2                   2/2     Running   0          57s
blackbox-exporter-cbb9c96b-t8z68      3/3     Running   0          94s
grafana-589787799d-pxsts              1/1     Running   0          80s
kube-state-metrics-557d857c5d-kt8dd   3/3     Running   0          78s
node-exporter-2n6sz                   2/2     Running   0          74s
node-exporter-mwq6b                   2/2     Running   0          74s
prometheus-adapter-758645c65b-54c7g   1/1     Running   0          64s
prometheus-adapter-758645c65b-cmjrv   1/1     Running   0          64s
prometheus-k8s-0                      2/2     Running   0          57s
prometheus-k8s-1                      2/2     Running   0          57s
prometheus-operator-c766b9756-vndp9   2/2     Running   0          63s
```
Pronto, já temos o Prometheus,` Alertmanager`,` Blackbox Exporter`,` Node Exporter` e `Grafana` instalados. 😄
Nesse meu cluster, eu estou com dois nodes, por isso temos dois pods do Node Exporter e dois pods do Prometheus chamados de` prometheus-k8s-0` e `prometheus-k8s-1`.

Agora que já temos o nosso` Kube-Prometheus` instalado, vamos acessar o nosso` Grafana` e verificar se está tudo funcionando corretamente. Para isso, vamos utilizar o kubectl port-forward para acessar o Grafana localmente. Para isso, basta executar o seguinte comando:
```sh
kubectl port-forward -n monitoring svc/grafana 33000:3000
```
Agora que já temos o nosso Grafana rodando localmente, vamos acessar o nosso Grafana através do navegador. Para isso, basta acessar a seguinte `URL: http://localhost:33000`

Para acessar o Grafana, vamos utilizar o usuário admin e a senha admin, e já no primeiro login ele irá pedir para você alterar a senha. Você já conhece o Grafana, não preciso mais apresenta-los, certo? 😄



O importante aqui é ver a quantidade de `Dashboards` criados pelo` Kube-Prometheus`. 😄
Temos `Dashboards` que mostram detalhes do API Server e de diversos componentes do Kubernetes, como Node, Pod, Deployment, etc.



Também temos `Dashboards` que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard` Kubernetes / Compute Resources / Cluster`, que mostra detalhes de CPU e memória utilizados por todos os nós do nosso cluster EKS.



`Dashboards` que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard `Kubernetes / Compute Resources / Namespace (Pods)`, que mostra detalhes de CPU e memória utilizados por todos os pods de todos os namespaces do nosso cluster EKS.



Ainda temos Dashboards que mostram detalhes do nosso cluster EKS, como por exemplo o `dashboard Kubernetes / Compute Resources / Namespace (Workloads)`, que mostra detalhes de CPU e memória utilizados por todos os deployments, statefulsets e daemonsets de todos os namespaces do nosso cluster EKS.



Também temos Dashboards que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard `Kubernetes / Compute Resources / Node`, que mostra detalhes de CPU e memória utilizados por todos os nós do nosso cluster EKS.



Também temos Dashboards que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard` Kubernetes / Compute Resources / Pod (Containers)`, que mostra detalhes de CPU e memória utilizados por todos os containers de todos os pods do nosso cluster EKS.



Eu não vou ficar aqui dando spoilers, vai lá você e confere a quantidade enorme de Dashboards que o` Kube-Prometheus` já vem com ele. \o/


Um dos principais recursos que o` Kube-Prometheus` utiliza é o` ServiceMonitor`. O ServiceMonitor é um recurso do Prometheus Operator que permite que você configure o Prometheus para monitorar um serviço. Para isso, você precisa criar um ServiceMonitor para cada serviço que você deseja monitorar.

O Kube-Prometheus já vem com vários ServiceMonitors configurados, como por exemplo o` ServiceMonitor` do `API Server`, do `Node Exporter`, do `Blackbox Exporter,` etc.

```sh
kubectl get servicemonitors -n monitoring
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
```sh
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
Eu vou dar uma limpada nessa saída para ficar mais fácil de entender:

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
    matchLabels:
      app.kubernetes.io/component: prometheus
      app.kubernetes.io/instance: k8s
      app.kubernetes.io/name: prometheus
      app.kubernetes.io/part-of: kube-prometheus
```
Pronto, eu tirei algumas informações que não são importantes para a criação do ServiceMonitor, elas apenas trazer as informações do service monitor que foi criado e que pegamos a saída.

Com o arquivo limpo, podemos entender melhor o que está acontecendo.
```sh
apiVersion: Versão da API do Kubernetes que estamos utilizando.
kind: Tipo de objeto que estamos criando.
metadata: Informações sobre o objeto que estamos criando.
metadata.annotations: Anotações que podemos adicionar ao nosso objeto.
metadata.labels: Labels que podemos adicionar ao nosso objeto.
metadata.name: Nome do nosso objeto.
metadata.namespace: Namespace onde o nosso objeto será criado.
spec: Especificações do nosso objeto.
spec.endpoints: Endpoints que o nosso ServiceMonitor irá monitorar.
spec.endpoints.interval: Intervalo de tempo que o Prometheus irá fazer a coleta de métricas.
spec.endpoints.port: Porta que o Prometheus irá utilizar para coletar as métricas.
spec.selector: Selector que o ServiceMonitor irá utilizar para encontrar os serviços que ele irá monitorar.
```
Com isso, sabemos que o ServiceMonitor do Prometheus irá monitorar os serviços que possuem as labels app.kubernetes.io/component: prometheus, app.kubernetes.io/instance: k8s, app.kubernetes.io/name: prometheus e app.kubernetes.io/part-of: kube-prometheus, e que ele irá monitorar as portas web e reloader-web com um intervalo de 30 segundos. É fácil ou não é?

Então sempre que precisarmos criar um ServiceMonitor para monitorar algum serviço, basta criarmos um arquivo YAML com as informações que precisamos e aplicarmos em nosso cluster.


Agora que já temos o nosso Kube-Prometheus instalado, vamos acessar o nosso Grafana e verificar se está tudo funcionando corretamente. Para isso, vamos utilizar o kubectl port-forward para acessar o Grafana localmente. Para isso, basta executar o seguinte comando:

kubectl port-forward -n monitoring svc/grafana 33000:3000
Agora que já temos o nosso Grafana rodando localmente, vamos acessar o nosso Grafana através do navegador. Para isso, basta acessar a seguinte` URL: http://localhost:33000`

Para acessar o Grafana, vamos utilizar o usuário admin e a senha admin, e já no primeiro login ele irá pedir para você alterar a senha. Você já conhece o Grafana, não preciso mais apresenta-los, certo? 😄



O importante aqui é ver a quantidade de Dashboards criados pelo` Kube-Prometheus`. 😄
Temos Dashboards que mostram detalhes do API Server e de diversos componentes do Kubernetes, como` Node`,` Pod,` `Deployment`, etc.



Também temos Dashboards que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard ``Kubernetes / Compute Resources / Cluster``, que mostra detalhes de `CPU` e memória utilizados por todos os nós do nosso cluster EKS.



Dashboards que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard `Kubernetes / Compute Resources / Namespace (Pods)`, que mostra detalhes de CPU e memória utilizados por todos os pods de todos os namespaces do nosso cluster EKS.



Ainda temos Dashboards que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard` Kubernetes / Compute Resources / Namespace (Workloads)`, que mostra detalhes de CPU e memória utilizados por todos os `deployments`, `statefulsets` e `daemonsets` de todos os` namespaces` do nosso cluster EKS.



Também temos Dashboards que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard` Kubernetes / Compute Resources / Node`, que mostra detalhes de CPU e memória utilizados por todos os nós do nosso cluster EKS.



Também temos `Dashboards` que mostram detalhes do nosso cluster EKS, como por exemplo o dashboard `Kubernetes / Compute Resources / Pod (Containers)`, que mostra detalhes de CPU e memória utilizados por todos os containers de todos os pods do nosso cluster EKS.



Eu não vou ficar aqui dando spoilers, vai lá você e confere a quantidade enorme de `Dashboards` que o` Kube-Prometheus` já vem com ele. \o/

Um dos principais recursos que o `Kube-Prometheus` utiliza é o ServiceMonitor. O ServiceMonitor é um recurso do Prometheus Operator que permite que você configure o Prometheus para monitorar um serviço. Para isso, você precisa criar um ServiceMonitor para cada serviço que você deseja monitorar.

O `Kube-Prometheus` já vem com vários ServiceMonitors configurados, como por exemplo o ServiceMonitor do `API Server`, do `Node Exporter`, do `Blackbox Exporter`, etc.

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

```sh
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
Eu vou dar uma limpada nessa saída para ficar mais fácil de entender:

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
    matchLabels:
      app.kubernetes.io/component: prometheus
      app.kubernetes.io/instance: k8s
      app.kubernetes.io/name: prometheus
      app.kubernetes.io/part-of: kube-prometheus
```
Pronto, eu tirei algumas informações que não são importantes para a criação do ServiceMonitor, elas apenas trazer as informações do service monitor que foi criado e que pegamos a saída.

Com o arquivo limpo, podemos entender melhor o que está acontecendo.
```sh
apiVersion: Versão da API do Kubernetes que estamos utilizando.
kind: Tipo de objeto que estamos criando.
metadata: Informações sobre o objeto que estamos criando.
metadata.annotations: Anotações que podemos adicionar ao nosso objeto.
metadata.labels: Labels que podemos adicionar ao nosso objeto.
metadata.name: Nome do nosso objeto.
metadata.namespace: Namespace onde o nosso objeto será criado.
spec: Especificações do nosso objeto.
spec.endpoints: Endpoints que o nosso ServiceMonitor irá monitorar.
spec.endpoints.interval: Intervalo de tempo que o Prometheus irá fazer a coleta de métricas.
spec.endpoints.port: Porta que o Prometheus irá utilizar para coletar as métricas.
spec.selector: Selector que o ServiceMonitor irá utilizar para encontrar os serviços que ele irá monitorar.
```
Com isso, sabemos que o` ServiceMonitor` do` Prometheus` irá monitorar os serviços que possuem as labels` app.kubernetes.io/component:` `prometheus, app.kubernetes.io/instance: k8s,`` app.kubernetes.io/name: prometheus` e `app.kubernetes.io/part-of: kube-prometheus,` e que ele irá monitorar as portas` web` e `reloader-web `com um intervalo de 30 segundos. É fácil ou não é?

Então sempre que precisarmos criar um `ServiceMonitor` para monitorar algum serviço, basta criarmos um arquivo `YAML` com as informações que precisamos e aplicarmos em nosso `cluster`.