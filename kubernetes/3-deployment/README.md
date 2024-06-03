## Day-3 Descomplicando Deployments e estratégias de rollout

- `O que é um Deployment`
  Em Kubernetes, um "Deployment" é um recurso que fornece gerenciamento de implantações e atualizações de aplicativos de forma declarativa. Um Deployment permite que você defina um estado desejado para seu aplicativo, especificando quantos réplicas (ou instâncias) do aplicativo devem estar em execução em um determinado momento. Além disso, o Deployment facilita a atualização do aplicativo para novas versões de maneira controlada e com garantia de disponibilidade.
- `Criando um Deployment através de um manifesto`
- `Criando mais Deployment através de um manifesto`
- `Como atualizar um Deployment`
- `Estrátegias de atualizações de nossos Deployments`
- `Fazendo Rollback e conhecendo o comando Rollout`

```bash
kubectl apply -f deployment.yaml
```

```bash
kubectl get deployments -l app=nginx-deployment
```

```bash

```

```bash
kubectl exec -ti -n reload nginx-deployment-c549ff78-5lffb -- nginx -v
```

```bash
kubectl rollout undo deployment -n reload nginx-deployment
```

```bash
kubectl rollout status deployment -n reload nginx-deployment
```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```
