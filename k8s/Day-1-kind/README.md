# Descomplicando Kubernetes-2023

## Day-1 - Entendendo o que são containers e o Kuberenets

- `O que é um container ?`
  Um container é uma unidade de software leve e independente que inclui tudo o que é necessário para executar um aplicativo, incluindo o código, as bibliotecas e as configurações. Containers são uma forma de virtualização a nível de sistema operacional que permite que vários contêineres compartilhem o mesmo sistema operacional host, mas permaneçam isolados uns dos outros.

- `O que é um container engine ?`
- `o que é OCI ?`
- `O que é o Kubernetes ?`
- `O que são os workers e o control plane do Kubernetes ?`
- `Quais os componentes do control plane do Kubernetes`
- `Quais os componentes dos workes do kubernetes ?`
- `Quais as portas TCP e UDP dos componentes do kubernetes`
- `Introdução a pods, replica sets, deployments e service`
- `Entendo e instalando o Kubectl`
- `Criando o nosso primeiro cluster com o Kind`
- `Primeiros passos no Kubernetes com o kubectl`
- `Conhecendo o YAML e o kubectl com dry-run`

## Instalação do Docker no GNU/Linux

```bash
curl -fsSL https://get.docker.com/ | sh
```

## Instalação do Kubectl no GNU/Linux

```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
```

```bash
chmod +x ./kubectl
```

```bash
sudo mv ./kubectl /usr/local/bin/kubectl
```

```bash
kubectl version --client
```

## Customizando o kubectl

### Auto-complete

Execute o seguinte comando para configurar o alias e autocomplete para o kubectl.

No Bash:

```bash
source <(kubectl completion bash) # configura o autocomplete na sua sessão atual (antes, certifique-se de ter instalado o pacote bash-completion).
```

```bash
echo "source <(kubectl completion bash)" >> ~/.bashrc # add autocomplete permanentemente ao seu shell.
```

No ZSH:

```bash
source <(kubectl completion zsh)
```

```bash
echo "[[ $commands[kubectl] ]] && source <(kubectl completion zsh)"
```

## Kind

O Kind (Kubernetes in Docker) é outra alternativa para executar o Kubernetes num ambiente local para testes e aprendizado, mas não é recomendado para uso em produção.

## Instalação no GNU/Linux

Para fazer a instalação no GNU/Linux, execute os seguintes comandos.

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.14.0/kind-linux-amd64
```

```bash
chmod +x ./kind
```

```bash
sudo mv ./kind /usr/local/bin/kind
```

## Criando um cluster com múltiplos nós locais com o Kind

```bash
kind create cluster --name kind-multinodes --config kind-3nodes.yaml
```

```bash
kubectl cluster-info --context kind-kind-multinodes
```

```bash
kind delete clusters $(kind get clusters)
```

cat << EOF > $HOME/kind-3nodes.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:

- role: control-plane
- role: worker
- role: worker
- role: worker
  EOF

## Para saber mais sobre Kubernetes, containers e instalações de componentes em outros sistemas operacionais, consulte o Livro Gratuito Descomplicando o Kubernetes.

[Descomplicando o Kubernetes - Livro Gratuito](https://livro.descomplicandokubernetes.com.br/?utm_medium=social&utm_source=linktree&utm_campaign=livro+descomplicando+o+kubernetes+gratuito)

No contexto do Kubernetes, o crescimento horizontal e vertical referem-se à escala de um cluster para lidar com a demanda de recursos ou carga de trabalho.

- ### Crescimento Horizontal (Scaling Out):

  O crescimento horizontal envolve adicionar mais instâncias (nodes) ao cluster. Quando um cluster Kubernetes escala horizontalmente, novos nós são adicionados para distribuir a carga de trabalho e aumentar a capacidade de processamento, armazenamento e rede. Essa abordagem ajuda a lidar com um aumento na demanda de tráfego ou de aplicativos, distribuindo a carga entre os nós adicionados.

- ### Crescimento Vertical (Scaling Up):
  O crescimento vertical refere-se ao aumento dos recursos de um nó individual dentro do cluster. Isso implica adicionar mais capacidade de CPU, memória ou outros recursos a um único nó. No contexto do Kubernetes, escalar verticalmente pode significar atualizar os recursos (como CPU ou memória) de um pod ou de um node existente para acomodar mais carga de trabalho ou processamento mais intensivo.

Ambos os métodos de escalabilidade, horizontal e vertical, têm suas vantagens e limitações:

- ### Crescimento Horizontal:

  Mais adequado para aplicativos que podem ser distribuídos e executados em paralelo em vários nodes, distribuindo a carga entre eles. É altamente escalável e pode melhorar a tolerância a falhas, mas pode requerer mais gerenciamento para manter a consistência do estado e comunicação entre os componentes distribuídos.

- ### Crescimento Vertical:
  Útil quando um único componente ou aplicativo precisa de mais recursos. Pode ser mais fácil de implementar inicialmente, mas pode eventualmente atingir limitações físicas ou de hardware em termos de escalabilidade, e pode ser menos resiliente a falhas do que o crescimento horizontal.

O Kubernetes oferece suporte a ambos os métodos de escalabilidade, permitindo que os operadores de cluster escolham a abordagem mais adequada às necessidades específicas de suas aplicações e ambientes.
