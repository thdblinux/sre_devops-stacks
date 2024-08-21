#  Arquitetura de VPC's para Ambientes de Containers

 **Regiões**

- Áreas Geograficas
- Contém 2 ou mais Zonas de Disponibilidades
- Completamente Independentes
- Isoladas de falhas de outras Regiões
- Latência de Falhas para Usuários Finais:
- Conformidade e Soberania de Dados:

## Regiões da AWS:

**América do Norte**
- US East (Norte da Virgínia) - us-east-1
- US East (Ohio) - us-east-2
- US West (Norte da Califórnia) - us-west-1
- US West (Oregon) - us-west-2
- Canadá (Centro) - ca-central-1
- América do Sul (São Paulo) - sa-east-1
  
**Europa**
- Europa (Irlanda) - eu-west-1
- Europa (Londres) - eu-west-2
- Europa (Paris) - eu-west-3
- Europa (Frankfurt) - eu-central-1
- Europa (Milão) - eu-south-1
- Europa (Estocolmo) - eu-north-1
  
**Ásia-Pacífico**
- Ásia-Pacífico (Mumbai) - ap-south-1
- Ásia-Pacífico (Tóquio) - ap-northeast-1
- Ásia-Pacífico (Seul) - ap-northeast-2
- Ásia-Pacífico (Osaka) - ap-northeast-3
- Ásia-Pacífico (Cingapura) - ap-southeast-1
- Ásia-Pacífico (Sydney) - ap-southeast-2
- Ásia-Pacífico (Hong Kong) - ap-east-1
 
**Oriente Médio e África**
- Oriente Médio (Barém) -me-south-1
- África (Cidade do Cabo) - af-south-1
  
**Outras Regiões**
- Governo dos EUA (Norte da Virgínia) - us-gov-east-1
- Governo dos EUA (Oregon) - us-gov-west-1

## Availability Zones

- Datacenters dentro de uma região
- Conectados dentro da região
- Replicação
- Redundância e Disponibilidade

## Subnets

- Divisões de uma rede maior (VPC)
- Segmentar a VPC em redes menores
- Organização e Gestão de Recursos
- Subnets Publicas
   - Exposição direta a internet
-  Subnets Privadas
   - Não são diretamentes acessíveis pela internet
  
## Internet Gateways

- Subnets Públicas
- Comunicação dos Recusrsos e a Internet
- Bidirecional
- Subnets para recursos públicos
- Load Balancers Públicos
- Host diretamente acessíveis

## NAT Gateways

- Subnets Privadas
- Permite que Recusros Privados Acessem a Internet
- Unidirecional
     - Recursos acessarem a internet sem estarem diretamente acessíveis
- Único IP de Saída para todos os hosts

## VPC Endpoints

- Garante a conexão privada entre sua VPC e serviços AWS
-  Sem necessidade de tráfego atravessar a internet.
-  Gateway Endpoints
     - S3, Dinamo, ECR, SQS
- Interface Endpoints
     - Serviços Customizados