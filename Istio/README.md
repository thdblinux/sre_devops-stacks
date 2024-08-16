![alt text](/assets/public/istio.png)

# Projeto AWS EKS com Service Mesh e Observabilidade
Este projeto implementa uma infraestrutura robusta e segura utilizando `AWS EKS` como plataforma de orquestração de contêineres, com `Istio` e `Kiali` como ferramentas de service mesh para gerenciar a comunicação entre `microserviços`. A observabilidade é aprimorada com `Prometheus` e `Grafana`, permitindo monitoramento e visualização de métricas em tempo real.

**Tecnologias Utilizadas:**
- **AWS EKS**: Plataforma de orquestração de contêineres.
- **Istio:** Service mesh para gestão de tráfego, segurança, e observabilidade entre microserviços.
- **Kiali:** Interface gráfica para visualização e configuração de service mesh com Istio.
- **Prometheus:** Sistema de monitoramento e alerta.
- **Grafana:** Ferramenta de análise e visualização de dados.
- **Helm:** Gerenciamento de pacotes Kubernetes.
- **Docker:** Contêineres para empacotamento e distribuição de aplicações.
- **Chainguard e Wolfi:** Imagens de contêiner seguras e com foco em segurança.
- **ArgoCD:** GitOps para implantação contínua e gerenciamento de aplicações.
- **GitLab CI:** Pipeline de CI/CD para automação de testes e deploy.
- **Terraform:** Infraestrutura como código para provisionamento de recursos na AWS.

## Funcionalidades Principais:
- **Service Mesh com Istio:** Gerenciamento de tráfego entre microserviços, segurança mTLS, e roteamento avançado.
- **Monitoramento com Prometheus e Grafana:** Coleta de métricas, alertas e dashboards personalizados.
- **GitOps com ArgoCD:** Deploys automatizados e gerenciados via Git, garantindo consistência e controle de versões.
CI/CD com GitLab CI: Pipelines automatizados para build, teste e deploy contínuo.

Este projeto serve como uma base sólida para ambientes Kubernetes altamente escaláveis e seguros, combinando o poder de várias ferramentas modernas para entrega contínua, monitoramento, e gerenciamento de microserviços.