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
error: Can't locate revision identified by '91eb2489ed74' 参考：https://blog.csdn.net/Super_Tiger_Lee/article/details/77772752
```
