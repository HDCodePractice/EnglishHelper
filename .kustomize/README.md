# 前提
- 有部署到 Kubernetes 集群的权限
- kubectl 已安装并配置妥当
- kustomize 已安装
- （可选）Kubernetes 集群已安装 Sealed Secrets

# 使用 kustomize 部署

```
kustomize build .kustomize/instance1 |kubectl apply -f -
```

另见 [kustomization.yaml](instance1/kustomization.yaml) 中的注释


