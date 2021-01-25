# An initialization project of flash

## run project

pipenv 使用教程：[pipenv](https://crazygit.wiseturtles.com/2018/01/08/pipenv-tour)

```
cd api
pipenv install
flask run
```
通过 
```
pipenv lock -r > requirements.txt
``` 
生成与 pip 相同格式的依赖管理文件。

## Database Initialization

windows cmd下启动项目报错`Error: Could not locate a Flask application`的[解决方案](https://github.com/Microsoft/vscode-docs/issues/1881)

```
set FLASK_APP=api/run.py
flask db init
flask db migrate
flask db upgrade
error: Can't locate revision identified by '91eb2489ed74' 参考：https://blog.csdn.net/Super_Tiger_Lee/article/details/77772752
```
