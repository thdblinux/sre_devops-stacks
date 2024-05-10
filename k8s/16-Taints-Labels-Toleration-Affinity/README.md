## O que vamos ver no dia de hoje?

Hoje é dia de falar sobre `Taints`, `Tolerations`, `Affinity` e `Antiaffinity`. Vamos entender como eles podem nos ajudar no dia-a-dia na administração de um cluster `Kubernetes`.

Com eles podemos isolar `workloads`, garantir que Pods sejam agendados em Nodes específicos e até mesmo evitar que Pods sejam agendados em determinados Nodes do cluster.

Bora lá, pois o dia será intenso de coisas novas e com certeza você vai aprender muito! Bora?

## O Nosso cluster de exemplo
Para que possamos ter alguns exemplos mais divertido, vamos imaginar que temos um empresa chamada Guilda, e que essa empresa tem o seu cluster `Kubernetes` de produção composto por 08 nodes, sendo 4 control planes e 4 workers. Ele está dividido em duas regiões, São Paulo e Salvador, chamadas de guilda-br-sp e guilda-br-ssa respectivamente. E cada região tem dois datacenters, guilda-sp-1 e guilda-sp-2 em São Paulo e guilda-br-ssa-1 e guilda-br-ssa-2 em Salvador.

```sh
kubectl get nodes
```

```sh
NAME                     STATUS   ROLES           AGE     VERSION
guilda-control-plane1   Ready    control-plane   65d     v1.27.3
guilda-control-plane2   Ready    control-plane   65d     v1.27.3
guilda-control-plane3   Ready    control-plane   65d     v1.27.3
guilda-control-plane4   Ready    control-plane   65d     v1.27.3
guilda-worker1          Ready    <none>          65d     v1.27.3
guilda-worker2          Ready    <none>          65d     v1.27.3
guilda-worker3          Ready    <none>          65d     v1.27.3
guilda-worker4          Ready    <none>          65d     v1.27.3
```
A nossa missão é criar as `Labels` e `Taints` necessárias para que nosso cluster fique organizado, seguro e com alta disponibilidade. E com isso, com alguns ajustes em nossos deployments, garantir que nossos Pods sejam agendados nos Nodes corretos e distribuídos entre os datacenters corretamente.

A distribuição dos nossos nodes nas regiões e datacenters é a seguinte:

- guilda-br-sp

  - guilda-br-sp-1
    - guilda-control-plane1
    - guilda-worker3
  - guilda-br-sp-2
    - guilda-control-plane4
    - guilda-worker1
- guilda-br-ssa
  - guilda-br-ssa-1
    - guilda-control-plane2
    - guilda-worker2
  - guilda-br-ssa-2
    - guilda-control-plane3
    - guilda-worker4
  
A primeira coisa que precisamos fazer é criar as `Labels` em nossos `Nodes`. Para isso, vamos utilizar o comando `kubectl label nodes` e vamos adicionar as labels `region` e `datacenter` em cada um dos nossos `Nodes`.

```sh
kubectl label nodes guilda-control-plane1 region=guilda-br-sp datacenter=guilda-br-sp-1
kubectl label nodes guilda-control-plane2 region=guilda-br-ssa datacenter=guilda-br-ssa-1
kubectl label nodes guilda-control-plane3 region=guilda-br-ssa datacenter=guilda-br-ssa-2
kubectl label nodes guilda-control-plane4 region=guilda-br-sp datacenter=guilda-br-sp-2
kubectl label nodes guilda-worker1 region=guilda-br-sp datacenter=guilda-br-sp-2
kubectl label nodes guilda-worker2 region=guilda-br-ssa datacenter=guilda-br-ssa-1
kubectl label nodes guilda-worker3 region=guilda-br-sp datacenter=guilda-br-sp-1
kubectl label nodes guilda-worker4 region=guilda-br-ssa datacenter=guilda-br-ssa-2
```
Com o comando acima estamos utilizando o `kubectl label nodes` para adicionar as `labels` `region` e `datacenter` em cada um dos nossos `Nodes`. Agora, se executarmos o comando `kubectl get nodes guilda-control-plane1 --show-labels`, veremos algo como:
```sh
NAME                     STATUS   ROLES           AGE     VERSION   LABELS
guilda-control-plane1   Ready    control-plane   65d     v1.27.3    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,datacenter=guilda-br-sp-1kubernetes.io/arch=amd64,kubernetes.io/hostname=guilda-control-plane1,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=region=guilda-br-sp
```
Pronto, as nossas` labels` estão criadas, com isso já conseguimos ter um pouco mais de organização em nosso `cluster`.

Mas ainda não acabou o nosso trabalho, cada uma das regiões possui um node com um `hardware` especial, que é uma `GPU`. Vamos criar uma label para identificar esses `nodes`, mas por enquanto é somente para identificar, não vamos fazer nada com eles ainda.
```sh
kubectl label nodes guilda-worker1 gpu=true
kubectl label nodes guilda-worker4 gpu=true
```
Pronto, por enquanto isso resolve, mas com certeza precisaremos adicionar mais labels em nossos nodes no futuro, mas por enquanto isso já resolve o nosso problema.

Caso eu queira remover alguma Label, basta utilizar o comando `kubectl label nodes guilda-control-plane1 region-` e a label será removida.

Agora vamos entender como funcionam as `Taints`.

## O que são Taints?
Taints são "manchas" ou "marcações" aplicadas aos Nodes que os marcam para evitar que certos Pods sejam agendados neles. Essa é uma forma bastante comum de isolar workloads em um cluster `Kubernetes`, por exemplo em momentos de manutenção ou quando você tem Nodes com recursos especiais, como GPUs.

Os Taints são aplicados nos Nodes e podem ter um efeito de `NoSchedule`, `PreferNoSchedule` ou `NoExecute`. O efeito `NoSchedule` faz com que o `Kubernetes` não agende Pods nesse Node a menos que eles tenham uma Toleration correspondente. O efeito Prefer`NoSchedule` faz com que o `Kubernetes` tente não agendar, mas não é uma garantia. E o efeito `NoExecute` faz com que os Pods existentes sejam removidos se não tiverem uma Toleration correspondente.

Agora vamos entender isso na prática!

Em nosso primeiro exemplo vamos conhecer a `Taint` `NoSchedule`. Para que você possa configurar um `Taint` em um Node, você utiliza o comando kubectl `taint`. Por exemplo:
```sh
kubectl taint nodes guilda-worker1 key=value:NoSchedule
```

kubectl `taint` nodes guilda-worker1 key=value:`NoSchedule`
No comando acima, estamos aplicando um `Taint` no Node guilda-worker com a chave `key` e o valor `value` e com o efeito `NoSchedule`. Isso significa que o `Kubernetes` não irá agendar nenhum Pod nesse Node a menos que ele tenha uma Toleration correspondente, que veremos mais adiante.

Nesse exemplo estamos utilizando a chave `key` e o valor `value`, mas você pode utilizar qualquer chave e valor que desejar. Por exemplo, você pode utilizar `environment=production` para marcar um Node como sendo de produção, ou gpu=true para marcar um Node com uma GPU.

Você irá entender melhor o porquê de utilizar Taints e o porquê de utilizar chaves e valores específicos quando falarmos sobre Tolerations.

Para visualizar os Taints aplicados em um Node, você pode utilizar o comando kubectl describe node guilda-worker1. Você verá algo como:
```sh
Taints:             key=value:`NoSchedule`
```
Está lá conforme esperado! Agora o que precisamos fazer é testar!
O nosso cluster ainda não está com nenhuma aplicação em execução, somente os Pods do próprio `Kubernetes`, então vamos criar alguns para testar. 😃

Para esse teste, vamos criar um Deployment com 10 réplicas do Nginx, e vamos ver o que acontece.
```sh
kubectl create deployment nginx --image=nginx --replicas=10
```
Agora vamos verificar se os Pods foram criados e se estão em execução.
```sh
kubectl get pods -o wide
```
A saída será algo como:

```sh
NAME                     READY   STATUS    RESTARTS   AGE   IP           NODE              NOMINATED NODE   READINESS GATES
nginx-77b4fdf86c-4rwb9   1/1     Running   0          12s   10.244.4.3   guilda-worker3   <none>           <none>
nginx-77b4fdf86c-chpgb   1/1     Running   0          12s   10.244.6.2   guilda-worker2   <none>           <none>
nginx-77b4fdf86c-dplq7   1/1     Running   0          12s   10.244.5.3   guilda-worker4   <none>           <none>
nginx-77b4fdf86c-l5vwq   1/1     Running   0          12s   10.244.6.4   guilda-worker2   <none>           <none>
nginx-77b4fdf86c-nwwvn   1/1     Running   0          12s   10.244.5.2   guilda-worker4   <none>           <none>
nginx-77b4fdf86c-qz9t4   1/1     Running   0          12s   10.244.5.4   guilda-worker4   <none>           <none>
nginx-77b4fdf86c-r4lt6   1/1     Running   0          12s   10.244.6.5   guilda-worker2   <none>           <none>
nginx-77b4fdf86c-rmqnm   1/1     Running   0          12s   10.244.4.4   guilda-worker3   <none>           <none>
nginx-77b4fdf86c-rsgbg   1/1     Running   0          12s   10.244.4.2   guilda-worker3   <none>           <none>
nginx-77b4fdf86c-wnxg7   1/1     Running   0          12s   10.244.6.3   guilda-worker2   <none>           <none>
```
Perceba que não temos nenhum Pod em execução no Node `guilda-worker1`, que é o Node que aplicamos o `Taint`. Isso acontece porque o `Kubernetes` não irá agendar nenhum Pod nesse Node a menos que ele tenha uma Toleration correspondente, que veremos mais adiante.

Agora vamos remover o `Taint` do Node `guilda-worker1` e ver o que acontece.
```sh
kubectl taint nodes guilda-worker1 key=value:NoSchedule-
```
Os Pods não serão movidos automaticamente para o Node `guilda-worker1`, mas podemos usar o comando kubectl rollout restart deployment nginx para reiniciar o Deployment e o `Kubernetes` redistribuirá os Pods entre os Nodes disponíveis.

```sh
kubectl rollout restart deployment nginx
```
Agora vamos verificar se os Pods foram criados e se estão em execução.
```sh
kubectl get pods -o wide
```
A saída será algo como:
```sh
NAME                     READY   STATUS    RESTARTS   AGE   IP            NODE              NOMINATED NODE   READINESS GATES
nginx-7c58f9889c-6qcpl   1/1     Running   0          28s   10.244.4.10   guilda-worker3   <none>           <none>
nginx-7c58f9889c-lj7p5   1/1     Running   0          29s   10.244.3.3    guilda-worker1   <none>           <none>
nginx-7c58f9889c-mdrj7   1/1     Running   0          29s   10.244.4.9    guilda-worker3   <none>           <none>
nginx-7c58f9889c-nr7h9   1/1     Running   0          29s   10.244.6.9    guilda-worker2   <none>           <none>
nginx-7c58f9889c-pqrb9   1/1     Running   0          26s   10.244.3.4    guilda-worker1   <none>           <none>
nginx-7c58f9889c-pzx7n   1/1     Running   0          29s   10.244.5.8    guilda-worker4   <none>           <none>
nginx-7c58f9889c-qn9hh   1/1     Running   0          28s   10.244.5.9    guilda-worker4   <none>           <none>
nginx-7c58f9889c-wmm2n   1/1     Running   0          26s   10.244.6.11   guilda-worker2   <none>           <none>
nginx-7c58f9889c-znrjt   1/1     Running   0          29s   10.244.3.2    guilda-worker1   <none>           <none>
nginx-7c58f9889c-zp9g9   1/1     Running   0          28s   10.244.6.10   guilda-worker2   <none>           <none>
```
Pronto, ele redistribuiu os Pods entre os Nodes disponíveis, e voltou a executar Pods no Node `guilda-worker1`, afinal, nós removemos o `Taint` dele.

Agora vamos testar o efeito `NoExecute`. Para isso, vamos aplicar um `Taint` no Node `guilda-worker1` com o efeito `NoExecute`.
```sh
kubectl taint nodes guilda-worker1 key=value:NoExecute
```
Diferente do efeito `NoSchedule`, o efeito `NoExecute` faz com que os Pods existentes sejam removidos se não tiverem uma Toleration correspondente.

Vamos ver o que aconteceu com os nossos Pods.
```sh
NAME                     READY   STATUS    RESTARTS   AGE     IP            NODE              NOMINATED NODE   READINESS GATES
nginx-7c58f9889c-6qcpl   1/1     Running   0          2m29s   10.244.4.10   guilda-worker3   <none>           <none>
nginx-7c58f9889c-gm6tb   1/1     Running   0          5s      10.244.4.11   guilda-worker3   <none>           <none>
nginx-7c58f9889c-lnhmf   1/1     Running   0          5s      10.244.5.10   guilda-worker4   <none>           <none>
nginx-7c58f9889c-mdrj7   1/1     Running   0          2m30s   10.244.4.9    guilda-worker3   <none>           <none>
nginx-7c58f9889c-mz78w   1/1     Running   0          5s      10.244.6.12   guilda-worker2   <none>           <none>
nginx-7c58f9889c-nr7h9   1/1     Running   0          2m30s   10.244.6.9    guilda-worker2   <none>           <none>
nginx-7c58f9889c-pzx7n   1/1     Running   0          2m30s   10.244.5.8    guilda-worker4   <none>           <none>
nginx-7c58f9889c-qn9hh   1/1     Running   0          2m29s   10.244.5.9    guilda-worker4   <none>           <none>
nginx-7c58f9889c-wmm2n   1/1     Running   0          2m27s   10.244.6.11   guilda-worker2   <none>           <none>
nginx-7c58f9889c-zp9g9   1/1     Running   0          2m29s   10.244.6.10   guilda-worker2   <none>           <none>
```
Funcionou! Os Pods que estavam executando no Node `guilda-worker1` foram removidos e agendados em outros Nodes.

Nesse caso, o `Kubernetes` não irá agendar nenhum Pod nesse Node a menos que ele tenha uma Toleration para o `Taint` que aplicamos.

Isso é interessante em momentos que você precisa realizar manutenção em um Node, garantindo que não teremos nenhum Pod executando nele e que nenhum Pod será agendado nesse Node.

Agora vamos remover o `Taint` do Node `guilda-worker1` e ver o que acontece.
```sh
kubectl taint nodes guilda-worker1 key=value:NoExecute-
```
Mais uma vez vale lembrar, o `Kubernetes` não irá mover os Pods automaticamente para o `Node` `guilda-worker1`, mas podemos usar o comando` kubectl rollout restart deployment nginx` para reiniciar o Deployment e o `Kubernetes` redistribuirá os Pods entre os Nodes disponíveis.
```sh
kubectl rollout restart deployment nginx
```
Simples como voar!

Agora vamos entender o efeito `PreferNoSchedule`. Para isso, vamos aplicar um `Taint` no `Node` `guilda-worker1` com o efeito `PreferNoSchedule`.
```sh
kubectl taint nodes guilda-worker1 key=value:PreferNoSchedule
```
Diferente do efeito `NoSchedule`, o efeito `PreferNoSchedule` faz com que o `Kubernetes` tente não agendar, mas não é uma garantia.

Ele tentará agendar os Pods em outros Nodes, mas se não for possível, ele irá agendar no Node que tem o `Taint`.

Os nossos Pods estão distribuidos da seguinte forma:
```sh
NAME                     READY   STATUS    RESTARTS   AGE   IP            NODE              NOMINATED NODE   READINESS GATES
nginx-67668985bc-6h2ml   1/1     Running   0          9s    10.244.3.5    guilda-worker1   <none>           <none>
nginx-67668985bc-dbnxr   1/1     Running   0          9s    10.244.5.11   guilda-worker4   <none>           <none>
nginx-67668985bc-hxkt8   1/1     Running   0          9s    10.244.3.6    guilda-worker1   <none>           <none>
nginx-67668985bc-ldwck   1/1     Running   0          9s    10.244.6.13   guilda-worker2   <none>           <none>
nginx-67668985bc-nvcd8   1/1     Running   0          7s    10.244.3.7    guilda-worker1   <none>           <none>
nginx-67668985bc-pwz4d   1/1     Running   0          9s    10.244.4.12   guilda-worker3   <none>           <none>
nginx-67668985bc-v2s2b   1/1     Running   0          7s    10.244.4.13   guilda-worker3   <none>           <none>
nginx-67668985bc-xdqjw   1/1     Running   0          7s    10.244.5.13   guilda-worker4   <none>           <none>
nginx-67668985bc-xkdt8   1/1     Running   0          7s    10.244.5.12   guilda-worker4   <none>           <none>
nginx-67668985bc-zdtsq   1/1     Running   0          7s    10.244.6.14   guilda-worker2   <none>           <none>
```
Temos Pods em execução no `Node` `guilda-worker1`, que é o Node que aplicamos o `Taint`, pois esses `Pods` já estavam em execução antes de aplicarmos o `Taint`.

Agora vamos aumentar o número de réplicas do nosso Deployment para 20 e ver o que acontece.
```sh
kubectl scale deployment nginx --replicas=20
```
Agora vamos verificar se os Pods foram criados e se estão em execução.
```sh
kubectl get pods -o wide
```
A saída será algo como:
```sh
NAME                     READY   STATUS    RESTARTS   AGE     IP            NODE              NOMINATED NODE   READINESS GATES
nginx-67668985bc-6h2ml   1/1     Running   0          2m24s   10.244.3.5    guilda-worker1   <none>           <none>
nginx-67668985bc-9298b   1/1     Running   0          22s     10.244.5.17   guilda-worker4   <none>           <none>
nginx-67668985bc-c8nck   1/1     Running   0          22s     10.244.4.17   guilda-worker3   <none>           <none>
nginx-67668985bc-dbnxr   1/1     Running   0          2m24s   10.244.5.11   guilda-worker4   <none>           <none>
nginx-67668985bc-fds62   1/1     Running   0          22s     10.244.6.18   guilda-worker2   <none>           <none>
nginx-67668985bc-gtmq8   1/1     Running   0          22s     10.244.4.19   guilda-worker3   <none>           <none>
nginx-67668985bc-hxkt8   1/1     Running   0          2m24s   10.244.3.6    guilda-worker1   <none>           <none>
nginx-67668985bc-kbtqc   1/1     Running   0          22s     10.244.4.20   guilda-worker3   <none>           <none>
nginx-67668985bc-ldwck   1/1     Running   0          2m24s   10.244.6.13   guilda-worker2   <none>           <none>
nginx-67668985bc-mtsxv   1/1     Running   0          22s     10.244.6.19   guilda-worker2   <none>           <none>
nginx-67668985bc-nvcd8   1/1     Running   0          2m22s   10.244.3.7    guilda-worker1    <none>           <none>
nginx-67668985bc-pwz4d   1/1     Running   0          2m24s   10.244.4.12   guilda-worker3   <none>           <none>
nginx-67668985bc-snvnt   1/1     Running   0          22s     10.244.5.16   guilda-worker4   <none>           <none>
nginx-67668985bc-txgd4   1/1     Running   0          22s     10.244.4.18   guilda-worker3   <none>           <none>
nginx-67668985bc-v2s2b   1/1     Running   0          2m22s   10.244.4.13   guilda-worker3   <none>           <none>
nginx-67668985bc-w9hmj   1/1     Running   0          22s     10.244.6.20   guilda-worker2   <none>           <none>
nginx-67668985bc-xdqjw   1/1     Running   0          2m22s   10.244.5.13   guilda-worker4   <none>           <none>
nginx-67668985bc-xkdt8   1/1     Running   0          2m22s   10.244.5.12   guilda-worker4   <none>           <none>
nginx-67668985bc-zdtsq   1/1     Running   0          2m22s   10.244.6.14   guilda-worker2   <none>           <none>
nginx-67668985bc-zfglb   1/1     Running   0          22s     10.244.6.21   guilda-worker2   <none>           <none>
```
O que vemos na saída do comando é que o `Kube-Scheduler `agendou os `Pods` em outros Nodes, mantendo somente os Pods que já estavam em execução no Node `guilda-worker1.`

O `Kube-scheduler` somente irá agendar novos pods no Node `guilda-worker1` se não houver nenhum outro Node disponível. Simples demais, não?!?
