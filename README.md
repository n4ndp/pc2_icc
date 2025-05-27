# **PC2 ICC**

```bash
docker network create app_network

docker build -t mysql_bd ./db
docker run -d --name mysql_bd_container --network app_network -p 3306:3306 -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=flaskapp mysql_bd

docker build -t flask_app ./app
docker run -d --name flask_app_container --network app_network -p 5000:5000 -e MYSQL_HOST=mysql_bd_container -e MYSQL_USER=root -e MYSQL_PASSWORD=rootpassword -e MYSQL_DB=flaskapp flask_app

docker stop $(docker ps -q)

docker rm $(docker ps -aq)
```
