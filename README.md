# EnglishHelper
English study corner小助手

[![codecov](https://codecov.io/gh/HDCodePractice/EnglishHelper/branch/main/graph/badge.svg?token=X6E5R9NSdR)](https://codecov.io/gh/HDCodePractice/EnglishHelper) [![GitHub Test Action](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_test.yaml/badge.svg)](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_test.yaml) [![Build Publish Docker image](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_publish_docker.yaml/badge.svg)](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_publish_docker.yaml) ![Irregular Words Number](/irregular.svg?raw=true "Irregular Words Number") 

## 功能

本Bot收录了以下这些Irregular形式：

* inouns.csv Irregular plural nouns
* iverbs.csv Irregular verbs

可以通过 /i word 来查询单词的Irregular形式。

可以通过 /t 来启动一个测试小游戏，Bot会寻找任意一个单词让你去回复它的其它形式。

可以通过 /p word 来查询单词的读音和类似读音的单词。

## 使用说明
### Docker
安装 Docker Compose，准备好你的[local.evn](blob/main/localenv.example)文件，并参照[docker-compose.yml](blob/main/docker-compose.yml)准备你自己的docker-compose.yml。

更新 Image

```
docker-compose pull
```

启动服务

```
docker-compose up -d
```

停止服务

```
docker-compose stop
```

查看运行log

```
docker-compose logs -f
```

### 部署到 Kubernetes 集群
(试验阶段）参考 [README](.kustomize/README.md)