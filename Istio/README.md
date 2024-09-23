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
- **CI/CD com GitLab CI:** Pipelines automatizados para build, teste e deploy contínuo.

Este projeto serve como uma base sólida para ambientes Kubernetes altamente escaláveis e seguros, combinando o poder de várias ferramentas modernas para entrega contínua, monitoramento, e gerenciamento de microserviços.


```sh
kubectl delete -f install/kubernetes/istio-demo-auth.yaml
```
```sh
 kubectl delete -f install/kubernetes/istio-demo.yaml
```
```
 for i in install/kubernetes/helm/istio-init/files/crd*yaml; do kubectl delete -f $i; done
```
```sh
 kubectl get virtualservices.networking.istio.io --all-namespaces
```
```sh
 for i in install/kubernetes/helm/istio-init/files/crd*yaml; do kubectl apply -f $i; done
```
```sh
wget https://get.helm.sh/helm-v2.14.3-linux-amd64.tar.gz
```
```sh
tar -xvzf helm-v2.14.3-linux-amd64.tar.gz
```

```sh
cd linux-amd64/
```
```sh
mv helm /usr/local/bin/
```
```sh
mv tiller /usr/local/bin/
```
```sh
helm init
```
```sh
kubectl get deployments. --all-namespaces
```
```sh
helm list
```
```sh
kubectl create serviceaccount --namespace=kube-system tiller
```
```sh
   kubectl create clusterrolebinding tiller-cluster-role --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
```
```sh
kubectl patch deployments -n kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'  # kubectl get deployments. --all-namespaces
```
```sh
kubectl get pods --all-namespaces
```
```sh
helm list
```
```sh
helm --help
```
```sh
helm search prometheus
```
```sh
helm template install/kubernetes/helm/istio --name istio --namespace istio-system --values install/kubernetes/helm/istio/values.yaml --set gateways.istio-ingresssgateway.type=NodePort --set grafana.enabled=true --set kiali.enabled=true --set tracing.enabled=true --set kiali.dashboard.username=admin --set kiali.dashboard.passphrase=admin --set servicegraph.enabled=true > meu_istio.yaml
```
```sh
vim meu_istio.yaml 
```
```sh
kubectl create namespace istio-system
```
```sh
   kubectl apply -f meu_istio.yaml
```
```sh
kubectl get pods -n istio-system
```
```sh
   kubectl get pods -n istio-system --watch
```
```
  KIALI_USERNAME=$(read -p 'Kiali Username: ' uval && echo -n $uval | base64)
  KIALI_PASSPHRASE=$(read -sp 'Kiali Passphrase: ' pval && echo -n $pval | base64)
  echo $KIALI_USERNAME
  echo $KIALI_PASSPHRASE
```
```yml
  NAMESPACE=istio-system
  cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: kiali
  namespace: $NAMESPACE
  labels:
    app: kiali
type: Opaque
data:
  username: $KIALI_USERNAME
  passphrase: $KIALI_PASSPHRASE
EOF
```
```sh
  kubectl get services -n istio-system
```

```sh
  kubectl port-forward svc/kiali 20001:20001 -n istio-system --address=0.0.0.0 &
```
 