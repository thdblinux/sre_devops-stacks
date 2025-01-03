# Arquitetura de Containers na AWS com ECS

Este projeto implementa uma arquitetura de containers utilizando Amazon Elastic Container Service (ECS) com integração ao Elastic Load Balancer (ALB) e outras ferramentas da AWS. O Terraform é utilizado como ferramenta de infraestrutura como código (IaC) para provisionar e configurar todos os recursos necessários, incluindo a criação de tasks e task definitions, e o uso do Elastic Container Registry (ECR) para armazenar as imagens dos containers.

Além disso, foi desenvolvido um módulo Terraform externo para facilitar a criação do ECS e a realização de deploys de aplicações cloud-native, como o **chip**.

## Estrutura do Projeto

O projeto está dividido nos seguintes arquivos principais:

- **backend.tf**: Define o backend para armazenar o estado remoto do Terraform.
- **data.tf**: Configura data sources, como VPC e subnets, para o projeto.
- **enviroment/**: Diretório contendo configurações específicas do ambiente.
- **iam.tf**: Contém as definições de papéis e permissões IAM necessárias para a execução dos serviços ECS.
- **main.tf**: Configura os serviços principais, como ECS Service, ALB, e Task Definitions.
- **output.tf**: Atualmente vazio, mas será usado para exportar informações importantes sobre os recursos criados.
- **providers.tf**: Define os provedores necessários, como AWS.
- **variables.tf**: Define as variáveis de entrada usadas no projeto para tornar o código mais dinâmico e reutilizável.

## Funcionalidades

- **Provisionamento de ECS Service**: Cria um serviço ECS que gerencia containers de forma escalável e eficiente.
- **Configuração de Load Balancer (ALB)**: Integra um ALB para distribuir o tráfego entre as instâncias de containers.
- **Task Definitions e Tasks**: Define as tasks e task definitions que especificam como as containers devem ser executadas no ECS.
- **Armazenamento de Imagens no ECR**: Usa o AWS Elastic Container Registry (ECR) para armazenar as imagens Docker que serão usadas pelas tasks do ECS.
- **Módulo Externo para ECS**: Um módulo Terraform externo foi criado para contribuir com a automação na criação do ECS e facilitar o deploy de aplicações cloud-native, como a aplicação **chip**.
- **Papéis e Permissões (IAM)**: Configura os papéis de execução e permissões necessárias para os serviços ECS.
- **Integração com VPC**: Utiliza data sources para se conectar a subnets e VPCs existentes.
- **Gerenciamento de Configurações**: Variáveis como o nome do cluster, CPU, memória, e portas de serviço são configuradas de forma flexível através de `variables.tf`.