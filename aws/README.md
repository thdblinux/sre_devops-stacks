# Arquitetura de VPC's para Ambientes de Containers

###  O conceito de Virtual Private Clouds (VPCs) na AWS é fundamental para a construção de uma infraestrutura de rede isolada na nuvem. As VPCs permitem que você tenha controle total sobre o ambiente de rede virtual. Vamos explorar como configurar, gerenciar e utilizar VPCs para otimizar sua infraestrutura em cloud, garantindo segurança, isolamento e eficiência.

# Regiões e Zonas de Disponibilidade
### Regiões
As regiões da AWS são áreas geográficas que contêm múltiplas zonas de disponibilidade. Cada região opera independentemente das outras, o que aumenta a tolerância a falhas e a estabilidade global da infraestrutura AWS.

# Zonas de Disponibilidade - AZ's

Dentro de cada região, as zonas de disponibilidade (AZs) são datacenters altamente disponíveis e resistentes a falhas. A conexão entre AZs em uma mesma região permite a construção de aplicações resilientes e de alta disponibilidade.

# VPC - Virtual Private Cloud
Uma VPC proporciona um isolamento rigoroso da sua rede na AWS de outras redes. Este isolamento é alcançado através de uma fronteira virtual que controla o acesso e o tráfego entre as redes. Dessa forma, organizações podem executar suas aplicações em um ambiente de nuvem privado, gerenciando o acesso de maneira segura e eficaz.

Com as VPCs, você obtém controle granular sobre as dimensões e definições de sua rede. Isso inclui:

Seleção do Intervalo de Endereços IP: Você pode escolher o bloco de IPs que será utilizado pela sua VPC.
Criação de Sub-redes: Dividir sua VPC em sub-redes permite segmentar e controlar o acesso a diferentes partes da sua rede.
Configuração de Tabelas de Rotas e Gateways de Rede: Essas ferramentas permitem definir como o tráfego é direcionado e gerenciado dentro da sua VPC e para o exterior.
Grupos de Segurança: Atuam como firewalls virtuais para suas instâncias, controlando o tráfego de entrada e saída.
Listas de Controle de Acesso à Rede (NACLs): Fornecem um nível adicional de controle de tráfego para e entre suas sub-redes.

# Subnets
Subnets, ou sub-redes, são divisões de uma rede maior. No contexto de uma Virtual Private Cloud (VPC) na AWS, subnets permitem que você segmente a VPC em redes menores, o que facilita a organização, o gerenciamento de tráfego e a aplicação de políticas de segurança de maneira mais granular.

Cada subnet pode ser configurada para hospedar uma parte diferente da infraestrutura, como aplicações front-end, back-end, ou bancos de dados, permitindo o isolamento entre esses componentes. Você pode criar essas sub-redes, que podem ser públicas (com acesso direto à Internet) ou privadas (sem acesso direto à Internet), para hospedar diferentes tipos de aplicações com base em requisitos de visibilidade e acesso.

# Subnets Públicas
Subnets públicas são aquelas configuradas para permitir acesso direto à Internet de forma bilateral, ou seja, os recursos pertencentes a ela podem acessar a internet tanto como podem ser acessados diretamente por meio dela. Elas são essenciais para hospedar recursos que precisam ser acessíveis externamente, como servidores web, proxies e gateways. Recursos nestas subnets são atribuídos a um Endereço IP público, permitindo-lhes comunicar-se com a Internet e serem acessados por usuários externos.

# Subnets Privadas
Subnets privadas são utilizadas para recursos que não devem ser acessados diretamente da Internet. Essas subnets não possuem rotas para a Internet, garantindo que o acesso externo seja bloqueado. Recursos nessas áreas da rede podem se comunicar com a Internet ou outros serviços externos através de soluções como NAT Gateways localizados em subnets públicas, mas não recebem tráfego direto da Internet. Elas são utilizadas para hospedar recursos como aplicações backend, servidores de aplicação, microserviços internos, e tarefas de processamento de dados e batchs e etc.

Além das medidas de segurança padrão, o acesso a estas subnets geralmente é controlado por VPNs ou Direct Connect, garantindo que apenas tráfego autorizado possa acessar os recursos.

# Subnets de Databases
Especificamente projetadas para hospedar bancos de dados, estas subnets são um tipo de subnet privada com regras adicionais de segurança e acessibilidade. Colocar bancos de dados em subnets dedicadas ajuda a proteger os dados sensíveis e otimizar a segurança, restringindo o acesso apenas a recursos autorizados dentro da VPC.

Utilizadas para hospedar recursos como bancos de dados SQL e NoSQL, caches em memória, e armazenamentos de dados em repouso.

Seu acesso é restrito a partir de subnets específicas, geralmente subnets de aplicação, e proteção adicional contra ataques e acesso não autorizado.

# Gateways e Conectividade
tralalala

# Internet Gateway (IGW)
Um IGW permite que suas instâncias na VPC acessem a Internet, funcionando como um ponto de acesso público para suas aplicações. Utilizado em subnets públicas para prover acesso bidirecional a internet.

# NAT Gateway
O NAT Gateway possibilita que instâncias em subnets privadas acessem recursos na Internet, mantendo o tráfego de entrada bloqueado, o que aumenta a segurança. Normalmente são criados em subnets públicas e são acessados pelas aplicações privadas através de regras de tabelas de rotas.

# VPC Endpoints
Os VPC Endpoints permitem conexões privadas entre sua VPC e serviços AWS, eliminando a necessidade de tráfego passar pela Internet pública.

Existem dois tipos de endpoints, o Gateway Endpoint (para serviços como S3 e DynamoDB) e o Interface Endpoint (para outros serviços AWS ou customizados).

# Arquitetura de VPC's para Ambientes de Containers
Projetar VPCs em qualquer player de nuvem para suportar ambientes de containers em larga escala envolve considerações importantes para garantir que a infraestrutura seja segura, escalável e eficiente. Ao utilizar serviços como Amazon Elastic Container Service (ECS) ou Amazon Elastic Kubernetes Service (EKS), é muito importante planejar cuidadosamente a arquitetura de rede para otimizar o desempenho, operação e segurança na gestão dos containers efemetros que podem variar constantemente sua quantidade e finalidade. Aqui estão alguns pontos de atenção essenciais:

# Projetar CIDR's de acordo com as necessidades atuais e futuras do ambiente
![alt text](/aws/assets/public/aws6.jpg)
Um dos principais desafios ao projetar VPCs para containers em larga escala é garantir uma gestão eficaz do espaço de endereçamento IP. Containers podem ser efêmeros, com ciclos de vida curtos e frequentemente reciclados. Isso significa que o planejamento de sub-redes e a alocação de IPs devem ser feitos de maneira que suporte um grande número de containers sem esgotar o espaço disponível. Utilizar sub-redes suficientemente grandes e considerar o uso de IPs privados em combinação com soluções de Service Discovery são estratégias que ajudam a gerenciar a comunicação entre serviços de forma eficiente.

É muito importante levar em consideração que, ainda mais em ambientes de clouds públicas, nem todos os recursos utilizados e presentes dentro de uma VPC serão apenas containers e terão as mesmas necessidades.

É de grande importância projetar grupos de subnets específicos para cada tipo de finalidade, como containers que serão gerenciados de forma privada sem acesso direto da internet, recursos públicos que vão estar expostos a internet, recursos sigilosos como bancos de dados e aplicações isoladas que não podem ter acesso nem unilateral nem bilateral para a internet sendo acessados apenas por outros grupos de subnets e etc.

# Segurança e Isolamento de Recursos
A segurança é outra consideração crítica ao projetar VPCs para ambientes de containers e também sem containers. Como comentado no tópico anterior, é importante implementar mecanismos de isolamento entre diferentes cargas de trabalho para minimizar o risco de acessos indesejados ou interferências entre serviços de diferentes escopos e níveis de acesso. O uso de sub-redes distintas para diferentes ambientes (por exemplo, desenvolvimento, teste e produção) e a aplicação de grupos de segurança e listas de controle de acesso à rede  específicos podem fornecer camadas adicionais de segurança como por exemplo o uso de NACL's para ranges e subnets específicas, permitindo que o acesso para grupos de subnets que concentrem recursos de dados sensíveis, só seja acessível através de aplicações pertencentes as subnets de aplicação.

# Segregação e Alta Disponibilidade
Dividir sua carga de trabalho entre várias grupos de subnets que são criados em várias zonas de disponibilidade é uma pratica quase obrigatória em ambientes que precisem garantir disponibilidade, resiliência e continuidade de negócios.

Operar em várias zonas de disponibilidade requer estratégias de balanceamento de carga entre todos os nodes e replicas de nossos recursos distribuídos, e segregar recursos de rede também pode ser uma boa prática para aumentar ainda mais nossos escopos de resiliência em caso de falha de alguma dessas zonas de disponibilidade.

![alt text](/aws/assets/public/aws5.jpg)
Separar os NAT Gateways em múltiplas zonas de disponibilidade (AZs) é uma estratégia avançada para garantir alta disponibilidade e resiliência do tráfego de saída em uma arquitetura de rede na AWS. Essa abordagem é particularmente importante para ambientes de produção críticos, onde a continuidade dos negócios depende da disponibilidade constante dos recursos de rede. Ao implementar NAT Gateways em várias AZs, você pode assegurar que os recursos nas subnets privadas mantenham o acesso à Internet, mesmo se uma AZ enfrentar interrupções.

<!-- BEGIN_TF_DOCS -->

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.42.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_eip.vpc_eip_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) | resource |
| [aws_eip.vpc_eip_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) | resource |
| [aws_eip.vpc_eip_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) | resource |
| [aws_internet_gateway.gw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/internet_gateway) | resource |
| [aws_nat_gateway.nat_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/nat_gateway) | resource |
| [aws_nat_gateway.nat_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/nat_gateway) | resource |
| [aws_nat_gateway.nat_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/nat_gateway) | resource |
| [aws_route.private_access_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route.private_access_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route.private_access_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route.public_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) | resource |
| [aws_route_table.private_internet_access_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) | resource |
| [aws_route_table.private_internet_access_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) | resource |
| [aws_route_table.private_internet_access_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) | resource |
| [aws_route_table.public_internet_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) | resource |
| [aws_route_table_association.private_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_route_table_association.private_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_route_table_association.private_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_route_table_association.public_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_route_table_association.public_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_route_table_association.public_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_ssm_parameter.databases_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.databases_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.databases_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.private_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.private_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.private_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.public_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.public_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.public_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_ssm_parameter.vpc](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |
| [aws_subnet.databases_subnet_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.databases_subnet_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.databases_subnet_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.private_subnet_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.private_subnet_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.private_subnet_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.public_subnet_1a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.public_subnet_1b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_subnet.public_subnet_1c](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) | resource |
| [aws_vpc.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_project_name"></a> [project\_name](#input\_project\_name) | Nome do projet. Essa variável será um prefixo para os recursos criados dentro desse projeto | `any` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | n/a | `string` | `"Região da AWS onde os recursos serão criados"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_ssm_subnet_databases_1a"></a> [ssm\_subnet\_databases\_1a](#output\_ssm\_subnet\_databases\_1a) | ID da subnet de bancos de dados na zona de disponibilidade 1a. Este ID é recuperado do AWS Systems Manager Parameter Store e usado para o provisionamento de instâncias de banco de dados nesta zona específica. |
| <a name="output_ssm_subnet_databases_1b"></a> [ssm\_subnet\_databases\_1b](#output\_ssm\_subnet\_databases\_1b) | ID da subnet de bancos de dados na zona de disponibilidade 1b. Obtido do AWS Systems Manager Parameter Store, é essencial para a alocação de instâncias de banco de dados que precisam ser isoladas nesta zona. |
| <a name="output_ssm_subnet_databases_1c"></a> [ssm\_subnet\_databases\_1c](#output\_ssm\_subnet\_databases\_1c) | ID da subnet de bancos de dados na zona de disponibilidade 1c, proveniente do AWS Systems Manager Parameter Store. Utilizado no provisionamento de instâncias de banco de dados que requerem isolamento nesta zona. |
| <a name="output_ssm_subnet_private_1a"></a> [ssm\_subnet\_private\_1a](#output\_ssm\_subnet\_private\_1a) | ID da subnet privada na zona de disponibilidade 1a. Valor armazenado no AWS Systems Manager Parameter Store, utilizado para provisionar recursos em uma subnet privada específica. |
| <a name="output_ssm_subnet_private_1b"></a> [ssm\_subnet\_private\_1b](#output\_ssm\_subnet\_private\_1b) | ID da subnet privada na zona de disponibilidade 1b. Armazenado no AWS Systems Manager Parameter Store, usado para alocação de recursos que requerem isolamento dentro desta zona de disponibilidade. |
| <a name="output_ssm_subnet_private_1c"></a> [ssm\_subnet\_private\_1c](#output\_ssm\_subnet\_private\_1c) | ID da subnet privada na zona de disponibilidade 1c. Guardado no AWS Systems Manager Parameter Store, é crucial para a criação de recursos que precisam ser isolados nesta zona específica. |
| <a name="output_ssm_subnet_public_1a"></a> [ssm\_subnet\_public\_1a](#output\_ssm\_subnet\_public\_1a) | ID da subnet pública na zona de disponibilidade 1a. Este ID, proveniente do AWS Systems Manager Parameter Store, é utilizado para provisionar recursos acessíveis publicamente nesta zona. |
| <a name="output_ssm_subnet_public_1b"></a> [ssm\_subnet\_public\_1b](#output\_ssm\_subnet\_public\_1b) | ID da subnet pública na zona de disponibilidade 1b. Disponível via AWS Systems Manager Parameter Store, permite a implementação de recursos com acesso público nesta zona específica. |
| <a name="output_ssm_subnet_public_1c"></a> [ssm\_subnet\_public\_1c](#output\_ssm\_subnet\_public\_1c) | ID da subnet pública na zona de disponibilidade 1c, armazenado no AWS Systems Manager Parameter Store. Usado para configurar recursos que necessitam de acesso público nesta zona. |
| <a name="output_ssm_vpc_id"></a> [ssm\_vpc\_id](#output\_ssm\_vpc\_id) | ID do VPC armazenado no AWS Systems Manager Parameter Store. Este ID é usado para identificar o VPC onde os recursos serão provisionados. |
<!-- END_TF_DOCS -->