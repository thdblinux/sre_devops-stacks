# O que é o Ingress?

O Ingress é um recurso do Kubernetes que gerencia o acesso externo aos serviços dentro de um cluster. Ele funciona como uma camada de roteamento HTTP/HTTPS, permitindo a definição de regras para direcionar o tráfego externo para diferentes serviços back-end. O Ingress é implementado através de um controlador de Ingress, que pode ser alimentado por várias soluções, como NGINX, Traefik ou Istio, para citar alguns.

Tecnicamente, o Ingress atua como uma abstração de regras de roteamento de alto nível que são interpretadas e aplicadas pelo controlador de Ingress. Ele permite recursos avançados como balanceamento de carga, SSL/TLS, redirecionamento, reescrita de URL, entre outros.

# Principais Componentes e Funcionalidades:
**Controlador de Ingress**: É a implementação real que satisfaz um recurso Ingress. Ele pode ser implementado através de várias soluções de proxy reverso, como NGINX ou HAProxy.

**Regras de Roteamento**: Definidas em um objeto YAML, essas regras determinam como as requisições externas devem ser encaminhadas aos serviços internos.

**Backend Padrão**: Um serviço de fallback para onde as requisições são encaminhadas se nenhuma regra de roteamento for correspondida.

**Balanceamento de Carga**: Distribuição automática de tráfego entre múltiplos pods de um serviço.

**Terminação SSL/TLS**: O Ingress permite a configuração de certificados SSL/TLS para a terminação de criptografia no ponto de entrada do cluster.

**Anexos de Recurso**: Possibilidade de anexar recursos adicionais como ConfigMaps ou Secrets, que podem ser utilizados para configurar comportamentos adicionais como autenticação básica, listas de controle de acesso etc.

# Usando KinD com Ingress
**Introdução**
KinD é uma ferramenta muito útil para testes e desenvolvimento com Kubernetes. Nesta seção atualizada, fornecemos detalhes específicos para garantir que o Ingress funcione como esperado em um cluster KinD.

**Criando o Cluster com Configurações Especiais**
Ao criar um cluster KinD, podemos especificar várias configurações que incluem mapeamentos de portas e rótulos para nós.

1.Crie um arquivo chamado kind-config.yaml com o conteúdo abaixo:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
```
2. Em seguida, crie o cluster usando este arquivo de configuração:
```sh
kind create cluster --config kind-config.yaml
```
**Instalando um Ingress Controller**
Vamos continuar usando o Nginx Ingress Controller como exemplo, que é amplamente adotado e bem documentado.

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
```
Você pode utilizar a opção `wait` do` kubectl`, assim quando os pods estiverem prontos, ele irá liberar o shell, veja:

```sh
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```
No comando acima, estamos esperando que os pods do Ingress Controller estejam prontos, com o label `app.kubernetes.io/component=controller`, no namespace `ingress-nginx`, e caso não estejam prontos em 90 segundos, o comando irá falhar.


# Minikube
Para instalar o ingress controller no Minikube, você pode usar o sistema de addons do próprio Minikube. O comando a ser executado é:

```sh
minikube addons enable ingress
```

# MicroK8s
No caso do MicroK8s, o ingress controller também pode ser instalado via sistema de addons. O comando para isso é:
```sh
microk8s enable ingress
```

# AWS (Amazon Web Services)
Na AWS, o ingress controller é exposto através de um Network Load Balancer (NLB). O comando para instalação é:
```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/aws/deploy.yaml
```
Você também pode configurar a terminação TLS no Load Balancer da AWS, editando o arquivo `deploy.yaml` com as informações do seu Certificate Manager (ACM).

# Azure
```sh
No Azure, o ingress controller é instalado com o comando:
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```

# GCP (Google Cloud Platform)
No GCP, primeiramente certifique-se de que seu usuário tem permissões de cluster-admin. Depois, instale o ingress controller com:
```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```
Você também pode precisar configurar regras de firewall se estiver usando um cluster privado.

# Bare Metal
Para instalações em Bare Metal ou VMs "cruas", você pode usar um NodePort para testes rápidos:
```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/baremetal/deploy.yaml
```
Este comando mapeará o ingress controller para uma porta no intervalo de 30000-32767.


# Criando um Recurso de Ingress
Agora, vamos criar um recurso de Ingress para nosso serviço giropops-senhas criado anteriormente. Crie um arquivo chamado ingress-1.yaml:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: giropops-senhas
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /giropops-senhas
        pathType: Prefix
        backend:
          service: 
            name: giropops-senhas
            port:
              number: 5000
```

## Após criar o arquivo, aplique-o:
```sh
kubectl apply -f ingress-1.yaml
```
**Agora vamos ver se o nosso Ingress foi criado corretamente:**
```sh
kubectl get ingress
```
**Para ver com mais detalhes, você pode usar o comando describe:**
```sh
kubectl describe ingress ingress-1
```
Tanto na saída do comando get quanto na saída do comando describe, você deve ver o endereço IP do seu Ingress no campo Address.

Você pode pegar esse IP através do comando:
```sh
kubectl get ingress ingress-1 -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```
Caso você esteja utilizando um cluster gerenciado por algum provedor de nuvem, como o GKE, você pode utilizar o comando:
```sh
kubectl get ingress ingress-1 -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```
Isso porque quando você possui um cluster EKS, AKS, GCP, etc, o Ingress Controller irá criar um LoadBalancer para você, e o endereço IP do LoadBalancer será o endereço IP do seu Ingress, simples assim.

Para testar, você pode usar o comando curl com o IP, hostname ou load balancer do seu Ingress:
```sh
curl ENDEREÇO_DO_INGRESS/giropops-senhas
```

