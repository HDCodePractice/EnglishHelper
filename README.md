# EnglishHelper
English study corner小助手

[![codecov](https://codecov.io/gh/HDCodePractice/EnglishHelper/branch/main/graph/badge.svg?token=X6E5R9NSdR)](https://codecov.io/gh/HDCodePractice/EnglishHelper) [![GitHub Test Action](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_test.yaml/badge.svg)](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_test.yaml) [![Build Publish Docker image](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_publish_docker.yaml/badge.svg)](https://github.com/HDCodePractice/EnglishHelper/actions/workflows/build_and_publish_docker.yaml) ![Irregular Words Number](/irregular.svg?raw=true "Irregular Words Number") 

## 功能

### 收录

本Bot收录了以下这些Irregular形式：

* inouns.csv Irregular plural nouns
* iverbs.csv Irregular verbs

来源自hdcola的录入和整理。

本Bot收录了 https://en.wikipedia.org/wiki/ARPABET 拼读标识出的词库。来源自[The CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict)

本Bot收录了 WordNet 提供的字典。来源自[WordNet](http://wordnet.princeton.edu/)

### Bot 命令

* 可以通过 /t 来启动一个测试小游戏，Bot会寻找任意一个单词让你去回复它的其它形式。
* 可以通过 /p word 来查询单词，如果单词有Irregular plural nouns或是 Irregular verbs，会显示出来。还会显示出单词的英文发音（如果有多个就会列出多个），以及每个发音的相似拼读的单词们。最后会通过google（正常和慢速发音）、google translate（发音、翻译）、youglish（无数个youtube上包括这个单词的视频）、urban（俚语解释）、youtue（发音和理解视频）来了解更多。


### 自定义词库更新

创建一个目录里面包括以下文件和文件夹:

* inouns.csv 参考[inouns.csv](https://github.com/HDCodePractice/EnglishHelper/blob/main/res/inouns.csv)
* iverbs.csv 参考[iverbs.csv](https://github.com/HDCodePractice/EnglishHelper/blob/main/res/iverbs.csv)
* picwords.csv 参考[picwords.csv](https://github.com/HDCodePractice/EnglishHelper/blob/main/res/picwords.csv)
* picwords目录，内包括所有的图片。

然后使用zip压缩res目录，得到res.zip文件。注意，你需要在 local.env 里设置你自己为ADMIN，然后把res.zip文件发送到你的群里，使用 /u 回复发进去的zip文件，这样就会更新自定义词库了。因为电报的限制，现在只支持20MB以内大小的文件。每次都是全量更新，暂还不支持增量更新。

## 使用说明
### Docker
安装 Docker Compose，准备好你的[local.evn](https://github.com/HDCodePractice/EnglishHelper/blob/main/localenv.example)文件，并参照[docker-compose.yml](https://github.com/HDCodePractice/EnglishHelper/blob/main/docker-compose.yml)准备你自己的docker-compose.yml。

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