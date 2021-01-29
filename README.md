# An initialization project of flash

## run project

pipenv 使用教程：[pipenv](https://crazygit.wiseturtles.com/2018/01/08/pipenv-tour)

安装 eventlet，flask_socketio使用该库支持websocket

配置vscode的settings.json文件的python.venvPath
`pipenv --venv`
详见 [venvPath](https://segmentfault.com/a/1190000017558652)

```
pipenv install
pipenv shell and flask run
or
F5
```

通过

```
pipenv lock -r > requirements.txt
```

生成与 pip 相同格式的依赖管理文件。

## Database Initialization

```
flask shell
flask db init
flask db migrate
flask db upgrade
error: Can't locate revision identified by '91eb2489ed74' 参考：https://blog.csdn.net/Super_Tiger_Lee/article/details/77772752
```

python 中使用 protocol buffer：[参考](https://www.jianshu.com/p/b723053a86a6)
protoc: command not found (Linux Mac Windows)，解决方法：[stackoverflow](https://stackoverflow.com/questions/47704968/protoc-command-not-found-linux)
