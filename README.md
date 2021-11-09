# EnglishHelper
English study corner小助手

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