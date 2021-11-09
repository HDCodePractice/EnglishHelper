# EnglishHelper
English study corner小助手

## 功能

本Bot收录了以下这些Irregular形式：

* inouns.csv Irregular plural nouns
* iverbs.csv Irregular verbs

你可以通过 /i word 来查询单词的Irregular形式。

你也可以通过 /t 来启动一个测试小游戏，Bot会寻找任意一个单词让你去回复它的其它形式。

## 使用说明

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