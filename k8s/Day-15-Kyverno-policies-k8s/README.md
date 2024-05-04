## Kyverno - Como fazer o seu cluster Kubernetes mais seguro

Kyverno é uma ferramenta de gerenciamento de políticas para Kubernetes, focada na automação de várias tarefas relacionadas à segurança e configuração dos clusters de Kubernetes. Ele permite que você defina, gerencie e aplique políticas de forma declarativa para garantir que os clusters e suas cargas de trabalho estejam em conformidade com as regras e normas definidas.

**Principais Funções do Kyverno:**

1. Validação de Recursos: Verifica se os recursos do Kubernetes estão em conformidade com as políticas definidas. Por exemplo, pode garantir que todos os Pods tenham limites de CPU e memória definidos.

2. Mutação de Recursos: Modifica automaticamente os recursos do Kubernetes para atender às políticas definidas. Por exemplo, pode adicionar automaticamente labels específicos a todos os novos Pods.

3. Geração de Recursos: Cria recursos adicionais do Kubernetes com base nas políticas definidas. Por exemplo, pode gerar NetworkPolicies para cada novo Namespace criado.

## Instalando o Kyverno
A instalação do Kyverno em um cluster Kubernetes pode ser feita de várias maneiras, incluindo a utilização de um gerenciador de pacotes como o Helm, ou diretamente através de arquivos YAML. Aqui estão os passos básicos para instalar o Kyverno:

**Utilizando Helm**
O Helm é um gerenciador de pacotes para Kubernetes, que facilita a instalação e gerenciamento de aplicações. Para instalar o Kyverno com Helm, siga estes passos:

1. Adicione o Repositório do Kyverno:
```sh
helm repo add kyverno https://kyverno.github.io/kyverno/
```
```sh
helm repo update
```
**Instale o Kyverno:**

Você pode instalar o Kyverno no namespace kyverno usando o seguinte comando:
```sh
helm install kyverno kyverno/kyverno --namespace kyverno --create-namespace
```
## Verificando a Instalação
Após a instalação, é importante verificar se o Kyverno foi instalado corretamente e está funcionando como esperado.

**Verifique os Pods:**
```sh
kubectl get pods -n kyverno
```
Este comando deve mostrar os pods do Kyverno em execução no namespace especificado.

**Verifique os CRDs:**
```sh
kubectl get crd | grep kyverno
```
Este comando deve listar os `CRDs` relacionados ao Kyverno, indicando que foram criados corretamente.

Lembrando que é sempre importante consultar a documentação oficial para obter as instruções mais atualizadas e detalhadas, especialmente se estiver trabalhando com uma configuração específica ou uma versão mais recente do Kyverno ou do Kubernetes.

## Criando a nossa primeira Policy
Kyverno permite que você defina, gerencie e aplique políticas de forma declarativa para garantir que os clusters e suas cargas de trabalho estejam em conformidade com as regras e normas definidas.

As políticas, ou as policies em inglês, do Kyverno podem ser aplicadas de duas maneiras principais: a nível de cluster (ClusterPolicy) ou a nível de namespace específico (Policy).

1. **ClusterPolicy:** Quando você define uma política como ClusterPolicy, ela é aplicada a todos os namespaces no cluster. Ou seja, as regras definidas em uma ClusterPolicy são automaticamente aplicadas a todos os recursos correspondentes em todos os namespaces, a menos que especificamente excluídos.

2. **Policy:** Se você deseja aplicar políticas a um namespace específico, você usaria o tipo Policy. As políticas definidas como Policy são aplicadas apenas dentro do namespace onde são criadas.

Se você não especificar nenhum namespace na política ou usar ClusterPolicy, o Kyverno assumirá que a política deve ser aplicada globalmente, ou seja, em todos os namespaces.

## Exemplo de Políticas do Kyverno:

1. Política de Limites de Recursos: Garantir que todos os containers em um Pod tenham limites de CPU e memória definidos. Isso pode ser importante para evitar o uso excessivo de recursos em um cluster compartilhado.

**Arquivo require-resources-limits.yaml:**
```yml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-cpu-memory-limits
spec:
  validationFailureAction: enforce
  rules:
  - name: validate-limits
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "CPU and memory limits are required"
      pattern:
        spec:
          containers:
          - name: "*"
            resources:
              limits:
                memory: "?*"
                cpu: "?*"
```

Depois do arquivo criado, agora bastar realizar o deploy em nosso cluster Kubernetes.
```sh
kubectl apply -f require-resources-limits.yaml
```

Agora, tenta realizar o deploy de um simples Nginx sem definir o limite para os recursos.

**Arquivo pod.yaml:**
```yml
apiVersion: v1
kind: Pod
metadata:
  name: exemplo-pod
spec:
  containers:
  - name: exemplo-container
    image: nginx
```

```sh
kubectl apply -f pod.yaml
```

## Exemplo de Política: Adicionar Label ao Namespace
A política `add-label-namespace` é projetada para automatizar a adição de um label específico a todos os Namespaces em um cluster Kubernetes. Esta abordagem é essencial para a organização, monitoramento e controle de acesso em ambientes complexos.

**Detalhes da Política**
O label adicionado por esta política é `Thadeu: "Lindo_Demais"`. A aplicação deste label a todos os Namespaces facilita a identificação e a categorização dos mesmos, permitindo uma gestão mais eficiente e uma padronização no uso de labels.

**Arquivo de Política:** `add-label-namespace.yaml`
```yml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-label-namespace
spec:
  rules:
  - name: add-label-ns
    match:
      resources:
        kinds:
        - Namespace
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            Thadeu: "Lindo_Demais"
```
## Utilização da Política
Esta política garante que cada Namespace no cluster seja automaticamente etiquetado com `Thadeu: "Lindo_Demais"`. Isso é particularmente útil para garantir a conformidade e a uniformidade na atribuição de labels, facilitando operações como filtragem e busca de Namespaces com base em critérios específicos.

## Exemplo de Política: Gerar ConfigMap para Namespace
A política `generate-configmap-for-namespace` é uma estratégia prática no gerenciamento de Kubernetes para automatizar a criação de ConfigMaps em Namespaces. Esta política simplifica a configuração e a gestão de múltiplos ambientes dentro de um cluster.

**Detalhes da Política**
Esta política é projetada para criar automaticamente um ConfigMap em cada Namespace recém-criado. O ConfigMap gerado, denominado `default-configmap`, inclui um conjunto padrão de chaves e valores, facilitando a configuração inicial e a padronização dos Namespaces.

**Arquivo de Política:** `generate-configmap-for-namespace.yaml`
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-configmap-for-namespace
spec:
  rules:
    - name: generate-namespace-configmap
      match:
        resources:
          kinds:
            - Namespace
      generate:
        kind: ConfigMap
        name: default-configmap
        namespace: "{{request.object.metadata.name}}"
        data:
          data:
            key1: "value1"
            key2: "value2"
```
**Implementação e Utilidade**
A aplicação desta política resulta na criação automática de um ConfigMap padrão em cada Namespace novo, proporcionando uma forma rápida e eficiente de distribuir configurações comuns e informações essenciais. Isso é particularmente útil em cenários onde a consistência e a automatização de configurações são cruciais.

## Exemplo de Política: Gerar ConfigMap para Namespace
A política generate-configmap-for-namespace é uma estratégia prática no gerenciamento de Kubernetes para automatizar a criação de ConfigMaps em Namespaces. Esta política simplifica a configuração e a gestão de múltiplos ambientes dentro de um cluster.

**Detalhes da Política**
Esta política é projetada para criar automaticamente um ConfigMap em cada Namespace recém-criado. O ConfigMap gerado, denominado default-configmap, inclui um conjunto padrão de chaves e valores, facilitando a configuração inicial e a padronização dos Namespaces.

**Arquivo de Política:** `generate-configmap-for-namespace.yaml`

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-configmap-for-namespace
spec:
  rules:
    - name: generate-namespace-configmap
      match:
        resources:
          kinds:
            - Namespace
      generate:
        kind: ConfigMap
        name: default-configmap
        namespace: "{{request.object.metadata.name}}"
        data:
          data:
            key1: "value1"
            key2: "value2"
```
**Implementação e Utilidade**
A aplicação desta política resulta na criação automática de um ConfigMap padrão em cada Namespace novo, proporcionando uma forma rápida e eficiente de distribuir configurações comuns e informações essenciais. Isso é particularmente útil em cenários onde a consistência e a automatização de configurações são cruciais.

## Exemplo de Política: Proibir Usuário Root
A política `disallow-root-user` é uma regra de segurança crítica no gerenciamento de clusters Kubernetes. Ela proíbe a execução de containers como usuário root dentro de Pods. Este controle ajuda a prevenir possíveis vulnerabilidades de segurança e a reforçar as melhores práticas no ambiente de contêineres.

**Detalhes da Política**
O principal objetivo desta política é garantir que nenhum Pod no cluster execute containers como o usuário root. A execução de containers como root pode expor o sistema a riscos de segurança, incluindo acessos não autorizados e potenciais danos ao sistema host.

**Arquivo de Política:** `disallow-root-user.yaml`
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-root-user
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-runAsNonRoot
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Running as root is not allowed. Set runAsNonRoot to true."
      pattern:
        spec:
          containers:
          - securityContext:
              runAsNonRoot: true
```
**Implementação e Efeito**
Ao aplicar esta política, todos os Pods que tentarem executar containers como usuário root serão impedidos, com a exibição de uma mensagem de erro indicando que a execução como root não é permitida. Isso assegura uma camada adicional de segurança no ambiente Kubernetes, evitando práticas que possam comprometer a integridade e a segurança do cluster.

## Exemplo de Política: Permitir Apenas Repositórios Confiáveis
A política `ensure-images-from-trusted-repo` é essencial para a segurança dos clusters Kubernetes, garantindo que todos os Pods utilizem imagens provenientes apenas de repositórios confiáveis. Esta política ajuda a prevenir a execução de imagens não verificadas ou potencialmente mal-intencionadas.

**Detalhes da Política**
Esta política impõe que todas as imagens de containers usadas nos Pods devem ser originárias de repositórios especificados e confiáveis. A estratégia é crucial para manter a integridade e a segurança do ambiente de containers, evitando riscos associados a imagens desconhecidas ou não autorizadas.

**Arquivo de Política:** `registry-allowed.yaml`
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: ensure-images-from-trusted-repo
spec:
  validationFailureAction: enforce
  rules:
  - name: trusted-repo-check
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Only images from trusted repositories are allowed"
      pattern:
        spec:
          containers:
          - name: "*"
            image: "trustedrepo.com/*"
```
**Implementação e Impacto**
Com a implementação desta política, qualquer tentativa de implantar um Pod com uma imagem de um repositório não confiável será bloqueada. A política assegura que apenas imagens de fontes aprovadas sejam usadas, fortalecendo a segurança do cluster contra vulnerabilidades e ataques externos.

## Exemplo de Política: Usando o Exclude
A política require-resources-limits é uma abordagem proativa para gerenciar a utilização de recursos em um cluster Kubernetes. Ela garante que todos os Pods tenham limites de recursos definidos, como CPU e memória, mas com uma exceção específica para um namespace.

**Detalhes da Política**
Essa política impõe que cada Pod no cluster tenha limites explícitos de CPU e memória configurados. Isso é crucial para evitar o consumo excessivo de recursos, que pode afetar outros Pods e a estabilidade geral do cluster. No entanto, esta política exclui especificamente o namespace beskar desta regra.

**Arquivo de Política**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resources-limits
spec:
  validationFailureAction: Enforce
  rules:
  - name: validate-limits
    match:
      resources:
        kinds:
        - Pod
    exclude:
      resources:
        namespaces:
        - beskar
    validate:
      message: "Precisa definir o limites de recursos"
      pattern:
        spec:
          containers:
          - name: "*"
            resources:
              limits:
                cpu: "?*"
                memory: "?*"
```
**Implementação e Efeitos**
Ao aplicar esta política, todos os Pods novos ou atualizados precisam ter limites de recursos claramente definidos, exceto aqueles no namespace `beskar`. Isso assegura uma melhor gestão de recursos e evita situações onde alguns Pods possam monopolizar recursos em detrimento de outros.

