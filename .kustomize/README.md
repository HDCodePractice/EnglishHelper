# 前提
- 有部署到 Kubernetes 集群的权限
- kubectl 已安装并配置妥当
- kustomize 已安装
- （可选）Kubernetes 集群已安装 Sealed Secrets

# 预览

```
# print out schema
kustomize build .kustomize/instance1 |less

# dry-run
kubectl apply -k .kustomize/instance1 --dry-run=client
```

# 部署

```
# old school kustomize
kustomize build .kustomize/instance1 |kubectl apply -f -

# kubectl only
kubectl apply -k .kustomize/instance1
```

另见 [kustomization.yaml](instance1/kustomization.yaml) 中的注释


