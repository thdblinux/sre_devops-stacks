## Day-2 - Descomplicando os pods e Limites de Recursos

- `O que é um Pod?`
  Um Pod é a unidade mais simples e básica no Kubernetes, sendo a menor unidade que você pode criar ou implantar. É um ambiente de execução para contêineres em um cluster Kubernetes.
- `Os sencacionais kubectl get pods e o kubectl describe pods`
- `Conhecendo o kubectl attach e o kubectl exec`
- `Criando o nosso primeiro pod multicontainer utilizando um manifesto`
- `Limitando o consumo de recursos de CPU e Memória`
- `Configurando o nosso primeiro volume EmptyDir`

```bash
git add .
```

```bash
git commit -m ""
```

```bash
git push origin [branch_principal]
```

```bash
kubectl get pod
```

```bash
kubectl get nodes
```

```bash
 kubectl get pod -o wide
```

```bash
kubectl get pods matrix -o yaml
```

```bash
kubectl exec -ti matrix -- bash
```

```bash
kubectl attach matrix -c matrix -ti
```

```bash
kubectl get pods -A
```

```bash
kubectl get pods --all-namespaces
```

```bash
kubectl get pods -n kube-system
```

```bash
 kubectl exec matrix -- cat /usr/share/nginx/html/index.html
```

```bash
kubectl run matrix-1 --image alpine --dry-run=client -o yaml
```

```bash
kubectl logs matrix-1 -f
```

```bash
kubectl logs matrix-1 -c busybox
```
