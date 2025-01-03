## Deploying with Helm
**Install**
Deploying KEDA with Helm is very simple:

1.Add Helm repo
```sh
helm repo add kedacore https://kedacore.github.io/charts
```

2.Update Helm repo
```sh
helm repo update
```
3.Install keda Helm chart

Helm 3
```sh
helm install keda kedacore/keda --namespace keda --create-namespace
```
To deploy the CRDs separately from the Helm chart, use the keda-2.xx.x-crds.yaml file provided on the GitHub releases page.

💡 NOTE: Are you upgrading to v2.2.1 or above? Make sure to read our troubleshooting guide to fix potential CRD issues.

## Uninstall
If you want to remove KEDA from a cluster, you first need to remove any ScaledObjects and ScaledJobs that you have created. Once that is done, the Helm chart can be uninstalled:
```sh
kubectl delete $(kubectl get scaledobjects.keda.sh,scaledjobs.keda.sh -A \
  -o jsonpath='{"-n "}{.items[*].metadata.namespace}{" "}{.items[*].kind}{"/"}{.items[*].metadata.name}{"\n"}')
helm uninstall keda -n keda
```
Note: if you uninstall the Helm chart without first deleting any ScaledObject or ScaledJob resources you have created, they will become orphaned. In this situation, you will need to patch the resources to remove their finalizers. Once this is done, they should automatically be removed:
```sh
for i in $(kubectl get scaledobjects -A \
  -o jsonpath='{"-n "}{.items[*].metadata.namespace}{" "}{.items[*].kind}{"/"}{.items[*].metadata.name}{"\n"}');
do kubectl patch $i -p '{"metadata":{"finalizers":null}}' --type=merge
done

for i in $(kubectl get scaledjobs -A \
  -o jsonpath='{"-n "}{.items[*].metadata.namespace}{" "}{.items[*].kind}{"/"}{.items[*].metadata.name}{"\n"}');
do kubectl patch $i -p '{"metadata":{"finalizers":null}}' --type=merge
done
```