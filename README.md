# 表白墙-后端

这是受到[我同学](https://github.com/jsun969)部署的[另一个表白墙项目](https://github.com/ping-xiong/saylovewall)启发，模仿着写的第一个 Django + DjangoRESTFramework 项目  
相当不成熟，如果你发现当前 commit 中有迷惑行为，欢迎通过 issue 告知

未写任何防御，求别攻击演示站点……

## 后端部署(Windows 下开发部署)

```
python -m venv venv # 创建虚拟环境
venv\Scripts\activate # 激活虚拟环境
pip install -r requirements.txt # 安装依赖
```

在 ConfessionWall_backend 目录下新建 securitysettings.py

```
# securitysettings.py:

SECRET_KEY = 'x&q5tl2ehmw2s(j15$qb(()o4ooati&h=li5ds1n0lvp+xhf^m'
# 生产部署请替换为自己的SECRET_KEY
```

```
python manage.py migrate # 迁移数据库
python manage.py createsuperuser # 创建管理员用户
python manage.py runserver # 运行开发服务器
```

前后端全部部署完毕后即可访问[用户入口](http://localhost:8080)和[管理员登陆入口](http://localhost:8080/login)
