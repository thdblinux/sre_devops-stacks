## Day-4 Descomplicando ReplicaSets, DaemonSets e as Probesdo Kubernets

- `O que é Replicaset ?`
  Um ReplicaSet é um recurso do Kubernetes que é usado para garantir que um número especificado de réplicas (ou pods) de um aplicativo esteja sempre em execução. Ele faz parte da estratégia de escalabilidade e alta disponibilidade no Kubernetes.

- `O Deployment e o ReplicaSet`
- `Crinado o nosso replicaSet`
- `Criando um DaemoSet`
  Vamos para o nosso primeiro exemplo, vamos criar um DaemonSet que vai garantir que todos os nós do cluster executem uma réplica do Pod do node-exporter, que é um exporter de métricas do Prometheus.
- `O que são as Probes no Kubernets ?`
  As probes são uma forma de você monitorar o seu Pod e saber se ele está em um estado saudável ou não. Com elas é possível assegurar que seus Pods estão rodando e respondendo de maneira correta, e mais do que isso, que o Kubernetes está testando o que está sendo executado dentro do seu Pod.
  Hoje nós temos disponíveis três tipos de probes, a livenessProbe, a readinessProbe e a startupProbe. Vamos ver no detalhe cada uma delas
  - `Liveness Probe`
    A livenessProbe é a nossa probe de verificação de integridade, o que ela faz é verificar se o que está rodando dentro do Pod está saudável. O que fazemos é criar uma forma de testar se o que temos dentro do Pod está respondendo conforme esperado. Se por acaso o teste falhar, o Pod será reiniciado.
    Para ficar mais claro, vamos mais uma vez utilizar o exemplo com o Nginx. Gosto de usar o Nginx como exemplo, pois sei que toda pessoa já o conhece, e assim, fica muito mais fácil de entender o que está acontecendo. Afinal, você está aqui para aprender Kubernetes, e se for com algo que você já conhece, fica muito mais fácil de entender.
- `Readiness Probe`
  A readinessProbe é uma forma de o Kubernetes verificar se o seu container está pronto para receber tráfego, se ele está pronto para receber requisições vindas de fora.
  Essa é a nossa probe de leitura, ela fica verificando se o nosso container está pronto para receber requisições, e se estiver pronto, ele irá receber requisições, caso contrário, ele não irá receber requisições, pois será removido do endpoint do serviço, fazendo com que o tráfego não chegue até ele.
- `Startup Probe`
  Chegou a hora de falar sobre a probe, que na minha humilde opinião, é a menos utilizada, mas que é muito importante, a startupProbe.
  Ela é a responsável por verificar se o nosso container foi inicializado corretamente, e se ele está pronto para receber requisições.
  Ele é muito parecido com a readinessProbe, mas a diferença é que a startupProbe é executada apenas uma vez no começo da vida do nosso container, e a readinessProbe é executada de tempos em tempos.
