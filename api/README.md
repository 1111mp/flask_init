# An initialization project of flash

## run project
```
cd api
pipenv install -r requirements.txt
flask run
```
通过 
```
pipenv lock -r > requirements.txt
``` 
生成与 pip 相同格式的依赖管理文件。

## Database Initialization
```
flask db init
flask db migrate
flask db upgrade
```
