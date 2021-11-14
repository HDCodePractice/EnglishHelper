# Prerequisites
- permission to deploy to a kubernetes cluster
- kubectl command installed and configured
- kustomize command installed

# Deploy with kustomize

```
kustomize build .kustomize/instance1 |kubectl apply -f -
```

Also please see comments in [kustomization.yaml](instance1/kustomization.yaml)


