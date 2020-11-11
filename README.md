# 表白墙-后端

这是受到[我同学](https://github.com/jsun969)部署的[另一个表白墙项目](https://github.com/ping-xiong/saylovewall)启发，模仿着写的第一个 Django + DjangoRESTFramework 项目  
相当不成熟，如果你发现当前 commit 中有迷惑行为，欢迎通过 issue 告知

版本号为 API 版本号，如：v1.2.x 的前端只能使用 v1.2.x 的后端

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

## 规则

每一个浏览器会话只能表白一次，给每条表白点一个赞，给每条表白评论一次  
可通过新建窗口访问或调用`window.reset()`清除会话存储

管理员次数无限制，且可删除表白和评论
